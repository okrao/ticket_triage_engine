# Automated Ticket Triage Engine

## Overview
An automated agentic workflow designed to eliminate manual support ticket routing. This engine ingests incoming customer support requests, analyzes the natural language for intent and urgency, and autonomously routes them to the correct department or triggers an immediate automated resolution.

## Business Impact
* **Eliminates Manual Triage:** Frees up Tier-1 support staff from reading, tagging, and categorizing the daily inbound ticket queue.
* **Accelerates SLA Compliance:** Instantly identifies and routes high-urgency issues (e.g., billing errors, account lockouts) directly to specialized teams.

## Tech Stack
* **Language:** Python
* **Workflow Automation:** n8n
* **LLM & Inference:** Groq API
* **Orchestration:** LangChain
* **Data Validation:** Pydantic