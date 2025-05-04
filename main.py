import asyncio
import os
import requests
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli, RoomInputOptions
from livekit.plugins import silero, deepgram

load_dotenv()

class MyAssistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a simple voice-to-text agent. Just transcribe what you hear.")

    async def on_transcription(self, ctx, transcript: str):
        print("🗣️ Transcribed:", transcript)
        try:
            response = requests.post(
                "http://localhost:5000/call",
                json={"question": transcript, "caller_info": "LiveKit Voice"}
            )
            if response.status_code == 200:
                data = response.json()
                print("📞 API Response:", data)
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception during API call: {e}")

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=None,
        tts=None,
    )

    await session.start(
        room=ctx.room,
        agent=MyAssistant(),
        room_input_options=RoomInputOptions(),
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
