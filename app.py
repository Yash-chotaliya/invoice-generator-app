from dotenv import load_dotenv
load_dotenv() # load all the environment variable from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import prompts
import webbrowser
import requests

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load gemini pro vision model
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image, prompt])
    return response.text

def get_image_data(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File Not Uploaded")
    
def generate_invoice(header, items, total_amount):
    
    res = requests.post("https://invoice-generator-api-jklu.onrender.com/test", data={"header": header, "items": items, "total_amount": total_amount})
    
    return res.content.decode("utf-8")

if __name__ == "__main__":
    # initialize streamlit app

    st.title("Invoice Generator")
    
    st.image("inv_1.png", use_column_width=True, caption="format of generated invoice")
    
    uploaded_file = st.file_uploader("Upload an image of Invoice", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
    submit = st.button("submit")
        
    if submit:
        if uploaded_file is not None:
            
            image_data=get_image_data(uploaded_file)
            
            input_prompt = """
            you are an expert in understanding invoices. we will 
            upload an image as invoice and you will
            have to answer any question based on 
            the uploaded invoice image"""
            
            try:
                header = get_gemini_response(input_prompt, image_data[0], prompts.header_prompt)[10:-4].strip()
                items = get_gemini_response(input_prompt, image_data[0], prompts.items_prompt).strip()
                total_amount = get_gemini_response(input_prompt, image_data[0], prompts.total_amount_prompt).strip()
                
                link = generate_invoice(header, items, total_amount)
                if(link!=None):    
                    st.write("Invoice generated, you can download it by clicking below button")
                    st.markdown(f'''<a href="{link}"><button style="background-color:Green;">Download</button></a>''',
                    unsafe_allow_html=True)
            except:
                st.error("Error Generating Invoice")
            
        else:
            st.write("please upload an image of invoice")

