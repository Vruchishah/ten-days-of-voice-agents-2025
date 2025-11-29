# Day 08 Challenge: The Voice Game Master Agent 🎲

This project implements an interactive, voice-controlled **Game Master (GM) Agent** built using the **LiveKit Agents** framework. The agent, named **"Benimaru,"** guides a player through a fantasy tabletop RPG adventure. It utilizes a variety of tools to manage the game state, track character progress, and dynamically react to player actions, leveraging the power of **Gemini's function calling** for intelligent decision-making.

-----

## Features

This Game Master Agent brings the world of tabletop RPGs to life with the following core functionalities:

  * **Immersive Narrative:** The agent provides vivid, atmospheric scene descriptions and maintains a consistent tone ("Mysterious, adventurous, but fair").
  * **Dynamic World State:** A dedicated `WorldState` class manages crucial game elements: location, inventory, character health points (HP), status, and active quests.
  * **Function Calling for Game Mechanics:** The agent is equipped with several tools to enforce game rules:
      * `roll_dice`: Used to determine the outcome of risky actions (e.g., attacks, checks, saving throws).
      * `check_inventory`, `add_item`, `remove_item`: Tools for comprehensive inventory management.
      * `get_character_sheet`: Provides a summary of the player's current health and stats.
      * `save_game` / `load_game`: Enables game persistence using a local JSON file.
  * **High-Quality Voice Stack:** Integrates best-in-class plugins for real-time, fluid conversation:
      * **LLM:** Google's **Gemini-2.5-flash** for powerful reasoning and narrative generation.
      * **STT (Speech-to-Text):** Deepgram.
      * **TTS (Text-to-Speech):** Murf for a professional, styled voice.
  * **Robust Turn Detection:** Uses the LiveKit multilingual Voice Activity Detector (VAD) to accurately determine when the player has finished speaking, ensuring a smooth, natural conversational flow.
