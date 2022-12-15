import boto3
import PyPDF2
from tkinter import Frame, filedialog, ttk, StringVar, Label
from os import environ, path


class Screen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.text = None
        self.pdf_path = None
        self.current_voice = "Kimberly"
        self.pdf_select_button = ttk.Button(self, text="Select PDF", command=self.ask_for_pdf_path)
        self.generate_audio_button = ttk.Button(self, text="Convert", command=self.convert)

        self.voice_opt = ["Kimberly", "Kimberly", "Ivy", "Joanna", "Kendra", "Salli", "Joey", "Justin", "Kevin",
                          "Matthew"]
        self.var = StringVar(self)
        self.var.set(self.voice_opt[0])
        self.voice_label = Label(self, text="Selected voice:")
        self.voice_suggest = ttk.OptionMenu(self, self.var, *self.voice_opt, command=self.set_voice)

        self.pdf_select_button.grid(row=0, column=0, padx=(15, 10), pady=(30, 10))
        self.voice_label.grid(row=1, column=0, padx=(15, 0))
        self.voice_suggest.grid(row=1, column=1, padx=(0, 20))
        self.generate_audio_button.grid(row=0, column=1, padx=(10, 20), pady=(30, 10))

    def set_voice(self, voice):
        self.current_voice = voice

    def ask_for_pdf_path(self):
        data = filedialog.askopenfilenames(title="Choose PDF file:", filetypes=[('PDF file', '.pdf')])
        if data != '':
            self.pdf_path = data

    def convert(self):
        self.pdf_to_text()
        self.text_to_speech()

    def pdf_to_text(self):
        if self.pdf_path is not None:
            with open(self.pdf_path[0], 'rb') as pdf:
                pdfReader = PyPDF2.PdfFileReader(pdf)
                count = pdfReader.numPages
                output = ""
                for char in range(count):
                    page = pdfReader.getPage(char)
                    output += page.extractText()
                if output != "":
                    self.text = output

    def text_to_speech(self):
        if self.text is not None:
            polly_client = boto3.Session(
                aws_access_key_id=environ["aws_access_key_id"],
                aws_secret_access_key=environ["aws_secret_access_key"],
                region_name='us-west-2').client('polly')

            response = polly_client.synthesize_speech(VoiceId=self.current_voice,
                                                      OutputFormat='mp3',
                                                      Text=self.text,
                                                      Engine='neural')
            directory = filedialog.askdirectory()
            name = (((self.pdf_path[0]).split("/"))[-1]).split('.')[0]
            with open(path.join(directory, f"{name}.mp3"), 'wb') as mp3:
                mp3.write(response['AudioStream'].read())
