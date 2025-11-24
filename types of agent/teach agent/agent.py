import logging
import json
import os

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


COURSE_CONTENT = [
  {
    "id": "variables",
    "title": "Variables",
    "summary": "Variables store values so you can reuse them later, much like a labeled box you put information into. For example, if you store the number 10 in a variable named 'age', you can refer to that value simply by saying 'age'. This is essential for writing code that can adapt and remember information.",
    "sample_question": "What is a variable and why is it useful? Try to teach it back to me in your own words."
  },
  {
    "id": "loops",
    "title": "Loops",
    "summary": "Loops let you repeat an action multiple times without having to write the same code over and over. Think of it like setting an alarm to go off every morning at 7 a.m.—the loop keeps repeating the action. The two main types are 'for' loops, which run a set number of times, and 'while' loops, which run as long as a certain condition is true.",
    "sample_question": "Explain the difference between a for loop and a while loop. I want you to teach this concept back to me."
  },
  {
    "id": "function",
    "title": "Functions",
    "summary": "Functions are blocks of organized, reusable code that perform a single, related action. They allow you to modularize your code, making it easier to read, test, and debug. When you need to perform an action multiple times, you simply call the function instead of writing the code repeatedly.",
    "sample_question": "Explain how functions help with code organization and reusability."
  },
  {
    "id": "if_else",
    "title": "If-Else Statements",
    "summary": "If-Else statements are the fundamental way to control the flow of a program. They allow your code to make decisions based on whether a condition is true or false. If the condition is true, the code in the 'if' block runs; otherwise, the code in the 'else' block runs.",
    "sample_question": "Describe a real-world scenario where an If-Else statement would be necessary in a program."
  },
  {
    "id": "data_types",
    "title": "Data Types",
    "summary": "Data types define the kind of value a variable can hold, such as numbers, text, or boolean (true/false) values. Common types include integers, floats, strings, and booleans. Using the correct data type is crucial for performing accurate operations and managing memory efficiently.",
    "sample_question": "What is a Data Type and what's the difference between an integer and a string?"
  },
  {
    "id": "operators",
    "title": "Operators",
    "summary": "Operators are special symbols that perform operations on variables and values. They are categorized into arithmetic (like +, -), comparison (like ==, >), and logical (like AND, OR) operators. They are the tools you use to manipulate data and create conditions in your code.",
    "sample_question": "Explain the difference between the assignment operator (=) and the comparison operator (==)."
  },
  {
    "id": "oop",
    "title": "OOP (Object-Oriented Programming)",
    "summary": "Object-Oriented Programming is a paradigm based on the concept of 'objects,' which can contain data and code. The main principles are encapsulation, inheritance, and polymorphism. It helps manage complexity by modeling real-world entities and their interactions in code.",
    "sample_question": "Summarize the core principles of Object-Oriented Programming (OOP)."
  }
]

VOICE_MAP = {
    "learn": {"id": "en-US-matthew", "name": "Matthew"},
    "quiz": {"id": "en-US-alicia", "name": "Alicia"},
    "teach_back": {"id": "en-US-ken", "name": "Ken"},
}

DEFAULT_VOICE = VOICE_MAP["learn"]["id"]

class Tutor(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the **Teach-the-Tutor: Active Recall Coach**. Your job is to help the user learn programming concepts.
            
            **Available Concepts:** The IDs you MUST use for the `concept` argument are: `variables`, `loops`, `function`, `if_else`, `data_types`, `operators`, `oop`.
            **Available Modes:** learn (explains concept), quiz (asks question), teach_back (user explains concept).
            
            **Initial State & Greeting:**
            1.  Start by greeting the user and asking which learning mode they would like to start with: 'learn', 'quiz', or 'teach_back'.
            2.  Your initial voice is **Matthew**.
            
            **Core Task & Tool Use:**
            -   The user can switch between modes or concepts at any time.
            -   If the user requests a mode or concept change (e.g., 'switch to quiz', 'start learning data types'), you **MUST** call the `set_learning_mode` tool immediately. 
            -   When calling the tool, if the user mentions "functions" you must use the ID `function`. If they mention "data types", use `data_types`.
            
            **Important Voice Rule:** The voice is automatically changed by the tool before your response is spoken. You do not need to include any voice changing tags in your final output.
            
            **Conversation Rules:**
            - In **quiz** and **teach_back** modes, when the user provides an answer, give a basic, qualitative, and encouraging feedback response.
            - Your responses must be concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            """,
        )

    @function_tool
    async def set_learning_mode(self, context: RunContext, mode: str, concept: str = "variables"):
        """
        Use this tool to change the learning mode and the concept.
        This must be called immediately when the user requests a mode change (learn, quiz, teach_back, or changes the concept).

        Args:
            mode: The desired learning mode. Must be one of 'learn', 'quiz', or 'teach_back'.
            concept: The concept to focus on. Must be one of 'variables', 'loops', 'function', 'if_else', 'data_types', 'operators', or 'oop'. Defaults to 'variables'.
        """
        mode = mode.lower()
        concept_input = concept 

        if mode not in VOICE_MAP:
            return f"Error: The mode '{mode}' is not supported. Please choose 'learn', 'quiz', or 'teach_back'."
        
        
        normalized_input = concept_input.lower().replace(' ', '_').replace('-', '_')
        
        possible_id = normalized_input
        if normalized_input.endswith('s') and normalized_input not in ['variables', 'loops', 'operators', 'data_types']:
             possible_id = normalized_input[:-1]
             
        content = next((c for c in COURSE_CONTENT if c["id"] == possible_id), None)
        
        if not content:
            content = next((c for c in COURSE_CONTENT if c["title"].lower() == concept_input.lower()), None)
            
        if not content:
            content = COURSE_CONTENT[0] 
            concept_id = content["id"]
            logger.warning(f"Failed to match user concept '{concept_input}' or normalized '{possible_id}'. Defaulting to {content['title']}")
        else:
            concept_id = content["id"]


        voice_info = VOICE_MAP[mode]
        voice_id = voice_info["id"]
        voice_name = voice_info["name"]

        # 1. Change the TTS voice dynamically
        try:
             context.agent_session.tts.update_options(voice=voice_id)
             logger.info(f"Successfully switched TTS voice to {voice_id} for mode {mode} for concept {concept_id}")
        except Exception as e:
             logger.warning(f"Failed to change TTS voice via update_options: {e}. Relying on LLM instruction.")
             pass
        
        # 2. Build the LLM's response based on the mode
        response_text = ""
        if mode == "learn":
            response_text = f"I am now speaking as the **Teacher ({voice_name})**. The concept is {content['title']}. Here is the summary: {content['summary']}"
        elif mode == "quiz":
            response_text = f"I am now speaking as the **Quizmaster ({voice_name})**. The concept is {content['title']}. Get ready for your question: {content['sample_question']}"
        elif mode == "teach_back":
            response_text = f"I am now speaking as the **Tutor ({voice_name})**. The concept is {content['title']}. It's your turn to teach me! The prompt is: {content['sample_question']}"
            
        # 3. Return only the response text, preventing the LLM from generating an error message.
        return response_text


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf's default Matthew voice initially
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Start with the default voice for the greeting (Matthew)
        tts=murf.TTS(
                voice=DEFAULT_VOICE, 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    # Metrics collection, to measure pipeline performance
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Tutor(), # Use the updated Tutor agent class
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))