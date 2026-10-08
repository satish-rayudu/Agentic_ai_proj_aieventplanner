# 📅 Event Planning Agent

A **Multi-Agent AI Event Planning System** built using **Python, LangChain, LangGraph, Gemini, Pydantic, and Streamlit**.

The application accepts natural-language event requirements and generates a complete event plan including requirements, budget, schedule, tasks, and recommendations.

---

## 🎯 Problem Statement

Event planning involves multiple activities such as understanding requirements, estimating expenses, preparing schedules, organizing tasks, and coordinating everything into one final plan.

This project uses a **Multi-Agent AI architecture** to automate these activities and generate a structured event plan from a simple natural-language request.

---

## 🎯 Objectives

- Extract event requirements from natural language.
- Identify event type, date, location, guests, and budget.
- Understand food and decoration preferences.
- Create a practical budget.
- Check whether the estimated cost fits the available budget.
- Generate preparation timelines.
- Create an event-day schedule.
- Generate a task checklist.
- Combine outputs from multiple specialized agents.
- Provide practical recommendations.
- Provide an interactive Streamlit interface.

---

## 🧠 Architecture

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │ Streamlit UI│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  LangGraph  │
                    └──────┬──────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Requirement Agent  │
                 └─────────┬──────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
        ┌─────────────────┐  ┌─────────────────┐
        │  Budget Agent   │  │ Schedule Agent  │
        └────────┬────────┘  └────────┬────────┘
                 │                    │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │ Final Planning     │
                 │ Agent              │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Complete Event Plan│
                 └────────────────────┘
