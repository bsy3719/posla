from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

class MicrophoneStream(object):
    def __init__(self):
        self.rate = 16000
        self.chunk = int(self.rate / 10)
        self.language_code = 'ko-KR'

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=""

        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                              sample_rate_hertz=self.rate, language_code=self.language_code)
        self.streaming_config = types.StreamingRecognitionConfig(config=self.config,interim_results=True) 

        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16, channels=1, rate=self.rate, input=True,
            frames_per_buffer=self.chunk, stream_callback=self._fill_buffer,)

        self.closed = False

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


    def listen_print_loop(self, responses, server):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print('dddd', transcript + overwrite_chars)
                server.Send_Data((transcript + overwrite_chars)).encode())

                num_chars_printed = 0

    def run(self, server) :
        audio_generator = self.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = self.client.streaming_recognize(self.streaming_config, requests)
        self.listen_print_loop(responses, server)


