import streamlit as st
import os

def render_sidebar():
    """Render the sidebar and handle API key configuration."""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Add some spacing
        st.write("")
        
        # Model selection in an expander
        with st.expander("🤖 Model Selection", expanded=True):
            llm_option = st.radio(
                "Select LLM Provider",
                ["OpenAI", "GROQ"],
                help="Choose which Large Language Model provider to use",
                horizontal=True
            )
        
        # API Keys in an expander
        with st.expander("🔑 API Keys", expanded=True):
            st.info("API keys are stored temporarily in memory and cleared when you close the browser.")
            
            if llm_option == "OpenAI":
                openai_api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    help="Enter your OpenAI API key"
                )
                if openai_api_key:
                    os.environ["OPENAI_API_KEY"] = openai_api_key
            else:  # GROQ
                groq_api_key = st.text_input(
                    "GROQ API Key",
                    type="password",
                    value=os.getenv("GROQ_API_KEY"),
                    help="Enter your GROQ API key"
                )
                if groq_api_key:
                    os.environ["GROQ_API_KEY"] = groq_api_key
            
            serper_api_key = st.text_input(
                "SerperDev API Key",
                type="password",
                value=os.getenv("SERPER_API_KEY"),
                help="Enter your SerperDev API key for web search capabilities"
            )
            if serper_api_key:
                os.environ["SERPER_API_KEY"] = serper_api_key
        
        # Add some spacing
        st.write("")
        
        # Add helpful information
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
                This research assistant uses advanced AI models to help you:
                - Research any topic in depth
                - Analyze and summarize information
                - Provide structured reports
                
                Choose your preferred model and enter the required API keys to get started.
            """)
                
    return llm_option