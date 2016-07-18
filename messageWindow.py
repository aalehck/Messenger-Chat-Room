#!/usr/bin/env python
import Tkinter
import thread
import zmq

def subscriberThread(socket, chatBox):
	while(True):

		[address, contents] = socket.subscriber.recv_multipart(zmq.NOBLOCK)
		print contents
		chatBox.config(state="normal")
		chatBox.insert("end", "{contents}".format(contents=contents))
		chatBox.config(state="disabled")

class messageWindow:
	def __init__(self, root, client, name):
		self.name = name
		self.client = client
		self.window = Tkinter.Toplevel()
		self.messageFrame = Tkinter.Frame(self.window)
		self.chatBox = Tkinter.Text(self.window, height=20, width=80)
		self.inputBox = Tkinter.Entry(self.messageFrame, width=50)

		Tkinter.Label(self.messageFrame, text="Text:").grid(row=0, column=0, sticky=('W'))
		Tkinter.Button(self.window, text='Send', command= lambda: self.enterDisplayText(self.chatBox, self.inputBox, client)).grid(row=1, column=2)
		self.window.bind('<Return>', lambda x: self.enterDisplayText(self.chatBox, self.inputBox, self.client))
		self.messageFrame.grid(row=1, column=0)
		self.chatBox.grid(row=0, columnspan=2)
		self.inputBox.grid(row=0, column=1)

		self.window.title(self.name)

	def enterDisplayText(self, chatBox, inputBox, client):
		self.chatBox.config(state="normal")
		self.client.sendMessage(self.name , "{string}\n".format(string=self.inputBox.get()))
		text = self.inputBox.get()
		self.inputBox.delete(0, len(text))

		self.chatBox.config(state="disabled")
