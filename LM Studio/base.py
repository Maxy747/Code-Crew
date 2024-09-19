import streamlit as st
from llama_cpp import Llama

# Load the LLaVA-v1.5-7B-GGUF model using llama-cpp with the correct paths
@st.cache_resource
def load_llm_model():
    # Path to the GGUF model file
    model_path = "C:/Users/mazin/.cache/lm-studio/models/second-state/Llava-v1.5-7B-GGUF/llava-v1.5-7b-Q4_0.gguf"
    
    # Load the GGUF model using Llama CPP
    llm = Llama(model_path=model_path)
    return llm

# Generate a response from the LLM model
def generate_response(llm, prompt):
    # Generate response using the loaded LLaVA model
    response = llm(prompt)
    return response['choices'][0]['text']

# Streamlit app layout
st.title("LLaVA v1.5-7B GGUF-powered Assistant")
st.write("Enter your query below, and the LLaVA model will generate a response:")

# User input text box
user_input = st.text_area("Enter your query here", placeholder="Type a question or request...")

# Load the model
llm = load_llm_model()

# If the user submits input
if st.button("Generate Response"):
    if user_input:
        # Generate response using the LLM
        response = generate_response(llm, user_input)
        st.write("### Response:")
        st.write(response)
    else:
        st.write("Please enter a query.")
