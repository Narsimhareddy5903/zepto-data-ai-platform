# Zepto Data & AI Platform

A three-module capstone project demonstrating a complete data-to-AI workflow:

1. **Data Pipeline** — web scraping, cleaning, SQLite database, SQL analysis, and pandas/SQL comparison
2. **Analytics & Machine Learning** — Titanic EDA, classification, imbalance handling, hyperparameter tuning, and regression
3. **GenAI Support Assistant** — RAG using ChromaDB, Sentence Transformers, LangGraph, Pydantic, FastAPI, and optional local Ollama

The project is designed to run with free, locally runnable tools and does not require paid APIs.

---

## Project Structure

```text
zepto-data-ai-platform/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data_pipeline/
│   ├── README.md
│   ├── scrape_books.py
│   ├── analyze_books.py
│   ├── database_pipeline.py
│   ├── sql_queries.py
│   ├── sql_pandas_comparison.py
│   ├── books.csv
│   ├── books.db
│   └── sql_query_results.txt
│
├── analytics/
│   ├── titanic.csv
│   ├── titanic_cleaned.csv
│   ├── best_titanic_model.joblib
│   └── notebooks/
│       ├── books_eda.ipynb
│       └── titanic_analysis.ipynb
│
└── support_assistant/
    ├── Dockerfile
    ├── ingest.py
    ├── query.py
    ├── main.py
    ├── rag_assistant.py
    └── docs/
        ├── doc_01.txt
        ├── doc_02.txt
        ├── doc_03.txt
        ├── doc_04.txt
        ├── doc_05.txt
        ├── doc_06.txt
        ├── doc_07.txt
        └── doc_08.txt
```

The generated `support_assistant/chroma_db/` directory is intentionally excluded from Git because it can be regenerated from the eight source documents.

---

# Requirements

## Software

* Python 3.11+ recommended
* Git
* VS Code or another Python IDE
* Docker Desktop for the containerized support assistant
* Optional: Ollama for local LLM generation

The project was developed and tested in a Python virtual environment.

## Python packages

Install the dependencies from the root `requirements.txt`:

```bash
pip install -r requirements.txt
```

Major libraries used:

* pandas
* requests
* BeautifulSoup
* matplotlib
* seaborn
* scikit-learn
* imbalanced-learn
* joblib
* Jupyter
* ChromaDB
* Sentence Transformers
* LangGraph
* FastAPI
* Uvicorn
* Pydantic

---

# Setup

From the project root:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Module 1 — Data Pipeline

## Objective

Build a complete data pipeline that:

1. Scrapes book information from Books to Scrape
2. Cleans and validates the data
3. Stores the cleaned data in SQLite
4. Runs SQL analysis queries
5. Reproduces SQL results using pandas

## Step 1 — Scrape books

Run:

```bash
python data_pipeline/scrape_books.py
```

The scraper processes the first three catalogue pages and collects:

* 60 books
* 60 unique titles
* title
* price in GBP
* availability text
* star rating
* category

The scraper uses:

* `requests`
* `BeautifulSoup`

The resulting dataset is saved to:

```text
data_pipeline/books.csv
```

## Step 2 — Analyze and validate

Run:

```bash
python data_pipeline/analyze_books.py
```

The analysis checks:

* DataFrame shape
* column names
* data types
* missing values
* duplicate rows
* price statistics
* rating distribution
* category distribution

The final dataset contains 60 rows with no missing values in the required fields.

## Step 3 — Create SQLite database

Run:

```bash
python data_pipeline/database_pipeline.py
```

This creates:

```text
data_pipeline/books.db
```

The cleaned data includes:

* `title`
* `price_gbp`
* `price_inr`
* `rating`
* `in_stock`
* `category`

### Currency conversion

The project uses a fixed project-defined conversion rate:

```text
1 GBP = 105.50 INR
```

Therefore:

```text
price_inr = price_gbp * 105.50
```

The fixed rate is used for reproducibility rather than fetching a changing exchange rate.

