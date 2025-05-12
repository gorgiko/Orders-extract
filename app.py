from dotenv import load_dotenv

load_dotenv() # load all the environment variables from .env


import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# function to load gemini pro vision


def get_response(model, input, image, prompt):
    response = model.generate_content([input, image[0], prompt])

    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



# Initialize streamlit
st.set_page_config(page_title='Multilanguage Invoice Extractor')

st.header("Orders Extractor")
input = st.text_input("Input Prompt: ", key='input')
uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])

image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded image', use_container_width=True)

submit = st.button("Tell me about the invoice")


input_prompt = """
You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structured and accuracy in your responses.

"""
if submit:
    model = genai.GenerativeModel('gemini-1.5-flash')
    image_data = input_image_details(uploaded_file)
    response = get_response(model, input_prompt, image_data, input)
    st.subheader('The Resposne is')
    st.write(response)

    
