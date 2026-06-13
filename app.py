import streamlit as st
import requests
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("News Filters")

countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

categories = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

country = st.sidebar.selectbox(
    "Select Country",
    list(countries.keys())
)

category = st.sidebar.selectbox(
    "Select Category",
    categories
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="e.g. AI, cricket, Tesla"
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

# -----------------------------
# Fetch News
# -----------------------------
@st.cache_data(ttl=600)
def fetch_news(country_code, category_name, search_term, page_size):
    
    if search_term:
        url = f"{BASE_URL}/everything"
        params = {
            "q": search_term,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": API_KEY
        }
    else:
        url = f"{BASE_URL}/top-headlines"
        params = {
            "country": country_code,
            "category": category_name,
            "pageSize": page_size,
            "apiKey": API_KEY
        }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# -----------------------------
# Main UI
# -----------------------------
st.title("📰 Advanced News Dashboard")
st.markdown("Search and explore the latest news worldwide.")

data = fetch_news(
    countries[country],
    category,
    keyword,
    num_articles
)

if data and data.get("articles"):

    articles = data["articles"]

    st.success(f"Found {len(articles)} articles")

    for article in articles:

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if article.get("urlToImage"):
                    st.image(
                        article["urlToImage"],
                        use_container_width=True
                    )

            with col2:

                st.subheader(article.get("title", "No Title"))

                st.write(
                    article.get("description", "No description available")
                )

                source = article.get("source", {}).get(
                    "name", "Unknown Source"
                )

                published = article.get(
                    "publishedAt", ""
                ).replace("T", " ").replace("Z", "")

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                st.link_button(
                    "Read Full Article",
                    article.get("url")
                )

            st.divider()

    # -------------------------
    # Download News Data
    # -------------------------
    df = pd.DataFrame([
        {
            "Title": a.get("title"),
            "Source": a.get("source", {}).get("name"),
            "Published": a.get("publishedAt"),
            "URL": a.get("url")
        }
        for a in articles
    ])

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Articles as CSV",
        csv,
        "news_articles.csv",
        "text/csv"
    )

else:
    st.error("No news articles found.")