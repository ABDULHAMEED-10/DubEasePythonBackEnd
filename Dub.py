import os
from utils import save_text_to_file, convert_audio_to_wav, convert_audio_to_text, translate_text, convert_video_to_mp4, extract_audio

def process_content(filename,source_lang,target_lang,format):
    
    content_path = os.path.join('./uploads/', filename)
    audio_output_path = f'./output/audio/{source_lang}/'
    pathOfTextFile = f'./output/text/{source_lang}/'
    textFileExtension = '.txt'
    os.makedirs(audio_output_path, exist_ok=True)
    os.makedirs(pathOfTextFile, exist_ok=True)
    audioFileExtension = '.wav'
    pathOfAudioFile = f'./output/audio/{source_lang}/'
    os.makedirs(pathOfAudioFile, exist_ok=True)
    wordsToremove=['.mp4','.webm']
    for word in wordsToremove:
        filename = filename.replace(word,'')
    audio_output_path = f'{pathOfAudioFile}{filename}{audioFileExtension}'
    text_output_path = f'{pathOfTextFile}{filename}{textFileExtension}'
    
    source_lang = 'ur-PK' if source_lang == 'UrIn' else 'en-US'


    if format=='audio':
        try:
            if content_path.lower().endswith('.wav'):
                audio_output_path = content_path
            elif content_path.lower().endswith(('.mp3', '.mpeg', '.ogg','.webm')):
                audio_output_path = convert_audio_to_wav(content_path, audio_output_path)
            audio_text = convert_audio_to_text(audio_output_path,source_lang)
            translated_text = translate_text(audio_text, target_language=target_lang)
            save_text_to_file(translated_text, text_output_path)
            return audio_output_path , translated_text
        except Exception as e:
            print(f"Error occurred during processing: {e}")
    
    elif format=='video':
        video_output_path=""
        try:
            if content_path.lower().endswith(('.mp4')): 
                audio_output_path = extract_audio(content_path, audio_output_path)
            elif content_path.lower().endswith(('.webm')):
                video_output_path = convert_video_to_mp4(content_path)
                audio_output_path = extract_audio(video_output_path, audio_output_path)
            

            audio_text = convert_audio_to_text(audio_output_path,source_lang)
            translated_text = translate_text(audio_text,target_language=target_lang)
            save_text_to_file(translated_text, text_output_path)
            
            return audio_output_path , translated_text , video_output_path
        except Exception as e:
            print(f"Error occurred during processing: {e}")

        
    
         


