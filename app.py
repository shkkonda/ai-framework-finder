import streamlit as st
import google.generativeai as genai
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Agentic AI Framework Recommender",
    page_icon="🤖",
    layout="wide"
)

# Framework information for context
FRAMEWORK_INFO = {
    "n8n": {
        "description": "A visual workflow automation tool with AI capabilities",
        "strengths": ["Visual workflow builder", "No-code/low-code", "Extensive integrations", "Easy to use"],
        "best_for": ["Workflow automation", "Data integration", "Business process automation", "Non-technical users"]
    },
    "LangGraph": {
        "description": "A library for building stateful, multi-actor applications with LLMs",
        "strengths": ["Stateful workflows", "Complex reasoning chains", "Graph-based architecture",
                      "LangChain integration"],
        "best_for": ["Complex reasoning tasks", "Multi-step workflows", "State management", "Research applications"]
    },
    "CrewAI": {
        "description": "A framework for orchestrating role-playing, autonomous AI agents",
        "strengths": ["Role-based agents", "Collaborative workflows", "Task delegation", "Hierarchical structures"],
        "best_for": ["Team collaboration simulation", "Multi-agent systems", "Role-specific tasks", "Creative projects"]
    },
    "AutoGen": {
        "description": "Microsoft's framework for multi-agent conversation systems",
        "strengths": ["Conversational AI", "Multi-agent chat", "Code generation", "Human-in-the-loop"],
        "best_for": ["Conversational workflows", "Code generation", "Problem-solving discussions", "Interactive agents"]
    }
}


def init_gemini_api():
    """Initialize Gemini API with key from environment variables or Streamlit secrets"""
    try:
        api_key = None

        # First, try to get from environment variables (local development)
        api_key = os.getenv('GEMINI_API_KEY')

        # If not found in env vars, try Streamlit secrets (deployment)
        if not api_key:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except (KeyError, FileNotFoundError):
                pass

        # If still no API key found
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found in environment variables or Streamlit secrets")
            st.info("""
            **Setup Instructions:**

            **For local development:**
            - Add `GEMINI_API_KEY=your_api_key_here` to your `.env` file

            **For Streamlit Cloud deployment:**
            - Add `GEMINI_API_KEY = "your_api_key_here"` to your app's secrets in the Streamlit Cloud dashboard
            """)
            return False

        genai.configure(api_key=api_key)
        return True

    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        return False


def validate_agentic_ai_task(task_description: str) -> Dict[str, Any]:
    """Validate if the task is related to agentic AI systems"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        validation_prompt = f"""
You are a validator for AI automation and agentic AI task descriptions. Your job is to determine if a user's input is asking about building an AI-powered system or workflow.

AI automation and agentic systems include:
- Autonomous agents that can act independently
- Multi-agent systems with collaboration
- AI workflows that automate tasks
- AI tools that process data and generate outputs
- Systems involving AI decision-making and personalization
- AI-powered automation for business processes
- Tools that use AI to analyze, generate, or personalize content
- Workflows where AI performs tasks with minimal human intervention

User Input: "{task_description}"

Analyze this input and respond with ONLY a JSON object:
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "reason": "Brief explanation of why this is/isn't an AI automation or agentic task"
}}

Examples of VALID requests:
- "Personalized email generator"
- "Tool that gets information from email domain and personalizes emails"
- "AI system for customer service automation"
- "Multi-agent system for data analysis and reporting"
- "Automated content creation workflow"
- "AI-powered lead qualification system"
- "Smart document processing pipeline"
- "Intelligent data extraction and analysis tool"

Examples of INVALID requests:
- "How do I cook pasta?"
- "What's the weather today?"
- "Help me with my homework"
- "Explain quantum physics"
- "Basic math calculator" (no AI involved)
- "Static website builder" (no AI automation)

Be inclusive - accept any genuine AI automation, workflow automation, or agentic AI system building requests.
"""

        response = model.generate_content(validation_prompt)
        response_text = response.text

        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            return {"is_valid": False, "confidence": 0.0, "reason": "Unable to validate input"}

    except Exception as e:
        return {"is_valid": False, "confidence": 0.0, "reason": f"Validation error: {str(e)}"}


def create_recommendation_prompt(task_description: str, coding_experience: str) -> str:
    """Create a detailed prompt for framework recommendation"""
    prompt = f"""
