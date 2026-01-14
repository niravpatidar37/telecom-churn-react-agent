# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from .react_agent import react_telecom_agent

app = FastAPI(title="Telecom Churn ReAct Agent")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask_agent(q: Question):
    answer = react_telecom_agent(q.question)
    return {"answer": answer}
