from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from TTS_urEn import text_to_speech, process_filename,  voiceCloningEnglish
from VCStarGanv2 import voice_cloning
from Synchronization import combine_audio_video
from Dub import process_content 
import time
import os
from flask import send_file
from utils import delete_folder

app = Flask(__name__)

os.makedirs('./uploads', exist_ok=True)
os.makedirs('./dubOutput', exist_ok=True)

app.config['uploads'] = './uploads'
app.config['output'] = './dubOutput'
app.config['UrInaudioOutput'] = './output/clone/URIn'
app.config['EngInaudioOutput'] = './output/clone/EngIn'


CORS(app, origins=['https://dub-client.vercel.app','https://dub-client-git-main-abdulhameed10s-projects.vercel.app','https://dub-client-abdulhameed10s-projects.vercel.app'])

@app.route('/flask/generateDub', methods=['POST','GET'])


def Dub():
    if request.method == 'POST':
        
        if 'source' not in request.files:
            return jsonify({"message": "Data sent unsuccessfully", "status": "error"}), 400
        else:
         
            f = request.files['source']
            timestamp = time.strftime("%M%S")
            filename = secure_filename(f.filename)
            filename_without_extension, file_extension = os.path.splitext(filename)
            filename_with_timestamp = f"{filename_without_extension}_{timestamp}{file_extension}"
            f.save(os.path.join(app.config['uploads'], filename_with_timestamp))
            filename = filename_with_timestamp
           
            ln = request.form['language']
            video_path = os.path.join(app.config['uploads'], filename)
            output_path = os.path.join(app.config['output'], filename)   
            try:
                if filename.lower().endswith('.mp4') or (filename.lower().startswith("camera_video") and filename.lower().endswith('.webm')):
                    if ln == 'urdu':
                        audioPath,text,converted_video = process_content(filename,source_lang="UrIn",target_lang="en",format="video")
                        filename_without_extension,clonedVoicePath = process_filename(filename,ln="UrIn")
                        # this code is written for Test to speach for speech English languag
                        voiceCloningEnglish(text,audioPath,clonedVoicePath)
            
                        if(filename.lower().startswith("camera_video") and filename.lower().endswith('.webm')):
                            output_path = os.path.join(app.config['output'], filename.replace('.webm', '.mp4'))
                            combine_audio_video(video_path,converted_video, clonedVoicePath, output_path,ln="UrIn",extension=".webm")
                        elif(filename.lower().endswith('.mp4')):
                            combine_audio_video(video_path,converted_video, clonedVoicePath, output_path,ln="UrIn",extension=".mp4")
                        delete_folder(['./uploads','./output/audio','./output/text'])
                    elif(ln == 'english'):
                        
                        audioPath,text,converted_video = process_content(filename,source_lang="EngIn",target_lang="ur",format="video")
                        filename_without_extension,clonedVoicePath = process_filename(filename,ln="EngIn")
                        # '''this code is written for Text to speech for speech Urdu language'''
                        speachPath = text_to_speech(filename_without_extension, text) 
                        # '''this code is written for Voice Conversion for any language'''
                        voice_cloning(speachPath,audioPath,clonedVoicePath)
                        if(filename.lower().startswith("camera_video") and filename.lower().endswith('.webm')):
                            output_path = os.path.join(app.config['output'], filename.replace('.webm', '.mp4'))
                            combine_audio_video(video_path,converted_video, clonedVoicePath, output_path,ln="EngIn",extension=".webm")
                        elif(filename.lower().endswith('.mp4')):
                            combine_audio_video(video_path,converted_video, clonedVoicePath, output_path,ln="EngIn",extension=".mp4")
                        delete_folder(['./uploads','./output/audio','./output/text','./output/textToSpeech'])
                    try:
                        video_files = os.listdir(app.config['output'])
                        if(filename.lower().startswith("camera_video") and filename.lower().endswith('.webm')):
                            video_dubbed = [file for file in video_files if file == filename_without_extension.replace(".webm",".mp4")]
                        elif(filename.lower().endswith('.mp4')):
                            video_dubbed = [file for file in video_files if file == filename_without_extension]
                        
                        return send_file(os.path.join(app.config['output'], video_dubbed[0]), mimetype='video/mp4')
                    except Exception as e:
                        return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500
                else:
                    if ln == 'urdu':
                        audioPath,text = process_content(filename,source_lang="UrIn",target_lang="en",format="audio")   
                        filename_without_extension,clonedVoicePath = process_filename(filename,ln="UrIn")
                        # this code is written for Test to speach for speech English language
                        voiceCloningEnglish(text,audioPath,clonedVoicePath)
                        delete_folder(['./uploads','./output/audio','./output/text'])
                    
                        try:
                            audio_files = os.listdir(app.config['UrInaudioOutput'])
                            audio_dubbed = [filenames for filenames in audio_files if filenames.startswith(filename_without_extension)]
                            return send_file(os.path.join(app.config['UrInaudioOutput'], audio_dubbed[0]), mimetype='audio/mpeg')
                        except Exception as e:
                            return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500
                    elif(ln == 'english'):
                        audioPath,text = process_content(filename,source_lang="EngIn",target_lang="ur",format="audio")
                        filename_without_extension, clonedVoicePath = process_filename(filename,ln="EngIn")
                        # '''this code is written for Text to speech for speech Urdu language'''
                        speachPath = text_to_speech(filename_without_extension, text) 
                        # '''this code is written for Voice Conversion for any language'''
                        voice_cloning(speachPath,audioPath,clonedVoicePath)
                        delete_folder(['./uploads','./output/audio','./output/text','./output/textToSpeech'])
                      
                        try:
                            audio_files = os.listdir(app.config['EngInaudioOutput'])
                            audio_dubbed = [filenames for filenames in audio_files if filenames.startswith(filename_without_extension)]
                            return send_file(os.path.join(app.config['EngInaudioOutput'], audio_dubbed[0]), mimetype='audio/mpeg')
                        except Exception as e:
                            return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500
                  
             
            except Exception as e:
                return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500

              

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)