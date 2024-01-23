from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os 
import google.generativeai as genai
from PIL import Image 

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image_data,user_prompt):
	response = model.generate_content([input,image_data[0],user_prompt])
	return response.text

def input_image_detaols(uploaded_file):
	if uploaded_file is not None:
		bytes_data = uploaded_file.getvalue()
		image_parts=[{
			'mime_type':uploaded_file.type,

			'data':bytes_data
        }]
		return image_parts
	else:
		raise FileNotFoundError('No file Uploaded')

st.header('cartoon character')
st.markdown('<p style="color:red;">famous cartoon character</p>',unsafe_allow_html=True)

input = st.text_input('Input Prompt',key='Input')
uploaded_file=st.file_uploader('Image',type=['jpg','jpeg','png'])

if uploaded_file is not None:
	image = Image.open(uploaded_file)
	st.image(image,caption='uploaded File',use_column_width=True)
	
sub = st.button('Tell me about the famous cartoon character')

input_prompt =""" You are an expert in guessing famous cartoon characters.
We will upload an image of any famous cartoon character and you will have to answer any 
question based on the uploaded famous cartoon character."""

if sub:
	with st.spinner('wait'):
		image_data = input_image_detaols(uploaded_file)
		response=get_gemini_response(input_prompt,image_data,input)
		st.subheader('The response is')
		st.text_area (label="",value=response,height=500) 
