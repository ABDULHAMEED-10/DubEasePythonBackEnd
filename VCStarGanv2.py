from TTS.api import TTS
def voice_cloning(source_wav, target_wav, output_wav):
    tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False).to("cpu")
    tts.voice_conversion_to_file(source_wav=source_wav, target_wav=target_wav, file_path=output_wav)
