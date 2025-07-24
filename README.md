# Documentation Helper Bot

This project provides a simple yet effective documentation helper bot built with Streamlit, Langchain, and Pinecone. It allows you to ask questions about the Langchain documentation, and the bot will retrieve relevant information and provide sources.

## Features

- **Intelligent Q&A:** Get answers to your questions about Langchain by leveraging a large language model.
- **Context-Aware Responses:** The bot considers the conversation history to provide more accurate and relevant answers.
- **Source Attribution:** All generated responses include links to the original source documents, allowing you to verify information and delve deeper.
- **Streamlit UI:** An interactive and user-friendly interface powered by Streamlit for easy interaction.

## Technologies Used

- **Langchain:** For building the core LLM application, including retrieval chains and history-aware retrieval.
- **Pinecone:** As the vector database to store and retrieve Langchain documentation embeddings.
- **Google Gemini (via `ChatGoogleGenerativeAI`):** The large language model powering the conversational AI.
- **Streamlit:** For creating the interactive web application interface.
- **`python-dotenv`:** For managing environment variables securely.

---

## Setup and Installation

Follow these steps to get your Documentation Helper Bot up and running locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd documentation-helper-bot
```

### 2. Set Up Your Environment Variables

Create a `.env` file in the root directory of your project with the following content:

- **`GEMINI_API_KEY`**: Obtain this from the Google AI Studio.
- **`PINECONE_API_KEY`**: Get this from your Pinecone dashboard.
- **`PINECONE_ENVIRONMENT`**: Find this in your Pinecone dashboard under API Keys.

### 3. Install Dependencies

This project uses `pipenv` for dependency management.

```bash
pip install pipenv
pipenv install
```

### 4. Prepare Langchain Documentation

This project assumes you have a local copy of the Langchain Python API documentation.

- **Download the documentation:** You'll need to download the HTML documentation for `api.python.langchain.com/en/latest/`. You can use tools like `wget` or `httrack` to mirror the website.
- **Place the documentation:** Ensure the downloaded documentation is located in a directory named `langchain-docs/api.python.langchain.com/en/latest/` relative to your project's root. The `ingestion.py` script specifically looks for this path.

Your directory structure should look something like this:

documentation-helper-bot/
├── backend/
│ ├── core.py
├── langchain-docs/
│ └── [api.python.langchain.com/](https://api.python.langchain.com/)
│ └── en/
│ └── latest/
│ ├── index.html
│ └── ... (other doc files)
├── .env
├── main.py
├── ingestion.py
├── Pipfile
├── Pipfile.lock
└── README.md

### 5. Ingest Documentation into Pinecone

Before running the bot, you need to process the Langchain documentation and upload its embeddings to your Pinecone index.

```bash
pipenv run python ingestion.py
```

This script will:

- Load documents from langchain-docs/api.python.langchain.com/en/latest/.
- Split the documents into manageable chunks.
- Generate embeddings for each chunk using the multilingual-e5-large model.
- Upload these embeddings to a Pinecone index named "langchain-doc-index". If the index doesn't exist, Pinecone will create it.

### Running the Application

Once the documentation is ingested, you can launch the Streamlit application

```bash
pipenv run streamlit run main.py
```

### This will open the Documentation Helper Bot in your web browser.

1.  Type your question related to Langchain in the **"Prompt"** text box.
2.  Press Enter or click outside the text box.
3.  The bot will generate a response, which will be displayed below, along with the source URLs from where the information was retrieved.
4.  You can continue the conversation, and the bot will remember previous interactions.
