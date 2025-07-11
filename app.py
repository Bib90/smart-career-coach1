import streamlit as st
import openai
import os
import re
import pandas as pd
from datetime import datetime
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Ensure feedback.csv exists ---
if not os.path.exists("feedback.csv"):
    with open("feedback.csv", "w") as f:
         f.write(f"{datetime.now()},Suggestion {idx},👍,{parts['confidence']}\n")

# --- Set up the app ---
st.set_page_config(page_title="Smart Career Coach", page_icon="📄")

tab1, tab2 = st.tabs(["📝 Resume Tailor", "📊 Feedback Log"])

# -----------------------------------
# 🚀 TAB 1: Resume Tailor Feature
# -----------------------------------
with tab1:
    st.title("📄 Smart Career Coach – Resume Tailor")

    resume = st.text_area("✍️ Paste your resume here:", height=300)
    job_description = st.text_area("📌 Paste the job description here:", height=300)

    if st.button("🚀 Tailor My Resume"):
        if not resume or not job_description:
            st.warning("Please fill out both fields.")
        else:
            with st.spinner("Analyzing resume..."):
                prompt = f"""
You are an AI resume expert. Compare the resume with the job description.

Return 3–5 suggestions using this format:
Original: [original text]  
Edit: [suggested edit]  
Confidence: [High/Medium/Low]  
Explanation: [short explanation]

Resume:
{resume}

Job Description:
{job_description}
"""

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )

                    raw_reply = response['choices'][0]['message']['content']
                    suggestions_raw = re.split(r"\n?Original:\s*", raw_reply)[1:]

                    st.success("Suggestions ready!")
                    st.markdown("### ✏️ Tailored Suggestions:")

                    for idx, suggestion_text in enumerate(suggestions_raw, 1):
                        parts = {
                            "original": "",
                            "edit": "",
                            "confidence": "",
                            "explanation": ""
                        }

                        lines = suggestion_text.strip().split("\n")
                        for line in lines:
                            if line.startswith("Edit:"):
                                parts["edit"] = line.replace("Edit:", "").strip()
                            elif line.startswith("Confidence:"):
                                parts["confidence"] = line.replace("Confidence:", "").strip()
                            elif line.startswith("Explanation:"):
                                parts["explanation"] = line.replace("Explanation:", "").strip()
                            else:
                                parts["original"] += line.strip() + " "

                        with st.expander(f"🔍 Suggestion {idx} – Confidence: {parts['confidence']}"):
                            st.markdown(f"""
                            **Original Text**  
                            `{parts['original']}`

                            **Suggested Edit**  
                            `{parts['edit']}`

                            **Explanation**  
                            {parts['explanation']}
                            """)

                            # 👍 👎 Feedback buttons
                            feedback_key = f"feedback_{idx}"
                            col1, col2 = st.columns(2)

                            with col1:
                                if st.button("👍 Helpful", key=f"{feedback_key}_up"):
                                    st.success("Thanks for the feedback!")
                                    with open("feedback.csv", "a") as f:
                                        f.write(f"{datetime.now()},Suggestion {idx},👍,{parts['confidence']}\n")

                            with col2:
                                if st.button("👎 Not Helpful", key=f"{feedback_key}_down"):
                                    st.info("Got it — we’ll improve this.")
                                    with open("feedback.csv", "a") as f:
                                        f.write(f"{datetime.now()},Suggestion {idx},👎,{parts['confidence']}\n")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# -----------------------------------
# 📊 TAB 2: Feedback Log Viewer
# -----------------------------------
with tab2:
    st.subheader("📊 Feedback Collected So Far")

    try:
        df_feedback = pd.read_csv("feedback.csv")
        if df_feedback.empty:
            st.info("No feedback collected yet.")
        else:
            st.dataframe(df_feedback)
    except Exception as e:
        st.warning(f"Could not load feedback: {e}")
