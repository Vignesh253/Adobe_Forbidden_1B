import os
import json
import time
from PyPDF2 import PdfReader

INPUT_FOLDER = "/app/input"
OUTPUT_FOLDER = "/app/output"

# Find JSON input (challenge1b_input.json)
json_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".json")]
if not json_files:
    raise FileNotFoundError("No input JSON found in /app/input")
input_json_path = os.path.join(INPUT_FOLDER, json_files[0])

with open(input_json_path, "r", encoding="utf-8") as f:
    input_data = json.load(f)

input_filenames = [doc.get("filename") for doc in input_data.get("documents", [])]
pdf_paths = [os.path.join(INPUT_FOLDER, fname) for fname in input_filenames if os.path.exists(os.path.join(INPUT_FOLDER, fname))]

if not pdf_paths:
    raise FileNotFoundError(f"No matching PDFs found in {INPUT_FOLDER}")

persona = input_data.get("persona", {}).get("role", "").strip()
job = input_data.get("job_to_be_done", {}).get("task", "").strip()

def extract_sections(pdf_path):
    reader = PdfReader(pdf_path)
    sections = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 10]
        title = lines[0][:120] if lines else f"Page {idx+1}"
        sections.append({
            "page": idx + 1,
            "title": title,
            "content": text
        })
    return sections

def rank_sections(sections, persona, job, topn=5):
    keywords = set((persona + " " + job).lower().split())
    scored = []
    for sec in sections:
        tokens = set(sec['content'].lower().split())
        overlap = len(keywords & tokens)
        scored.append((overlap, sec))
    ranked = sorted(scored, key=lambda x: (-x[0], x[1]['page']))
    results = []
    for rank, (_, sec) in enumerate(ranked[:topn], 1):
        results.append({
            "document": "",
            "section_title": sec['title'],
            "importance_rank": rank,
            "page_number": sec['page']
        })
    return results

def analyze_subsections(sections, persona, job, topn=5):
    keywords = set((persona + " " + job).lower().split())
    results = []
    for sec in sections[:topn]:
        paras = [p for p in sec['content'].split('\n\n') if len(p.strip()) > 10]
        best_para = ""
        best_score = 0
        for p in paras:
            score = len(keywords & set(p.lower().split()))
            if score > best_score:
                best_para = p
                best_score = score
        summary = best_para or (paras[0] if paras else "")
        results.append({
            "document": "",
            "refined_text": summary[:700],
            "page_number": sec['page']
        })
    return results

output_data = {
    "metadata": {
        "input_documents": input_filenames,
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    },
    "extracted_sections": [],
    "subsection_analysis": []
}

for pdf_path, fname in zip(pdf_paths, input_filenames):
    sections = extract_sections(pdf_path)
    ranked = rank_sections(sections, persona, job)
    for sec in ranked:
        sec["document"] = fname
    analyzed = analyze_subsections(sections, persona, job)
    for sub in analyzed:
        sub["document"] = fname
    output_data["extracted_sections"].extend(ranked)
    output_data["subsection_analysis"].extend(analyzed)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
output_path = os.path.join(OUTPUT_FOLDER, "output.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Done! Output saved to {output_path}")
