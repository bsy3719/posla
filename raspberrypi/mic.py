from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
#RATE = 16000
#CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
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
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


    def listen_print_loop(self, responses):
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

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
           # if re.search(r'\b(exit|quit)\b', transcript, re.I):
            #    print('Exiting..')
             #   break

                num_chars_printed = 0

    def run(self) :
        audio_generator = self.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = self.client.streaming_recognize(self.streaming_config, requests)
        self.listen_print_loop(responses)


#def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    #language_code = 'en-US'  # a BCP-47 language tag
    #language_code = 'ko-KR'
    
    #import os

    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pirl/Documents/BCODE/project/speech/Speech-58bc93fd5c7a.json"
    
    #client = speech.SpeechClient()
    #config = types.RecognitionConfig(
    #    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    #    sample_rate_hertz=RATE,
    #    language_code=language_code)
    #streaming_config = types.StreamingRecognitionConfig(
    #    config=config,
    #    interim_results=True)

#    with MicrophoneStream(RATE, CHUNK) as stream:
#        audio_generator = stream.generator()
#        requests = (types.StreamingRecognizeRequest(audio_content=content)
#                    for content in audio_generator)
#
#        responses = client.streaming_recognize(streaming_config, requests)
#
        # Now, put the transcription responses to use.
#        listen_print_loop(responses)


#if __name__ == '__main__':
#    main()
