from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3

class MusicPlayer:
    def __init__(self, window):
        window.geometry("500x300")
        window.title("Music Player")
        window.configure(background="black")
        window.resizable(0, 0)

        Load = Button(window, text="Load", 
                      command=self.load_file, 
                      width=10, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        Play = Button(window, text="Play", 
                      command=self.play_music, 
                      width=10, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        Pause = Button(window, text="Pause", 
                       command=self.pause_music, 
                       width=10, 
                       bg="white", 
                       fg="blue", 
                       font=("Times", 15, "bold"))
        Stop = Button(window, text="Stop", 
                      command=self.stop_music, 
                      width=10, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        

        Load.place(x=0, y=100)
        Play.place(x=180, y=100)
        Pause.place(x=380, y=100)
        Stop.place(x=180, y=140)

        self.music_file = ""
        self.play = False
        self.progress = None
        self.title= ""
        self.artist=""
        self.duration = 0

    def load_file(self):
        self.music_file = filedialog.askopenfilename(title="Select Music File", filetypes=(("MP3 Files", "*.mp3"), 
                                                                                           ("WAV Files", "*.wav"), 
                                                                                           ("MP4 Files", "*.mp4"),
                                                                                           ("AAC Files", "*.aac")))
        audio = MP3(self.music_file, ID3=EasyID3)

        self.label = audio.get('title')[0]
        self.artist = audio.get('artist')[0]
        self.duration = audio.info.length

        self.progress = Progressbar(root, 
                                    orient=HORIZONTAL, 
                                    length=(2 * int(self.duration)), 
                                    mode="determinate")
        self.progress.place(x=0, y=60)

        self.label1 = Label(root, 
                           text=self.label,
                           bg="black", fg="yellow", 
                           font=("Times", 15, "bold"), 
                           underline=True,
                           highlightbackground="red",
                           justify="center")
        self.label1.place(x=5, y=10)

        self.label2 = Label(root, 
                           text=self.artist, 
                           bg="black", fg="yellow", 
                           font=("Times", 15, "bold"), 
                           underline=True,
                           highlightbackground="red",
                           justify="center")
        self.label2.place(x=5, y=28)

    def progress_step(self):
        if self.play:
            for i in range(0, int(self.duration)):
                self.progress["value"] = i
                self.progress.update()
                self.progress.after(2000)
                

    def play_music(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            self.play = True
            self.progress_step()

    def pause_music(self):
        if self.play:
            mixer.music.pause()
            self.play = False
        else:
            mixer.music.unpause()
            self.play = True

    def stop_music(self):
        mixer.music.stop()
        self.play = False


root = Tk()
obj = MusicPlayer(root)
root.mainloop()