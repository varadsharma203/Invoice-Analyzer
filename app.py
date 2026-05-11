from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types # Imported so we can use system instructions

load_dotenv()
my_api_key = os.getenv("GOOGLE_API_KEY")

def analyze_image_with_gemini(system_instruction, pil_image, user_prompt):
    # Initialize the client
    client = genai.Client(api_key=my_api_key)
    
    # We pass the PIL image and the user's question in the contents list.
    # We use the config to pass the "expert invoice analyzer" system instruction.
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[pil_image, user_prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )
        
    return response.text

## Initialize our Streamlit app
st.title("INVOICE ANALYZER")
st.write("Upload an invoice image and get insights about it using GEMINI")
st.header("GEMINI APPLICATION")

user_input = st.text_input("Input Prompt:", key="input_prompt")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
image = None

# Display the image if uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

system_prompt = """You are an expert in analyzing invoices. 
You will be given an image of an invoice and you will be asked to extract information from it."""

if submit:
    if image is not None:
        # Notice we don't need 'input_image_setup' anymore! 
        # We just pass the 'image' variable directly.
        response = analyze_image_with_gemini(
            system_instruction=system_prompt, 
            pil_image=image, 
            user_prompt=user_input
        )
        st.subheader("GEMINI RESPONSE")
        st.write(response)
    else:
        st.error("Please upload an image first!")