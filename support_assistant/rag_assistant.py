import os
import json
from typing import TypedDict

import requests
import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:latest"


# ---------------------------------------------------------
# Pydantic structured response
# ---------------------------------------------------------

class SupportResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


# ---------------------------------------------------------
# Load embedding model and ChromaDB
# ---------------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

db_path = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)

client = chromadb.PersistentClient(
    path=db_path
)

collection = client.get_collection(
    name="zepto_support"
)


# ---------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------

class SupportState(TypedDict, total=False):
    query: str
    intent: str
    context: list[str]
    sources: list[str]
    answer: str
    confidence: float


# ---------------------------------------------------------
# Node 1: Classify Intent
# ---------------------------------------------------------

def classify_intent(
    state: SupportState
) -> SupportState:

    query = state["query"].lower()

    support_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
        "damaged",
        "spoiled",
        "missing",
        "issue",
    ]

    if any(
        keyword in query
        for keyword in support_keywords
    ):
        intent = "support"
    else:
        intent = "direct"

    return {
        "intent": intent
    }


# ---------------------------------------------------------
# Structured Prompt
# ---------------------------------------------------------

def build_prompt(
    query: str,
    context: list[str]
) -> str:

    context_text = "\n\n".join(context)

    return f"""
ROLE:
You are a helpful Zepto customer support assistant.

CONTEXT:
Use only the retrieved Zepto policy information below.

{context_text}

TASK:
Answer the customer's question using only the provided context.

FORMAT:
Return valid JSON with exactly these fields:
answer, sources, confidence.

LENGTH:
Keep the answer concise and directly useful.

NEGATIVE CONSTRAINT:
Do not invent policies, prices, deadlines, refunds, or other information.
If the answer is not available in the context, say:
"I don't have enough information to answer that."

FEW-SHOT EXAMPLE:

Question:
What is the delivery fee for an order below INR 149?

Answer:
{{
  "answer": "Orders below INR 149 incur a flat INR 25 delivery fee.",
  "sources": ["doc_01.txt_chunk_1"],
  "confidence": 0.95
}}

Customer question:
{query}

Return JSON only.
"""


# ---------------------------------------------------------
# Real LLM call with validation and retry
# ---------------------------------------------------------

def call_real_llm(
    prompt: str,
    source_ids: list[str]
) -> SupportResponse:

    last_error = None

    for attempt in range(3):

        retry_instruction = ""

        if attempt > 0:
            retry_instruction = """
Your previous response failed Pydantic validation.

Return ONLY valid JSON with:
- answer: string
- sources: list of strings
- confidence: number between 0 and 1

Do not include markdown or explanations.
"""

        try:

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt + retry_instruction,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

            raw_answer = response.json()["response"].strip()

            # Remove accidental markdown code fences
            if raw_answer.startswith("```"):
                raw_answer = raw_answer.replace(
                    "```json",
                    ""
                ).replace(
                    "```",
                    ""
                ).strip()

            parsed = json.loads(raw_answer)

            validated = SupportResponse.model_validate(
                parsed
            )

            return validated

        except (
            requests.RequestException,
            json.JSONDecodeError,
            ValidationError,
            KeyError,
        ) as error:

            last_error = error

    # Safe fallback after all retries fail
    return SupportResponse(
        answer=(
            "I don't have enough information to answer "
            "that."
        ),
        sources=source_ids,
        confidence=0.0,
    )


# ---------------------------------------------------------
# Node 2: Retrieve and Answer
# ---------------------------------------------------------

def retrieve_and_answer(
    state: SupportState
) -> SupportState:

    query = state["query"]

    # Convert question into embedding
    query_embedding = model.encode(
        query
    ).tolist()

    # Retrieve top 3 chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    source_ids = results["ids"][0]

    context = documents

    # Build structured prompt
    prompt = build_prompt(
        query,
        context
    )

    # -----------------------------------------------------
    # Deterministic MOCK_LLM mode
    # -----------------------------------------------------

    if MOCK_LLM:

        snippet = documents[0][:300]

        validated = SupportResponse(
            answer=(
                "Based on the retrieved context: "
                + snippet
            ),
            sources=source_ids,
            confidence=0.90,
        )

    # -----------------------------------------------------
    # Real Ollama LLM mode
    # -----------------------------------------------------

    else:

        validated = call_real_llm(
            prompt,
            source_ids
        )

    return {
        "context": context,
        "sources": validated.sources,
        "answer": validated.answer,
        "confidence": validated.confidence,
    }


# ---------------------------------------------------------
# Node 3: Direct Answer
# ---------------------------------------------------------

def direct_answer(
    state: SupportState
) -> SupportState:

    validated = SupportResponse(
        answer=(
            "I can help with Zepto support questions about "
            "delivery, returns, refunds, membership, "
            "tracking, cancellations, gift cards, and "
            "support."
        ),
        sources=[],
        confidence=0.80,
    )

    return {
        "context": [],
        "sources": validated.sources,
        "answer": validated.answer,
        "confidence": validated.confidence,
    }


# ---------------------------------------------------------
# Conditional Routing
# ---------------------------------------------------------

def route_intent(
    state: SupportState
) -> str:

    if state["intent"] == "support":
        return "retrieve_and_answer"

    return "direct_answer"


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------

graph_builder = StateGraph(
    SupportState
)

graph_builder.add_node(
    "classify_intent",
    classify_intent
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

graph_builder.add_node(
    "direct_answer",
    direct_answer
)

graph_builder.set_entry_point(
    "classify_intent"
)

graph_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

graph_builder.add_edge(
    "retrieve_and_answer",
    END
)

graph_builder.add_edge(
    "direct_answer",
    END
)

graph = graph_builder.compile()


# ---------------------------------------------------------
# Local Test
# ---------------------------------------------------------

if __name__ == "__main__":

    question = (
        "What should I do if my order arrives damaged?"
    )

    result = graph.invoke({
        "query": question
    })

    print("\nCustomer Question:")
    print(question)

    print("\nIntent:")
    print(result["intent"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print("-", source)

    print("\nConfidence:")
    print(result["confidence"])
