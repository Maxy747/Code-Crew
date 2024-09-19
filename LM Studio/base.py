import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the LM Studio model and tokenizer
model_id = "lmstudio-community/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create the Streamlit app
def main():
    st.title("Mistral 7B Instruct v0.3")

    # Get user input
    prompt = st.text_input("Enter your prompt:")

    # Generate text using the model
    if st.button("Generate"):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=200, num_beams=4)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display the generated text
        st.text_area("Generated Text", value=generated_text)

if __name__ == "__main__":
    main()