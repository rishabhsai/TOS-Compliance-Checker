import gradio as gr
from src.document_loader import extract_text_from_pdf, chunk_text
from src.llm_analyzer import compare_clauses
import json
import csv
import tempfile

def analyze_tos(bank_pdf, partner_pdf, chunk_mode):
    bank_path = bank_pdf.name
    partner_path = partner_pdf.name
    bank_text = extract_text_from_pdf(bank_path)
    partner_text = extract_text_from_pdf(partner_path)
    bank_clauses = chunk_text(bank_text, mode=chunk_mode)
    partner_clauses = chunk_text(partner_text, mode=chunk_mode)
    results = compare_clauses(bank_clauses, partner_clauses)
    table = [[r["bank_clause"], r["partner_clause"], r["compliance"], r["explanation"]] for r in results]
    json_str = json.dumps(results, indent=2)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as f_json:
        f_json.write(json_str)
        json_path = f_json.name
    csv_headers = ["bank_clause", "partner_clause", "compliance", "explanation"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline='') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=csv_headers)
        writer.writeheader()
        for r in results:
            writer.writerow({h: r.get(h, "") for h in csv_headers})
        csv_path = f_csv.name
    return table, json_str, json_path, csv_path, results

def chat_with_llm(history, message, results):
    # Use the LLM to answer questions about the results, streaming output
    import openai
    from src.llm_analyzer import LLM_MODEL
    context = json.dumps(results, indent=2)
    prompt = f"Here is the compliance analysis result in JSON:\n{context}\n\nUser question: {message}\nAnswer in plain English."
    messages = [
        {"role": "system", "content": "You are a helpful assistant who answers questions about TOS compliance analysis results."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=256,
        temperature=0,
        stream=True
    )
    answer = ""
    for chunk in response:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            answer += delta.content
            yield history + [[message, answer]], ""
    # Final yield to ensure chat input is cleared
    yield history + [[message, answer]], ""

chunking_options = [
    ("By Clause (Best for TOS, splits by numbered points)", "clause", "Splits the document at each numbered clause or section. Best for structured legal documents."),
    ("By Size (Best for unstructured/large docs)", "size", "Splits the document into chunks of a fixed size, regardless of content structure.")
]

with gr.Blocks() as demo:
    gr.Markdown("# TOS Compliance Checker\nUpload two TOS PDFs to check compliance. Choose how to split the documents. Download the results as JSON or CSV. Ask follow-up questions in the chat!")
    with gr.Row():
        bank_pdf = gr.File(label="Bank TOS PDF", file_types=[".pdf"])
        partner_pdf = gr.File(label="Partner TOS PDF", file_types=[".pdf"])
    with gr.Row():
        chunk_mode = gr.Radio(
            [o[0] for o in chunking_options],
            value=chunking_options[0][0],
            label="How to Split Document?",
            info="Choose how to break up the documents for analysis."
        )
    analyze_btn = gr.Button("Analyze Compliance")
    output_table = gr.Dataframe(headers=["Bank Clause", "Partner Clause", "Compliance", "LLM Explanation"], label="Results")
    with gr.Accordion("JSON Report (click to expand and download)", open=False):
        json_view = gr.Code(label="JSON Report", language="json")
        download_json_btn = gr.DownloadButton(label="Download JSON")
        download_csv_btn = gr.DownloadButton(label="Download CSV")
    chatbot = gr.Chatbot(label="Ask about the results (LLM Q&A)")
    chat_input = gr.Textbox(label="Ask a question about the results", placeholder="e.g. Which clauses are non-compliant?")
    state = gr.State()
    # Logic
    def run_analysis(bank_pdf_file, partner_pdf_file, chunk_mode_label):
        for label, value, _ in chunking_options:
            if chunk_mode_label == label:
                chunk_mode = value
                break
        table, json_str, json_path, csv_path, results = analyze_tos(bank_pdf_file, partner_pdf_file, chunk_mode)
        return table, json_str, json_path, csv_path, results, [], None
    analyze_btn.click(
        run_analysis,
        inputs=[bank_pdf, partner_pdf, chunk_mode],
        outputs=[output_table, json_view, download_json_btn, download_csv_btn, state, chatbot, chat_input]
    )
    chat_input.submit(
        chat_with_llm,
        inputs=[chatbot, chat_input, state],
        outputs=[chatbot, chat_input],
        queue=True
    )

demo.launch() 