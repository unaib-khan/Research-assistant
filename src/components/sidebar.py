import streamlit as st
import os
import requests

#--------------------------------#
#      Ollama Integration        #
#--------------------------------#
def is_ollama_available():
    """Check if Ollama is available by attempting to connect to its API.
    
    Returns:
        bool: True if Ollama is running and accessible, False otherwise
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
        return response.status_code == 200
    except:
        return False

def get_ollama_models():
    """Get list of available Ollama models from local instance.
    
    Returns:
        list: Names of available Ollama models, or empty list if Ollama is not running
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            return [model["name"] for model in models["models"]]
        return []
    except:
        return []

#--------------------------------#
#      Sidebar Configuration     #
#--------------------------------#
def render_sidebar():
    """Render the sidebar and handle API key & model configuration.
    
    The sidebar allows users to:
    1. Select an LLM provider (OpenAI, GROQ, or Ollama)
    2. Choose or input a specific model
    3. Enter necessary API keys
    
    Returns:
        dict: Contains selected provider and model information
    """
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.write("")
        with st.expander("🤖 Model Selection", expanded=True):
            # Show message if not running locally
            ollama_available = is_ollama_available()
            if not ollama_available:
                st.info("⚠️ Ollama is not available. Make sure it's running locally if you want to use it.")
            
            provider = st.radio(
                "Select LLM Provider",
                ["OpenAI", "GROQ", "Ollama"] if ollama_available else ["OpenAI", "GROQ"],
                help="Choose which Large Language Model provider to use",
                horizontal=True,
                captions=[
                    "Reliable performance",
                    "Ultra-fast inference",
                    "Local deployment" if ollama_available else None
                ][:2] if not ollama_available else None
            )
            
            if provider == "OpenAI":
                model_option = st.selectbox(
                    "Select OpenAI Model",
                    ["gpt-4o-mini", "gpt-4o"],
                    index=0
                )
                if model_option == "Custom":
                    model = st.text_input("Enter your custom OpenAI model:", value="", help="Specify your custom model string")
                else:
                    model = model_option
            elif provider == "GROQ":
                model = st.selectbox(
                    "Select GROQ Model",
                    [
                        "qwen-2.5-32b",
                        "deepseek-r1-distill-qwen-32b",
                        "deepseek-r1-distill-llama-70b"
                    ],
                    index=0,
                    help="Choose from GROQ's available models. All these models support tool use and parallel tool use."
                )
                if model == "Custom":
                    model = st.text_input("Enter your custom GROQ model:", value="", help="Specify your custom model string")
            elif provider == "Ollama":
                # Get available Ollama models
                ollama_models = get_ollama_models()
                if not ollama_models:
                    st.warning("⚠️ No Ollama models found. Make sure Ollama is running locally.")
                    model = None
                else:
                    st.warning("⚠️ Note: Most Ollama models have limited function-calling capabilities. This may affect research quality as they might not effectively use web search tools.")
                    model = st.selectbox(
                        "Select Ollama Model",
                        ollama_models,
                        help="Choose from your locally available Ollama models. For best results, use models known to handle function calling well (e.g., mixtral, openhermes)."
                    )
        
        with st.expander("🔑 API Keys", expanded=True):
            st.info("API keys are stored temporarily in memory and cleared when you close the browser.")
            if provider == "OpenAI":
                openai_api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    value=os.getenv("OPENAI_API_KEY"),
                    help="Enter your OpenAI API key"
                )
                if openai_api_key:
                    os.environ["OPENAI_API_KEY"] = openai_api_key
            elif provider == "GROQ":
                groq_api_key = st.text_input(
                    "GROQ API Key",
                    type="password",
                    value=os.getenv("GROQ_API_KEY"),
                    help="Enter your GROQ API key"
                )
                if groq_api_key:
                    os.environ["GROQ_API_KEY"] = groq_api_key
            
            # Only show EXA key input if not using Ollama
            if provider != "Ollama":
                exa_api_key = st.text_input(
                    "EXA API Key",
                    type="password",
                    value=os.getenv("EXA_API_KEY"),
                    help="Enter your EXA API key for web search capabilities"
                )
                if exa_api_key:
                    os.environ["EXA_API_KEY"] = exa_api_key

        st.write("")
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
                This research assistant uses advanced AI models to help you:
                - Research any topic in depth
                - Analyze and summarize information
                - Provide structured reports
                
                Choose your preferred model and enter the required API keys to get started.
                
                **Note on Model Selection:**
                - OpenAI and GROQ models provide full functionality with web search capabilities
                - Ollama models run locally but have limited function-calling abilities
                  and will rely more on their base knowledge
                
                For Ollama users:
                - Make sure Ollama is running locally with your desired models loaded
                - Best results with models that handle function calling (e.g., mixtral, openhermes)
                - Web search functionality is disabled for Ollama models
            """)
    return {
        "provider": provider,
        "model": model
    }
