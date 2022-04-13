import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


class Player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.songList = []
        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                               yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.volume = tk.DoubleVar(self)
        self.next = None
        self.pause = tk.Button(self.controls, image=pause)
        self.prev = tk.Button(self.controls, image=prev)
        self.loadSongs = tk.Button(self.controls, bg='black', fg='white', font=10)
        self.songTrack = tk.Label(self.track, font=("times new roman", 16, "bold"),
                                  bg="black", fg="white")
        self.canvas = tk.Label(self.track, image=img)
        self.controls = tk.LabelFrame(self,
                                      font=("times new roman", 15, "bold"),
                                      bg="white", fg="white", bd=2, relief=tk.GROOVE)
        self.trackList = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
                                       font=("times new roman", 15, "bold"),
                                       bg="pink", fg="black", bd=5, relief=tk.GROOVE)
        self.v = None
        self.track = tk.LabelFrame(self, text='Song Track',
                                   font=("times new roman", 15, "bold"),
                                   bg="grey", fg="red", bd=5, relief=tk.GROOVE)
        self.master = master
        self.pack()
        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.track_list_widgets()

        self.master.bind('<Left>', self.prev_song)
        self.master.bind('<space>', self.play_pause_song)
        self.master.bind('<Right>', self.next_song)

    def create_frames(self):
        self.track.config(width=410, height=300)
        self.track.grid(row=0, column=0, padx=10)

        self.trackList.config(width=190, height=400)
        self.trackList.grid(row=0, column=1, rowspan=3, pady=5)

        self.controls.config(width=410, height=80)
        self.controls.grid(row=2, column=0, pady=5, padx=10)

    def track_widgets(self):
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.songTrack['text'] = 'NANI,s PLAYER'
        self.songTrack.config(width=30, height=1)
        self.songTrack.grid(row=1, column=0, padx=10)

    def control_widgets(self):
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = tk.Button(self.controls, image=next_)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    def track_list_widgets(self):
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def retrieve_songs(self):
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.songList.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songList, f)
        self.playlist = self.songList
        self.trackList['text'] = f'PlayList - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_pause_song(self):
        if self.paused:
            self.play_song()
        else:
            self.pause_song()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songTrack['anchor'] = 'w'
        self.songTrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if not self.played:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):
        self.master.focus_set()
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_song(self):
        self.master.focus_set()
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()

    def change_volume(self):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)


# ----------------------------- Main -------------------------------------------

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('Music!!')
    root.iconbitmap(r'icons/app.ico')

    img = PhotoImage(file='icons/music.gif')
    next_ = PhotoImage(file='icons/next.gif')
    prev = PhotoImage(file='icons/previous.gif')
    play = PhotoImage(file='icons/play.gif')
    pause = PhotoImage(file='icons/pause.gif')

    app = Player(master=root)
    app.mainloop()
