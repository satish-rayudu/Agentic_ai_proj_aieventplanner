from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# DEMO MODE AGENTS
# =========================================================

def create_demo_agents():

    # -----------------------------------------------------
    # 1. REQUIREMENT AGENT
    # -----------------------------------------------------

    def requirement_agent(event_request):

        return """
Event Type: Birthday Party
Date: 20 December 2026
Location: Hyderabad
Guests: 30
Budget: ₹25,000
Food: Vegetarian
Decoration: Simple
"""


    # -----------------------------------------------------
    # 2. BUDGET AGENT
    # -----------------------------------------------------

    def budget_agent(requirements):

        return """
Food: ₹12,000
Decoration: ₹4,000
Venue: ₹5,000
Entertainment: ₹2,000
Miscellaneous: ₹2,000

Total: ₹25,000
Status: Within budget
"""


    # -----------------------------------------------------
    # 3. SCHEDULE AGENT
    # -----------------------------------------------------

    def schedule_agent(requirements):

        return """
2 weeks before:
- Confirm venue
- Confirm catering

1 week before:
- Finalize decoration
- Finalize guest list

2 days before:
- Confirm all arrangements

Event day:
- Venue setup
- Food arrangement
- Guest reception
- Birthday celebration
"""


    # -----------------------------------------------------
    # 4. FINAL AGENT
    # -----------------------------------------------------

    def final_agent(
        requirements,
        budget_plan,
        schedule_plan
    ):

        return f"""
# COMPLETE EVENT PLAN

## 1. EVENT DETAILS

{requirements}

## 2. BUDGET BREAKDOWN

{budget_plan}

## 3. PREPARATION TIMELINE

{schedule_plan}

## 4. EVENT-DAY SCHEDULE

- Venue setup
- Food arrangement
- Guest reception
- Main event
- Final cleanup

## 5. TASK CHECKLIST

- Confirm venue
- Confirm catering
- Finalize decoration
- Finalize guest list
- Confirm all arrangements
- Prepare event-day setup

## 6. IMPORTANT RECOMMENDATIONS

Keep the event within the ₹25,000 budget and maintain a small contingency amount.
"""

    return (
        requirement_agent,
        budget_agent,
        schedule_agent,
        final_agent
    )


# =========================================================
# GEMINI MODE AGENTS
# =========================================================

def create_gemini_agents(api_key):

    # -----------------------------------------------------
    # GEMINI MODEL
    # -----------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.2,
        max_output_tokens=2000,
        max_retries=0
    )


    # =====================================================
    # 1. REQUIREMENT AGENT
    # =====================================================

    requirement_prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            """You are an Event Requirement Agent.

Your job is to extract the event requirements from
the user's request.

Extract:

- Event type
- Date
- Location
- Number of guests
- Budget
- Food preferences
- Decoration preferences
- Other requirements

IMPORTANT RULES:

1. Do not invent information.
2. If the user provides the number of guests, preserve it exactly.
3. If the user provides a budget, preserve it exactly.
4. Clearly write the number of guests.
5. Clearly write the budget.
6. Use simple bullet points.

Return the information in this format:

Event Type:
Date:
Location:
Number of Guests:
Budget:
Food Preferences:
Decoration Preferences:
Other Requirements:
"""
        ),

        (
            "human",

            "{event_request}"
        )

    ])

    requirement_agent = requirement_prompt | llm


    # =====================================================
    # 2. BUDGET PLANNING AGENT
    # =====================================================

    budget_prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            """You are a Budget Planning Agent.

Create a practical budget plan based on the
event requirements.

Consider:

1. Food
2. Decoration
3. Venue
4. Entertainment
5. Photography if relevant
6. Music if relevant
7. Miscellaneous

Then provide:

- Individual expenses
- Estimated total
- Available budget
- Remaining amount
- Budget status

IMPORTANT:

Use the exact guest count and budget provided
by the Requirement Agent.

Show calculations clearly.

If the budget is insufficient, suggest practical
ways to reduce costs.
"""
        ),

        (
            "human",

            """EVENT REQUIREMENTS:

{requirements}

Create the budget plan."""
        )

    ])

    budget_agent = budget_prompt | llm


    # =====================================================
    # 3. SCHEDULE & TASK AGENT
    # =====================================================

    schedule_prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            """You are a Schedule and Task Agent.

Create a practical event preparation timeline.

Use the event date and number of guests provided
in the requirements.

Include:

1. Several weeks before the event
2. One week before
3. A few days before
4. One day before
5. Event-day schedule
6. Task checklist

IMPORTANT:

Do not invent a different event date.

Make the schedule realistic and easy to follow.
"""
        ),

        (
            "human",

            """EVENT REQUIREMENTS:

{requirements}

Create the schedule and task plan."""
        )

    ])

    schedule_agent = schedule_prompt | llm


    # =====================================================
    # 4. FINAL PLANNING AGENT
    # =====================================================

    final_prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            """You are the Final Event Planning Agent.

Create a COMPLETE and DETAILED event plan by
combining the outputs from:

1. Event Requirement Agent
2. Budget Planning Agent
3. Schedule & Task Agent

IMPORTANT:

You MUST preserve all important information from
the Event Requirement Agent.

The Event Details section MUST contain:

- Event Type
- Date
- Location
- Number of Guests
- Budget
- Food Preferences
- Decoration Preferences
- Other Requirements

CRITICAL RULES:

1. Copy the exact number of guests from EVENT REQUIREMENTS.
2. NEVER leave Number of Guests blank if a number exists.
3. Copy the exact budget from EVENT REQUIREMENTS.
4. NEVER leave Budget blank if a budget exists.
5. Do not invent important information.
6. Do not change the event date.
7. Do not change the guest count.
8. Do not change the user's budget.
9. Do not stop after an introduction.
10. Generate the COMPLETE plan.

Your response MUST use exactly this structure:

# COMPLETE EVENT PLAN

## 1. EVENT DETAILS

- Event Type:
- Date:
- Location:
- Number of Guests:
- Budget:
- Food Preferences:
- Decoration Preferences:
- Other Requirements:

## 2. BUDGET BREAKDOWN

Show:

- Food
- Decoration
- Venue
- Entertainment
- Photography
- Music
- Miscellaneous
- Estimated Total
- Available Budget
- Remaining Amount
- Budget Status

Only include categories that are relevant.

## 3. PREPARATION TIMELINE

Include:

- Several weeks before
- One week before
- Few days before
- One day before
- Final checks

## 4. EVENT-DAY SCHEDULE

Give a practical sequence of activities
for the event day.

## 5. TASK CHECKLIST

Provide a clear checklist of important tasks.

## 6. IMPORTANT RECOMMENDATIONS

Provide practical recommendations based on:

- Event type
- Guest count
- Budget
- Location
- Food
- Decoration
- Other requirements

IMPORTANT:

The response must be complete.

Do NOT write:

"Guests:"

without a number when the guest count
exists in EVENT REQUIREMENTS.

Do NOT write:

"Budget:"

without an amount when the budget
exists in EVENT REQUIREMENTS.
"""
        ),

        (
            "human",

            """EVENT REQUIREMENTS:

{requirements}


BUDGET PLAN:

{budget_plan}


SCHEDULE & TASK PLAN:

{schedule_plan}


Now generate the COMPLETE EVENT PLAN.

Make sure the Number of Guests and Budget
are explicitly included in EVENT DETAILS."""
        )

    ])

    final_agent = final_prompt | llm


    # =====================================================
    # RETURN ALL FOUR AGENTS
    # =====================================================

    return (
        requirement_agent,
        budget_agent,
        schedule_agent,
        final_agent
    )