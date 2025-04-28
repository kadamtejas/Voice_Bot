import sys
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import os
import gradio as gr

history = []
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def transcribe(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        return "Could not understand the audio."
   
def voice_bot(text):
   
   history.append({"role":"user","content":text})
   chat_completion = client.chat.completions.create(
   messages = history,
   model = "llama-3.3-70b-versatile"
   )

   bot_response = chat_completion.choices[0].message.content
   history.append({"role":"assistant","content":bot_response})
   print(history)
   return bot_response

   
def clear_history():
    global history
    history = []
    return "History Cleared"


with gr.Blocks() as demo:
   audio_input = gr.Audio(label="Speak Now", type="filepath", interactive=True)
   text_input = gr.Textbox(label = "Transcribed Text")
   processed_output = gr.Textbox(label="Processed Text")

   transcribe_btn = gr.Button("Transcribe")
   

   transcribe_btn.click(fn = transcribe , inputs = audio_input , outputs = text_input).then(
   fn=voice_bot,inputs = text_input,outputs = processed_output)

   reset_btn = gr.Button("Reset Chat")
   reset_btn.click(fn=clear_history, inputs=[], outputs=processed_output)



if __name__ == "__main__":
   demo.launch()