The SQLite database uses a normalized design with separate category and book information and a primary-key/foreign-key relationship.

## Step 4 — Run SQL queries

Run:

```bash
python data_pipeline/sql_queries.py
```

The project demonstrates:

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `BETWEEN`
* `JOIN`

The query strings and outputs are saved in:

```text
data_pipeline/sql_query_results.txt
```

## Step 5 — Compare SQL and pandas

Run:

```bash
python data_pipeline/sql_pandas_comparison.py
```

This script:

* reads SQL results using `pd.read_sql`
* reads multiple query results into pandas
* reproduces the SQL JOIN using `pd.merge`
* compares the SQL and pandas outputs

The SQL JOIN and pandas merge produce equivalent results for the demonstrated comparison.

---

# Module 2 — Analytics & Machine Learning

## Objective

Analyze the Titanic dataset and build classification and regression models while demonstrating standard machine-learning workflow practices.

Notebook:

```text
analytics/notebooks/titanic_analysis.ipynb
```

## Dataset

The Titanic dataset is initially loaded using:

```python
sns.load_dataset("titanic")
```

The downloaded dataset is immediately saved locally as:

```text
analytics/titanic.csv
```

This provides an offline fallback.

The cleaned dataset is:

```text
analytics/titanic_cleaned.csv
```

The final cleaned dataset contains:

```text
889 rows × 13 columns
```

with zero missing values.

## Exploratory Data Analysis

The notebook includes:

* dataset shape
* `info()`
* descriptive statistics
* missing-value analysis
* missing-value handling
* age distribution
* fare distribution
* boxplots
* IQR-based outlier analysis
* mean, median, and mode analysis
* skew interpretation
* survival by sex
* survival by passenger class
* survival by sex and passenger class
* multivariate visualizations

## Correlation analysis

The correlation analysis focuses on the required six numeric variables:

```text
survived
pclass
age
sibsp
parch
fare
```

Variables such as `adult_male` and `alone` are excluded from this correlation analysis.

The notebook includes a correlation heatmap and interpretation of the strongest relationships.

## Standardization

Age and fare are standardized using `StandardScaler`.

The notebook records the values before and after standardization to demonstrate the effect of scaling.

## Classification

The classification workflow uses a stratified train/test split followed by preprocessing fitted on the training data.

The preprocessing pipeline includes:

* numerical imputation
* categorical imputation
* one-hot encoding
* feature scaling

A `ColumnTransformer` and `Pipeline` are used to keep preprocessing and model fitting together.

Three classifiers are evaluated:

1. Logistic Regression
2. Decision Tree
3. Random Forest

Evaluation includes:

* confusion matrix
* accuracy
* precision
* recall
* F1-score
* ROC-AUC

The decision tree structure is also visualized using `plot_tree`.

## Class imbalance

The notebook compares:

* baseline classification
* `class_weight="balanced"`
* SMOTE applied to training data

Precision, recall, and F1-score are compared to show the effect of imbalance handling.

## Random Forest tuning

`GridSearchCV` is used to tune the Random Forest over parameters including:

* `n_estimators`
* `max_depth`
* `max_features`

The Random Forest estimator uses:

```python
oob_score=True
```

The best parameters and OOB score are recorded in the notebook.

## Regression

A Linear Regression model is used to predict fare from passenger features.

The notebook reports:

* MAE
* RMSE
* R²
* adjusted R²

A residual plot is used to inspect the model errors and discuss possible heteroscedasticity.

## Saved model

The complete fitted preprocessing and estimator pipeline is saved as:

```text
analytics/best_titanic_model.joblib
```

The notebook also demonstrates reloading the saved pipeline and making predictions on raw input data.

---

# Module 3 — GenAI Support Assistant

## Objective

Build a retrieval-augmented customer support assistant using a local vector database and optional local LLM generation.

Architecture:

