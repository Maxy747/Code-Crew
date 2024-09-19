import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the Gemini model and tokenizer
model_id = "AIzaSyDsp-Q1M2CM548oSCoAAO_UCAaeM2dOdVI"  # Replace with your actual Gemini model ID
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create the Streamlit app
def main():
    st.title("Simple Chatbot")

    # Get user input
    prompt = st.text_input("Enter your message:")

    # Generate a response using the Gemini model
    if st.button("Send"):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=1024, num_beams=4)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display the generated response
        st.text_area("Response", value=generated_text)

if __name__ == "__main__":
    main()