# 📝 TOS Compliance Checker

A modern web-based tool for comparing two Terms of Service (TOS) documents (PDFs) and checking if one complies with the other—prioritizing the bank's TOS. Built with OpenAI's LLM and Gradio, this app provides clause-by-clause analysis, compliance reporting, and an interactive UI for legal and business teams.

---

## 🚀 Features
- **Upload and compare two TOS PDF documents** (e.g., bank and partner)
- **Automatic text extraction and chunking** (by clause or by size)
- **LLM-powered clause comparison** for compliance, using OpenAI API
- **Clear compliance report** (JSON and CSV download)
- **Interactive Gradio web interface**
- **Ask follow-up questions** about the results (LLM chat)
- **Collapsible JSON viewer** for easy inspection
- **Customizable chunking and output**

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your-key-here
     LLM_MODEL=gpt-4o
     ```
   - Or export your key as an environment variable:
     ```bash
     export OPENAI_API_KEY=your-key-here
     export LLM_MODEL=gpt-4o
     ```
4. **Run the app**
   ```bash
   python -m src.app
   ```
   - The app will launch at http://127.0.0.1:7860

---

## 💡 Usage
- Open the Gradio web interface in your browser.
- Upload the two TOS PDF files (bank and partner).
- Choose how to split the documents (by clause or by size).
- Click "Analyze Compliance" to generate the report.
- Download the JSON or CSV report, or inspect results in the UI.
- Use the chat to ask follow-up questions about the analysis.

---

**Made with ❤️ for legal, compliance, and business teams.** 