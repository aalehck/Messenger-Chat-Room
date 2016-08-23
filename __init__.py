#!/usr/bin/env python

import Tkinter
import argparse
import thread
from messageSocket import messageClient
from messageWindow import messageWindow

def subscriberThread(socket, conversations, chatBox):
	while(True):
		[address, contents] = socket.subscriber.recv_multipart()
		print contents
                
                conversations[address].text.append("{}\n".format(contents))

                if socket.currentConversation == address:
                        chatBox.config(state="normal")
                        chatBox.insert("end", "{contents}\n".format(contents=contents))
                        chatBox.config(state="disabled")

def enterDisplayText(chatBox, inputBox, client, conversations):
        chatBox.config(state="normal")
        text = inputBox.get()

        client.sendMessage(client.currentConversation, text)
        #conversations[client.currentConversation].text.append(text)
        inputBox.delete(0, len(text))
        chatBox.config(state="disabled")
        

def createNewThread(conversationFrame, client, root, conversations, chatBox):
	window = Tkinter.Toplevel(width=100, height=100)
	nameInput = Tkinter.Entry(window, width=30)
	Tkinter.Label(window, text="Enter chatroom name or username:").grid(row=0, column=0)
	Tkinter.Button(window, text='Send', command= lambda: connectConversation(nameInput, conversationFrame, window, client, root, conversations, chatBox)).grid(row=0, column=2)
	nameInput.grid(row=0, column=1 )
	window.bind('<Return>', lambda x: connectConversation(nameInput, conversationFrame, window, client, root, conversations, chatBox))
	#conversationBox.config(state="disabled")

def connectConversation(nameInput, conversationFrame, window, client, root, conversations, chatBox):
	string = nameInput.get()
        label = Tkinter.Label(conversationFrame, text=string)
       
	window.withdraw()

	client.createNewConnection(string)
	conversations[string] = messageWindow(root, client, string)
        label.bind("<Button-1>", lambda x: reopenConversationWindow(conversations, string, client, chatBox))
        label.grid(sticky=('W'))
        reopenConversationWindow(conversations, string, client, chatBox)

def reopenConversationWindow(conversations, identifier, client, chatBox):
        if client.currentConversation != identifier:
                client.currentConversation = identifier
                chatBox.config(state="normal")
                chatBox.delete(1.0, "end")
                chatBox.insert("end", "".join(conversations[identifier].text))
                chatBox.config(state="disable")

def main():
	parser = argparse.ArgumentParser(description='Name For Chat Account',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('accountName', type=str)
	args=parser.parse_args()

	conversations = {}
	client = messageClient("localhost", args.accountName)

	root = Tkinter.Tk()
	conversationFrame = Tkinter.Frame(root)
	messageFrame = Tkinter.Frame(root)

	chatBox = Tkinter.Text(root, height=20, width=80)
	inputBox = Tkinter.Entry(messageFrame, width=50)

	Tkinter.Label(messageFrame, text="Text:").grid(row=0, column=0, sticky=('W'))
	Tkinter.Button(root, text='Send', command= lambda: enterDisplayText(chatBox, inputBox, client, conversations)).grid(row=1, column=2)
	Tkinter.Button(conversationFrame, text='Create New Thread', command= lambda: createNewThread(conversationFrame, client, root, conversations, chatBox)).grid(row=0, sticky=('N','W'), pady=1)

	root.bind('<Return>', lambda x: enterDisplayText(chatBox, inputBox, client, conversations))
	chatBox.config(state="disabled")

	conversationFrame.grid(row=0, column=2, sticky=('N'))
	messageFrame.grid(row=1, column=0)
	chatBox.grid(row=0, columnspan=2)
	inputBox.grid(row=0, column=1)

	root.rowconfigure(1, weight=3)
	root.columnconfigure(2, weight=3)
	conversationFrame.rowconfigure(0, weight=5)

	thread.start_new_thread(subscriberThread, (client, conversations, chatBox))

	root.mainloop()

if __name__ == "__main__":
	main()
