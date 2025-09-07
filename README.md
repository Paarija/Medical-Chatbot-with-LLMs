# 🩺 Build a Complete Medical Chatbot with LLMs, LangChain, Pinecone & Flask  

A medical chatbot powered by **Large Language Models (LLMs)**, **LangChain**, **Pinecone** and **Flask**.  

---

## 🚀 How to Run  

Follow these steps to set up and run the chatbot on your machine:  

```bash
# STEP 1️⃣ - Clone the repository
git clone https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git
cd Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS

# STEP 2️⃣ - Create a Conda environment
conda create -n medibot python=3.10 -y
conda activate medibot

# STEP 3️⃣ - Install dependencies
pip install -r requirements.txt

# STEP 4️⃣ - Configure environment variables (create a .env file in root directory)
# Add the following:
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key

# STEP 5️⃣ - Store embeddings into Pinecone
python store_index.py

# STEP 6️⃣ - Run the Flask app
python app.py
