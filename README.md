Here's a `README.md` file for your project, explaining what it does, how to install and run it, and how it works:

---

## 🧠 Software Company AI Representative

This project is a **Streamlit-based AI assistant** that helps software development teams **qualify inbound leads** through a conversational interface. It uses **Groq's LLaMA 3 model** to classify leads based on their relevance and potential.

---

### 🚀 Features

* Collects lead details through a conversational chat interface.
* Validates email and company name input.
* Evaluates the lead using an LLM (`llama3-70b-8192`) hosted on Groq.
* Categorizes leads as:

  * `not relevant`
  * `weak lead`
  * `hot lead`
  * `big customer in mongo`
* Suggests a scheduling link for high-potential leads.

---

### 📦 Tech Stack

* Python
* [Streamlit](https://streamlit.io/)
* [Groq API](https://groq.com/)
* LLaMA 3 via `openai`-compatible client
---

### ⚙️ Setup Instructions

#### 1. Clone the repo

```bash
git https://github.com/username/Software-Company-AI-Representative.git
cd Software-Company-AI-Representative.git
```

#### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set up your API key

Create a `.env` file or modify `config.py` to include your **Groq API key**:

```python
# config.py
GROQ_API_KEY = "your-groq-api-key-here"
```

Alternatively, you can set the environment variable:

```bash
export GROQ_API_KEY=your-groq-api-key-here
```

#### 5. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

---

### 📬 API Alternative (Optional)

The app also includes commented code to make a POST request to a local FastAPI server (endpoint: `http://localhost:8000/conversations/lead`). You can enable that by replacing the local function call with the HTTP request code.

---

### 🧪 Example Lead Flow

1. User enters their **email**.
2. Then they provide their **company name**.
3. Finally, they describe their **project needs**.
4. The assistant evaluates and replies with:

   * Lead relevance category
   * A calendar scheduling link if it’s a strong lead

---
