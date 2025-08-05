import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import google, noise_cancellation

from system_control import control_screen

from jarvis_prompts import BEHAVIOR_PROMPT, REPLY_PROMPT

# Load environment variables
load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=BEHAVIOR_PROMPT,
            tools=[
                control_screen  # Unified screen vision and control logic
            ],
        )



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(voice="Charon")
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await session.generate_reply(instructions=REPLY_PROMPT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
