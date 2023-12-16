import torchaudio
from speechbrain.pretrained import HIFIGAN
hifi_gan = HIFIGAN.from_hparams(source='speechbrain/tts-hifigan-ljspeech', savedir='tmp')
text = 'Hello, this is a test run.'
speech = hifi_gan.synthesize(text)
torchaudio.save('output_speech.wav', speech.unsqueeze(0), 16000)
