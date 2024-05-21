import openai

import google.cloud.texttospeech as tts
import os
from pydub import AudioSegment
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key=os.getenv("OPENAI_API_KEY")

def text_to_wav(voice_name: str, text: str, filename: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')


def saveAllAudio(dir: str, MAXLENGTH: int):
    final_audio = AudioSegment.from_file(os.path.join(dir,"AI-0.wav"), format="wav") + AudioSegment.from_file(os.path.join(dir,"User-0.wav"), format="wav")
    for i in range(1,MAXLENGTH):
        final_audio += AudioSegment.from_file(os.path.join(dir,f"AI-{i}.wav"), format="wav") + AudioSegment.from_file(os.path.join(dir,f"User-{i}.wav"), format="wav")
    final_audio.export(f"{dir}/finalAudio.wav", format = "wav")

def saveAllText(dir: str, messages: list):
    with open('data.json', 'w') as file:
        json.dump(messages, file)