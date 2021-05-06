from tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from os import listdir, path

songs = listdir('./songs')
index_of_song = 0


class Player:
    def __init__(self, root=Tk()):
        self.root = root
        self.root.geometry("450x400")
        self.root.title('Music Player')
        self.is_playing = True
        play_btn = Button(self.root, text="Play", command=self.play, width=7)
        play_btn.grid(row=1, column=2, columnspan=3, padx=(60, 20))

        pause_btn = Button(self.root, text="Pause",
                           command=self.pause, width=7)
        pause_btn.grid(row=1, column=3, columnspan=3, padx=(80, 0))

        next_btn = Button(self.root, text="Next", command=self.next, width=7)
        next_btn.grid(row=2, column=2, columnspan=3, padx=(90, 0))

        prev_btn = Button(self.root, text="Previous",
                          command=self.prev, width=7)
        prev_btn.grid(row=2, column=3, columnspan=3, padx=(90, 0))

        self.song_picture = ImageTk.PhotoImage(Image.open("music-note.png"))
        picture = Label(self.root, image=self.song_picture,
                        bd="4px", relief='groove')
        picture.grid(row=0, column=3, columnspan=3, padx=130)

        self.error_banner = Label(self.root, text="No more songs to play")

    def play(self):
        if self.is_playing == False:
            mixer.init()
            mixer.music.unpause()
        else:
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            mixer.music.play()

    def pause(self):
        mixer.init()
        mixer.music.pause()
        self.is_playing = False

    def next(self):
        global index_of_song
        index_of_song += 1

        if index_of_song >= len(songs):
            self.error_banner.grid(row=3, column=3, columnspan=3)
            return
        if index_of_song <= 0:
            index_of_song = 1
            mixer.init()
            mixer.music.load(path.join('songs', songs[index_of_song]))
            mixer.music.play()
            self.error_banner.grid_forget()
            return

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
            mixer.music.play()
            self.error_banner.grid_forget()
            return

        if index_of_song < 0:
            self.error_banner.grid(row=3, column=3, columnspan=3)
            return
        mixer.init()
        mixer.music.load(path.join('songs', songs[index_of_song]))
        mixer.music.play()

    def loop(self):
        self.root.mainloop()


player = Player()


player.loop()
