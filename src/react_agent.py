# src/react_agent.py
import os
import json
from typing import Any, Dict
from dotenv import load_dotenv
import requests

from .tools import overall_churn_rate, churn_rate_by_column

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"  # or compatible model name

TOOL_REGISTRY = {
    "overall_churn_rate": overall_churn_rate,
    "churn_rate_by_column": churn_rate_by_column,
}

TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "overall_churn_rate",
            "description": "Get overall churn rate across all telecom customers.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "churn_rate_by_column",
            "description": (
                "Get churn rate grouped by a categorical column "
                "such as 'contract', 'payment_method', or 'internet_service'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Name of the column to group by.",
                    }
                },
                "required": ["column"],
            },
        },
    },
]


def call_llm(messages: list, tools: list | None = None, tool_choice: str = "auto") -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": MODEL,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = tool_choice

    resp = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def react_telecom_agent(question: str) -> str:
    """
    Simple ReAct-style loop:
      - Give the model tools
      - Let it decide whether to call them
      - Execute tool calls, feed back results
      - Stop when model gives a final answer
    """
    messages: list[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a telecom churn analytics assistant. "
                "You can use tools to compute churn metrics. "
                "Think step-by-step and call tools when needed. "
                "If you use a tool, explain the results in your final answer."
            ),
        },
        {"role": "user", "content": question},
    ]

    for _ in range(5):  # limit number of tool-use cycles
        result = call_llm(messages, tools=TOOL_DESCRIPTIONS)
        msg = result["choices"][0]["message"]

        # If no tool_calls, model is giving final answer
        if "tool_calls" not in msg:
            return msg.get("content", "")

        # Handle each tool call
        for tool_call in msg["tool_calls"]:
            name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"] or "{}")
            tool_fn = TOOL_REGISTRY.get(name)

            if not tool_fn:
                tool_result = {"error": f"Unknown tool: {name}"}
            else:
                try:
                    tool_result = tool_fn(**args)
                except Exception as e:
                    tool_result = {"error": str(e)}

            # Add the tool call and result back into the conversation
            messages.append(msg)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": json.dumps(tool_result),
                }
            )

    return "I couldn't compute an answer within my tool-use limit."


if __name__ == "__main__":
    q = "What is the overall churn rate, and which contract type has the highest churn?"
    ans = react_telecom_agent(q)
    print(ans)