```text
Support Documents
       │
       ▼
   Chunking
       │
       ▼
Sentence Transformers
all-MiniLM-L6-v2
       │
       ▼
    ChromaDB
       │
       ▼
User Question
       │
       ▼
LangGraph
       │
       ├── classify_intent
       │
       ├── retrieve_and_answer
       │
       └── direct_answer
       │
       ▼
Pydantic Validation
       │
       ▼
FastAPI /ask
```

## Knowledge base

The assistant uses exactly eight support documents:

```text
doc_01.txt
doc_02.txt
doc_03.txt
doc_04.txt
doc_05.txt
doc_06.txt
doc_07.txt
doc_08.txt
```

They are stored in:

```text
support_assistant/docs/
```

## Step 1 — Build the vector database

Run:

```bash
python support_assistant/ingest.py
```

The ingestion process:

1. Reads all eight documents
2. Removes unnecessary UTF-8 BOM characters
3. Splits documents into chunks
4. Creates embeddings using:

```text
all-MiniLM-L6-v2
```

5. Stores the chunks and embeddings in ChromaDB

The resulting ChromaDB data is stored locally under:

```text
support_assistant/chroma_db/
```

The database is regenerated whenever `ingest.py` is run.

## Step 2 — Test retrieval

Run:

```bash
python support_assistant/query.py
```

This embeds a query and retrieves the top three relevant chunks from ChromaDB.

## LangGraph workflow

The assistant uses a LangGraph `StateGraph` with a typed state.

### Node 1 — `classify_intent`

A lightweight keyword-based classifier identifies whether the question is a support question.

Examples of recognized support topics include:

* delivery
* returns
* refunds
* membership
* tracking
* cancellation
* gift cards
* damaged/spoiled/missing orders
* support hours

### Node 2 — `retrieve_and_answer`

For support questions:

1. Embed the query
2. Retrieve the top three ChromaDB results
3. Build a grounded prompt
4. Generate an answer
5. Validate the result using Pydantic

The mock mode produces a deterministic answer based on the retrieved context.

When real LLM mode is enabled, the application can use the local Ollama model.

### Node 3 — `direct_answer`

For general questions outside the support retrieval path, the assistant returns a deterministic general support response.

## Prompt design

The RAG prompt explicitly contains:

* Role
* Context
* Task
* Format
* Length
* Negative constraint
* Few-shot example

The negative constraint instructs the assistant not to invent:

* policies
* prices
* deadlines
* refunds
* other unsupported information

If the retrieved context is insufficient, the assistant is instructed to state that there is not enough information.

## Pydantic response validation

The response schema is:

```json
{
  "answer": "string",
  "sources": ["source_id"],
  "confidence": 0.0
}
```

`confidence` is constrained to the range:

```text
0.0 to 1.0
```

Invalid real-LLM responses are retried up to two additional times with a validation-focused instruction.

---

# FastAPI

The support assistant exposes:

```text
POST /ask
```

Request:

```json
{
  "query": "What should I do if my order arrives damaged?"
}
```

Example response in mock mode:

```json
{
  "answer": "Based on the retrieved context: If an order arrives with damaged, spoiled, or missing items...",
  "sources": [
    "doc_06.txt_chunk_1",
    "doc_02.txt_chunk_1",
    "doc_04.txt_chunk_1"
  ],
  "confidence": 0.9
}
```

## Run FastAPI locally

From the project root:

```bash
python -m uvicorn support_assistant.main:app --host 127.0.0.1 --port 8000
```

The API is then available at:

```text
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Mock mode

Mock mode is enabled by default:

```text
MOCK_LLM=1
```

On Windows PowerShell:

```powershell
$env:MOCK_LLM="1"
python -m uvicorn support_assistant.main:app --host 127.0.0.1 --port 8000
```

Mock mode does not require a paid API or external LLM service.

## Local Ollama mode

The project was also tested with a local Ollama model:

```text
llama3:latest
```

To enable the real local LLM path:

```powershell
$env:MOCK_LLM="0"
python support_assistant/rag_assistant.py
```

Ollama must already be running locally.

The real local LLM test successfully generated a grounded answer for a damaged-order question and returned its source ID and confidence.

---

# Docker

The support assistant includes:

```text
support_assistant/Dockerfile
```

The Docker image uses Python 3.11 and runs FastAPI with Uvicorn.

## Build

From the project root:

```bash
docker build -f support_assistant/Dockerfile -t zepto-support-assistant .
```

## Run

```bash
docker run -d --name zepto-support -p 8000:8000 zepto-support-assistant
```

Check the container:

```bash
docker ps
```

The container runs FastAPI on:

```text
http://localhost:8000
```

## Docker API test

PowerShell:

```powershell
$body = @{query="What should I do if my order arrives damaged?"} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:8000/ask" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

