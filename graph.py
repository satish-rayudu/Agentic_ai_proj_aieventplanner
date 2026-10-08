from langgraph.graph import StateGraph, START, END
from state import EventState


def build_graph(
    requirement_agent,
    budget_agent,
    schedule_agent,
    final_agent,
    demo_mode=False
):

    # =====================================================
    # REQUIREMENT AGENT NODE
    # =====================================================

    def requirement_node(state: EventState):

        if demo_mode:
            result = requirement_agent(
                state["event_request"]
            )
        else:
            response = requirement_agent.invoke({
                "event_request": state["event_request"]
            })

            result = response.text

        return {
            "requirements": result
        }


    # =====================================================
    # BUDGET AGENT NODE
    # =====================================================

    def budget_node(state: EventState):

        if demo_mode:
            result = budget_agent(
                state["requirements"]
            )
        else:
            response = budget_agent.invoke({
                "requirements": state["requirements"]
            })

            result = response.text

        return {
            "budget_plan": result
        }


    # =====================================================
    # SCHEDULE AGENT NODE
    # =====================================================

    def schedule_node(state: EventState):

        if demo_mode:
            result = schedule_agent(
                state["requirements"]
            )
        else:
            response = schedule_agent.invoke({
                "requirements": state["requirements"]
            })

            result = response.text

        return {
            "schedule_plan": result
        }


    # =====================================================
    # FINAL PLANNING AGENT NODE
    # =====================================================

    def final_node(state: EventState):

        if demo_mode:
            result = final_agent(
                state["requirements"],
                state["budget_plan"],
                state["schedule_plan"]
            )
        else:
            response = final_agent.invoke({
                "requirements": state["requirements"],
                "budget_plan": state["budget_plan"],
                "schedule_plan": state["schedule_plan"]
            })

            result = response.text

        return {
            "final_plan": result
        }


    # =====================================================
    # CREATE LANGGRAPH
    # =====================================================

    workflow = StateGraph(EventState)


    # =====================================================
    # ADD AGENT NODES
    # =====================================================

    workflow.add_node(
        "requirements",
        requirement_node
    )

    workflow.add_node(
        "budget",
        budget_node
    )

    workflow.add_node(
        "schedule",
        schedule_node
    )

    workflow.add_node(
        "final",
        final_node
    )


    # =====================================================
    # AGENT FLOW
    # =====================================================

    workflow.add_edge(
        START,
        "requirements"
    )

    workflow.add_edge(
        "requirements",
        "budget"
    )

    workflow.add_edge(
        "requirements",
        "schedule"
    )

    workflow.add_edge(
        "budget",
        "final"
    )

    workflow.add_edge(
        "schedule",
        "final"
    )

    workflow.add_edge(
        "final",
        END
    )


    # =====================================================
    # COMPILE
    # =====================================================

    return workflow.compile()