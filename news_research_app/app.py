import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------- UI Setup ----------
st.set_page_config(page_title="📰 GrokNews AI", page_icon="🧠", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0f0f0f;
            color: #e0e0e0;
        }
        .stApp {
            background-color: #0f0f0f;
        }
        .stTextInput > div > div > input {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .stButton>button {
            background-color: #1da1f2;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 10em;
        }
        .stButton>button:hover {
            background-color: #0d8af0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 GrokNews — The AI Research Assistant")
st.caption("Get factual summaries from the latest news — powered by LLaMA 3 via Groq API 🐂")

topic = st.text_input("Enter a trending topic:", placeholder="e.g. Elon Musk, AI, Elections")

# ---------- Search and Process ----------
if st.button("Summon Grok"):
    if not NEWS_API_KEY or not GROQ_API_KEY:
        st.error("⚠️ Missing API Keys. Please check your `.env` file.")
    elif not topic.strip():
        st.warning("Try typing *something*, Genius 😏")
    else:
        with st.spinner("Fetching news... hold your neurons 🧬"):
            url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={topic}&language=en"
            response = requests.get(url)
            data = response.json()

        if "results" not in data or not data["results"]:
            st.warning("No juicy headlines found. Maybe it’s too boring?")
        else:
            st.subheader("🗞 Latest News Articles")
            articles_text = ""

            for i, article in enumerate(data["results"][:5], 1):
                title = article.get("title", "No title available")
                desc = article.get("description", "No description.")
                link = article.get("link", "#")

                st.markdown(f"### {i}. [{title}]({link})")
                st.write(desc)
                st.divider()

                articles_text += f"{title}. {desc}\n"

            # ---------- AI Summary ----------
            st.subheader("🤖 Grok’s Sarcastic Summary")
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            prompt = f"""
            You are Grok — an AI with sharp wit, sarcasm, and intelligence.
            Summarize the following news articles about '{topic}'.
            Make it informative but slightly funny, like you're roasting the situation.
            Then, add a brief sentiment analysis (positive/neutral/negative) for each headline.
            Here’s the news:\n{articles_text}
            """

            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }

            with st.spinner("Grok is thinking (or pretending to)... 🤔"):
                groq_response = requests.post(groq_url, headers=headers, json=payload)

            if groq_response.status_code == 200:
                summary = groq_response.json()["choices"][0]["message"]["content"]
                st.markdown(f"🌌 {summary}")
            else:
                st.error(f"Grok API Error: {groq_response.text}")
