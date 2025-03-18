import streamlit as st
import datetime
import google.generativeai as genai
import os

# ✅ Use Streamlit secrets management or environment variables for security
GOOGLE_API_KEY = os.getenv("AIzaSyBqGySM48uyNlErVXI9NA_dkScRpE-JIJg")  # Set this in Streamlit secrets
if not GOOGLE_API_KEY:
    st.error("API Key is missing. Set it as an environment variable or in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Model initialization
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config
)

def get_ai_response(prompt, fallback_message):
    """Generates AI response with error handling."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if hasattr(response, "text") and response.text.strip() else fallback_message
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n{fallback_message}"

def get_event_recommendation():
    """Generates AI-powered event recommendation."""
    today = datetime.datetime.today().strftime("%B %d")
    prompt = f"""
    Today is {today}. Identify any special occasion (e.g., Valentine's Day, Christmas, Thanksgiving) and recommend:
    - Restaurant theme
    - Cuisine type
    - Drinks
    - Dessert pairing
    - Discount strategy
    - Marketing slogan
    - Instagram caption & hashtags
    - Lighting and music style
    - Sustainability strategies
    - Seating arrangement
    - Customer sentiment prediction
    - Pricing strategy for discounts
    - Event entertainment options
    - Staff dress code
    - Social media engagement tips
    - Promotional email template
    """
    return get_ai_response(prompt, "⚠️ AI response unavailable. Please try again later.")

def get_reservation_recommendation(occasion, people, cuisine_type, drink_type, budget):
    """Generates AI-powered reservation recommendation."""
    if not all([occasion, people, cuisine_type, drink_type, budget]):
        return "⚠️ Please fill in all fields before generating a recommendation."
    
    prompt = f"""
    A restaurant reservation has been made with:
    - Occasion: {occasion}
    - Guests: {people}
    - Cuisine: {cuisine_type}
    - Drinks: {drink_type}
    - Budget: {budget}
    
    Recommend:
    - Suitable event theme
    - Decoration style
    - Custom menu (dishes, drinks, desserts)
    - Discount offer
    - Marketing slogan
    - Instagram caption & hashtags
    - Seating optimization
    - Allergy-friendly recommendations
    - Sustainable dining strategies
    - Personalized thank-you message
    - Music playlist
    - Table arrangements
    - Guest experience enhancements
    - Loyalty program offers
    """
    return get_ai_response(prompt, "⚠️ AI response unavailable. Please try again later.")

# ✅ Streamlit UI
st.set_page_config(page_title="AI-Powered Restaurant Manager", layout="wide")
st.title("🍽️ AI-Powered Smart Restaurant Management")

# 🌟 Event Recommendation
st.header("📅 AI-Powered Event Recommendation for Today")
if st.button("Generate Event Recommendation"):
    st.text_area("Event Recommendation:", get_event_recommendation(), height=300)

# 🎊 Custom Event Recommendation
st.header("🎊 Custom AI-Powered Event Recommendation")

occasion = st.text_input("🎉 Occasion (e.g., Birthday, Anniversary, Business Meeting)")
people = st.number_input("👥 Number of Guests", min_value=1, value=2)
cuisine_type = st.selectbox("🍽 Preferred Cuisine", ["Veg", "Non-Veg", "Vegan"])
drink_type = st.selectbox("🍹 Preferred Drink", ["Soft Drinks", "Mocktails", "Cocktails", "Beer"])
budget = st.text_input("💰 Budget Range")

if st.button("Generate Reservation Recommendation"):
    result = get_reservation_recommendation(occasion, people, cuisine_type, drink_type, budget)
    st.text_area("Reservation Recommendation:", result, height=300)

st.write("\n🚀 Powered by Gemini AI")
