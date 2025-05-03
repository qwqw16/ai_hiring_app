import streamlit as st
import openai
import os
import re
from langdetect import detect
from utils import extract_text_from_pdf, compute_offer

# 设置 API 密钥（新版 SDK 直接使用 openai.api_key）
openai.api_key = os.getenv("OPENAI_API_KEY")

# 页面设置
st.set_page_config(page_title="AI Hiring Assistant", layout="centered")
st.title("🤖 AI Hiring Assistant")
st.markdown("**Position:** Data Analyst  **Salary Range:** Up to $90,000")

# 上传简历
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file, max_chars=500)
    st.success("✅ Resume extracted successfully!")

    with st.expander("📄 Resume Preview (first 500 characters)"):
        st.write(resume_text)

    lang = detect(resume_text)
    lang_label = "Chinese" if lang.startswith("zh") else "English"

    job_desc = "We are hiring a Data Analyst with skills in data analysis, Python, and SQL."

    st.markdown("### 🔍 Resume Match Score")
    with st.spinner("AI is evaluating..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional recruiter."},
                {"role": "user", "content": f"""
Please evaluate the following resume written in **{lang_label}**, based on the English job description.

Respond in English.
Start with the score in format: Score:7 (not 7/10). Then briefly explain your reasoning.

Job Description (English):  
{job_desc}

Resume Content (in {lang_label}):  
{resume_text}
"""}
            ]
        )
        score_text = response.choices[0].message.content.strip()
        st.write(score_text)

    match = re.search(r'\b(10|[1-9])\b', score_text[:30])
    match_score = int(match.group(1)) if match else st.slider("❓ Score not detected. Select manually:", 1, 10)

    if match_score < 6:
        st.error("❌ Unfortunately, your resume did not meet our requirements.")
        st.stop()
    else:
        st.success("🎉 Resume passed! Proceeding to the interview...")

        response_q = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a recruiter."},
                {"role": "user", "content": f"Please generate 2 interview questions in English based on this resume (written in {lang_label}):\n\n{resume_text}"}
            ]
        )
        questions = response_q.choices[0].message.content
        st.markdown("### 📋 Interview Questions")
        st.write(questions)

        answer = st.text_area("🗣️ Please answer the above interview questions:", height=200)

        if st.button("Submit Answer") and "eval_done" not in st.session_state:
            with st.spinner("AI is scoring your response..."):
                eval_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an interview evaluator."},
                        {"role": "user", "content": f"""
Evaluate the following candidate answer. Respond in English.

Start your response with: Score:X (e.g., Score:8). Then briefly explain your evaluation.

Candidate's Answer:
{answer}
"""}
                    ]
                )
                eval_text = eval_response.choices[0].message.content.strip()
                st.session_state["eval_text"] = eval_text

                eval_match = re.search(r'\b(10|[1-9])\b', eval_text[:30])
                st.session_state["interview_score"] = int(eval_match.group(1)) if eval_match else None
                st.session_state["eval_done"] = True

        if st.session_state.get("eval_done"):
            st.markdown("### 🧠 Interview Evaluation")
            st.write(st.session_state["eval_text"])

            interview_score = st.session_state.get("interview_score")
            if interview_score is None:
                interview_score = st.slider("❓ Score not detected. Select manually:", 1, 10)

            if interview_score < 6:
                st.error("❌ Unfortunately, your interview performance did not meet the hiring criteria.")
            else:
                expected = st.number_input("💵 Please enter your expected salary (USD):", min_value=0)

                if expected:
                    offer = compute_offer(90000, interview_score)

                    if expected <= offer:
                        st.success(f"🎉 Congratulations! You are hired. Final salary: ${expected}")
                        st.balloons()
                    else:
                        st.error("❌ Sorry, your expected salary exceeds our offer limit.")
                        st.markdown(f"💡 Based on your score, we can offer up to **${offer}**.")

                        st.markdown("### 🎁 Additional Benefits Included in the Offer:")
                        if interview_score >= 8:
                            benefits = [
                                "🏡 Hybrid Remote Work",
                                "🌴 15 Days Annual Leave",
                                "💰 $2,000 Signing Bonus",
                                "🎓 $1,000 Training Budget"
                            ]
                            hr_pitch = "We believe you are a great match and would love to welcome you with an enhanced benefits package."
                        else:
                            benefits = [
                                "🏡 Flexible Work Hours",
                                "🌴 10 Days Annual Leave"
                            ]
                            hr_pitch = "We see potential and are happy to offer a standard benefits package tailored to your needs."

                        st.info(hr_pitch)
                        for b in benefits:
                            st.markdown(f"- {b}")

                        st.markdown("### 🤝 Would you be willing to accept this offer?")
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("✅ Accept Offer"):
                                st.success(f"🎉 Welcome aboard! Your final salary is **${offer}**.")
                                st.balloons()

                        with col2:
                            if st.button("❌ Decline Offer"):
                                st.warning("💔 We're sorry we couldn't work together. Best wishes!")
                                st.snow()
