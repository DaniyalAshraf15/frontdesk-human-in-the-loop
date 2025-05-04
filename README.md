# Frontdesk AI Supervisor Dashboard

This project is a prototype for a Human-in-the-Loop AI voice assistant system built for **Frontdesk**. The goal is to simulate an AI receptionist that escalates questions it cannot answer, stores supervisor responses, and learns over time.

---

## Features

### ✅ Real-Time Voice-to-Text AI Agent

* Built with **LiveKit Agents SDK**
* Accepts voice input through microphone (browser-based)
* Transcribes audio and processes queries

### 🧱 Escalation System

* If AI doesn't know the answer, it escalates to a supervisor
* Creates a pending request
* Notifies the supervisor via dashboard

### ✉️ Supervisor Interface

* View all pending help requests
* Submit answers manually
* Automatically responds back to original caller

### 💡 Learned Knowledge Base

* Automatically updates internal knowledge with new supervisor answers
* New answers are visible in a "Learned Answers" section of the UI

---

## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-repo/frontdesk-ai.git
cd frontdesk-ai
```

### 2. Backend Setup (Flask)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python api.py  # Starts the Flask server
```

### 3. Voice Agent Setup (LiveKit)

```bash
# Requires Python 3.9+
source venv/bin/activate
python main.py dev  # Starts LiveKit agent
```

### 4. Frontend

Simply open `index.html` in a browser.

---

## API Endpoints

### POST `/call`

* Handles voice or text question
* If answer is found, returns `status: answered`
* If not found, escalates and returns `status: escalated`

### GET `/pending-requests`

* Returns all pending help requests

### POST `/resolve-request`

* Supervisor submits answer for a help request

### GET `/learned-answers`

* Returns the current knowledge base (questions + answers)

---

## Example Flow

1. User speaks into the mic: *"Do you offer hair coloring?"*
2. If AI knows: returns answer immediately
3. If AI doesn't know:

   * Escalates and creates a help request
   * Supervisor logs into dashboard
   * Submits an answer
   * AI replies to user & learns this answer

---

## File Structure

```
/
|-- api.py                # Flask backend with business logic
|-- main.py               # LiveKit voice agent logic
|-- index.html            # Supervisor Dashboard
|-- knowledge_base.json   # Stores learned answers
|-- help_requests.json    # Tracks escalated help tickets
```

---

## Future Improvements

* Real-time WebSocket updates
* Persistent DB storage (PostgreSQL / DynamoDB)
* Timeout handling & analytics
* Live call transfer to supervisors

---



---

## License

MIT

---

Built with ❤️ for Frontdesk.ai Engineering Test.
