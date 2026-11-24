# 🤖 AI Personal Assistant

An AI-powered Personal Assistant built using **Python, Flask, Groq API, and PostgreSQL**. It helps users get intelligent AI responses and summarize emails using Generative AI.

## 🚀 Features

- **AI Chat Assistant:** Ask questions and get intelligent AI-generated responses.
- **Email Summarization:** Convert long emails into short and meaningful summaries.
- **Groq API Integration:** Generate fast AI responses using Groq's LLM API.
- **PostgreSQL Database:** Store user questions, AI answers, emails, and summaries.
- **AI History Management:** Save conversations for future reference.
- **Web Interface:** Simple and user-friendly interface.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Flask | Web Framework |
| Groq API | AI Response Generation |
| PostgreSQL | Database |
| SQLAlchemy | Database Management |
| HTML | Frontend Structure |
| CSS | Frontend Styling |
| JavaScript | Frontend Functionality |

## 📂 Project Structure

```text
AI-Personal-Assistant/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

## ⚙️ Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/mdaasifansari573-boop/AI-Personal-Assistant.git
```

### 2. Open Project Folder

```bash
cd AI-Personal-Assistant
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your credentials:

```env
GROQ_API_KEY=your_groq_api_key

DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_assistant
```

**Note:** Never share or upload your actual `.env` file or API keys to GitHub.

### 6. Setup PostgreSQL

- Install PostgreSQL.
- Create a database named `ai_assistant`.
- Configure your database credentials in `.env`.

The application automatically creates the required tables when started.

### 7. Run Application

```bash
python main.py
```

Open your browser:

http://127.0.0.1:5000/

## 🔗 Application Routes

| Route | Function |
|---|---|
| `/` | Home Page |
| `/ask` | AI Assistant |
| `/summarize` | Email Summarization |
| `/db-test` | PostgreSQL Connection Test |

## 🔐 Security

- API keys are stored in environment variables.
- Database credentials are not committed to GitHub.
- `.env` is excluded using `.gitignore`.

## 👨‍💻 Developer

**MD Aasif Ansari**

B.Tech – Computer Science & Engineering (AI & ML)

Brainware University, Kolkata

## ⭐ Support

If you find this project useful, give this repository a star!
