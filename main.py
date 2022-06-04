import json
import time
import socket
import requests
from demo import*

import pandas as pd
import tkinter as tk


class Application(tk.Frame):
	def __init__(self, master=None):
		self.status = 'disconnected'

		self.DEVICE_IP = self.ping_device()
		if self.DEVICE_IP:
			self.status = 'connected'

		print(f' Device IP  = {self.DEVICE_IP}')

		super().__init__(master)
		self.master = master
		self.master.geometry("320x240")
		self.pack()
		self.create_widgets()
		self.recording = False

		
	def find_device(self):
		IP = ''
		while True:
			try:
				IP = socket.gethostbyname('raspberrypi.local')
				time.sleep(1)
				if IP:
					break
			except Exception as e:
				print('Error! Code : {c}, Message :  {m}'.format(c = type(e).__name__, m = str(e)))
				#print(type(e).__name__)
				#if 
				print("Device Not Found")
		return IP
		
	def ping_device(self):
		IP =''
		try:
				IP = socket.gethostbyname('raspberrypi.local')
				return IP
		except Exception as e:
				return IP
				
	def create_widgets(self):
		self.start = tk.Button(self)
		self.start["text"] = "Start"
		self.start["command"] = self.started
		self.start.pack(fill = "both", expand = True, pady=5)

		self.stop = tk.Button(self)
		self.stop["text"] = "Stop"
		self.stop["command"] = self.stoped
		self.stop.pack(fill = "both", expand = True, pady=5)
		
		# TextBox Creation
		self.inputtxt = tk.Text(self, height = 1, width = 24)
		self.inputtxt.insert(tk.END, self.DEVICE_IP)
		self.inputtxt.pack(fill = "both", expand = True, pady=5)
		self.status =str(time.time())
		self.status_label = tk.Label(self, text=self.status,bd=1, relief=tk.SUNKEN, anchor=tk.W, bg = 'red')
		self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
		self.update_label()
	
	def update_label(self):
		self.status = 'disconnected'
		color = 'red'
		IP = self.ping_device()
		if IP:
			self.status = 'connected'
			color = 'green'
		#self.status = str(time.time())
		self.status_label.config(text=self.status,bg= color)
		#self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
		self.status_label.after(5000, self.update_label)
		
	def started(self):
		self.start.configure(bg="green")
		self.stop.configure(bg="white")
		self.recording = True

		print("Command Sent: start")
		inp = self.inputtxt.get(1.0, "end-1c")
		#print(inp)
		start_cmd = "http://"+ str(inp) +":5000/start"
		resp = requests.get(start_cmd)			
		print(resp.status_code)
		print(resp.text)

	
	def stoped(self):
		self.start.configure(bg="white")
		self.stop.configure(bg="red")
		print("Command Sent: Stoped")
		inp = self.inputtxt.get(1.0, "end-1c")
		#print(inp)
		stop_cmd = "http://"+ str(inp) +":5000/stop"
		data = requests.get(stop_cmd)
		print(data.status_code)
		print(data.text)
		data = json.loads(data.text)
		df = pd.DataFrame(data)
		df = df.fillna(0)
		df = df.fillna(0)
		#print(df.columns)
		#print(df.head())
		if self.recording and len(df) > 2:
			self.recording = False 
			self.foo(df)

	@staticmethod
	def foo(df):
		show_data(df)
		
		
def main():
	

	
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
	'''
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
	'''
if __name__ == "__main__":
	main()


