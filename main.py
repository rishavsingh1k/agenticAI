from graph import build_graph

# build app
app = build_graph()

def ask(question, thread_id="1"):
    state = {
        "question": question,
        "messages": [],
        "eval_retries": 0
    }

    result = app.invoke(
        state,
        config={"configurable": {"thread_id": thread_id}}
    )

    return result["answer"]


# -------- INTERACTIVE MODE --------
if __name__ == "__main__":
    print("AI Assistant Started (type 'exit' to stop)\n")

    thread_id = "1"

    while True:
        q = input("You: ")

        if q.lower() == "exit":
            break

        ans = ask(q, thread_id=thread_id)
        print("AI:", ans)