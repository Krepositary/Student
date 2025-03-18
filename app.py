import streamlit as st
import datetime
import google.generativeai as genai
import os

# ✅ Configure API Key from Streamlit Secrets (for GitHub deployment)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

api_key = st.secrets["AIzaSyAIZINFcr_D4rCFTgO9V9G9Rlo4xbL6gsA"]
genai.configure(api_key=api_key)

# 🔥 Function to interact with Gemini API
def get_ai_response(prompt, fallback_message="⚠️ AI response unavailable. Please try again later."):
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            generation_config={
                "temperature": 0.9,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
            }
        )
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else fallback_message
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n{fallback_message}"

# 🔥 Food Menu Recommendation
def get_food_recommendation(cuisine, dietary_pref, budget):
    prompt = f"""
    Recommend a restaurant food menu based on:
    - Cuisine: {cuisine}
    - Dietary preference: {dietary_pref}
    - Budget: {budget}

    Include:
    - Appetizers (2 options)
    - Main courses (3 options)
    - Desserts (2 options)
    - Beverage pairing suggestions
    - Pricing and serving size
    - Trending dishes and customer favorites
    - Calorie details and allergens
    """
    return get_ai_response(prompt)

# 🔥 Event Manager
def get_event_recommendation(event_type, guest_count, theme, budget):
    prompt = f"""
    Generate a detailed event management plan for:
    - Event Type: {event_type}
    - Number of Guests: {guest_count}
    - Theme: {theme}
    - Budget: {budget}

    Include:
    - Decoration and ambiance recommendations
    - Special food & drink menu
    - Entertainment suggestions
    - Discount offers and deals
    - Custom event slogans
    - Marketing tips (Instagram captions, hashtags)
    - AI-enhanced seating plan for guest interaction
    - Sustainability and eco-friendly tips
    """
    return get_ai_response(prompt)

# 🔥 Leftover Management
def get_leftover_management(plan_type, food_type, quantity):
    prompt = f"""
    Suggest a smart leftover management plan:
    - Plan Type: {plan_type}
    - Food Type: {food_type}
    - Quantity: {quantity}

    Include:
    - Redistribution options (charity, staff meals)
    - Storage tips (temperature, duration)
    - Recipes for repurposing leftovers
    - AI-suggested food donation programs
    - Tips for minimizing food waste
    """
    return get_ai_response(prompt)

# ✅ Streamlit UI
st.set_page_config(page_title="🍽️ Smart Restaurant Menu Manager", layout="wide")
st.title("🍴 Smart Restaurant Menu Management with Gemini 1.5 Pro")

# 🔥 Tabs for different features
tab1, tab2, tab3 = st.tabs(["🍽️ Food Menu", "🎊 Event Manager", "♻️ Leftover Management"])

# 📌 Food Menu Recommendation Tab
with tab1:
    st.header("🍽️ Food Menu Recommendation")

    cuisine = st.selectbox("Select Cuisine", ["Italian", "Indian", "Mexican", "Chinese", "Mediterranean"])
    dietary_pref = st.selectbox("Dietary Preference", ["Vegetarian", "Vegan", "Gluten-Free", "Non-Vegetarian"])
    budget = st.text_input("💰 Budget Range", "500-1500 INR")

    if st.button("Generate Menu"):
        st.text_area("🍴 Recommended Menu:", get_food_recommendation(cuisine, dietary_pref, budget), height=300)

# 📌 Event Manager Tab
with tab2:
    st.header("🎊 Event Manager")

    event_type = st.selectbox("Event Type", ["Birthday", "Anniversary", "Corporate Event", "Wedding"])
    guest_count = st.number_input("👥 Number of Guests", min_value=1, value=50)
    theme = st.text_input("🎉 Theme (e.g., Bollywood, Retro, Casual)")
    event_budget = st.text_input("💰 Budget Range", "10000-50000 INR")

    if st.button("Generate Event Plan"):
        st.text_area("🎊 Event Plan:", get_event_recommendation(event_type, guest_count, theme, event_budget), height=300)

# 📌 Leftover Management Tab
with tab3:
    st.header("♻️ Leftover Management")

    plan_type = st.selectbox("Plan Type", ["Redistribution", "Storage", "Repurposing"])
    food_type = st.text_input("🍕 Food Type (e.g., Rice, Bread, Veggies)")
    quantity = st.number_input("🥘 Quantity (kg)", min_value=1, value=5)

    if st.button("Generate Leftover Plan"):
        st.text_area("♻️ Leftover Plan:", get_leftover_management(plan_type, food_type, quantity), height=300)

st.write("\n🚀 Powered by Gemini AI")
