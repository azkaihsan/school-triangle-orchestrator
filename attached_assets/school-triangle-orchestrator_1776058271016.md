# Project Summary: School Triangle Orchestrator

## 1. Project Overview
[cite_start]**Project Name:** School Triangle Orchestrator [cite: 8, 11]  
[cite_start]**Author:** Azka Ihsan Nurrahman [cite: 7]  
[cite_start]**Event:** Prototype Submission for Google Cloud Gen AI Academy APAC Edition [cite: 1, 2, 3]  

[cite_start]The **School Triangle Orchestrator** is designed for Pastilulus to act as an "intelligence layer" connecting the three primary stakeholders in education: students, teachers, and parents[cite: 12, 24]. [cite_start]It is a multi-agent AI system that coordinates learning follow-ups and synchronizes educational efforts across the board[cite: 8].

---

## 2. Problem Statement
[cite_start]Primary education currently suffers from a broken "school triangle"[cite: 23]. Specifically:
* [cite_start]**Students** often have short attention spans and shallow understanding[cite: 23].
* [cite_start]**Teachers** struggle to personalize learning effectively at scale[cite: 23].
* [cite_start]**Parents** lack clear, real-time visibility into their child's educational progress[cite: 23].

[cite_start]Existing solutions generally focus on fragmented tools like video lessons, question banks, or basic reminders, which fail to connect the gaps between these three critical stakeholders[cite: 46, 47].

---

## 3. Solution Statement
[cite_start]To solve the broken school triangle, Pastilulus introduces the **School Triangle Orchestrator**, a multi-agent AI system built to act as an intelligence layer rather than replacing traditional schooling[cite: 24]. 

[cite_start]**Important Developer Note:** This solution is strictly designed to be deployed as an **API-based system**[cite: 89]. [cite_start]Instead of a single chatbot answering queries, the primary orchestrator receives external triggers (e.g., "student is struggling in fractions") and coordinates specialized sub-agents to execute tasks[cite: 13, 49]. [cite_start]The Orchestrator tracks execution across all sub-agents and returns one unified response via API[cite: 38]. 

[cite_start]The system utilizes Model Context Protocol (MCP) to seamlessly connect to external tools like calendars and task managers, and relies on an AlloyDB structured database to manage student profiles, interventions, and logs[cite: 26, 27].

---

## 4. Unique Selling Proposition (USP)
* [cite_start]**360° Value Creation:** Students receive adaptive support, teachers achieve personalized instruction without extra manual coordination burden, and parents gain holistic visibility into their child's progress[cite: 57].
* [cite_start]**Actionable & Operational Workflow:** The system goes beyond basic analysis; it operationalizes insights by converting them into tangible tasks, schedules, assignments, and communications through integrated tools[cite: 58].
* [cite_start]**High Stickiness Ecosystem:** By serving all three stakeholders simultaneously, the platform creates a strong ecosystem effect, leading to higher adoption potential[cite: 59].
* [cite_start]**Deep Contextual Triggers:** Unlike standard edtech solutions, this system uses deep learning context (e.g., logic deduction analysis, curriculum mapping) to trigger meaningful interventions, not just simple reminders[cite: 48].

---

## 5. Features
[cite_start]The platform operates via a Primary Orchestrator Agent that delegates tasks to four highly specialized sub-agents[cite: 25]:
* [cite_start]**Student Insight Agent:** Analyzes student misconceptions and mastery gaps utilizing structured learning data[cite: 64].
* [cite_start]**Teacher Action Agent:** Generates targeted intervention tasks and creates necessary curriculum adjustments[cite: 65].
* [cite_start]**Parent Communication Agent:** Prepares holistic progress updates and formulates practical, actionable suggestions for parents[cite: 66].
* [cite_start]**Scheduling Agent:** Uses Model Context Protocol (MCP) to arrange reminders, study sessions, and parent-teacher follow-ups via calendar and task tools[cite: 66].

---

