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
# AGENT MODE
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
# GEMINI API KEY
# =========================================================

api_key = ""


if mode == "Gemini AI Mode":

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

    except Exception:

        st.error(
            "❌ GEMINI_API_KEY is not configured in Streamlit Secrets."
        )

        st.info(
            "Go to Streamlit Cloud → App Settings → Secrets "
            "and add your Gemini API key."
        )

        st.stop()


# =========================================================
# EVENT INPUT
# =========================================================

event_request = st.text_area(
    "📝 Enter your event requirements",
    height=180,
    placeholder="""Example:

Plan a wedding for 100 people in Vijayawada
on 10 February 2027 with a budget of ₹2,00,000.

I need catering, decoration, photography
and music."""
)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button(
    "🚀 Generate Event Plan",
    use_container_width=True
):

    # -----------------------------------------------------
    # VALIDATE INPUT
    # -----------------------------------------------------

    if not event_request.strip():

        st.warning(
            "⚠️ Please enter your event requirements."
        )

        st.stop()


    # =====================================================
    # RUN AGENTS
    # =====================================================

    try:

        with st.spinner(
            "🤖 Agents are planning your event..."
        ):

            # -------------------------------------------------
            # DEMO MODE
            # -------------------------------------------------

            if mode == "Demo Mode":

                (
                    requirement_agent,
                    budget_agent,
                    schedule_agent,
                    final_agent
                ) = create_demo_agents()

                demo_mode = True


            # -------------------------------------------------
            # GEMINI MODE
            # -------------------------------------------------

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


            # -------------------------------------------------
            # BUILD LANGGRAPH
            # -------------------------------------------------

            event_graph = build_graph(
                requirement_agent,
                budget_agent,
                schedule_agent,
                final_agent,
                demo_mode=demo_mode
            )


            # -------------------------------------------------
            # RUN GRAPH
            # -------------------------------------------------

            result = event_graph.invoke({
                "event_request": event_request
            })


        # =====================================================
        # SUCCESS MESSAGE
        # =====================================================

        st.success(
            "✅ Event plan generated successfully!"
        )


        # =====================================================
        # FINAL EVENT PLAN
        # =====================================================

        st.subheader(
            "📋 Final Event Plan"
        )

        st.markdown(
            result["final_plan"]
        )


        # =====================================================
        # INDIVIDUAL AGENT OUTPUTS
        # =====================================================

        with st.expander(
            "🔍 View Individual Agent Outputs"
        ):

            # -------------------------------------------------
            # REQUIREMENT AGENT
            # -------------------------------------------------

            st.markdown(
                "### 1️⃣ Requirement Agent"
            )

            st.markdown(
                result["requirements"]
            )


            # -------------------------------------------------
            # BUDGET AGENT
            # -------------------------------------------------

            st.markdown(
                "### 2️⃣ Budget Planning Agent"
            )

            st.markdown(
                result["budget_plan"]
            )


            # -------------------------------------------------
            # SCHEDULE AGENT
            # -------------------------------------------------

            st.markdown(
                "### 3️⃣ Schedule & Task Agent"
            )

            st.markdown(
                result["schedule_plan"]
            )


            # -------------------------------------------------
            # FINAL AGENT
            # -------------------------------------------------

            st.markdown(
                "### 4️⃣ Final Planning Agent"
            )

            st.markdown(
                result["final_plan"]
            )


    # =========================================================
    # ERROR HANDLING
    # =========================================================

    except Exception as e:

        st.error(
            "❌ Something went wrong while running the agents."
        )

        st.exception(e)
