## LASSO Grant Tagging System


### How I Put It Together
- I kept the Flask app focused on a single job: accept grants, call Groq’s LLaMA 3.1 model, and persist the tagged payloads in MongoDB.
- I stored the curated tag list in Python as required in the assessment instructions.
- I exposed clean endpoints (`/api/grants`, `/api/tags`, `/api/health`) and leaned on `flask-cors` so the React client can talk to the API without ceremony.
- I built the UI around two tabs— Add and Browse —so I can quickly seed data, then filter grants by the tags the model returns.

### Run It Locally
1. **Backend**
   - `cd backend`
   - `python -m venv venv && venv\Scripts\activate`
   - `pip install -r requirements.txt`
   - Create `.env` with `MONGO_URL=<connection-string>` and `GROQ_API_KEY=<key>`
   - `python app.py`

2. **Frontend**
   - `cd frontend`
   - `npm install`
   - `npm run dev`

The React app expects the API at `http://localhost:5000`. I start the backend first, then open the Vite URL that prints in the terminal. Once both are up, I can add grants, watch the tags roll in, and filter them in real time.
