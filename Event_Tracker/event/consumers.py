# import asyncio
# import base64
# import json
# import os
# import tempfile
# from datetime import datetime, timedelta
# from asgiref.sync import sync_to_async


# import ffmpeg
# import whisper
# from channels.generic.websocket import AsyncWebsocketConsumer
# from pydub import AudioSegment

# # Preload Whisper model
# model = whisper.load_model("base")
# model = model.float()  # Convert the model to float32

# audio_recordings_dir = 'audio_recordings'
# os.makedirs(audio_recordings_dir, exist_ok=True)

# class TranscribeConsumer(AsyncWebsocketConsumer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.transcription = ['']
#         self.audio_queue = asyncio.Queue()
#         self.audio_file_path = None

#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         if self.audio_file_path and os.path.exists(self.audio_file_path):
#             os.remove(self.audio_file_path)
#         pass

#     def is_audio_content_valid(self, audio_file_path):
#         try:
#             audio_segment = AudioSegment.from_wav(audio_file_path)
#             if len(audio_segment) < 1000 or audio_segment.rms < 200:
#                 return False
#             return True
#         except Exception as e:
#             print(f"Audio validation failed: {e}")
#             return False

#     async def receive(self, text_data=None, bytes_data=None):
#         if bytes_data:
#             await self.audio_queue.put(bytes_data)
#             print("Received audio chunk.")

#             if not hasattr(self, 'audio_processor_task') or self.audio_processor_task.done():
#                 self.audio_processor_task = asyncio.create_task(self.process_audio_queue())

#     async def process_audio_queue(self):
#         while not self.audio_queue.empty():
#             current_chunk = await self.audio_queue.get()
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             webm_file_path = os.path.join(audio_recordings_dir, f"audio_{timestamp}.webm")
#             wav_file_path = os.path.join(audio_recordings_dir, f"audio_{timestamp}.wav")

#             with open(webm_file_path, 'wb') as f:
#                 f.write(current_chunk)

#             # Run FFmpeg synchronously within the async method
#             process = await sync_to_async(ffmpeg.input(webm_file_path).output(wav_file_path, format='wav', y=True).run_async, thread_sensitive=True)()
#             await sync_to_async(process.wait)()  # Ensure FFmpeg finishes

#             if os.path.exists(webm_file_path):
#                 os.remove(webm_file_path)

#             if self.is_audio_content_valid(wav_file_path):
#                 await self.handle_transcription(wav_file_path)
#                 os.remove(wav_file_path)  # Clean up immediately after processing


#     async def handle_transcription(self, wav_file_path):
#         try:
#             # Load audio and generate Mel spectrogram
#             print("trying to handle_transcrip")
#             print("filepth:",wav_file_path)
#             audio = whisper.audio.load_audio(wav_file_path)
#             mel = whisper.log_mel_spectrogram(audio).to(model.device).float()

#             # Transcribe audio and immediately log the result
#             result = model.transcribe(mel)
#             print(f"Transcription result type: {type(result)}")  # Log the type of the result
#             print(f"Transcription result content: {result}")  # Log the content of the result

#             # Safely extract text and language if result is a dictionary
#             if isinstance(result, dict):
#                 text = result.get('text', '').strip()
#                 language = result.get('language', 'unknown')
#                 await self.send(text_data=json.dumps({
#                     'transcription': text,
#                     'language': language
#                 }))
#             else:
#                 print("Unexpected result format:", result)

#         except Exception as e:
#             # Log any error that occurs during the transcription process
#             print(f"Error during transcription: {e}")

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import whisper
from pydub import AudioSegment
from datetime import datetime, timedelta
import torch
import io
import os
import numpy as np

# Load and prepare the Whisper model for real-time processing
model = whisper.load_model("base").to("cuda" if torch.cuda.is_available() else "cpu").float()

class TranscribeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master_audio = AudioSegment.empty()
        self.phrase_time = None
        self.phrase_timeout = 5  # Timeout to consider the end of a phrase
        self.transcription = ['']
        self.process_task = None

    async def connect(self):
        await self.accept()
        print("WebSocket connection accepted")
        self.process_task = asyncio.create_task(self.periodic_buffer_check())

    async def disconnect(self, close_code):
        if self.process_task:
            self.process_task.cancel()
        self.master_audio = AudioSegment.empty()
        print("WebSocket connection closed with code:", close_code)

    async def receive(self, bytes_data=None):
        if bytes_data:
            print("Received bytes data of length:", len(bytes_data))
            try:
                webm_io = io.BytesIO(bytes_data)
                new_audio_segment = AudioSegment.from_file(webm_io, format="webm")
                self.master_audio += new_audio_segment
                print("Appended new audio segment, current master duration:", self.master_audio.duration_seconds)
            except Exception as e:
                print(f"Error decoding audio segment: {e}")

        now = datetime.utcnow()
        if self.phrase_time is None:
            self.phrase_time = now
            print("Initial phrase time set:", self.phrase_time)


    async def periodic_buffer_check(self):
        while True:
            await asyncio.sleep(1)  # Check every second
            now = datetime.utcnow()
            if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                print("Phrase timeout reached, processing buffer")
                await self.process_buffer()
                self.phrase_time = None

    async def process_buffer(self):
        if self.master_audio.duration_seconds == 0:
            print("Buffer is empty, nothing to process.")
            return

        print("Processing buffer of duration:", self.master_audio.duration_seconds, "seconds")

        # Create in-memory wav file
        wav_io = io.BytesIO()
        self.master_audio.export(wav_io, format="wav")
        wav_io.seek(0)
        print("Converted audio segment to WAV format in memory")

        try:
            print("Loading audio from in-memory WAV file")
            audio_np = np.frombuffer(wav_io.read(), dtype=np.int16).astype(np.float32) / 32768.0
            wav_io.seek(0)

            # Temporarily save the BytesIO to a file for Whisper processing
            temp_wav_path = "/tmp/temp_audio.wav"
            with open(temp_wav_path, 'wb') as temp_wav_file:
                temp_wav_file.write(wav_io.read())

            audio = whisper.audio.load_audio(temp_wav_path, sr=16000)
            mel = whisper.log_mel_spectrogram(audio).to(model.device).float()
            print(f"Generated Mel spectrogram of shape: {mel.shape}")

            # Transcribe audio and immediately log the result
            print("Starting transcription using Whisper model")
            result = model.transcribe(audio, fp16=torch.cuda.is_available())
            print(f"Transcription result type: {type(result)}")
            print(f"Transcription result content: {result}")

            if 'text' in result:
                text = result['text'].strip()
                if text:
                    print(f"Transcribed text: {text}")
                    if len(self.transcription) > 0 and not self.transcription[-1]:
                        self.transcription[-1] = text
                    else:
                        self.transcription.append(text)

                    await self.send(text_data=json.dumps({
                        'transcription': text,
                        'language': result.get('language', 'unknown')
                    }))

            # Remove the temporary file
            os.remove(temp_wav_path)
        except Exception as e:
            print(f"Error during transcription: {e}")
            await self.send(text_data=json.dumps({'error': str(e)}))
        print("Finished processing buffer")