## 6. Core Workflow & Process Flow
[cite_start]The execution flow for the multi-agent system follows a structured pipeline[cite: 33]:
1. [cite_start]**Data Retrieval:** Student learning data is stored in and retrieved from the system's database[cite: 34].
2. [cite_start]**Analysis:** The Student Insight Agent detects specific misconceptions and mastery gaps using adaptive logic[cite: 35].
3. [cite_start]**Intervention Generation:** Based on the insights, the Teacher Agent generates targeted assignments and intervention plans[cite: 35].
4. [cite_start]**Communication Structuring:** The Parent Agent formulates holistic progress summaries alongside practical at-home suggestions[cite: 37].
5. [cite_start]**Operational Scheduling:** The Scheduling Agent connects to external tools (via MCP) to officially create the required study tasks, meetings, or reminders[cite: 37].
6. [cite_start]**Unified Output:** Finally, the Primary Orchestrator tracks the successful execution across all sub-agents and delivers a single, unified response via the API[cite: 38].

---

## 7. Architecture Explanation
The architecture relies heavily on Google Cloud services combined with open-source frameworks. 
* [cite_start]**Eventing / Triggering:** Workflow steps (e.g., a student data update triggering the insight agent, which notifies a parent) are decoupled using an event-driven architecture[cite: 128]. [cite_start]This separates synchronous API calls from asynchronous background tasks like report generation[cite: 130].
* [cite_start]**Application Runtime:** The entire multi-agent backend is containerized and deployed on an auto-scaling runtime environment to handle school-hour traffic spikes efficiently[cite: 90, 91].
* [cite_start]**Multi-Agent Logic:** The reasoning layer coordinates multiple agents using a lightweight framework capable of exposing endpoints for tool callbacks and orchestrator execution[cite: 99, 100]. [cite_start]This layer handles the reasoning to interpret structured data and generate contextual outputs[cite: 86].
* [cite_start]**Tool Integration:** To execute operations outside the application, the agents use a standardized protocol (MCP) to call external APIs (calendars, mail, documents)[cite: 113, 114].
* [cite_start]**Data Storage:** A robust, relational database handles structured data like student profiles, curriculum mapping, and operational logs, ensuring data consistency and auditability[cite: 104, 106].

---

## 8. Tech Stack and Google Services Used
* [cite_start]**Core AI Model:** **Gemini** – Provides production-ready managed inference for the orchestrator and sub-agent reasoning layer, allowing it to interpret data and generate complex outputs[cite: 85, 86, 87].
* [cite_start]**Application Runtime:** **Google Cloud Run** – Hosts the containerized API, sub-agent endpoints, webhook handlers, and MCP connectors with automatic scaling and request-based billing[cite: 88, 90, 91].
* [cite_start]**Multi-Agent Backend:** **Python + FastAPI** – A lightweight, async-friendly framework ideal for building the orchestrator and sub-agent endpoints[cite: 98, 99, 100].
* [cite_start]**Structured Data Layer:** **AlloyDB for PostgreSQL** – A production-grade relational database for storing student profiles, assignments, parent notifications, and logs[cite: 102, 104, 105].
* [cite_start]**Tool Integration Protocol:** **Model Context Protocol (MCP)** – Standardizes how agents call external tools and retrieve information, keeping the system modular and extensible[cite: 111, 113, 114].
* [cite_start]**Eventing / Workflow Triggering:** **Google Cloud Pub/Sub** – Decouples workflow steps and improves resilience by separating synchronous API calls from asynchronous background processes[cite: 127, 128, 130].
* [cite_start]**Scheduling & Productivity Tools:** * **Google Calendar API:** Schedules parent-teacher follow-ups and intervention sessions[cite: 116].
    * [cite_start]**Gmail API:** Sends teacher alerts and parent summaries[cite: 116].
    * [cite_start]**Google Tasks API:** Creates actionable follow-up tasks for assignments and interventions[cite: 117].
* [cite_start]**Document & Collaboration Tools:** **Google Docs API / Google Drive API** – Used to generate, store, and collaboratively share Smart Evaluation Reports, intervention notes, and parent summaries[cite: 123, 124, 125, 126].