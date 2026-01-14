# Telecom Churn ReAct Agent

A FastAPI-based application that uses a ReAct (Reasoning and Acting) agent to analyze telecom customer churn data. The agent can answer questions about overall churn rates and churn metrics grouped by various categories (e.g., contract type, payment method).

## Features

- **Natural Language Querying**: Ask questions about churn data in plain English.
- **ReAct Agent**: Uses OpenAI's GPT models to reason about the user's question and call appropriate analytical tools.
- **Data Analysis**:
  - Calculate overall churn rates.
  - Analyze churn rates grouped by specific columns (e.g., Contract, PaymentMethod).
- **FastAPI Server**: Exposes a REST API for interacting with the agent.

## Project Structure

- `src/`: Source code for the application.
  - `api.py`: FastAPI application and route definitions.
  - `react_agent.py`: Implementation of the ReAct agent logic.
  - `tools.py`: Data analysis tools used by the agent.
  - `telecom_data.py`: Data loading and preprocessing.
- `data/`: Contains the dataset (`telecom_users.csv`).
- `tests/`: Test suite.
- `main.py`: Entry point to run the application.

## Prerequisites

- Python 3.11+
- An OpenAI API Key

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd telecom-churn-react-agent
   ```

2. **Install dependencies:**
   This project uses `uv` for dependency management, but standard `pip` works too.
   ```bash
   # Using pip
   pip install -r requirements.txt  # (If you generate one)
   # OR directly using pyproject.toml
   pip install -e .
   ```

3. **Configure Environment:**
   Copy the example environment file and add your OpenAI API key.
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Running the Server

Start the API server using the entry point script:

```bash
python main.py
```

The server will start at `http://0.0.0.0:8000`.

### API Documentation

Once the server is running, you can access the interactive API docs at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Example Request

**Endpoint:** `POST /ask`

**Payload:**
```json
{
  "question": "What is the overall churn rate?"
}
```

**Response:**
```json
{
  "answer": "The overall churn rate is approximately 26.5%."
}
```
