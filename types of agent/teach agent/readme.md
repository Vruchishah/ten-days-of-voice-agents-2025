# 🤖 Day 4: Teach-the-Tutor: Active Recall Coach

[![Challenge Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)](https://github.com/[YOUR_GITHUB_USER]/[YOUR_REPO_NAME])
[![Challenge](https://img.shields.io/badge/Murf%20AI-Voice%20Agent%20Challenge-blue.svg)](https://murf.ai/)

This project solves Day 4 of the **Murf AI Voice Agent Challenge**, focusing on the development of a conversational AI coach designed around the **Active Recall** principle. The agent leverages the **Murf Falcon TTS API** to dynamically switch between three distinct personas, providing a highly engaging and context-aware learning experience.

---

## ✨ Core Functionality: Three Learning Modes

The agent implements a "Teach-the-Tutor" workflow with seamless, function-driven voice handoffs, ensuring a clear role for each stage of the learning process.

| Mode | Purpose | Voice ID | Murf Persona |
| :--- | :--- | :--- | :--- |
| **`learn`** | Delivers the concept summary. | `en-US-matthew` | The Teacher |
| **`quiz`** | Asks a targeted question for recall. | `en-US-alicia` | The Quizmaster |
| **`teach_back`** | Prompts the user to explain the concept. | `en-US-ken` | The Tutor |

---

## 🛠️ Implementation & Technical Details

All required functionality, including tool definition, mode switching, and content storage, is contained within the agent's core file.

### 1. Centralized Course Content

To meet the requirement of providing content via a "small content file," the material was hardcoded into a global list of dictionaries within the agent file: `backend/src/agent.py`.

The supported concepts include:

variables, loops, function, if_else, data_types, operators, oop

### 2. The `set_learning_mode` Function Tool

The core logic is encapsulated in a `@function_tool` that the Large Language Model (LLM) calls upon user request for a mode or concept change.

| Feature | Implementation Detail |
| :--- | :--- |
| **Voice Handoff** | Uses `context.agent_session.tts.update_options(voice=voice_id)` to programmatically change the Murf Falcon voice before the response is synthesized. |
| **Robust Matching** | Includes logic to normalize user input (e.g., handling "functions" as the ID `function`) to prevent erroneous concept fallback. |
| **LLM Instruction** | Agent instructions explicitly guide the LLM (Gemini) to pass the correct concept IDs to the tool. |

---

## 🚀 Getting Started

To run this agent locally, follow the standard setup process for the challenge:

1.  **Code Check:** Ensure your `backend/src/agent.py` contains the final, corrected code from the challenge resolution.
2.  **Environment Setup:** Update the `.env.local` file with valid keys for **LIVEKIT**, **MURF**, **DEEPGRAM**, and **GOOGLE** services.
3.  **Execution:**
    * Navigate to the backend directory (`cd backend`).
    * Run the agent worker (e.g., using `task dev` or your preferred method).
4.  **Frontend:** Start the frontend application and connect to the running agent to begin the learning session.
