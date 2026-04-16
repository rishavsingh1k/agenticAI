from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def memory_node(state):
    msgs = state.get("messages", [])
    msgs.append(state["question"])
    return {"messages": msgs[-6:]}


def router_node(state):
    q = state["question"].lower()

    if "time" in q or "date" in q:
        return {"route": "tool"}
    elif "remember" in q or "previous" in q:
        return {"route": "skip"}
    else:
        return {"route": "retrieve"}


def retrieval_node(state):
    return {"retrieved": "", "sources": []}


def skip_node(state):
    return {"retrieved": "", "sources": []}


def tool_node(state):
    return {"tool_result": f"Current date and time is: {datetime.now()}"}


def answer_node(state):
    question = state["question"]
    context = state.get("retrieved", "")
    tool_result = state.get("tool_result", "")

    if tool_result:
        return {"answer": tool_result}

    prompt = f"""
You are a helpful AI assistant.

If context is provided, use it.
If no context, answer normally using your knowledge.

Context:
{context}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ latest working model
            messages=[{"role": "user", "content": prompt}]
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"answer": f"Error occurred: {str(e)}"}


def eval_node(state):
    return {
        "faithfulness": 1.0,
        "eval_retries": state.get("eval_retries", 0) + 1
    }


def save_node(state):
    msgs = state.get("messages", [])
    msgs.append(state["answer"])
    return {"messages": msgs}