# src/react_agent.py
import json
import logging
from typing import Any, Dict, List

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from .config import settings
from .tools import overall_churn_rate, churn_rate_by_column

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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


def react_telecom_agent(question: str) -> str:
    """
    Simple ReAct-style loop using OpenAI SDK:
      - Give the model tools
      - Let it decide whether to call them
      - Execute tool calls, feed back results
      - Stop when model gives a final answer
    """
    messages: List[Dict[str, Any]] = [
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
        try:
            response = client.chat.completions.create(
                model=settings.MODEL,
                messages=messages,
                tools=TOOL_DESCRIPTIONS,
                tool_choice="auto",
            )
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return "I encountered an error communicating with the AI service."

        msg = response.choices[0].message
        
        # Add the assistant's message to conversation
        messages.append(msg)

        # If no tool_calls, model is giving final answer
        if not msg.tool_calls:
            return msg.content or ""

        # Handle each tool call
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args_str = tool_call.function.arguments or "{}"
            try:
                args = json.loads(args_str)
                tool_fn = TOOL_REGISTRY.get(name)

                if not tool_fn:
                    tool_result = {"error": f"Unknown tool: {name}"}
                else:
                    tool_result = tool_fn(**args)
            except json.JSONDecodeError:
                tool_result = {"error": "Invalid JSON arguments"}
            except Exception as e:
                tool_result = {"error": str(e)}

            # Add the tool result back into the conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": json.dumps(tool_result),
                }
            )

    return "I couldn't compute an answer within my tool-use limit."


if __name__ == "__main__":
    q = "What is the overall churn rate, and which contract type has the highest churn?"
    ans = react_telecom_agent(q)
    print(ans)
