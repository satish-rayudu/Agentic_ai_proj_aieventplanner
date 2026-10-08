import streamlit as st

from agents import create_demo_agents, create_gemini_agents
from graph import build_graph


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Event Planning Agent",
    page_icon="📅",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📅 Event Planning Agent")

st.write(
    "Multi-Agent Event Planning System using "
    "LangGraph and Gemini"
)


# =========================================================
# MODE SELECTION
# =========================================================

mode = st.radio(
    "Select Agent Mode",
    [
        "Demo Mode",
        "Gemini AI Mode"
    ],
    horizontal=True
)


# =========================================================
# API KEY
# =========================================================

api_key = ""

if mode == "Gemini AI Mode":

    api_key = st.text_input(
        "🔑 Enter Gemini API Key",
        type="password"
    )


# =========================================================
# EVENT REQUEST
# =========================================================

event_request = st.text_area(
    "📝 Enter your event requirements",
    height=180,
    placeholder="""Example:

Plan a birthday party for 30 people in Hyderabad
on 20 December 2026 with a budget of ₹25,000.
I want vegetarian food and simple decoration."""
)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button(
    "🚀 Generate Event Plan",
    use_container_width=True
):

    # -----------------------------------------------------
    # INPUT VALIDATION
    # -----------------------------------------------------

    if not event_request.strip():

        st.warning(
            "⚠️ Please enter your event requirements."
        )

        st.stop()


    if mode == "Gemini AI Mode" and not api_key.strip():

        st.error(
            "❌ Please enter your Gemini API key."
        )

        st.stop()


    # -----------------------------------------------------
    # RUN AGENTS
    # -----------------------------------------------------

    try:

        with st.spinner(
            "🤖 Agents are planning your event..."
        ):

            # =============================================
            # CREATE AGENTS
            # =============================================

            if mode == "Demo Mode":

                (
                    requirement_agent,
                    budget_agent,
                    schedule_agent,
                    final_agent
                ) = create_demo_agents()

                demo_mode = True

            else:

                (
                    requirement_agent,
                    budget_agent,
                    schedule_agent,
                    final_agent
                ) = create_gemini_agents(
                    api_key
                )

                demo_mode = False


            # =============================================
            # BUILD LANGGRAPH
            # =============================================

            event_graph = build_graph(
                requirement_agent,
                budget_agent,
                schedule_agent,
                final_agent,
                demo_mode=demo_mode
            )


            # =============================================
            # RUN WORKFLOW
            # =============================================

            result = event_graph.invoke({
                "event_request": event_request
            })


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        st.success(
            "✅ Event plan generated successfully!"
        )


        # =================================================
        # FINAL EVENT PLAN
        # =================================================

        st.subheader(
            "📋 Final Event Plan"
        )

        st.markdown(
            result["final_plan"]
        )


        # =================================================
        # INDIVIDUAL AGENT OUTPUTS
        # =================================================

        with st.expander(
            "🔍 View Individual Agent Outputs"
        ):

            # ---------------------------------------------
            # Requirement Agent
            # ---------------------------------------------

            st.markdown(
                "### 1️⃣ Requirement Agent"
            )

            st.markdown(
                result["requirements"]
            )


            # ---------------------------------------------
            # Budget Agent
            # ---------------------------------------------

            st.markdown(
                "### 2️⃣ Budget Planning Agent"
            )

            st.markdown(
                result["budget_plan"]
            )


            # ---------------------------------------------
            # Schedule Agent
            # ---------------------------------------------

            st.markdown(
                "### 3️⃣ Schedule & Task Agent"
            )

            st.markdown(
                result["schedule_plan"]
            )


            # ---------------------------------------------
            # Final Agent
            # ---------------------------------------------

            st.markdown(
                "### 4️⃣ Final Planning Agent"
            )

            st.markdown(
                result["final_plan"]
            )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        st.error(
            "❌ Something went wrong while running the agents."
        )

        st.exception(e)