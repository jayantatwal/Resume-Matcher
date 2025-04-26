import re
import pdfplumber
import docx
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_contact_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\-\(\) ]{8,}\d', text)
    return email[0] if email else None, phone[0] if phone else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text, skill_set):
    found = set()
    text_lower = text.lower()
    for skill in skill_set:
        if skill.lower() in text_lower:
            found.add(skill)
    return list(found)