You are an expert in agentic AI frameworks. The user has already been validated as asking about building an agentic AI system. Based on the following task description and their coding experience, recommend the most suitable framework from these options: n8n, LangGraph, CrewAI, or AutoGen.

Task Description: {task_description}
User's Coding Experience: {coding_experience}

Framework Options:
1. n8n - Visual workflow automation tool with AI capabilities. Best for: workflow automation, data integration, business processes, non-technical users.

2. LangGraph - Library for building stateful, multi-actor applications with LLMs. Best for: complex reasoning tasks, multi-step workflows, state management, research applications.

3. CrewAI - Framework for orchestrating role-playing, autonomous AI agents. Best for: team collaboration simulation, multi-agent systems, role-specific tasks, creative projects.

4. AutoGen - Microsoft's framework for multi-agent conversation systems. Best for: conversational workflows, code generation, problem-solving discussions, interactive agents.

IMPORTANT: Consider the user's coding experience when making recommendations:
- If coding experience is "No": Strongly favor n8n for its visual, no-code approach
- If coding experience is "Yes": Consider all frameworks based on the specific requirements

Please provide your recommendation in the following JSON format:
{{
    "recommended_framework": "framework_name",
    "confidence_score": 0.85,
    "reasoning": "Detailed explanation of why this framework is best suited for this agentic AI system, considering their coding experience",
    "alternative_options": ["alternative1", "alternative2"],
    "implementation_tips": ["tip1", "tip2", "tip3"],
    "potential_challenges": ["challenge1", "challenge2"]
}}

