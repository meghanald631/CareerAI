CareerAI Frontend - Backend Integration

1. Keep this Frontend folder inside your existing project.
2. Start FastAPI from the project root:
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8006
3. Open http://127.0.0.1:8006/docs to confirm the API is running.
4. Serve the Frontend folder through PyCharm's built-in server (usually localhost:63342).
5. Open index.html through that server, register or log in, then use the dashboard.

API base URL is set once in api.js:
   const API_BASE_URL = "http://127.0.0.1:8006";

If your backend uses another port, change that one line.

Backend contract notes:
- Profile creation is supported, but the supplied backend has no profile update endpoint.
- Candidate facts can be added, but the supplied backend has no endpoint to mark a fact as verified.
- The AI answer endpoint only uses verified facts, so it will report that no verified facts exist until the backend supports verification.
- The job document upload endpoint analyses a PDF/DOCX file. Job matching and resume/cover-letter generation currently use the text in the job description field; after uploading, paste the description text there if you want to use those actions.
- Resume and cover-letter generation require an existing saved application and are saved as application artifacts.
- This frontend does not contain or store API keys. Keep .env and secrets outside the Frontend folder.
