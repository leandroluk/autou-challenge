# AutoU Challenge - Email Analisys

## 📖 About the Project
This project was developed as part of a technical challenge to create a digital email triage solution for the financial sector. The system uses Artificial Intelligence (LLMs) to automatically classify incoming emails as "Productive" or "Unproductive" and suggest replies, optimizing the team's workflow.

## 🏗️ Project Architecture
The project follows a **Monorepo** structure, divided into three main applications:

- **API (`apps/api`)**: Backend application developed in Python with **FastAPI**. It follows **Domain-Driven Design (DDD)** principles and a **Ports and Adapters** (Hexagonal) architecture. It integrates with multiple AI providers: **Gemini, OpenAI, and Anthropic**, sending the content extracted from PDF files or free text directly for analysis by the language model.
- **Web (`apps/web`)**: Built with **Next.js**, **Tailwind CSS**, and **shadcn/ui** components. Developed with an emphasis on intuitive design. It has a complete configuration for CSS class obfuscation for security and optimization.
- **E2E (`apps/e2e`)**: End-to-end automated testing suite using the **Robot Framework**, ensuring the quality and functioning of the entire platform systemically.

## 🚀 Features
- **Email Classification**: Evaluates whether an email is Productive (requires immediate action like support, commercial questions) or Unproductive (does not require immediate action, e.g., congratulatory emails).
- **Reply Suggestion**: Depending on the classification and content of the email, it generates a short and relevant automatic reply.
- **AI Options**: The interface allows dynamically choosing which provider (LLM) to use: Gemini 2.5 Flash, ChatGPT 4o-mini, or Claude 3.5 Sonnet.
- **Flexible Interface**: Users on the web can triage an email either by *copying/pasting* the text or *uploading a PDF document*.

## 🛠️ Technologies Used
- **Backend:** Python 3.13, FastAPI, Uvicorn, Pydantic, PyMuPDF.
- **Frontend:** Next.js (React), Tailwind CSS, TypeScript, Vitest, Zod.
- **E2E Tests:** Robot Framework.
- **Code Quality and Typing (Backend):** Use of **Ruff** as an ultra-fast Linter/Formatter for syntax checks and **Pyright** as a *Type Checker*, ensuring development safety with strong and strict typing in Python.
- **Package Manager:** `uv` (for Python) and `pnpm` (for Javascript).

---

## 🔀 API Documentation (Use Cases and OpenAPI Format)
Fundamental endpoints for communication with the AIs. The API is exposed based on these main routes:

### 1. Email Analysis (`POST /api/v1/email/analyze`)
Analyzes a received email (free text or PDF) to obtain the classification and a suggested reply generated via LLM.

**Request (`multipart/form-data`):**
- `provider` (string, required): LLM provider to be used. Valid options: `gemini:2.5-flash`, `anthropic:claude-sonnet-4.5`, `openai:gpt-4o-mini`.
- `api_key` (string, required): Authentication API key of the selected provider.
- `file` (binary/octet-stream, optional): Email file in **PDF** format.
- `text` (textarea, optional): Free text containing the complete email. (Ex: `Subject: Hello\n\nThis is a long email body content...`).

**Success Response (`200 OK` - `application/json`):**
```json
{
  "category": "Productive",
  "reply": "Thank you for your email. I will get back to you as soon as possible."
}
```
* **category:** `Productive` or `Unproductive`.
* **reply:** The suggested reply.

### 2. Health Check (`GET /api/v1/system/health`)
Verifies the backend system's integrity and its availability.

**Success Response (`200 OK` - `application/json`):**
```json
{
  "status": "ok",
  "uptime": "1h"
}
```

---

## ⚙️ How to Run the Project Locally

### Prerequisites
- [Python 3.13+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/)
- [uv](https://docs.astral.sh/uv/) (Innovative environment and dependency manager for Python)
- **Make:** Necessary to orchestrate and run `Makefile` commands.
- **Docker:** Necessary to build and manage the project's containers.
- At least one LLM API Key (Gemini, OpenAI, or Anthropic).

### 🔑 Obtaining API Keys (LLMs)
For the AI email analysis to work, you will need to generate an API Key from your preferred provider.

> **Important Notice:** Currently, only **Google Gemini** offers a robust **free tier** quota. To run with OpenAI (ChatGPT) or Anthropic (Claude), it is mandatory to add balance/credits to their respective accounts (Billing) for the API to work without errors.

- **Google Gemini (Recommended / Free):** Access the [Google AI Studio](https://aistudio.google.com/app/apikey), log in with your Google account, and click **"Create API key"**.
- **OpenAI (ChatGPT):** Access the [OpenAI Developer Platform](https://platform.openai.com/api-keys), create an account, and click **"Create new secret key"**. *Requires prior credit recharge.*
- **Anthropic (Claude):** Access the [Anthropic Console](https://console.anthropic.com/settings/keys), authenticate, and click **"Create Key"**. *Requires prior credit recharge.*

### 🐳 Running via Docker Compose (Recommended)
The most practical and fastest way to spin up the environments with ready routing is through Docker, which will mount your API, Frontend, and Nginx (reverse proxy to access subdomains):

1. **Clone the repository:**
```bash
git clone https://github.com/leandroluk/autou-challenge.git
cd autou-challenge
```

2. **Configure your Environment Variables:**  
Rename the `.env.example` files to `.env` in the corresponding folders `apps/api/.env` (optional if you want to redefine the base) and include your `NEXT_PUBLIC_API_URL=http://api.localhost.nip.io` variable in the `apps/web` `.env` (or simply leave default).

3. **Start the Containers:**
```bash
docker compose up -d --build
```
Wait until images are downloaded and compiled.

4. **All set! Access the application:**
- **Web Page:** [http://web.localhost.nip.io](http://web.localhost.nip.io)
- **API Documentation:** [http://api.localhost.nip.io/docs](http://api.localhost.nip.io/docs)

---

### 💻 Running Manually (Development Mode)

1. **Clone the repository:**
```bash
git clone https://github.com/leandroluk/autou-challenge.git
cd autou-challenge
```

2. **Install dependencies with `Makefile` via root:**
The Makefile in the root orchestrates the installation of API/E2E dependencies (via `uv`) and the Web application (via `pnpm`).
```bash
make install
```

3. **Environment Variables Configuration:**
Some folders have examples of actual environments. Rename and fill out these example files so the project can integrate with the appropriate panels:
- `apps/api/.env.example` -> `apps/api/.env`
- `apps/e2e/.env.example` -> `apps/e2e/.env`
*(Insert your preferred provider's `API_KEY` in the frontend and the variables in the global envs)*

4. **Tests, Lint, and Formatting:**
There are global commands configured in the main `Makefile` to run across the entire monorepo:
- `make test`: Runs unit tests (API/Web).
- `make lint`: Runs the linter (Ruff for python, ESLint for web).
- `make format`: Interactively formats the code.

5. **Running the Applications:**
Since this is a monorepo, you can expose the backend and frontend simultaneously in separate tabs in your terminal:
- **API:**
  ```bash
  make _run CMD="run uvicorn src.__main__:app --reload"
  # or alternatively from the API root:
  # cd apps/api && uv run python -m src
  ```
- **Web:**
  ```bash
  cd apps/web
  pnpm dev
  ```
*(The frontend can be primarily accessed at `http://localhost:3000`)*
