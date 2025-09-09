from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Load .env file
load_dotenv()
# -------------------------------
# Gemini API Setup
# -------------------------------
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)  # Apni Gemini API key lagao


def ask_gemini(query):
    """Send query to Gemini with modern, clear, engaging formatting and line/length limits."""
    prompt = f"""
    You are an education assistant for Pakistani students.
    Answer questions about study, career, exams, degrees, fields, or courses after FSc, ICS, Matric, or any education level.
    Format your answer in a modern, visually clear way:
    - Use bullet points, numbered lists, or short sections (not just a paragraph)
    - Add emojis for friendliness and clarity
    - Use bold or headings for key points if possible
    - Sentences can be longer for clarity, but keep the answer easy to read
    - Limit your answer to a maximum of 10–12 lines. If the answer is long, summarize the most important points.
    - Use line breaks for clarity and avoid messy formatting.
    If the question is completely off-topic (not about education, career, or study), reply: '❌ Please ask study-related questions only.'
    Question: {query}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


# -------------------------------
# Abbreviation Normalization
# -------------------------------
ABBREV_MAP = {
    "cs": "computer science",
    "bscs": "bachelor of science in computer science",
    "bsse": "bachelor of software engineering",
    "bsit": "bachelor of science in information technology",
    "ics": "intermediate computer science",
    "fsc": "intermediate pre-engineering",
    "preeng": "pre-engineering",
    "mdcat": "medical entrance test (MDCAT)",
    "ecat": "engineering entrance test (ECAT)",
    "nts": "national testing service",
    "css": "central superior services",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "ds": "data science",
    "js": "javascript",
    "py": "python",
    "webdev": "web development",
}


def normalize_abbreviations(text):
    """Expand common abbreviations (cs → computer science, etc.)."""
    words = text.lower().split()
    return " ".join([ABBREV_MAP.get(w, w) for w in words])


# -------------------------------
# Study Keywords (Allowlist)
# -------------------------------
STUDY_KEYWORDS = [
    "scope",
    "syllabus",
    "exam",
    "admission",
    "career",
    "jobs",
    "skills",
    "salary",
    "subjects",
    "degree",
    "degrees",
    "university",
    "uni",
    "college",
    "scholarship",
    "mdcat",
    "ecat",
    "nts",
    "css",
    "sat",
    "gre",
    "gmat",
    "ielts",
    "toefl",
    "computer science",
    "artificial intelligence",
    "machine learning",
    "data science",
    "python",
    "javascript",
    "django",
    "react",
    "node",
    "web development",
    "field",
    "fields",
    "ics",
    "fsc",
    "future",
    "after",
    "program",
    "programs",
    "course",
    "courses",
    "matric",
    "pre engineering",
    "pre medical",
    "schedule",
    "timetable",
]


def is_study_related(text):
    """Check if message contains study-related terms."""
    return any(kw in text for kw in STUDY_KEYWORDS)


# -------------------------------
# Rule-Based Responses
# -------------------------------


def process_message(message):
    message = normalize_abbreviations(message)
    msg = message.lower().strip()

    # --- Institute feedback/rating ---
    institute_keywords = ["jawad institute", "this portal", "this institute"]
    for kw in institute_keywords:
        if kw in msg:
            return "Jawad Institute is one of the best educational institutes in the market, known for its quality guidance, expert faculty, and student success. We are proud to help you achieve your goals!"

    # --- User positive feedback ---
    positive_feedback = [
        "great",
        "fine",
        "awesome",
        "amazing",
        "very good",
        "excellent",
        "outstanding",
        "superb",
        "best",
        "helpful",
        "useful",
        "nice",
        "good",
    ]
    # Only trigger if message is short (<=4 words) or matches exactly
    words = msg.split()
    if len(words) <= 4:
        for pf in positive_feedback:
            if msg == pf or msg == f"very {pf}" or msg == f"so {pf}":
                return "Thank you for your kind words! 😊 If you have any more questions about Jawad Institute or your career, feel free to ask."

    # --- Greetings ---
    greetings = [
        "hi",
        "hello",
        "hey",
        "salam",
        "asslam o alaikum",
        "good morning",
        "good evening",
        "hy",
    ]
    for g in greetings:
        if msg == g or msg.startswith(g + " "):
            return "Hello! 👋 How can I help you with your studies or career?"

    # --- Farewells ---
    farewells = [
        "bye",
        "goodbye",
        "see you",
        "thanks",
        "thank you",
        "shukriya",
        "khuda hafiz",
    ]
    for f in farewells:
        if f in msg:
            return "Goodbye! 😊 If you have more questions, just ask."

    # --- Common confirmations ---
    if any(word in msg for word in ["ok", "okay", "fine", "thik hai", "acha", "hmm"]):
        return "👍 Noted! Let me know if you have any study or career questions."

    # --- University/college specific queries ---
    if "uni" in msg or "university" in msg or "college" in msg:
        try:
            return ask_gemini(message)
        except Exception:
            return "⚠️ I couldn’t fetch extra details right now. Please try again."

    # --- Study encouragement ---
    # Only trigger for short/generic study messages
    study_words = ["study", "parhai", "parhna", "exam", "test", "revision"]
    if any(word in msg for word in study_words) and len(msg.split()) <= 4:
        return "Stay focused and keep a regular study schedule. Consistency is key to success!"

    # --- Career guidance ---
    if "career" in msg:
        return "There are many career options: CS, AI, Medicine, Engineering, etc. Which one are you interested in?"

    if "exam" in msg or "test" in msg:
        return "Exams like MDCAT, ECAT, CSS, and NTS are common in Pakistan. Which exam are you asking about?"

    if "appointment" in msg:
        return "You can book an appointment with a teacher through the portal."

    if "profile" in msg:
        return "You can update your profile in the student dashboard."

    if "skills" in msg:
        return "CS students should focus on coding, problem-solving, data structures, and algorithms."

    if "recommend" in msg:
        return "Based on your interest, I recommend exploring AI, Data Science, and Web Development."

    # --- Forward to Gemini if study-related ---
    if is_study_related(msg):
        try:
            return ask_gemini(message)
        except Exception:
            return "⚠️ I couldn’t fetch extra details right now. Please try again."

    # --- Default fallback ---
    return "❌ Please ask study or career-related questions only."


# -------------------------------
# API Routes
# -------------------------------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "⚠️ Please send a valid message."})

    return jsonify({"reply": process_message(user_message)})


@app.route("/api/careers", methods=["GET"])
def get_careers():
    return jsonify(
        [
            "Computer Science",
            "Artificial Intelligence",
            "Software Engineering",
            "Medicine",
            "Civil Engineering",
        ]
    )


@app.route("/api/exams/<stream>", methods=["GET"])
def get_exams(stream):
    exams = {"cs": ["NTS", "GAT", "GRE"], "medical": ["MDCAT"], "engineering": ["ECAT"]}
    return jsonify(exams.get(stream.lower(), ["No exams found for this stream."]))


@app.route("/api/appointment", methods=["POST"])
def appointment():
    return jsonify({"message": "✅ Appointment booked successfully!"})


@app.route("/api/user/profile", methods=["POST"])
def update_profile():
    return jsonify({"message": "✅ Profile updated successfully!"})


@app.route("/api/recommendations/<user_id>", methods=["GET"])
def recommendations(user_id):
    return jsonify(
        {
            "user_id": user_id,
            "recommendations": ["AI", "Data Science", "Web Development"],
        }
    )


@app.route("/api/feedback", methods=["POST"])
def feedback():
    return jsonify({"message": "✅ Feedback submitted. Thank you!"})


@app.route("/api/conversation/<user_id>", methods=["GET"])
def conversation(user_id):
    return jsonify(
        {"user_id": user_id, "history": ["Hi", "Hello! How can I help you?"]}
    )


@app.route("/api/skills/<stream>", methods=["GET"])
def skills(stream):
    skills_map = {
        "cs": ["Programming", "Problem Solving", "Data Structures"],
        "ai": ["Python", "Machine Learning", "Math"],
        "medical": ["Biology", "Chemistry", "Critical Thinking"],
    }
    return jsonify(skills_map.get(stream.lower(), ["No skills found for this stream."]))


@app.route("/api/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "")
    return jsonify({"results": [f"Result for {query} 1", f"Result for {query} 2"]})


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
