
import os
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, text


# Load environment variables
load_dotenv()

app = Flask(__name__)


# -------------------------------
# PostgreSQL Configuration
# -------------------------------

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "ai_assistant")
)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------------
# Database Tables
# -------------------------------

class AIHistory(db.Model):
    __tablename__ = "ai_history"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


class EmailSummary(db.Model):
    __tablename__ = "email_summaries"

    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


# -------------------------------
# Groq API Configuration
# -------------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-20b"


# -------------------------------
# Groq AI Function
# -------------------------------

def generate_ai_response(prompt, temperature=0.7):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("Groq returned an empty response.")

    return answer.strip()


# -------------------------------
# Home Page
# -------------------------------

@app.route("/")
def hello_world():
    return render_template("index.html")


# -------------------------------
# PostgreSQL Connection Test
# -------------------------------

@app.route("/db-test")
def db_test():

    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "success",
            "message": "PostgreSQL Connected Successfully!"
        })

    except Exception as e:

        db.session.rollback()
        print("Database Error:", str(e))

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


# -------------------------------
# Personal AI Assistant
# -------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:
        question = request.form.get("question", "").strip()

        if not question:
            return jsonify({
                "response": "Please enter your question."
            }), 400

        prompt = f"""
        You are a helpful personal AI assistant.

        Instructions:
        - Answer the user's complete question.
        - Use simple and clear English.
        - Give useful explanations.
        - Do not stop your answer in the middle of a sentence.
        - Use bullet points when helpful.
        - Keep the answer relevant to the question.

        User Question:
        {question}
        """

        answer = generate_ai_response(prompt)

        # Save question and answer in PostgreSQL
        try:
            history = AIHistory(
                question=question,
                answer=answer
            )

            db.session.add(history)
            db.session.commit()

        except Exception as db_error:
            db.session.rollback()
            print("History Save Error:", str(db_error))

        return jsonify({
            "response": answer
        }), 200

    except Exception as e:

        print("Ask Error:", str(e))

        return jsonify({
            "response": "AI Assistant is temporarily unavailable. Please try again."
        }), 500


# -------------------------------
# Email Summarizer
# -------------------------------

@app.route("/summarize", methods=["POST"])
def summarize():

    try:
        email_text = request.form.get("email", "").strip()

        if not email_text:
            return jsonify({
                "response": "Please enter email text."
            }), 400

        prompt = f"""
        You are an expert email summarization assistant.

        Task:
        Summarize the following email in 2-3 complete sentences.

        Instructions:
        - Mention the main purpose of the email.
        - Include important information.
        - Use simple professional English.
        - Do not add information that is not in the email.

        Email:
        {email_text}
        """

        summary = generate_ai_response(
            prompt,
            temperature=0.3
        )

        # Save email and summary in PostgreSQL
        try:
            email_record = EmailSummary(
                email_text=email_text,
                summary=summary
            )

            db.session.add(email_record)
            db.session.commit()

        except Exception as db_error:
            db.session.rollback()
            print("Email Save Error:", str(db_error))

        return jsonify({
            "response": summary
        }), 200

    except Exception as e:

        print("Summarize Error:", str(e))

        return jsonify({
            "response": "Email summarization is temporarily unavailable. Please try again."
        }), 500


# -------------------------------
# Create Database Tables
# -------------------------------

with app.app_context():
    db.create_all()
    print("PostgreSQL Connected and Tables Created!")


# -------------------------------
# Run Flask Application
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
