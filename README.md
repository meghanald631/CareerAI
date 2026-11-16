# CareerAI — AI-Powered Job Application Agent

CareerAI is an AI-powered job application management platform designed to help job seekers organize their applications, analyze job descriptions, tailor application documents, and prepare for interviews.

The goal is to build a centralized application assistant that uses a candidate's verified profile, skills, experience, and previous application history to support a more structured and personalized job search.

> **Project Status:** Under Active Development

## Overview

Managing multiple job applications can become difficult when resumes, cover letters, recruiter communications, interview details, and application statuses are scattered across different platforms.

CareerAI aims to simplify this process by bringing these activities together in one platform and integrating AI-assisted features into the application workflow.

## Key Features

### 1. User Authentication
- User registration and login.
- JWT-based authentication.
- Protected user-specific information.

### 2. Candidate Profile Management
- Store candidate profile information.
- Manage technical and professional skills.
- Maintain candidate facts and experience information.

### 3. Job Application Management
- Create and track job applications.
- Update application statuses.
- Maintain application history.
- View application-related information.

### 4. AI-Powered Job Analysis
- Analyze job descriptions.
- Identify relevant skills and requirements.
- Support job-to-candidate matching.

### 5. Resume and Cover Letter Assistance
- AI-assisted resume generation.
- Personalized cover letter generation.
- Candidate information-based document preparation.

### 6. Document Processing
- Extract text from PDF documents.
- Extract text from DOCX documents.
- Analyze uploaded job-related documents.

### 7. Interview Preparation
- Store interview details.
- Manage interview questions.
- Generate interview-related answers.
- Track interview preparation information.

### 8. Application Communication and Insights
- Maintain application-related communication records.
- Track application artifacts.
- Provide application insights and improvement suggestions.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Database Integration | SQLAlchemy |
| Authentication | JWT |
| AI Integration | OpenAI API |
| Document Processing | PyMuPDF, python-docx |
| API Testing | Swagger UI |

## Project Structure

```text
CareerAI/
│
├── Frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── applications.html
│   ├── resume.html
│   ├── cover-letter.html
│   ├── job_analysis.html
│   ├── interviews.html
│   ├── insights.html
│   ├── api.js
│   ├── script.js
│   └── style.css
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── security.py
│   ├── token.py
│   ├── ai_service.py
│   ├── document_services.py
│   └── learning_service.py
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- OpenAI API key with available API credits
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/meghanald631/CareerAI.git
```

```bash
cd CareerAI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the Python packages required by the backend. A `requirements.txt` file will be added to make this installation reproducible.

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the database credentials and AI API key according to the variable names used in the backend configuration.

Do not commit `.env` or expose API keys, database passwords, or other credentials.

### 5. Start the Backend

From the project root, run:

```bash
uvicorn app.main:app --reload --port 8006
```

### 6. Access the API Documentation

Open:

```text
http://127.0.0.1:8006/docs
```

Swagger UI can be used to explore and test the available backend API endpoints.

## Current Development Status

CareerAI is an ongoing development project.

The current implementation includes the initial frontend, FastAPI backend, database integration, authentication, candidate information management, application-related modules, document extraction, and AI service integration.

The following areas are still being improved:

- Complete frontend and backend integration.
- Reliable end-to-end application workflows.
- AI API configuration and testing.
- Candidate fact verification.
- Document generation and artifact history.
- Deployment and production testing.

Some AI-powered features require a properly configured OpenAI API account with available API credits.

## Future Enhancements

- Improve the candidate knowledge base.
- Learn from historical job applications and recruiter responses.
- Improve resume and cover letter personalization.
- Add intelligent application recommendations.
- Automate more of the job application workflow.
- Deploy the application for public access.

## Project Repository

**GitHub:** https://github.com/meghanald631/CareerAI

---

*CareerAI is being developed as a practical project to explore the integration of artificial intelligence, backend development, database management, and job application workflows.*