from src.document_loader import extract_text_from_pdf, chunk_text

if __name__ == "__main__":
    pdf_path = "src/samples/Term Sheet from WhatsApp.pdf"  # Updated path to sample PDF
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters from {pdf_path}.")

    print("\n--- Chunk by size (default) ---")
    chunks_size = chunk_text(text, mode="size", max_chars=2000)
    print(f"Split into {len(chunks_size)} chunks.")
    print("First chunk:\n" + "-"*40)
    print(chunks_size[0])

    print("\n--- Chunk by clause ---")
    chunks_clause = chunk_text(text, mode="clause")
    print(f"Split into {len(chunks_clause)} chunks.")
    print("First 5 clause chunks:")
    for i, chunk in enumerate(chunks_clause[:5], 1):
        print(f"\nClause {i}:\n{'-'*20}\n{chunk}") 