# Project Tasks & File Directory

## File Directory
- src/
    - app.py
    - main.py
    - document_loader.py
    - llm_analyzer.py
    - samples/
        - Term Sheet from WhatsApp.pdf
        - docdocument.pdf
- tests/
    - test_llm_analyzer.py
    - test_document_loader.py
- README.md
- requirements.txt
- tasks.md

## Tasks Checklist

- [x] Scaffold project structure
- [x] Create requirements.txt
- [x] Create README.md
- [x] Create main.py entry point
- [x] Implement PDF extraction and chunking logic (dual modes: size & clause)
- [x] Update test script for both chunking modes
- [x] Implement LLM-based clause comparison
- [x] Improve prompt engineering and enforce JSON output for compliance checking
- [x] Add plain English explanation function for compliance results
- [x] Build Gradio web interface
- [x] Output JSON report and explanations
- [x] Add ability to download JSON report
- [x] Add ability to download CSV report
- [x] Make JSON report viewer collapsible (initially collapsed)
- [x] Add LLM chat interface for plain text Q&A on results
- [x] Restructure files for clean project layout
- [x] Improve chunking mode UI: rename modes, add info tooltips for each
- [x] Truncate long text in table with ellipsis
- [x] Update accordion label to 'JSON Report (click to expand and download)'

---

## 🚩 Priority Tasks
- [ ] **Add support for DOCX/TXT files**
- [ ] **Test with larger files (performance, memory, and accuracy)**
- [ ] **Improve "By size" chunking mode for better splitting and context retention**
- [ ] **Add user authentication for web app**
- [ ] **Add database integration to store user data and chat history**
    - [ ] Choose and set up a suitable database (e.g., SQLite, PostgreSQL)
    - [ ] Design schema for users, chat sessions, and chat messages
    - [ ] Implement database models and migration scripts
    - [ ] Integrate database with authentication system
    - [ ] Store chat history and user-uploaded documents in the database
    - [ ] Add endpoints or UI to view/download past chat sessions and documents
- [ ] **Add documentation for API and usage examples**

---

## Recommended Next Tasks
- [ ] Add unit tests for core functions
- [ ] Add logging and error handling
- [ ] Add Dockerfile for easy deployment
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Add advanced analytics (e.g., clause similarity heatmap)
- [ ] Add API endpoint for programmatic access
- [ ] Add accessibility improvements to UI
- [ ] Add multi-language support
- [ ] Add usage tracking/analytics  
- [ ] Add bounding box overlay feature