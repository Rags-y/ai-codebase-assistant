# AI Codebase & Bug Investigation Assistant

An AI-powered codebase investigation assistant that uses code-aware chunking, semantic retrieval, graph-based relationships, and an LLM to answer questions about a software repository.

Instead of searching through files manually, you can ask questions such as:

* How are tasks created?
* Which function deletes a task?
* Which functions use the `Task` model?
* How does task updating work?
* What validates task input?
* How does the API handle a missing task?

The assistant retrieves relevant code, builds a grounded context, and generates an explanation with file and line references.



## Features

* Recursive repository ingestion
* Python AST-based code chunking
* Sentence Transformer embeddings
* Semantic code retrieval
* Metadata-rich code chunks
* Code relationship extraction
* Graph-based investigation
* Context construction with file and line information
* Groq-powered answer generation
* Retrieval evaluation
* Generation evaluation
* Faithfulness evaluation
* Relevance evaluation
* Simple command-line interface



## Architecture

```text
                    Local Git Repository
                            │
                            ▼
                  Repository Ingestion
                            │
                            ▼
                 AST-Based Code Chunking
                            │
                            ▼
                       Embeddings
                            │
                            ▼
                  Semantic Retrieval
                            │
                            ├──────────────┐
                            │              │
                            ▼              ▼
                    Entity Resolution   Graph
                            │              │
                            └──────┬───────┘
                                   ▼
                         Retrieval Pipeline
                                   │
                                   ▼
                         Context Construction
                                   │
                                   ▼
                              Groq LLM
                                   │
                                   ▼
                       Grounded Code Answer
```



## Tech Stack

* **Python**
* **Pydantic**
* **Python AST**
* **Sentence Transformers**
* **NumPy**
* **Groq API**
* **GPT-OSS 120B**
* **Git / GitHub**



## Project Structure

```text
ai-codebase-assistant/
│
├── src/
│   ├── ingestion/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── chunks.py
│   │   └── code_chunker.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── retrieval/
│   │   ├── semantic.py
│   │   ├── hybrid.py
│   │   ├── entity_resolver.py
│   │   ├── investigator.py
│   │   ├── pipeline.py
│   │   ├── context.py
│   │   └── reranker.py
│   │
│   ├── graph/
│   │   ├── models.py
│   │   ├── extractor.py
│   │   └── retriever.py
│   │
│   └── generation/
│       └── generator.py
│
├── scripts/
│   ├── build_chunks.py
│   ├── build_embeddings.py
│   ├── build_graph.py
│   ├── ask.py
│   ├── evaluate_retrieval.py
│   ├── evaluate_generation.py
│   ├── evaluate_faithfulness.py
│   ├── evaluate_relevance.py
│   └── ...
│
├── data/
│   └── processed/
│       ├── chunks.json
│       ├── embeddings.npy
│       ├── relationships.json
│       └── evaluation_questions.json
│
└── README.md
```



## How It Works

### 1. Repository ingestion

The repository scanner recursively finds supported source files and extracts metadata such as:

* File path
* Filename
* Programming language
* File size
* Modification time
* Content hash

Ignored directories such as `.git`, `.venv`, `node_modules`, and cache directories are skipped.

### 2. Code-aware chunking

Instead of splitting code into arbitrary text windows, Python files are parsed using the Python AST.

The system creates chunks for:

* Functions
* Async functions
* Classes
* Module-level context

Each chunk stores its file path and source line range.

Example:

```text
routes.py:12-27
create_task
```

### 3. Embeddings

Each code chunk is converted into a vector using:

```text
all-MiniLM-L6-v2
```

The resulting embeddings are stored locally and used for semantic similarity search.

### 4. Semantic retrieval

When a user asks a question, the question is embedded and compared against the stored code embeddings.

The system retrieves the most relevant code chunks.

### 5. Code relationships

The project also extracts relationships between code entities.

For example:

```text
create_task
    │
    └── uses ──► Task
```

This allows the system to investigate relationships between functions and models rather than relying only on semantic similarity.

### 6. Context construction

Retrieved chunks are formatted with metadata:

```text
routes.py:12-27
Name: create_task
Source: semantic

<code>
```

This gives the language model precise information about where the retrieved code came from.

### 7. Answer generation

The retrieved context is passed to the Groq API.

The model is instructed to:

* Use only the provided code context
* Avoid inventing information
* Explain the relevant implementation
* Reference file paths and line numbers
* State when evidence is insufficient



## Example

### Question

```text
How are tasks created?
```

### Answer

The assistant identifies:

```text
routes.py:12-27
create_task
```

and explains that the function:

1. Receives a `Task` model.
2. Uses `next_task_id` to generate an ID.
3. Stores the task in the `tasks` dictionary.
4. Uses `task.model_dump()` to convert the model to a dictionary.
5. Increments the ID counter.
6. Returns the created task.



## Evaluation

The project includes a 10-question evaluation dataset covering common codebase investigation tasks.

### Retrieval

| Metric    |   Result |
| --------- | -------: |
| Recall    | **1.00** |
| Precision | **0.32** |

The retrieval system found the expected evidence for all 10 questions.

The relatively lower precision reflects the small demonstration repository and the intentionally broad semantic retrieval candidate set.

### Generation

| Metric        |   Result |
| ------------- | -------: |
| Concept Score | **0.97** |

The generated answers successfully covered the expected concepts across the evaluation questions.

### Faithfulness

| Metric                   |    Result |
| ------------------------ | --------: |
| Average Faithfulness     |  **0.97** |
| Fully Faithful Questions | **10/10** |

### Relevance

| Metric             |    Result |
| ------------------ | --------: |
| Average Relevance  |  **1.00** |
| Relevant Questions | **10/10** |

These results are based on the project's current 10-question evaluation dataset.



## Reranking Experiment

A cross-encoder reranking experiment was also tested separately.

Baseline:

```text
Recall:    1.00
Precision: 0.32
```

Cross-encoder reranking:

```text
Recall:    0.85
Precision: 0.26
```

Because the experiment did not improve the baseline on the current evaluation set, it was not adopted into the main retrieval pipeline.

This keeps the final system simpler while retaining the experiment as part of the project's retrieval engineering analysis.



## Setup

Clone the repository and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Set the Groq API key:

```powershell
$env:GROQ_API_KEY="your_api_key"
```

Set the Python path:

```powershell
$env:PYTHONPATH="$PWD"
```



## Run the Assistant

Start the CLI:

```powershell
python scripts/ask.py
```

Example:

```text
AI CODEBASE & BUG INVESTIGATION ASSISTANT

Ask a question about the codebase: How are tasks created?
```

The assistant retrieves relevant code and generates a grounded answer.



## Build the Index for a Repository

The current demonstration uses the FastAPI Task Manager repository.

The processing pipeline can be run through:

```powers
```
## Author
Raghav Kumar
