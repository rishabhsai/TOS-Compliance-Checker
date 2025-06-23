from src.document_loader import extract_text_from_pdf, chunk_text
from src.llm_analyzer import compare_clauses

if __name__ == "__main__":
    bank_pdf = "src/samples/Term Sheet from WhatsApp.pdf"
    partner_pdf = "src/samples/docdocument.pdf"

    print(f"Extracting and chunking bank TOS: {bank_pdf}")
    bank_text = extract_text_from_pdf(bank_pdf)
    bank_clauses = chunk_text(bank_text, mode="clause")
    print(f"Found {len(bank_clauses)} bank clauses.")

    print(f"Extracting and chunking partner TOS: {partner_pdf}")
    partner_text = extract_text_from_pdf(partner_pdf)
    partner_clauses = chunk_text(partner_text, mode="clause")
    print(f"Found {len(partner_clauses)} partner clauses.")

    print("\nComparing clauses using LLM...")
    results = compare_clauses(bank_clauses, partner_clauses)

    for i, result in enumerate(results, 1):
        print(f"\nBank Clause {i}: {result['bank_clause']}")
        print(f"Partner Clause: {result['partner_clause']}")
        print(f"Compliance: {result['compliance']}")
        print(f"Explanation: {result['explanation']}") 