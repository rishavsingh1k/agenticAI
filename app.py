from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from graph import build_graph
import os

app = Flask(__name__)
CORS(app)

# Build LangGraph app
graph_app = build_graph()

# -------------------------------
# Serve Frontend (index.html)
# -------------------------------
@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")


# -------------------------------
# Ask API (POST)
# -------------------------------
def ask(question):
    state = {
        "question": question,
        "messages": [],
        "eval_retries": 0
    }
    result = graph_app.invoke(state)
    return result.get("answer", "No response")


@app.route("/ask", methods=["POST"])
def handle():
    try:
        data = request.get_json()
        question = data.get("question", "")
        answer = ask(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


# -------------------------------
# Run server (Render compatible)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)