from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3

root= Tk()
root.title("ADITYA")
root.iconbitmap('C:\MUSIC PLAYER')
root.geometry("500x350")

#initialize
pygame.mixer.init()

#get song time info
def play_time():
	#grab current song elapsed time
	current_time = pygame.mixer.music.get_pos() / 1000


	#converting to time format
	converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

	#get the current song info
	current_song = song_box.curselection()

	#grab the title from playlist
	song = song_box.get(current_song)
	#adding directory structure and mp3 to song title
	song = f'C:/MUSIC PLAYER/audio/{song}.mp3'

	#load song with mutagen
	song_mut = MP3(song)

	#get song length
	song_length=song_mut.info.length

	#converted time format
	converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))




	#output time to status bar
	status_bar.config(text=f'Time elapsed: {converted_current_time} of {converted_song_length}   ')

	#updating time every second
	status_bar.after(1000, play_time)


#add song function
def add_song():
	song=filedialog.askopenfilename(initialdir='C:\MUSIC PLAYER\audio',title="Choose a song" , filetypes=(("mp3 Files" , "*.mp3"),))
	#strip up
	song=song.replace("C:/MUSIC PLAYER/audio/","")
	song=song.replace(".mp3","")
	#add song to listbox
	song_box.insert(END,song)
#add many songs to playlist
def add_many_song():
	songs =filedialog.askopenfilenames(initialdir='C:\MUSIC PLAYER\audio',title="Choose a song" , filetypes=(("mp3 Files" , "*.mp3"),))

	#loop for each song for stripup
	for song in songs:
		#strip up
		song=song.replace("C:/MUSIC PLAYER/audio/","")
		song=song.replace(".mp3","")
		#add song to listbox
		song_box.insert(END,song)



#play selected song
def play():
	song = song_box.get(ACTIVE)
	song = f'C:/MUSIC PLAYER/audio/{song}.mp3'


	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#calling the function get_time to get length

	play_time()

#stop the selected song
def stop():
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

#global paused 
global paused
paused = False
#pause and unpause the selected song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused= False
	else:

		pygame.mixer.music.pause()
		paused=True

# goint to the next song
def next_song():
	#getting know the playing song
	next_one = song_box.curselection()
	#adding one to current song number
	next_one = next_one[0]+1
	#grab the title from playlist
	song = song_box.get(next_one)
	#adding directory structure and mp3 to song title
	song = f'C:/MUSIC PLAYER/audio/{song}.mp3'

    #loading and playing the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#clearing the active bar
	song_box.selection_clear(0,END)

	#activate the new song bar
	song_box.activate(next_one)

	#set active bar to next song
	song_box.selection_set(next_one,last=None)

#goint to the previous song
def previous_song():
	#getting know the playing song
	next_one = song_box.curselection()
	#adding one to current song number
	next_one = next_one[0]-1
	#grab the title from playlist
	song = song_box.get(next_one)
	#adding directory structure and mp3 to song title
	song = f'C:/MUSIC PLAYER/audio/{song}.mp3'

    #loading and playing the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#clearing the active bar
	song_box.selection_clear(0,END)

	#activate the new song bar
	song_box.activate(next_one)

	#set active bar to next song
	song_box.selection_set(next_one,last=None)

# deleting one song from playlist
def delete_song():
	#getting current song and deleting it
	song_box.delete(ANCHOR)
	pygame.mixer.music.stop()

#deleting more songs
def delete_all_song():

	song_box.delete(0,END)
	#stoping music if its playing
	pygame.mixer.music.stop()


	



# create playlist box
song_box = Listbox(root, bg="black" , fg="yellow" , width=60,selectbackground="grey",selectforeground="black")
song_box.pack(pady=20)

# Define player control buttons images
play_btn_img= PhotoImage(file="C:\MUSIC PLAYER\icons\play.png")
pause_btn_img=PhotoImage(file="C:\MUSIC PLAYER\icons\pause.png")
forward_btn_img=PhotoImage(file="C:\MUSIC PLAYER\icons\orward.png")
back_btn_img=PhotoImage(file="C:\MUSIC PLAYER\icons\previous.png")
stop_btn_img=PhotoImage(file="C:\MUSIC PLAYER\icons\stop.png")

#create player control frame
control_frame= Frame(root)
control_frame.pack()


#create player control buttons
play_button= Button(control_frame,image=play_btn_img ,borderwidth=0,command=play)
pause_button=Button(control_frame,image=pause_btn_img ,borderwidth=0,command= lambda:pause(paused))
forward_button=Button(control_frame,image=forward_btn_img ,borderwidth=0,command=next_song)
back_button=Button(control_frame,image=back_btn_img ,borderwidth=0,command=previous_song)
stop_button=Button(control_frame,image=stop_btn_img ,borderwidth=0,command=stop)


play_button.grid(row=0,column=2, padx=10)
pause_button.grid(row=0,column=3,padx=10)
forward_button.grid(row=0,column=1,padx=10)
back_button.grid(row=0,column=0,padx=10)
stop_button.grid(row=0,column=4,padx=10)


#create menu
my_menu=Menu(root)
root.config(menu=my_menu)

# add song menu
add_song_menu= Menu(my_menu)
my_menu.add_cascade(label="Add songs",menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=add_song)
add_song_menu.add_command(label="Add many song to playlist",command=add_many_song)

# remove song menu
remove_song_menu= Menu(my_menu)
my_menu.add_cascade(label="Remove songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete one song from playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All song to playlist",command=delete_all_song)


#create status bar
status_bar = Label(root,text=" ",bd=1, relief=GROOVE , anchor=E)
status_bar.pack(fill=X, side=BOTTOM,ipady=2)






root.mainloop()