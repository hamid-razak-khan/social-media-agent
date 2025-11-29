# Social Media Content Generator Agent

An AI-powered social media content generator built with **Python**, **Streamlit**, **LangChain**, and **Groq**.

Generate high-quality:
- Captions
- Post ideas
- Hashtags
- Reels ideas
- Weekly content plans

for platforms like Instagram, LinkedIn, Twitter, and YouTube.

---

## Features

- **Modern Streamlit UI** with sidebar controls
- **Business-aware & audience-aware** content
- **Tone selector** (professional, casual, inspirational, humorous)
- **Platform selector** (Instagram, LinkedIn, Twitter, YouTube)
- **Content type selector** (caption, post ideas, hashtags, reels ideas, weekly plan)
- Backend powered by **LangChain PromptTemplate** + **OpenAI GPT model**
- **Structured Markdown output** optimized per content type
- **Download result as .txt** with helpful metadata

---

## Project structure

```text
.
├── app.py
├── prompts
│   └── content_prompt.txt
├── utils
│   └── formatter.py
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.9+ recommended
- A Groq API key

> **Important:** Never commit or share your real API key publicly.

---

## Setup

1. **Clone or open this project folder** in your IDE.

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   # source .venv/bin/activate  # on macOS / Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Groq API key and model** in a `.env` file in the project root:

   ```bash
   # .env
   GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
   # Optional: override model name (defaults to openai/gpt-oss-20b)
   # GROQ_MODEL_NAME="openai/gpt-oss-20b"
   ```

   The app uses `python-dotenv` to load environment variables. The key is never hardcoded in the code.

---

## Running the app

From the project root directory, run:

```bash
streamlit run app.py
```

This will open the Streamlit app in your browser (or provide a local URL in the terminal).

---

## How it works

- `app.py` defines the **Streamlit UI** and the `generate_content()` function.
- `prompts/content_prompt.txt` contains the reusable **LangChain PromptTemplate** text.
- `utils/formatter.py` contains small helper functions for **filenames** and **download text formatting**.
- `generate_content()` wires together:
  - the PromptTemplate (loaded from `content_prompt.txt`),
  - the `ChatGroq` model (via `langchain-groq`),
  - and a `StrOutputParser` to return plain Markdown text.

---

## Customization tips

- Tweak the prompt logic in `prompts/content_prompt.txt` to change how captions, hashtags, or weekly plans are structured.
- Adjust the model by setting `GROQ_MODEL_NAME` in `.env` (e.g., `openai/gpt-oss-20b` or another Groq-supported model), depending on your access.
- Modify the UI or add new content types in `app.py`.

---

## Security notes

- Keep your `.env` file out of version control (e.g., add it to `.gitignore`).
- Do **not** paste or commit real API keys into the code or README.