The Docker image uses:

```text
MOCK_LLM=1
```

by default so that it does not depend on an Ollama server inside the container.

---

# Design Decisions

## Reproducibility

The project saves important generated datasets and model artifacts locally so the workflow can be reproduced without repeatedly downloading the same data.

Examples:

```text
data_pipeline/books.csv
data_pipeline/books.db
analytics/titanic.csv
analytics/titanic_cleaned.csv
analytics/best_titanic_model.joblib
```

## Fixed exchange rate

The book pipeline uses a fixed conversion rate of:

```text
1 GBP = 105.50 INR
```

This makes the generated INR values deterministic.

## Offline Titanic fallback

The Titanic dataset is saved immediately after the initial load so later notebook analysis does not depend on repeated external dataset loading.

## Training-only preprocessing

Machine-learning preprocessing is fitted on the training data to reduce the risk of data leakage.

## Pipeline-based ML model

The saved Titanic model includes both preprocessing and the estimator so that raw input can be passed through the same transformations used during training.

## Local GenAI

The support assistant is designed to work without paid GenAI services.

The default mock mode provides deterministic behavior for evaluation and Docker execution.

Optional Ollama integration provides local LLM generation without requiring a paid cloud API.

## RAG grounding

The support assistant retrieves relevant support-document chunks before generating an answer. The prompt explicitly instructs the model to use the retrieved context and avoid unsupported claims.

## ChromaDB persistence

ChromaDB is used as the local vector store. Its database is generated from the eight source documents rather than being treated as the source of truth.

---

# End-to-End Execution

## Module 1

```bash
python data_pipeline/scrape_books.py
python data_pipeline/analyze_books.py
python data_pipeline/database_pipeline.py
python data_pipeline/sql_queries.py
python data_pipeline/sql_pandas_comparison.py
```

## Module 2

Open:

```text
analytics/notebooks/titanic_analysis.ipynb
```

Run the notebook from top to bottom.

The trained model is saved to:

```text
analytics/best_titanic_model.joblib
```

## Module 3

Build the vector database:

```bash
python support_assistant/ingest.py
```

Test retrieval:

```bash
python support_assistant/query.py
```

Run the API:

```bash
python -m uvicorn support_assistant.main:app --host 127.0.0.1 --port 8000
```

Or build and run Docker:

```bash
docker build -f support_assistant/Dockerfile -t zepto-support-assistant .
docker run -d --name zepto-support -p 8000:8000 zepto-support-assistant
```

---

# Git Workflow

Development was performed using a feature branch:

```text
feature/data-pipeline
```

The repository contains multiple commits covering:

* initial project setup
* documentation
* data scraping
* SQL/database pipeline
* EDA
* Titanic analytics
* RAG support assistant
* Docker support

The final feature branch should be merged back into `main` before submission.

---

# Final Capstone Outcome

The project demonstrates an end-to-end progression:

```text
Web Data
   │
   ▼
Data Cleaning
   │
   ▼
SQL Database
   │
   ▼
Analytics
   │
   ▼
Machine Learning
   │
   ▼
Embeddings
   │
   ▼
Vector Search
   │
   ▼
RAG Support Assistant
   │
   ▼
FastAPI
   │
   ▼
Docker
```

The three modules collectively demonstrate data ingestion, cleaning, SQL, pandas, exploratory analysis, machine learning, model evaluation, model persistence, embeddings, vector search, RAG, structured LLM output validation, API development, and containerization.
