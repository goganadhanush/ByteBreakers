import streamlit as st
import requests
import io
import contextlib

# Hugging Face API Key (Replace with your own)
HUGGINGFACE_API_KEY = "API KEY"
MODEL_NAME = "mistralai/Mistral-7B-Instruct"  # You can change this to another model if needed

st.set_page_config(page_title="CodeGenie AI", page_icon="✨", layout="wide")

languages = ["Python", "JavaScript", "Java"]

def query_code_llama(prompt, language):
    """Generates code using Hugging Face's Code Llama API."""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": f"Generate a {language} function for: {prompt}",
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(f"https://api-inference.huggingface.co/models/{MODEL_NAME}", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"⚠️ API Error: {response.json()}"

# Sidebar Navigation
with st.sidebar:
    st.title("📌 Navigation")
    menu_option = st.radio("Select an Option", ["🏠 Dashboard", "💻 Code Generator", "⚡ Online Compiler"])

if menu_option == "🏠 Dashboard":
    st.markdown("""
        <div style='text-align: center;'>
            <h1>👋 Welcome to CodeGenie AI!</h1>
            <p>Your AI-powered coding assistant!</p>
        </div>
    """, unsafe_allow_html=True)

elif menu_option == "💻 Code Generator":
    st.header("💻 AI-Powered Code Generator")
    st.markdown("Describe your code requirement, and AI will generate it.")

    code_description = st.text_area("Enter your code description:", placeholder="E.g., 'Create a function that calculates the factorial of a number.'")
    language = st.selectbox("Select Programming Language:", languages, index=0)

    if st.button("Generate Code"):
        if not code_description.strip():
            st.error("❌ Please enter a valid description!")
        else:
            with st.spinner("Generating code with AI... ⏳"):
                generated_code = query_code_llama(code_description, language)
            
            st.success(f"✅ Code generated successfully in {language}!")
            st.code(generated_code, language=language.lower())

elif menu_option == "⚡ Online Compiler":
    st.header("⚡ Online Python Compiler")
    st.markdown("Write and execute your Python code below:")

    code_input = st.text_area("Enter Python Code:", height=300, placeholder="Write your Python code here...")

    if st.button("Run Code"):
        output_buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code_input, {})
            output = output_buffer.getvalue()
            st.markdown("### Output:")
            st.code(output, language="bash")
        except Exception as e:
            st.error(f"❌ Error: {e}")
