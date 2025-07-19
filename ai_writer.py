# ai_writer.py

import json
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

def load_chapter(input_path="scraped_data/chapter_1.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["title"], data["content"]

def rewrite_text(text, tokenizer, model, device, max_length=512):
    input_text = f"summarize: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=max_length, truncation=True).to(device)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def chunk_text(text, max_tokens=300):
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len((current + para).split()) <= max_tokens:
            current += para + "\n\n"
        else:
            chunks.append(current.strip())
            current = para + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

def main():
    # Load the model and tokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)

    title, content = load_chapter()

    print("🔄 Splitting content into chunks...")
    chunks = chunk_text(content)
    rewritten_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"✍️ Rewriting chunk {i+1}/{len(chunks)}...")
        rewritten = rewrite_text(chunk, tokenizer, model, device)
        rewritten_chunks.append(rewritten)

    rewritten_text = "\n\n".join(rewritten_chunks)

    os.makedirs("rewritten_output", exist_ok=True)
    with open("rewritten_output/output_ai_written.json", "w", encoding="utf-8") as f:
        json.dump({
            "title": title,
            "rewritten_content": rewritten_text
        }, f, indent=4)

    print("✅ Rewritten content saved to rewritten_output/output_ai_written.json")

if __name__ == "__main__":
    main()
