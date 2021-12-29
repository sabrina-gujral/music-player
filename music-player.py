from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import os
class MusicPlayer:
    def __init__(self, window):
        window.geometry("600x400")
        window.title("Music Player")
        window.configure(background="black")
        window.resizable(0, 0)

        Load = Button(window, text="Load", 
                      command=self.load_file, 
                      width=8, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        Play = Button(window, text="Play", 
                      command=self.play_music, 
                      width=8, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        Pause = Button(window, text="Pause", 
                       command=self.pause_music, 
                       width=8, 
                       bg="white", 
                       fg="blue", 
                       font=("Times", 15, "bold"))
        Stop = Button(window, text="Stop", 
                      command=self.stop_music, 
                      width=8, 
                      bg="white", 
                      fg="blue", 
                      font=("Times", 15, "bold"))
        
        Load.place(x=240, y=160)
        Play.place(x=140, y=120)
        Pause.place(x=240, y=120)
        Stop.place(x=340, y=120)

        self.music_file = ""
        self.play = False
        self.progress = None
        self.songsframe = None
        self.duration = 0
        self.bar_value = StringVar()

        self.progress = Progressbar(root, 
                                    orient=HORIZONTAL, 
                                    length=600, 
                                    variable=self.bar_value,
                                    mode="determinate")
        self.progress.place(x=0, y=60)
        self.progress_lbl = Label(root, textvariable = self.bar_value, bg="black", fg="magenta",)
        self.progress_lbl.place(x=250, y=90)

    def load_file(self):
        directory = filedialog.askdirectory()
        os.chdir(directory)
        song_list = os.listdir()

        songs_frame = LabelFrame(root, 
                                 text="My Playlist", 
                                 bg="grey", 
                                 fg="white", 
                                 font=("Times", 15, "bold"), 
                                 relief=GROOVE, 
                                 bd=5)
        songs_frame.place(x=0, y=200, width=600, height=200)
        scroll_y = Scrollbar(songs_frame, 
                             orient=VERTICAL)
        self.songsframe = Listbox(songs_frame, 
                                  yscrollcommand=scroll_y.set, 
                                  font=("Times", 15, "bold"), 
                                  bg="#133d67", 
                                  selectmode=SINGLE, 
                                  fg="white", 
                                  selectbackground="cyan", 
                                  selectforeground="black", 
                                  relief=GROOVE, 
                                  bd=5)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.songsframe.yview)
        self.songsframe.pack(fill=BOTH)

        for song in song_list:
            self.songsframe.insert(END, song)

    def format_duration(self, time):
        minutes = time // 60
        seconds = time % 60
        return f"{int(minutes)}:{int(seconds)}"

    def progress_step(self):
        if mixer.music.get_busy():
            current_time = mixer.music.get_pos() / 1000
            progress = current_time / self.duration * 100
            progress_label = f"{self.format_duration(time=current_time)} / {self.format_duration(time=self.duration)}"
            self.bar_value.set(progress_label)
            self.progress['value'] = progress
            root.after(1000, self.progress_step)

    
    def play_music(self):
        self.music_file = self.songsframe.get(ACTIVE)

        mixer.init()
        mixer.music.load(self.music_file)
        mixer.music.play()

        audio = MP3(self.music_file, ID3=EasyID3)
        label = audio.get('title')[0]
        artist = audio.get('artist')[0]
        self.duration = audio.info.length

        label1 = Label(root, 
                           text=label,
                           bg="black", fg="yellow", 
                           font=("Times", 15, "bold"))
        label1.place(x=5, y=10)

        label2 = Label(root, 
                           text=artist, 
                           bg="black", fg="yellow", 
                           font=("Times", 15, "bold"))
        label2.place(x=5, y=30)

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