Consider factors specific to agentic AI systems:
- Agent autonomy requirements
- Multi-agent coordination needs
- Task complexity and reasoning depth
- Integration with external systems
- Scalability for multiple agents
- Development and maintenance complexity
- User's technical background and coding experience
"""
    return prompt


def get_gemini_recommendation(task_description: str, coding_experience: str, model_name: str = "gemini-1.5-flash") -> \
Dict[Any, Any]:
    """Get framework recommendation from Gemini API"""
    try:
        model = genai.GenerativeModel(model_name)
        prompt = create_recommendation_prompt(task_description, coding_experience)

        response = model.generate_content(prompt)

        # Extract JSON from response
        response_text = response.text

        # Find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            # Fallback if JSON parsing fails
            return {
                "recommended_framework": "Unable to parse",
                "reasoning": response_text,
                "confidence_score": 0.0,
                "alternative_options": [],
                "implementation_tips": [],
                "potential_challenges": []
            }

    except Exception as e:
        st.error(f"Error getting recommendation: {str(e)}")
        return None


def display_framework_overview():
    """Display comprehensive framework information"""
    st.header("📚 Framework Overview")
    st.markdown("Learn about each agentic AI framework and their capabilities")

    # Create expandable sections for each framework
    for framework, info in FRAMEWORK_INFO.items():
        with st.expander(f"🔧 {framework}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Description:** {info['description']}")

                st.write("**Key Strengths:**")
                for strength in info['strengths']:
                    st.write(f"• {strength}")

                st.write("**Best Use Cases:**")
                for use_case in info['best_for']:
                    st.write(f"• {use_case}")

            with col2:
                # Add some visual elements or additional info
                if framework == "n8n":
                    st.info("🎨 **Visual & No-Code**\n\nPerfect for teams without deep technical expertise")
                elif framework == "LangGraph":
                    st.info("🧠 **Complex Reasoning**\n\nIdeal for sophisticated multi-step workflows")
                elif framework == "CrewAI":
                    st.info("👥 **Role-Based Agents**\n\nGreat for simulating team collaboration")
                elif framework == "AutoGen":
                    st.info("💬 **Conversational AI**\n\nExcellent for interactive agent systems")

    # Comparison table
    st.subheader("🔍 Quick Comparison")

    comparison_data = {
        "Framework": list(FRAMEWORK_INFO.keys()),
        "Complexity": ["Low", "High", "Medium", "Medium"],
        "Learning Curve": ["Easy", "Steep", "Moderate", "Moderate"],
        "Best For": [
            "Business Automation",
            "Research & Complex Tasks",
            "Creative & Role-Play",
            "Conversational Systems"
        ]
    }

    st.table(comparison_data)


def main():
    st.title("🤖 Agentic AI Framework Recommender")

    # Initialize API
    if not init_gemini_api():
        st.error("Please ensure GEMINI_API_KEY is set in your .env file")
        st.stop()

    # Create main tabs
    tab1, tab2 = st.tabs(["🔍 Get Recommendation", "📚 Framework Overview"])

    with tab1:
        st.header("📝 Describe Your Agentic AI System")

        # Initialize session state for coding experience
        if 'coding_experience' not in st.session_state:
            st.session_state.coding_experience = "Yes"

        task_description = st.text_area(
            "Describe your AI automation system:",
            placeholder="Example: I want to build a personalized email generator that gets information from email domains and creates customized outreach emails based on the company's profile and industry...",
            height=150,
            help="Describe any AI-powered automation, workflow, or agentic system"
        )

        # Coding experience radio button
        st.subheader("👨‍💻 Technical Background")
        coding_experience = st.radio(
            "Do you have coding experience?",
            ["Yes", "No"],
            index=0 if st.session_state.coding_experience == "Yes" else 1,
            help="This helps us recommend the most suitable framework for your technical level"
        )

        # Update session state
        if coding_experience != st.session_state.coding_experience:
            st.session_state.coding_experience = coding_experience


        # Get recommendation button
        if st.button("🔍 Get Recommendation", type="primary", use_container_width=True):
            if task_description.strip():
                with st.spinner("Validating your request..."):
                    # First validate if the task is related to agentic AI
                    validation = validate_agentic_ai_task(task_description)

                if validation["is_valid"]:
                    with st.spinner("Analyzing your AI automation task and generating recommendation..."):
                        recommendation = get_gemini_recommendation(task_description, st.session_state.coding_experience)

                    if recommendation:
                        st.success("✅ Recommendation generated!")

                        # Display recommendation
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.header(f"🎯 Recommended Framework: **{recommendation['recommended_framework']}**")

                            # Confidence score
                            confidence = recommendation.get('confidence_score', 0)
                            st.metric("Confidence Score", f"{confidence:.0%}")

                            # Reasoning
                            st.subheader("🧠 Reasoning")
                            st.write(recommendation['reasoning'])

                            # Alternative options - always show
                            if recommendation.get('alternative_options'):
                                st.subheader("🔄 Alternative Options")
                                for alt in recommendation['alternative_options']:
                                    st.write(f"• {alt}")

                            # Implementation tips - always show
                            if recommendation.get('implementation_tips'):
                                st.subheader("💡 Implementation Tips")
                                for tip in recommendation['implementation_tips']:
                                    st.write(f"• {tip}")

                            # Potential challenges
                            if recommendation.get('potential_challenges'):
                                st.subheader("⚠️ Potential Challenges")
                                for challenge in recommendation['potential_challenges']:
                                    st.write(f"• {challenge}")

                        with col2:
                            # Framework details
                            rec_framework = recommendation['recommended_framework']
                            if rec_framework in FRAMEWORK_INFO:
                                st.subheader("📋 Framework Details")
                                info = FRAMEWORK_INFO[rec_framework]
                                st.write(f"**Description:** {info['description']}")
                                st.write("**Key Strengths:**")
                                for strength in info['strengths'][:3]:  # Show top 3
                                    st.write(f"• {strength}")
                else:
                    # Display validation failure
                    st.error("❌ Invalid Request")
                    st.warning(f"**Reason:** {validation['reason']}")

                    # Show what makes a valid request
                    with st.expander("ℹ️ What makes a valid AI automation request?"):
                        st.markdown("""
                        **This tool is for AI automation systems that involve:**

                        ✅ **Valid Examples:**
                        - AI workflows that automate business processes
                        - Tools that use AI to analyze, generate, or personalize content
                        - Multi-agent systems with role-based AI agents
                        - Autonomous agents that can make decisions independently
                        - AI-powered data processing and analysis systems
                        - Intelligent automation for customer service, sales, or marketing

                        ❌ **Invalid Examples:**
                        - General programming questions
                        - Non-AI related tasks or basic calculators
                        - Educational questions about AI concepts
                        - Simple static websites without AI components

                        **Try describing:**
                        - What AI capabilities your system needs
                        - How the AI will process or analyze data
                        - What automated decisions or actions the AI will take
                        - How different AI components will work together
                        """)

                    # Show suggested improvements
                    st.subheader("💡 Suggestion")
                    st.info(
                        "Try describing a system that uses AI to automate tasks, analyze data, or make intelligent decisions.")

            else:
                st.warning("Please describe your AI automation task first!")

    with tab2:
        display_framework_overview()


if __name__ == "__main__":
    main()
