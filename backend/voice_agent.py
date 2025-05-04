import os
import asyncio
from dotenv import load_dotenv
from livekit_agents.transcriber import Transcriber
from livekit.plugins import silero
from livekit import RoomOptions, create_room, TrackSubscribeOptions
import requests

load_dotenv()

async def main():
    transcriber = silero.SileroTranscriber()
    
    room = await create_room(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        name="voice-transcriber",
        options=RoomOptions(
            auto_subscribe=True
        )
    )

    print("[LiveKit] Connected to room.")

    async for track in transcriber.transcribe_room(room):
        if track.transcription:
            print(f"[Voice Agent] Transcribed: {track.transcription}")
            # Optionally: Send to your Flask API
            try:
                requests.post(
                    "http://localhost:5000/call",
                    json={
                        "question": track.transcription,
                        "caller_info": "LiveCall#1"
                    }
                )
            except Exception as e:
                print(f"Error posting to API: {e}")

if __name__ == "__main__":
    asyncio.run(main())
