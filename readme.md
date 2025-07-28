Persona-Driven Document Intelligence: Round 1B Solution
This repository contains the solution for Round 1B ("Persona-Driven Document Intelligence") of Adobe's "Connecting the Dots" Hackathon.

Our system analyzes a set of related PDF documents and, based on the provided user persona and job-to-be-done, extracts and ranks the most relevant sections and sub-sections for that user's specific need. The code is fully offline, generic, and scalable for any set of eligible challenge documents, personas, or tasks. All code and documentation are included for reproducibility and review.

Approach
We designed our solution to be modular, generic, and efficient, as required by the challenge constraints. The core pipeline operates as follows:

Input Parsing: The system takes a user-supplied input JSON (e.g., challenge1b_input.json), which specifies the PDF files to process, the persona (i.e., user type), and the concrete job-to-be-done (task).

Section Extraction: Each PDF is parsed page-by-page. On each page, the first significant line is designated as a provisional "section title". (For enhanced solutions, this step can be replaced with advanced heading or outline extraction.)

Relevance Scoring: Each section is ranked by relevance to the persona and job. The ranking is initially based on keyword overlap, but the system modularly supports replacement with NLP techniques or text embeddings for higher accuracy and semantic matching.

Subsection Summarization: For each top-ranked section, we extract or summarize the most relevant paragraph or sub-section, again using keyword and context overlap with persona and job.

Output: The system assembles all results (including metadata such as input files, persona, job, timestamp; extracted sections; and subsection analyses) into a single standards-compliant output JSON.

Key principles:

No hardcoding for any specific file or persona—fully generic logic.

No network or API dependence; runs entirely on CPU.

Model size and runtime constraints are rigorously respected.

Models and Libraries Used
PyPDF2 (for extracting text from PDFs)

Python Standard Library (os, glob, time, json)

ipywidgets (for interactive file selection in Colab/Jupyter, optional)

No external LLMs or pretrained ML models are required for baseline operation; any semantic model used for improvement is kept ≤1GB.

See requirements.txt for exact package versions.

How to Build and Run
Colab or Jupyter Notebook (Recommended for Development/Testing)
Install dependencies:

text
pip install PyPDF2 ipywidgets
Upload your PDFs and input JSON to the directories /content/input/ and /content/.

Launch the notebook/cell:

You'll be prompted (via dropdown) to select your input JSON.

The system will automatically process the correct PDFs and output results.

Output will appear as /content/output/output.json.

Local/Dockerized (for hackathon evaluation)
Place your PDFs in input/ and the input JSON in the working directory.

Build Docker image:

text
docker build --platform linux/amd64 -t persona-intelligence .
Run:

text
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-intelligence
The code will read challenge1b_input.json (or equivalent) and process accordingly.

Output appears in output/output.json.

Input/Output Formats
Input JSON Example:

json
{
  "documents": [
    {"filename": "doc1.pdf", "title": "Document 1"},
    {"filename": "doc2.pdf", "title": "Document 2"}
  ],
  "persona": {"role": "Undergraduate Chemistry Student"},
  "job_to_be_done": {"task": "Identify key concepts for exam preparation"}
}
Output JSON Example:

json
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "...",
      "section_title": "...",
      "importance_rank": 1,
      "page_number": ...
    }
  ],
  "subsection_analysis": [
    {
      "document": "...",
      "refined_text": "...",
      "page_number": ...
    }
  ]
}
The output fields and structure match the challenge specification exactly.

Notes and Troubleshooting
The script will produce helpful errors if PDF or input JSON files are missing.

For Docker builds, all dependencies are automatically installed; no extra internet access is required at runtime.

For local/interactive use, all file selections are guided by the notebook (dropdown/dialogs).

Supplementary Materials
See approach_explanation.md for full methodology (required).

See requirements.txt for dependencies.

Sample input/output files are provided for testing.

Contact/Support
For questions or issues, please contact the repository maintainer using the information in this directory.
