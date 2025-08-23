# Career Compass AI

## Democratizing College Guidance for Every Student

*Your personalized companion for discovering the right branch, exploring best-fit colleges, and making smart, informed decisions—all in one place*

---

## 📌 Project Poster
![Poster Thumbnail](assets/poster.png)

---

## 🚀 Features

### Modules
1. **Specialization Recommender**  
   *Questionnaire-powered recommendations aligned with your strengths.*

2. **Branch Explorer**  
   *Discover courses, careers, pay, and opportunities.*

3. **College Filter & Map**  
   *Match Colleges to your profile: Smart filters + interactive map for institute choices.*

4. **College–Branch Insight Hub**  
   *Deep insights & comparisons to guide your choice.*

5. **JEE Docs Chat**  
   *Your AI-powered guide to official JEE rules & FAQs.*

---

## 🛠️ Tech Stack
- **Core**: Python  
- **LLM & AI Frameworks**: LangChain, LangGraph, Hugging Face, Groq Cloud (API)  
- **Vector Search**: FAISS  
- **Frontend / UI**: Streamlit, Folium (for interactive maps)  
- **Data Handling**: Pandas, NumPy, Unstructured  

---

## ⚙️ Setup

1. Clone the repo:  

   ```bash
   git clone https://github.com/your-username/Career-Compass-AI.git
   cd Career-Compass-AI
   ```
2. Create a virtual environment (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables

Create a `.env` file in the root folder and add your keys:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   HF_TOKEN=your_huggingface_token
   ```
5. Download vector store

* The vector store is not included in this repository due to GitHub’s file size limits.  
* To use the app without rebuilding embeddings from scratch, download the prebuilt vector store:

📥 [Download vector_store from Google Drive](https://drive.google.com/drive/folders/1A2ibtHlumIechILpXJdSS4YTl2QbDaWi?usp=sharing)

Place the extracted `vector_store/` folder inside the project root (alongside `main.py`).

Final structure:
```
Career-Compass-AI/
├── assets/
├── data/
├── prompts/
├── src/
├── vector_store/   <-- place it here
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
```
6. Run the app

   ```bash
   streamlit run main.py
   ```   

## Context

This project is designed in the context of **India’s JEE exam** and the **JoSAA counseling process**, empowering students to explore branches, compare colleges, and make informed career decisions. That said, this can be adaptable to college counselling systems worldwide.

## License

This project is licensed under the [MPL 2.0 License](./LICENSE).







