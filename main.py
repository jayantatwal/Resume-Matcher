import os
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_contact_info,
    extract_name,
    extract_skills,
)
import pandas as pd

# Sample skill list
SKILLS = ["Python", "Java", "SQL", "C++", "Data Analysis", "Communication", "Leadership"]

def read_resume(path):
    if path.endswith('.pdf'):
        return extract_text_from_pdf(path)
    elif path.endswith('.docx'):
        return extract_text_from_docx(path)
    else:
        raise ValueError("Unsupported file format.")

def calculate_match(resume_skills, jd_skills): 
    # Calculates how many job description skills match resume skills
    if not jd_skills:
        return 0
    return int((len(set(resume_skills) & set(jd_skills)) / len(jd_skills)) * 100)

def main():
    # Reads resume and job description
    # Extracts info using helper functions from utils
    # Calculates match %
    # Prints and saves results in a CSV
    resume_path = "resume.pdf"
    jd_path = "job_description.txt"

    # Load data
    text = read_resume(resume_path)
    with open(jd_path, "r") as f:
        jd_text = f.read()

    jd_skills = extract_skills(jd_text, SKILLS)
    resume_skills = extract_skills(text, SKILLS)
    name = extract_name(text)
    email, phone = extract_contact_info(text)
    match_percentage = calculate_match(resume_skills, jd_skills)

    # Output
    data = {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills Found": ", ".join(resume_skills),
        "Match %": match_percentage
    }

    print("\n--- Resume Analysis ---")
    for k, v in data.items():
        print(f"{k}: {v}")

    # Optional: Save to CSV
    pd.DataFrame([data]).to_csv("scanned_resume_output.csv", index=False)

if __name__ == "__main__":
    main()
