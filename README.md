# Streamlit RAG Genie

## Overview
Streamlit RAG Genie is a web application that allows users to upload PDF files, process them into a Chroma database, and ask questions based on the content of the uploaded PDFs as well as general inquiries using the Gemini model.

## Project Structure
```
streamlit-rag-genie
├── app.py               # Main entry point for the Streamlit application
├── rag_utils.py         # Utility functions for processing PDFs and retrieving answers
├── requirements.txt     # List of dependencies for the project
├── .gitignore           # Files and directories to be ignored by version control
├── README.md            # Documentation for the project
└── tests                # Directory containing unit tests
    └── test_rag_utils.py # Tests for rag_utils functions
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd streamlit-rag-genie
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**
   ```bash
   streamlit run app.py
   ```

2. **Upload PDF Files**
   - Use the upload center in the sidebar to upload one or more PDF files.

3. **Enter API Key**
   - Provide your Google API key in the designated input field.

4. **Ask Questions**
   - Use the chat interface to ask questions about the uploaded PDFs or general inquiries.

## Testing
To run the unit tests for the utility functions, navigate to the `tests` directory and run:
```bash
pytest test_rag_utils.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.