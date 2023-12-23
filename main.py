from tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from os import listdir, path
from tkinter import ttk
from mutagen.mp3 import MP3

songs = listdir('./songs')
index_of_song = 0
song_length = MP3(path.join('songs', songs[index_of_song])).info.length


class Player:
    def __init__(self, root=Tk()):
        self.root = root
        self.root.geometry("500x400")
        self.root.title('Music Player')
        self.is_paused = True

        self.song_picture = ImageTk.PhotoImage(Image.open("music-note.png"))
        self.song_picture_label = Label(
            self.root, image=self.song_picture, bd="4px", relief='groove')
        self.song_picture_label.grid(row=0, column=3, columnspan=4, padx=130)

        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL,
                                value=0, length=250, command=self.slide)
        self.slider.grid(row=1, column=3, columnspan=4, rowspan=2, padx=130, pady=(10,10))
        # self.slider.bind('<Button-1>', self.pause)
        # self.slider.bind('<ButtonRelease-1>', self.slide)
        

        self.play_btn = Button(self.root, text="Play",
                                  command=self.play, width=7)
        self.play_btn.grid(row=3, column=1, columnspan=4, padx=(150, 20))
        
        self.pause_btn = Button(self.root, text="Pause",
                                   command=self.pause, width=7)
        self.pause_btn.grid(row=3, column=2, columnspan=4, padx=(190, 20))

        self.next_btn = Button(self.root, text="Next",
                                  command=self.next, width=7)
        self.next_btn.grid(row=3, column=3, columnspan=4, padx=(230, 20))

        self.prev_btn = Button(self.root, text="Previous",
                                  command=self.prev, width=7)
        self.prev_btn.grid(row=3, column=0, columnspan=4, padx=(110, 20))

        self.error_banner = Label(self.root, text="No more songs to play")

        self.song_length = MP3(
            path.join('songs', songs[index_of_song])).info.length

    def play(self, start=0):
        if(self.is_paused != False):
            self.is_paused = False
            global index_of_song
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            self.slider.config(to=self.getLength(index_of_song))
            self.slider.config(length=self.getLength(index_of_song))
            self.moveSlider()
            mixer.music.play(start=start)
        
        
    def pause(self):
        mixer.init()
        mixer.music.pause()
        self.is_paused = True
        

    def next(self):
        global index_of_song
        index_of_song += 1
        
        if index_of_song >= len(songs):
            self.error_banner.grid(row=4, column=3, columnspan=4)
            return
        elif index_of_song <= 0:
            index_of_song = 1
            self.slider.config(value=0)
            self.song_length = self.getLength(index_of_song)
            self.slider.config(to=f'{self.song_length}')
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            mixer.music.play()
            self.error_banner.grid_forget()
            return

        # Change slider to 0 and slider label
        else:
            self.slider.config(value=0)
            self.song_length = self.getLength(index_of_song)
            self.slider.config(to=f'{self.song_length}')
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            mixer.music.play()

    def prev(self):
        global index_of_song
        index_of_song -= 1
        if index_of_song >= len(songs):
            index_of_song = len(songs)-2
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            self.slider.config(value=0)
            self.song_length = self.getLength(index_of_song)
            self.slider.config(to=f'{self.song_length}')
            mixer.music.play()
            self.error_banner.grid_forget()
            return

        if index_of_song < 0:
            self.error_banner.grid(row=4, column=3, columnspan=4)
            return

        # Change slider value to 0 and slider label
        self.slider.config(value=0)
        self.song_length = self.getLength(index_of_song)
        self.slider.config(to=f'{self.song_length}')
        mixer.init()
        mixer.music.load(path.join('songs', songs[index_of_song]))
        mixer.music.play()
       
    def slide(self, none):
        mixer.init()
        mixer.music.play(start=int(self.slider.get()))
        

    def getLength(self, index_of_song):
        self.song_length = MP3(path.join('songs', songs[index_of_song])).info.length
        return self.song_length

    def moveSlider(self, x=0):
        if self.is_paused == True:
            pass
        else:
            if int(self.slider.get()) != int(self.song_length):
                next_position = int(self.slider.get())+1
                self.slider.config(value=next_position)
                self.slider.after(1000, self.moveSlider)
            else:
                mixer.music.stop()


    def loop(self):
        self.root.mainloop()


player = Player()

player.loop()
