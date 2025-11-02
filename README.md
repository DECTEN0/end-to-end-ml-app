<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/Container-Docker-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/Deployment-AWS%20|%20Azure-orange.svg" alt="Deployment">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License">
</p>

---
<h1 align="center">End-to-End Machine Learning Project</h1>

## 📘 Overview
This repository contains a **fully modular, production-ready Machine Learning project** built from scratch and deployed on **AWS** and **Azure** using **Docker containerization**.

The project demonstrates the complete lifecycle of an ML application from **data ingestion and transformation** to **model training**, **Flask API deployment**, and **cloud deployment** following best software engineering practices like **logging**, **custom exception handling**, and **config-driven modularization**.

## 🧱 Project Architecture
```
project-root/
│
├── artifacts/ # Stored artifacts and serialized models
│ ├── data.csv
│ ├── train.csv
│ ├── test.csv
│ └── preprocessor.pkl
│
├── data/
│ └── stud.csv # Raw dataset
│
├── notebooks/ # Jupyter notebooks for experiments
│ ├── 01.eda.ipynb
│ └── 02.modeling.ipynb
│
├── src/
│ ├── components/ # Data and model pipeline components
│ │ ├── data_ingestion.py
│ │ ├── data_transformation.py
│ │ └── model_trainer.py
│ │
│ ├── pipeline/ # End-to-end pipeline orchestration
│ │ └── training_pipeline.py
│ │
│ ├── exception.py # Custom exception handler
│ ├── logger.py # Logging configuration
│ ├── utils.py # Helper functions
│ └── init.py
│
├── app.py # Flask API for model inference
├── Dockerfile # Docker container configuration
├── setup.py # Project packaging setup
├── requirements.txt # Python dependencies
├── LICENSE
└── README.md
```

## 🧠 Features
- 🔄 **End-to-End ML Pipeline:** Data ingestion → transformation → model training → evaluation  
- 🧹 **Automated Preprocessing:** Handles missing values, encoding, and scaling  
- 🧪 **Exploratory Analysis:** Jupyter notebooks for EDA and feature engineering  
- 🪵 **Logging System:** Real-time tracking of all pipeline stages (`logger.py`)  
- ⚡ **Custom Exception Handling:** Graceful error capture and debugging via `CustomException`  
- 🧰 **Utility Functions:** Common operations abstracted into `utils.py`  
- 🌐 **Flask REST API:** Exposes prediction endpoints for integration  
- 🐳 **Docker Containerization:** Consistent, portable environment for deployment  
- ☁️ **Cloud Deployment:** Hosted on **AWS EC2** and **Azure Web App**  
- 🧩 **Configurable Setup:** Uses `setup.py` and `requirements.txt` for easy installation  

## 🧩 Key Components
| Module | Description |
|--------|-------------|
| **`data_ingestion.py`** | Loads and validates data from source, splits into train/test sets |
| **`data_transformation.py`** | Cleans data, performs feature engineering, and builds preprocessing pipeline |
| **`model_trainer.py`** | Trains, tunes, and evaluates ML models; saves best model to `artifacts/` |
| **`logger.py`** | Centralized logging utility for all pipeline steps |
| **`exception.py`** | Custom error-handling framework with detailed traceback logging |
| **`utils.py`** | Helper utilities (e.g., file handling, model saving/loading) |
| **`app.py`** | Flask application for model inference |
| **`Dockerfile`** | Defines environment for containerized deployment |

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2️⃣ Create and Activate a Virtual Environment
```
python -m venv venv
```
```
source venv/bin/activate      # macOS/Linux
````
```
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the ML Pipeline
```bash
python -m src.pipeline.training_pipeline
```

### 5️⃣ Start the Flask API
```bash
python app.py
```
Your API will be available at:

👉 http://127.0.0.1:5000/predict

### 🐳 Running with Docker
Build Docker Image
```bash
docker build -t rentify-ml-app .
```

### Run Docker Container
`docker run -p 5000:5000 rentify-ml-app`

Access the API at:
👉 http://localhost:5000/predict

## ☁️ Deployment
### AWS EC2

- Launch an EC2 instance 

- Install Docker and pull your image from Docker Hub

- Run the container and expose port 5000

### Azure Web App

- Create a Web App for Containers

- Push your Docker image to Azure Container Registry (ACR)

- Deploy the container to your Web App

## 🧾 Logging & Monitoring

- Logs are automatically generated and stored in the logs/ directory.

- Each major pipeline component logs start, end, and error states.

- Critical exceptions are captured by CustomException and written to both console and log files.

## 🧰 Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| **Language** | Python 3.10+ |
| **Data Handling** | Pandas, NumPy |
| **ML Framework** | Scikit-learn |
| **API Framework** | Flask |
| **Containerization** | Docker |
| **Deployment** | AWS EC2, Azure Web App |
| **Utilities** | Logging, OS, sys, pickle |


## 📈 Future Enhancements

- Model versioning with MLflow

- Front-end interface (Streamlit or React)

- API authentication and rate limiting

## 👨‍💻 Author
**Derrick Nyongesa**  
B.Sc. Electrical & Electronics Engineering | Data Scientist  
📧 [derricknyongesa0.email@gmail.com](derricknyongesa0.email@gmail.com)  
🌐 [LinkedIn](https://www.linkedin.com/in/derrick-nyongesa/) | [GitHub](https://github.com/DECTEN0/)



