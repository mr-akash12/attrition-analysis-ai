# 🧠 Employee Attrition AI Agent

## 📌 Overview

This project is an AI-powered HR analytics system that predicts employee attrition and provides clear explanations using Machine Learning and Large Language Models (LLMs).

It combines structured prediction with natural language understanding to handle both clean and messy user inputs.

---

## 🚀 Features

* 🤖 Chatbot interface for natural queries
* 📊 Employee attrition prediction using ML model
* 🧠 LLM-powered explanations for predictions
* 🔀 Intelligent routing using LangGraph
* 🧾 Structured input form for accurate predictions
* 🧠 Handles real-world messy input (LLM + regex fallback)

---

## 🧱 Tech Stack

* Python
* Streamlit (UI)
* LangGraph (workflow orchestration)
* LangChain
* Ollama (phi3 local LLM)
* Scikit-learn (ML model)
* Pandas

---

## 🏗️ Architecture

User Input → LLM Decision Node → Route

* If **prediction request** → ML Model
* If **general question** → Knowledge Node

Final Output → Prediction + Explanation

---

## 📁 Project Structure

```id="struct01"
employee-attrition-ai/
│
├── app.py
├── requirements.txt
├── rf_pipeline_model.pkl
├── .gitignore
│
└── chatbot/
    ├── graph.py
    ├── tools.py
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone Repository

```bash id="run01"
git clone https://github.com/mr-akash12/attrition-analysis-ai.git
cd attrition-analysis-ai
```

### 2️⃣ Create Virtual Environment

```bash id="run02"
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash id="run03"
pip install -r requirements.txt
```

### 4️⃣ Run Ollama (Local LLM)

```bash id="run04"
ollama run phi3
```

### 5️⃣ Run App

```bash id="run05"
streamlit run app.py
```

---

## 🧪 Example Queries

### 🔹 Knowledge

* What causes employee attrition?
* How can companies reduce turnover?

### 🔹 Prediction

* satisfaction=0.2, 250 hours, low salary
* This employee works 260 hours, satisfaction is 0.2, salary is low

---

## 🧠 Key Highlights

* Combines LLM reasoning with ML prediction
* Supports structured and unstructured inputs
* Provides explainable AI outputs
* Works locally without API cost (using Ollama)

---

## ⚠️ Deployment Note

Ollama-based models may not run on free cloud platforms.
For deployment, switch to OpenAI or similar API-based models.

---

## 🔮 Future Improvements

* Improve model accuracy
* Add analytics dashboard
* Deploy full-stack (FastAPI + React)
* Add authentication system

---

## 👤 Author

**Akash (mr-akash12)**
Data Science & GenAI Enthusiast

---
