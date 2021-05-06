from tkinter import *

from pygame import mixer


class Player:
    def __init__(self, root=Tk()):
        self.root = root
        self.root.geometry("400x200")
        self.root.title('Music Player')
        self.is_playing = True
        play_btn = Button(self.root, text="Play", command=self.play)
        play_btn.grid(row=0, column=0)

        pause_btn = Button(self.root, text="Pause", command=self.pause)
        pause_btn.grid(row=0, column=1)

    def play(self):
        if self.is_playing == False:
            mixer.init()
            mixer.music.unpause()
        else:
            mixer.init()
            mixer.music.load('muon-roi-ma-sao-con.mp3')
            mixer.music.play()

    def pause(self):
        mixer.init()
        mixer.music.pause()
        self.is_playing = False

    def loop(self):
        self.root.mainloop()


player = Player()


player.loop()
