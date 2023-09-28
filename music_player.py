#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 08:39:18 2023

@author: tom
"""


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pygame
import os
from pathlib import Path
from downloadermp3 import DownloadAndConvertToMP3
import random
from itertools import cycle


class MusicPlayer:
	def __init__(self,root):
	        self.root = root
	        # Title of the window
	        self.root.title("MusicPlayer")
	        # Window Geometry
	        self.root.geometry("1000x600")#self.root.geometry("1200x200+200+200")
	        #self.root.geometry("%dx%d" % (self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
	        # Initiating Pygame
	        pygame.init()
	        # Initiating Pygame Mixer
	        pygame.mixer.init()
	        #music end event
	        self.MUSIC_END_EVENT = pygame.USEREVENT+1
	        # Declaring track Variable
	        self.track = StringVar()
	        # Declaring Status Variable
	        self.status = StringVar()
	    
	        # Creating the Track Frames for Song label & status label
	        trackframe = LabelFrame(self.root,text="Song 	Track",font=("times 	new roman",	15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
	        trackframe.place(x=200,y=400,width=800,height=100)
	        # Inserting Song Track Label
	        self.songtrack = Label(trackframe,text="",font=("times new roman",24,"bold"),bg="silver",fg="black", width=17)
	        self.songtrack.grid(row=0,column=0,padx=10,pady=5)
	        self.defilement=" "
	        # Inserting Status Label
	        trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="silver",fg="black").grid(row=0,column=1,padx=10,pady=5)
	    
	        # Creating Button Frame
	        buttonframe = LabelFrame(self.root,text="Control 	Panel",font=("times 	new roman",	15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
	        buttonframe.place(x=200,y=500,width=800,height=100)
	        # Inserting Play Button
	        self.play_btn = Button(buttonframe,text="PLAY",command=self.play,width=10,height=1,font=("times 	new roman",	16,"bold"),fg="black",bg="silver")
	        self.play_btn.grid(row=0,column=0,padx=10,pady=5)
	        # Inserting Pause Button
	        self.pause_btn = Button(buttonframe,text="PAUSE",command=self.pausesong,width=8,height=1,font=("times 		new roman",	16,"bold"),fg="black",bg="silver")
	        self.pause_btn.grid(row=0,column=1,padx=10,pady=5)
	        # Inserting Unpause Button
	        self.stop_btn = Button(buttonframe,text="STOP",command=self.stopsong,width=10,height=1,font=("times 		new roman",	16,"bold"),fg="black",bg="silver")
	        self.stop_btn.grid(row=0,column=2,padx=10,pady=5)
	        self.stop = False
	        # Inserting Stop Button
	        self.mode_btn = Button(buttonframe,text="RANDOM",command=self.change_mode,width=10,height=1,font=("times 	new roman",	16,"bold"),fg="black",bg="silver")
	        self.mode_btn.grid(row=0,column=3,padx=10,pady=5)
	    
	        # Creating Playlist Frame
	        songsframe = LabelFrame(self.root,text="Song 	Playlist",font=("times 	new roman",	15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
	        songsframe.place(x=200,y=0,width=800,height=400)
	        # Inserting scrollbar
	        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
	        # Inserting Playlist listbox
	        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times 	new roman",12,"bold"),bg="silver",fg="black",bd=5,relief=GROOVE, height=18)
	        # Applying Scrollbar to listbox
	        scrol_y.pack(side=RIGHT,fill=Y)
	        scrol_y.config(command=self.playlist.yview)
	        self.playlist.pack(fill=BOTH)
	        # Changing Directory for fetching Songs
	        os.chdir(str(Path.home()/'MyMusic'))
	        # Fetching Songs
	        songtracks = os.listdir()
	        # Inserting Songs into Playlist
	        for track in songtracks:
		        if track[-3:] == "mp3":
			        self.playlist.insert(END,track[:-4])
	          
		#creating menu
	       	menuframe = LabelFrame(self.root, text="Option", font=("times 	new roman", 	15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
	        menuframe.place(x=0, y=0, width=200, height=600)

	        self.menu = Listbox(menuframe, selectbackground="gold", selectmode=SINGLE, font=("times new roman", 12, "bold"), bg="silver", fg="black",  bd=5, relief=GROOVE, height=28)
	        self.menu.pack(fill=BOTH)
	        self.menu.insert(END, "Télécharger")


	        #progress bar 
	        #progressframe = LabelFrame(self.root,text="Progress",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
	        #progressframe.place(x=200,y=500,width=800,height=100)
	        self.progress_bar = ttk.Progressbar(trackframe, orient="horizontal", length=300, mode="determinate")
	        self.progress_bar.grid(row=0, column=3, padx=10, pady=5)
	        self.start_time = None #permet de suivre l'avancement de la musique 
	        self.temps_total = None 
	        self.pause_time = None
	        self.update_progress_bar()


		#scroll label 
	        self.scroll_label()


	        #binding
	        self.root.bind("<Double-Button-1>", self.double_clic)


	        #changement et fin
	        self.on_music_end()

	

	def double_clic(self, event):
		if self.menu.curselection():
			if self.menu.get(self.menu.curselection()) == "Télécharger":
				self.download()
	      
	     
	def play(self):
		self.stop = False
		self.pause_btn.config(text="PAUSE")
		self.playsong()


	def playsong(self):
	        # Displaying Selected Song title
	       	self.track.set(self.playlist.get(self.playlist.curselection()))
	        self.defilement = self.track.get() + "     "
	       	# Displaying Status
	       	self.status.set("-Playing")
	       	# Loading Selected Song
	        song = pygame.mixer.music.load(self.playlist.get(self.playlist.curselection())+".mp3")	
		#creating end event
	        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
	        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)
	       	# Playing Selected Song
	       	song = pygame.mixer.music.play()
	       	#song.play()
	
	        #temps écoulé
	        self.start_time = pygame.time.get_ticks()
	        self.temps_total = pygame.mixer.Sound(self.track.get()+".mp3").get_length()
	        
	        
	def stopsong(self):
        	# Displaying Status
	       	self.status.set("-Stopped")
	       	# Stopped Song
	       	pygame.mixer.music.stop()
	        #status song
	        self.stop = True
	        #reset
	        self.pause_btn.config(text="PAUSE")
	        self.progress_bar["value"]=0
	        self.track.set(" ")
	        self.defilement = " "
	        	    
	        	    
	        
	def pausesong(self):
	        if self.pause_btn.cget('text') == "PAUSE":
	       		# Displaying Status
	        	self.status.set("-Paused")
	        	self.pause_btn.config(text="UNPAUSE")
	       		# Paused Song
	       		pygame.mixer.music.pause()
			#get time paused
	        	self.pause_time = pygame.time.get_ticks()
            
	        else:
	        	# It will Display the  Status
	        	self.status.set("-Playing")
	        	self.pause_btn.config(text="PAUSE")
	        	# Playing back Song
	        	pygame.mixer.music.unpause()
	        	self.start_time += (pygame.time.get_ticks()-self.pause_time)

	def on_music_end(self):
		#define the next music
	        if self.stop:
	        	pass
	        else:
	        	for event in pygame.event.get():
	        		if event.type == self.MUSIC_END_EVENT:
	        			if self.mode_btn.cget('text')=="INFINITE":
	        				self.playlist.selection_clear(self.playlist.curselection()[0])
	        				for i in range(self.playlist.size()):
	        					if self.playlist.get(i) == self.track.get():
	        						self.playlist.selection_set(i)
	        						break
	        				self.playsong()
	        			else:
	        				song_dic = {}
	        				for i in range(self.playlist.size()):
	        					song_dic[self.playlist.get(i)] = i
	        				previous = self.track.get()
	        				del song_dic[previous]
	        				self.playlist.selection_clear(self.playlist.curselection()[0])
	        				next_selection = song_dic[random.choice(list(song_dic.keys()))]
	        				self.playlist.selection_set(next_selection)
	        				self.playsong()


	        self.root.after(100, self.on_music_end)
	
	def change_mode(self):
		if self.mode_btn.cget('text') == "RANDOM":
			self.mode_btn.config(text="INFINITE")
		elif self.mode_btn.cget('text') == "INFINITE":
			self.mode_btn.config(text="RANDOM")
	
	def update_progress_bar(self):
		if pygame.mixer.music.get_busy():
			position = (pygame.time.get_ticks() - self.start_time)/1000 
			total = self.temps_total 
			progress = (position/total)*100
			#self.progress_bar.set(progress)
			self.progress_bar["value"] = progress
		self.root.after(1000, self.update_progress_bar)

	def scroll_label(self):
		if self.pause_btn.cget("text") == "UNPAUSE":
			pass
		else:
			tmp = self.defilement[-1]
			for i in range(len(self.defilement)-1):
				tmp += self.defilement[i]
			self.defilement = tmp
			text_cycle = cycle(self.defilement)
			scrolled_text = ''.join(next(text_cycle) for _ in range(len(self.defilement) + 30))
			self.songtrack.config(text=scrolled_text)
		self.root.after(200, self.scroll_label)
	
	def download(self):
	        #download a song
	        dialog = Toplevel(root, width=400, height=400)
	        dialog.title("Fenêtre de Dialogue")

	        frame = Frame(dialog, width=400, height=400)
	        frame.pack()
    
	        # Labels
	        title_label = Label(frame, text="Titre:")
	        title_label.grid(column=1, row=1, padx=10, pady=5)

	        path_label = Label(frame, text="Chemin d'enregistrement:")
	        path_label.grid(column=1, row=2, padx=10, pady=5)

	        url_label = Label(frame, text="url de la vidéo:")
	        url_label.grid(column=1, row=3, padx=10, pady=5)

    		# Entry widgets
	        title_entry = Entry(frame)
	        title_entry.grid(column=2, row=1, padx=10, pady=5)

	        path_entry = Entry(frame)
	        path_entry.grid(column=2, row=2, padx=10, pady=5)

	        url_entry = Entry(frame)
	        url_entry.grid(column=2, row=3, padx=10, pady=5)
	
    		# Browse button
	        def browse_path():
    		    selected_path = filedialog.askdirectory()
    		    path_entry.delete(0, END)  # Efface le contenu actuel
    		    path_entry.insert(0, selected_path)
	
	        browse_button = Button(frame, text="Parcourir", command=browse_path)
	        browse_button.grid(column=3, row=2, padx=10, pady=5)

    		# OK button
	        def save_data():
    		    title = title_entry.get()
    		    path = path_entry.get()
    		    url = url_entry.get()
    		    DownloadAndConvertToMP3(url, path, title)
    		    self.playlist.insert(END, title)
    		    dialog.destroy()  # Ferme la fenêtre de dialogue

	        ok_button = Button(frame, text="Télécharger", command=save_data)
	        ok_button.grid(column=2, row=4, padx=10, pady=5)


		

	            
root = Tk()
MusicPlayer(root)
root.mainloop()  
