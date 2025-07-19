# human_reviewer_app.py

import streamlit as st
import json
import os

# File paths
AI_WRITTEN_FILE = "rewritten_output/output_ai_written.json"
REVIEWED_OUTPUT_FILE = "reviewed_output/final_reviewed_chapter.json"
HUMAN_APPROVED_FILE = "human_reviewed/human_approved_output.json"

# Load AI-written content
def load_ai_output():
    with open(AI_WRITTEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Save reviewed content
def save_reviewed_content(data):
    os.makedirs("reviewed_output", exist_ok=True)
    os.makedirs("human_reviewed", exist_ok=True)
    
    with open(REVIEWED_OUTPUT_FILE, "w", encoding="utf-8") as f1, \
         open(HUMAN_APPROVED_FILE, "w", encoding="utf-8") as f2:
        json.dump(data, f1, indent=4, ensure_ascii=False)
        json.dump(data, f2, indent=4, ensure_ascii=False)

# Streamlit interface
def main():
    st.set_page_config(page_title="Human Reviewer", layout="wide")
    st.title("📖 Human-in-the-loop Review Interface")

    data = load_ai_output()
    st.subheader("Chapter Title")
    title = st.text_input("Edit Chapter Title:", data.get("title", ""))

    updated_paragraphs = []
    st.subheader("📝 Review and Edit Each Paragraph")

    for idx, para in enumerate(data.get("paragraphs", [])):
        updated_para = st.text_area(f"Paragraph {idx+1}", para, height=200)
        updated_paragraphs.append(updated_para)

    if st.button("💾 Save Reviewed Content"):
        final_data = {
            "title": title,
            "paragraphs": updated_paragraphs
        }
        save_reviewed_content(final_data)
        st.success("✅ Final reviewed content saved successfully!")

if __name__ == "__main__":
    main()
