import pdfplumber

def extract_text_from_pdf(uploaded_file, max_chars=500):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            if len(text) > max_chars:
                break
    return text[:max_chars]

def compute_offer(base_salary, interview_score):
    if interview_score < 6:
        return 0
    else:
        multiplier = 1 + 0.1 * (interview_score - 6)
        return round(base_salary * min(multiplier, 1.5))
