import os
from flask import Flask, render_template, request, session
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_contact_info,
    extract_name,
    extract_skills,
)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte key

SKILLS = ["Python", "Java", "SQL", "C++", "Data Analysis", "Communication", "Leadership"]

def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    return int((len(set(resume_skills) & set(jd_skills)) / len(jd_skills)) * 100)

@app.route("/", methods=["GET", "POST"]) #Think of this like "When the user visits this URL, run this code."
def index(): #	This is the function that runs when someone visits /.
    if request.method == "POST": #If user submits the form
        job_description = request.form["job_description"] #Get the job description text from the form.
        resume_file = request.files["resume"]# Get the uploaded resume file.

        session["job_description"] = job_description  # Save to session

        if resume_file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(resume_file)
        elif resume_file.filename.endswith(".docx"):
            text = extract_text_from_docx(resume_file)
        else:
            return "Unsupported file format", 400

        resume_skills = extract_skills(text, SKILLS)
        jd_skills = extract_skills(job_description, SKILLS)
        name = extract_name(text)
        email, phone = extract_contact_info(text)
        match_percentage = calculate_match(resume_skills, jd_skills)

        return render_template("result.html", name=name, email=email, phone=phone,
                               skills=resume_skills, match=match_percentage, job_description=job_description)

    # On GET, load job description from session if available
    job_description = session.get("job_description", "")
    return render_template("index.html", job_description=job_description)
