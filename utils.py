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
    # Look at the first 10 lines — most resumes have name at the top
    lines = text.strip().split('\n')[:10]

    org_keywords = [
        'university', 'college', 'school', 'institute', 'academy', 'department',
        'iit', 'nit', 'technology', 'engineering', 'campus'
    ]

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        # Skip lines with email or numbers (likely contact info or address)
        if re.search(r'\d', line_clean) or '@' in line_clean:
            continue

        # Check for org-like keywords
        if any(org in line_clean.lower() for org in org_keywords):
            continue

        # Check if the line has 2 or 3 capitalized words
        words = line_clean.split()
        if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w[0].isalpha()):
            return line_clean

    # As a fallback, use spaCy NER on the first 500 characters
    snippet = text[:500]
    doc = nlp(snippet)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            candidate = ent.text.strip()
            if '@' not in candidate and not any(org in candidate.lower() for org in org_keywords):
                return candidate

    return None




def extract_skills(text, skill_set):
    found = set()
    text_lower = text.lower()
    for skill in skill_set:
        if skill.lower() in text_lower:
            found.add(skill)
    return list(found)
