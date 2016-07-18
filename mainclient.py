#!/usr/bin/env python

import Tkinter
import argparse
import thread
from messageSocket import messageClient
from messageWindow import messageWindow

def subscriberThread(socket, conversations):
	while(True):
		[address, contents] = socket.subscriber.recv_multipart()
		print contents

		conversations[address].chatBox.config(state="normal")
		conversations[address].chatBox.insert("end", "{contents}".format(contents=contents))
		conversations[address].chatBox.config(state="disabled")

def createNewThread(conversationBox, client, root, conversations):
	window = Tkinter.Toplevel(width=100, height=100)
	nameInput = Tkinter.Entry(window, width=30)
	Tkinter.Label(window, text="Enter chatroom name or username:").grid(row=0, column=0)
	Tkinter.Button(window, text='Send', command= lambda: connectConversation(nameInput, conversationBox, window)).grid(row=0, column=2)
	nameInput.grid(row=0, column=1 )
	window.bind('<Return>', lambda x: connectConversation(nameInput, conversationBox, window, client, root, conversations))
	conversationBox.config(state="disabled")

def connectConversation(nameInput, conversationBox, window, client, root, conversations):
	conversationBox.config(state="normal")
	string = nameInput.get()
        convStart = conversationBox.index("end")
	conversationBox.insert("end", "{string}\n".format(string=string))
        conversationBox.tag_add(string,"{start}".format(start=convStart), "{start}.{length}".format(start=int(convStart), length=len(string)))
        conversationBox.tag_bind(string, "<1>", )
	window.withdraw()
	conversationBox.config(state="disabled")

	client.createNewConnection(string)
	conversations[string] = messageWindow(root, client, string)

def checkConversationWindow():

def main():
	parser = argparse.ArgumentParser(description='Name For Chat Account',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('accountName', type=str)
	args=parser.parse_args()

	conversations = {}
	client = messageClient("localhost", args.accountName)

	root = Tkinter.Tk()
	conversationFrame = Tkinter.Frame(root)
	#messageFrame = Tkinter.Frame(root)

	#chatBox = Tkinter.Text(root, height=20, width=80)
	#inputBox = Tkinter.Entry(messageFrame, width=50)
	conversationBox = Tkinter.Text(conversationFrame, height=15, width=20)

	#Tkinter.Label(messageFrame, text="Text:").grid(row=0, column=0, sticky=('W'))
	#Tkinter.Button(root, text='Send', command= lambda: enterDisplayText(chatBox, inputBox, client)).grid(row=1, column=2)
	Tkinter.Button(conversationFrame, text='Create New Thread', command= lambda: createNewThread(conversationBox, client, root, conversations)).grid(row=0, sticky=('N','W'), pady=1)

	#root.bind('<Return>', lambda x: enterDisplayText(chatBox, inputBox, client))
	#chatBox.config(state="disabled")

	conversationFrame.grid(row=0, column=2)
	#messageFrame.grid(row=1, column=0)
	#chatBox.grid(row=0, columnspan=2)
	#inputBox.grid(row=0, column=1)
	conversationBox.grid(row=1, sticky=('N','W'))

	root.rowconfigure(1, weight=3)
	root.columnconfigure(2, weight=3)
	conversationFrame.rowconfigure(0, weight=5)

	thread.start_new_thread(subscriberThread, (client, conversations))

	root.mainloop()

if __name__ == "__main__":
	main()
