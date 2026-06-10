# AI-powered-health-prediction-app-using-Streamlit-and-Groq-Llama-3.3-70B-for-diabetes-risk-assessment
# 🏥 MIRA Health Prediction App

**Medical Intelligence Robotic Automation** – An AI-powered web application that predicts diabetes risk using patient health data. Built with Streamlit, SQLite, and Groq's Llama 3.3 70B API.

---

## ✨ Features

- ✅ **CRUD Operations** – Create, Read, Update, Delete patient records
- 🤖 **AI Health Assessment** – Uses Groq API (Llama 3.3 70B) to analyze glucose, haemoglobin, and cholesterol levels
- 📊 **Persistent Storage** – SQLite database stores all patient data
- 🔒 **Data Validation** – Email format, future date check, positive numeric values
- 🎨 **Clean UI** – Built with Streamlit (no HTML/CSS required)
- 📤 **Exportable Data** – View all records in a sortable/filterable table

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend/UI | Python + Streamlit |
| Database | SQLite (via sqlalchemy) |
| AI/ML API | Groq (Llama 3.3 70B) |
| Data Validation | Regex, datetime |
| Deployment | Local / Streamlit Cloud (optional) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher (3.11 recommended)
- Groq API key ([Get one for free](https://console.groq.com/keys))

### Installation

1. Clone the repository
```bash
git clone https://github.com/Ananaya222/health-prediction-app.git
cd health-prediction-app
