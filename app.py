from flask import Flask
import speech_recognition  as sr
import moviepy.editor as mp
from rake_nltk import Rake
app = Flask(__name__)


@app.route('/')



def fileopen(filename):
        file = filename
        if file[-3:] == "mp4":
            clip = mp.VideoFileClip(file).subclip(0, 30)
            clip.audio.write_audiofile("theaudio.wav")
            r = sr.Recognizer()
            audio = 'theaudio.wav'
            with sr.AudioFile(audio) as source:
                audio = r.record(source)
                print('video converted to audio')
        elif file[-3:] == "wav":
            audio = file
            with sr.AudioFile(audio) as source:
                r = sr.Recognizer()
                audio = r.record(source)
                print('Audio processed')

        try:
            text = r.recognize_google(audio)
            text_file = open("output.txt", "w")
            text_file.write(text)
            text_file.close()
            print("Output written in file successfully")
        except Exception as e:
            print(e)
        # rake algo to extract the keywords from the file Output.txt
        with open('output.txt', 'r') as content_file:
            content = content_file.read()
        r = Rake()
        r.extract_keywords_from_text(content)
        output = r.get_ranked_phrases()

        # saving the keywords to a file named keywords.txt
        text_file = open("keywords.txt", "w")
        text_file.write(str(output))
        text_file.close()
        print("Keywords written to a file keywords.txt successfully")
        return 'text_file'




if __name__ == '__main__':
    app.run()
