from tkinter import *
import tkinter.messagebox
from pygame import mixer
from PIL import ImageTk, Image
from os import listdir, path, remove
from tkinter import ttk
from mutagen.mp3 import MP3 # module to get MP3 file information like video duration
from pytube import YouTube # module to download video from Youtube
from moviepy.editor import VideoFileClip # module to convert mp4 to mp3
import threading


class Player:
    def __init__(self, root=Tk()):
        mixer.init(frequency=48000)
        self.root = root
        self.root.geometry("500x500")
        self.root.title('Music Player')
        self.root.wm_resizable(False, False)
        self.is_paused = True
        self.songs = listdir('./songs')
        self.index_of_song = 0

        self.song_picture = ImageTk.PhotoImage(Image.open("music-note.png"))
        self.song_picture_label = Label(
            self.root, image=self.song_picture, bd="4px", relief='groove')
        self.song_picture_label.grid(row=0, column=3, columnspan=4, padx=130)

        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL,
                                value=0, length=250, command=self.slide)
        self.slider.grid(row=1, column=3, columnspan=4, rowspan=2, padx=130, pady=(10,10))

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

        self.error_banner = Label(self.root)
        self.error_banner.grid(row=4, column=3, columnspan=4)

        self.download_text_var = StringVar()
        self.download_box = Entry(self.root, width=30, textvariable=self.download_text_var)
        self.download_box.grid(row=5, column=3, columnspan=4)

        self.download_btn = ttk.Button(self.root, text="Download", command=self.start_download_from_youtube_in_bg, width=15)
        self.download_btn.grid(row=6, column=3, columnspan=4)

        self.song_length = 0

        # Create progress popup window
        self.progress_window = Toplevel()
        self.progress_window.title("Download Status")
        self.progress_window.geometry("400x200")
        self.progress_window.withdraw()
        self.progress_window.protocol("WM_DELETE_WINDOW", self.close_progress_window)

        self.update_progress_bar = ''

        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100, mode='determinate')

        self.download_text_progress_var = DoubleVar(0)
        self.progress_label = ttk.Label(self.progress_window, text=f'Downloading: {self.download_text_progress_var.get()}' )
        
        self.progress_label.grid(row=0, column=2, columnspan=4, padx=150, pady=(50,0))
        self.progress_bar.grid(row = 1, column = 2, columnspan=6, padx=155, pady=(25,0))

    def play(self, start=0):
        if(self.is_paused != False):
            self.is_paused = False
            mixer.music.load(path.join('songs', self.songs[self.index_of_song]))
            self.song_length = self.getLength(self.index_of_song)
            self.slider.config(to=self.song_length, value=0, length=self.song_length)
            # mixer.music.rewind()
            mixer.music.play(start=start)
            self.moveSlider()

    def pause(self):
        mixer.music.pause()
        self.is_paused = True
        
    def next(self):
        self.index_of_song += 1
        
        if self.index_of_song >= len(self.songs):
            self.error_banner.config(text="No more song to play")
            return
        elif self.index_of_song <= 0:
            self.index_of_song = 1
            self.song_length = self.getLength(self.index_of_song)
            self.slider.config(to=self.song_length, length=self.song_length, value=0)
            mixer.music.load(path.join('songs', self.songs[self.index_of_song]))
            self.error_banner.grid_forget()
            return

        # Change slider to 0 and slider label
        else:
            self.song_length = self.getLength(self.index_of_song)
            self.slider.config(to=self.song_length, length=self.song_length, value=0)
            mixer.music.load(path.join('songs', self.songs[self.index_of_song]))
            mixer.music.play()
            

    def prev(self):
        self.index_of_song -= 1
        if self.index_of_song >= len(self.songs):
            self.index_of_song = len(self.songs)-2
            mixer.music.load(path.join('songs', self.songs[self.index_of_song]))
            self.song_length = self.getLength(self.index_of_song)
            self.slider.config(to=self.song_length, length=self.song_length, value=0)
            mixer.music.play()
            self.error_banner.grid_forget()
            return

        if self.index_of_song < 0:
            self.error_banner.config(text="No more song to play")
            return

        # Change slider value to 0 and slider label
        self.song_length = self.getLength(self.index_of_song)
        self.slider.config(to=self.song_length, length=self.song_length, value=0)
        mixer.music.load(path.join('songs', self.songs[self.index_of_song]))
       
    def slide(self,none):
        mixer.music.play(start=int(self.slider.get()))
        

    def getLength(self, index_of_song = 0):
        song_length = MP3(path.join('songs', self.songs[index_of_song])).info.length
        return round(song_length)

    def moveSlider(self):
        if self.is_paused == True:
            pass
        else:
            if int(self.slider.get()) <= int(self.song_length):
                next_position = self.slider.get()+1
                self.slider.config(value=next_position)
                self.slider.after(1000, self.moveSlider)
            else:
                print(self.slider.get())
                mixer.music.stop()

    def close_progress_window(self):
        self.progress_bar.stop()
        self.progress_bar.after_cancel(self.update_progress_bar)
        self.progress_var.set(0)
        self.progress_label.configure(text=f'Downloading: {self.progress_var.get()}')
        self.progress_window.wm_withdraw()


    def update_progress(self, exit=0):
        if(exit == 1):
            return
        self.download_text_progress_var.set(self.progress_var.get())
        self.progress_label.configure(text=f'Downloading: {self.download_text_progress_var.get()}')
        self.progress_bar.configure(value=1)
        print("I run")
        if self.progress_var.get() >= 90:
            self.progress_var.set(99.9)
            self.progress_label.configure(text=f'Downloading: {self.progress_var.get()}')
            self.progress_bar.stop() 
            # self.progress_window.wm_withdraw() # close the progress window
            return
        self.update_progress_bar = self.progress_bar.after(50, self.update_progress)

    def create_after_download_popup(self, state):
        if state == 1:
            tkinter.messagebox.showinfo("Download finish",  "The song has been downloaded successfully") 
        else:
            tkinter.messagebox.showinfo("Error",  "Unsuccessfully downloaded the song") 

    def download_from_youtube(self):
        try:
            self.progress_bar.start(50)
            url = self.download_text_var.get()
            if(url.strip() != ""):
                youtube = YouTube(f'{url}')
                song = youtube.streams.filter(file_extension='mp4').first()
                out_file = song.download(output_path="./songs")

                # Covert mp4 to mp3 and then delete the mp4
                video = VideoFileClip(f"./songs/{song.title}.mp4")
                video.audio.write_audiofile(f"./songs/{song.title}.mp3")
                video.close()
                remove(f"./songs/{song.title}.mp4")

                # Update song list
                self.songs = listdir("./songs")

                # Reset download box
                self.download_text_var.set("")
                
                self.progress_window.withdraw()
            else:
                self.error_banner.config(text="URL can not be empty")
        except Exception as e:
            print(repr(e))
            # Make error message disappear after a certain amount of time
            self.error_banner.config(text="URL not found", fg="red")
            self.root.after(1200, lambda: self.error_banner.config(text=""))
            self.root.after(1200, lambda: self.download_text_var.set(""))
    

    def start_download_from_youtube_in_bg(self):
        if self.progress_window.wm_state() != 'normal' : # if this window is open, the state will be 'normal'. If it is closed then the state will be 'withdrawn'
            self.progress_window.wm_deiconify()
            self.update_progress()
            self.progress_bar.start(50)
        thread1 = threading.Thread(target=self.download_from_youtube)
        thread1.start()

    def loop(self):
        self.root.mainloop()


player = Player()

player.loop()
