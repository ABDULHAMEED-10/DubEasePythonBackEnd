from transformers import VitsModel, AutoTokenizer
from TTS.api import TTS
import torch
import scipy
# from transformers import VitsModel, AutoTokenizer
# import torch
# import scipy
# model = VitsModel.from_pretrained("facebook/mms-tts-eng")
# tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
# text = "some example text in the English language"
# inputs = tokenizer(text, return_tensors="pt")
# with torch.no_grad():
#     output = model(**inputs).waveform
# scipy.io.wavfile.write("techno.wav", rate=model.config.sampling_rate, data=output.float().numpy())

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

def process_filename(filename, ln):
    words_to_remove = ['.mp4', '.webm', '.mp3','.ogg','.mpeg','.wav']
    for word in words_to_remove:
        filename_without_extension = filename.replace(word, '')
    cloned_voice_path = f'E:/DubEase/Python Server/output/clone/{ln}/{filename_without_extension}.wav'
    return filename_without_extension , cloned_voice_path
def text_to_speech(filename,text):
    model = VitsModel.from_pretrained("facebook/mms-tts-urd-script_arabic")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-urd-script_arabic")

    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = model(**inputs).waveform

    output_path = f"E:/DubEase/Python Server/output/textToSpeach/{filename}.wav"  
    scipy.io.wavfile.write(output_path, rate=model.config.sampling_rate, data=output.squeeze().numpy())
    
    return output_path

def voiceCloningEnglish(text, speaker_wav, output_file):
    try:
        tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=output_file)
    except Exception as e:
        print(f"An error occurred: {e}")