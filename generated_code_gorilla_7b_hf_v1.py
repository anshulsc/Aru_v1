
from transformers import pipeline

def load_model():
    audio_classifier = pipeline('audio-classification', model='MIT/ast-finetuned-audioset-10-10-0.4593')
    return audio_classifier

def process_data(audio_path, audio_classifier):
    response = audio_classifier(audio_path)
    return response

audio_path = 'your/audio/path.wav'

# Load the model
audio_classifier = load_model()

# Process the data
response = process_data(audio_path, audio_classifier)
print(response)