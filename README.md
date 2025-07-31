
# 📄 Document-Based Information Retrieval API

A scalable and modular RESTful API built with **FastAPI** for performing intelligent search over `.pdf` and `.docx` documents. It extracts, indexes, and retrieves list of most relevant documents using BM25 algorithm.

<br>

## 🚀 Features

- 🔍 Information retrival using BM25 ranking algorithm.  
- 🧠 NLP preprocessing pipeline for enhanced matching.  
- 🗃️ Document indexing for efficient retrieval.  
- 📁 Support for `.pdf` and `.docx` files.  
- ⚡ FastAPI backend with clean, modular architecture.
- 📥 Download of documents supported.

<br>

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Document_Search_Api.git
cd Document_Search_Api
```

### 2. Create a virtual environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate (On Mac)
    or
cd venv\Scripts\activate (on Windows)
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app:app --reload
```

<br>

## 📥 API Endpoints

| Method              | Endpoint | Description |
| :----------------: | :------: | :----: |
| Get        |   /search   | Returns list of relevant documents |
| Get           |   /download/{filename}  | Returns file mentioned as path variable |

<br>

## 🧠 How it works 
<img width="1653" height="608" alt="flowchart" src="https://github.com/user-attachments/assets/dffbf197-2e5d-4af9-9f60-2549ad614833" />


<br><br>

## 📌 Technologies Used

- FastAPI - for building the RESTful API.
- PyMuPDF / python-docx - for extracting text from documents.
-  spaCy - for NLP preprocessing.

<br>

## 📄 License

This project is open-source and available under the MIT License.

<br>

## 📬 Contact

Feel free to contact on [linkedin](https://www.linkedin.com/in/zaid-khatri-dev/) or email at zaidkhatri.work@gmail.com 
