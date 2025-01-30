import streamlit as st
import os
from src.components.sidebar import render_sidebar
from src.components.researcher import create_researcher, create_research_task, run_research
from src.utils.output_handler import capture_output

# Configure the page
st.set_page_config(
    page_title="CrewAI Research Assistant",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo
st.logo("https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg", link="https://www.crewai.com/", size="large")

# Main layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔍 :red[CrewAI] Research Assistant", anchor=False)

# Render sidebar and get LLM option
llm_option = render_sidebar()

# Check if API keys are set
if (llm_option == "OpenAI" and not os.getenv("OPENAI_API_KEY")) or \
   (llm_option == "GROQ" and not os.getenv("GROQ_API_KEY")) or \
   not os.getenv("SERPER_API_KEY"):
    st.warning("⚠️ Please enter your API keys in the sidebar to get started")
    st.stop()

# # Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([1, 3, 1])

with input_col2:
    task_description = st.text_area(
        "What would you like to research?",
        value="Research the latest AI developments in 2025 and summarize the key trends.",
        height=100
    )

col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")

if start_research:
    with st.status("🤖 Researching...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context
            with capture_output(output_container):
                # Create and run the research
                researcher = create_researcher(llm_option)
                task = create_research_task(researcher, task_description)
                result = run_research(researcher, task)
                
                # Update status when complete
                status.update(label="✅ Research completed!", state="complete", expanded=False)
                
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()

    # Display the final result
    st.markdown(result)

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com), [Exa](https://exa.ai) and [Streamlit](https://streamlit.io)")