from langgraph.graph import StateGraph, END
from state import CapstoneState

# import all nodes
from nodes import (
    memory_node,
    router_node,
    retrieval_node,
    skip_node,
    tool_node,
    answer_node,
    eval_node,
    save_node
)


# ---------- ROUTING ----------

def route_decision(state):
    return state["route"]


def eval_decision(state):
    # retry if low confidence
    if state.get("faithfulness", 1.0) < 0.7 and state.get("eval_retries", 0) < 2:
        return "answer"
    return "save"


# ---------- BUILD GRAPH ----------

def build_graph():
    graph = StateGraph(CapstoneState)

    # nodes
    graph.add_node("memory", memory_node)
    graph.add_node("router", router_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("skip", skip_node)
    graph.add_node("tool", tool_node)
    graph.add_node("answer", answer_node)
    graph.add_node("eval", eval_node)
    graph.add_node("save", save_node)

    # entry
    graph.set_entry_point("memory")

    # flow
    graph.add_edge("memory", "router")

    # router decision
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "retrieve": "retrieve",
            "skip": "skip",
            "tool": "tool"
        }
    )

    # after action → answer
    graph.add_edge("retrieve", "answer")
    graph.add_edge("skip", "answer")
    graph.add_edge("tool", "answer")

    # evaluation
    graph.add_edge("answer", "eval")

    graph.add_conditional_edges(
        "eval",
        eval_decision,
        {
            "answer": "answer",   # retry
            "save": "save"
        }
    )

    # end
    graph.add_edge("save", END)

    return graph.compile()