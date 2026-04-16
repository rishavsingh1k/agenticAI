from flask import Flask, request, jsonify
from flask_cors import CORS
from graph import build_graph

app = Flask(__name__)
CORS(app)

graph_app = build_graph()

def ask(question):
    state = {
        "question": question,
        "messages": [],
        "eval_retries": 0
    }
    result = graph_app.invoke(state)
    return result["answer"]

@app.route("/ask", methods=["POST"])
def handle():
    data = request.json
    question = data.get("question", "")
    answer = ask(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)