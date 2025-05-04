from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models.help_request import HelpRequest
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers="*")


# Load static knowledge base
knowledge_base = {
    "what are your salon hours?": "We are open from 9 AM to 7 PM, Monday to Saturday.",
    "do you offer hair coloring?": "Yes, we offer a full range of hair coloring services!"
}

# Load dynamic learned knowledge base
if os.path.exists('knowledge_base.json'):
    with open('knowledge_base.json', 'r') as f:
        dynamic_knowledge = json.load(f)
else:
    dynamic_knowledge = {}



# Load environment variables
load_dotenv()



# Dummy Knowledge Base
knowledge_base = {
    "what are your salon hours?": "We are open from 9 AM to 7 PM, Monday to Saturday.",
    "do you offer hair coloring?": "Yes, we offer a full range of hair coloring services!"
}

help_requests = []  # List to store all help requests temporarily

@app.route('/call', methods=['POST'])
def receive_call():
    data = request.json
    question = data.get("question", "").lower()
    caller_info = data.get("caller_info", "Unknown Caller")

    # 🔄 Reload the dynamic knowledge base each time
    global dynamic_knowledge
    try:
        if os.path.exists('knowledge_base.json'):
            with open('knowledge_base.json', 'r') as f:
                dynamic_knowledge = json.load(f)
        else:
            dynamic_knowledge = {}
    except:
        dynamic_knowledge = {}

    # First check in static knowledge
    if question in knowledge_base:
        response = knowledge_base[question]
        print(f"[AI Agent] Responding from static knowledge base: {response}")
        return jsonify({"response": response, "status": "answered"}), 200

    # Then check in learned dynamic knowledge
    if question in dynamic_knowledge:
        response = dynamic_knowledge[question]
        print(f"[AI Agent] Responding from learned knowledge base: {response}")
        return jsonify({"response": response, "status": "answered"}), 200

    # If not known → Escalate
    print(f"[AI Agent] I don't know the answer to: {question}. Requesting supervisor help.")

    help_request = HelpRequest(question=question, caller_info=caller_info)
    help_requests.append(help_request.to_dict())

    with open('help_requests.json', 'w') as f:
        json.dump(help_requests, f, indent=4)

    print(f"[Supervisor Alert] Help needed for question: '{question}' from {caller_info}")

    return jsonify({
        "response": "Let me check with my supervisor and get back to you.",
        "status": "escalated",
        "help_request_id": help_request.id
    }), 200

@app.route('/pending-requests', methods=['GET'])
def get_pending_requests():
    try:
        with open('help_requests.json', 'r') as f:
            help_requests = json.load(f)
    except FileNotFoundError:
        help_requests = []

    pending = [req for req in help_requests if req['status'] == "Pending"]
    return jsonify(pending), 200
# Save new learning into knowledge_base.json

@app.route('/resolve-request', methods=['POST'])
def resolve_request():
    data = request.json
    request_id = data.get('id')
    answer = data.get('answer')

    try:
        with open('help_requests.json', 'r') as f:
            help_requests = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "No help requests found."}), 404

    updated = False

    for req in help_requests:
        if req['id'] == request_id and req['status'] == "Pending":
            req['status'] = "Resolved"
            req['resolved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            req['answer'] = answer
            updated = True
            break

    if updated:
        with open('help_requests.json', 'w') as f:
            json.dump(help_requests, f, indent=4)

        # Save new learning into knowledge_base.json
        try:
            if os.path.exists('knowledge_base.json'):
                with open('knowledge_base.json', 'r') as f:
                    dynamic_knowledge = json.load(f)
            else:
                dynamic_knowledge = {}
        except:
            dynamic_knowledge = {}

        dynamic_knowledge[req['question']] = req['answer']

        with open('knowledge_base.json', 'w') as f:
            json.dump(dynamic_knowledge, f, indent=4)

        return jsonify({"message": "Request resolved."}), 200

    else:
        return jsonify({"error": "Request not found or already resolved."}), 404
@app.route("/learned-answers", methods=["GET"])
def get_learned_answers():
    if os.path.exists('knowledge_base.json'):
        with open('knowledge_base.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
