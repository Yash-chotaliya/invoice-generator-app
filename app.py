from dotenv import load_dotenv
load_dotenv() # load all the environment variable from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import prompts
import asyncio
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
    
async def generate_invoice(header, items, total_amount) :
    
    res = requests.post("https://invoice-generator-api-jklu.onrender.com/test", data={"header": header, "items": items, "total_amount": total_amount})
    
    if res.status_code != 200:
        return ""
    
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
                        
            link = ""
            x = st.progress(10, "waiting...")
            download_widget = st.empty()
            

            image_data=get_image_data(uploaded_file)
            
            input_prompt = """
            you are an expert in understanding invoices. we will 
            upload an image as invoice and you will
            have to answer any question based on 
            the uploaded invoice image"""
            
            try:
                header = get_gemini_response(input_prompt, image_data[0], prompts.header_prompt)[10:-4].strip()
                x.progress(20, "waiting...")
                items = get_gemini_response(input_prompt, image_data[0], prompts.items_prompt).strip()
                x.progress(30, "waiting...")
                total_amount = get_gemini_response(input_prompt, image_data[0], prompts.total_amount_prompt).strip()
                x.progress(60, "waiting...")
                
                link = asyncio.run(generate_invoice(header, items, total_amount))
                
                if(link!="" & link!="Format Error"):    
                    x.success("Invoice generated, you can download it by clicking below button")
                    download_widget.markdown(f'''<a href="{link}"><button style="background-color:Green;">Download</button></a>''',
                    unsafe_allow_html=True)
                    
                elif link == "Format Error":
                    st.error(link)
                    
                else:
                    st.error("Error Generating Invoice")
            except:
                st.error("Error Generating Invoice")
            
        else:
            st.error("please upload an image of invoice")

