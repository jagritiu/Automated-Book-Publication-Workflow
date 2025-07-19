# Automated-Book-Publication-Workflow# Soft-Nerve: AI-Powered Book Publishing Workflow

This repo implements Phase 1 of the Soft-Nerve Book Publishing pipeline.

## ✅ Features

- Scrape book content from URLs (`scraper.py`)
- Rewrite using Hugging Face model (`ai_writer.py`)
- Review via Streamlit UI (`human_reviewer_app.py`)
- Store + search AI & human-edited content using ChromaDB (`version_store_and_search.py`)

## 🔁 Final Outputs

- `rewritten_output/output_ai_written.json`
- `reviewed_output/final_reviewed_chapter.json`
- `human_reviewed/human_approved_output.json`

## 💡 Run

```bash
pip install -r requirements.txt
streamlit run human_reviewer_app.py
python version_store_and_search.py
