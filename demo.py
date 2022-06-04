import navpy
import gmplot
import numpy as np
import pandas as pd
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt

import os

SPRINT_VEL_MIN = 1.6


def lla2ned(df):
	lattitude, longitude, altitude = df['latitude'], df['longitude'], df['altitude']
	North, East, Down =[], [], []

	lat_ref, lon_ref, alt_ref = df['latitude'].mean() ,df['longitude'].mean() ,df['altitude'].mean()

	for i in range(len(lattitude)):
		N, E, D = navpy.lla2ned(lattitude[i], longitude[i],  altitude[i],lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
		North.append(N)
		East.append(-E)
		Down.append(D)

	df['North'] = North
	df['East'] = East
	df['Down'] = Down

	return df
	
	
def process_data(df):

	North, East, Down = df['North'], df['East'], df['Down'] 
	total_distance, sprint_distance, top_speed = 0, 0, 0
	
	for i in range(len(North)):
		if i > 1 and i < len(North) -1:
			dx = North[i + 1] - North[i - 1]
			dy = East[i + 1] - East[i - 1]
			ds = np.sqrt(dx**2 + dy**2)
			dt = df['time'][i + 1] - df['time'][i - 1]
			heading = df['heading'][i]#np.arctan2(dy,dx)
			velocity  = df['velocity'][i]#ds / dt
			#rate = heading / dt
			if velocity > 0.2:
				total_distance += ds
			if velocity > SPRINT_VEL_MIN:
				sprint_distance +=ds

	df['smoothed_velocity'] = df['velocity'].ewm(span=10).mean()
	df['smoothed_heading'] = df['heading'].ewm(span=10).mean()
	top_speed = df['velocity'].max()
	print(f'Total Distance : {total_distance:.2f} meter	Sprint Distance : {sprint_distance:.2f} meter  Top Speed : {top_speed:.2f} meter/second')
	
	return df


def show_data(arg):
	df_gps =arg
	df_gps = lla2ned(df_gps)
	df_gps= process_data(df_gps)
	# Initialise the subplot function using number of rows and columns
	figure, axis = plt.subplots(2, 2, figsize=(10, 10))
	figure.canvas.set_window_title('Test')
	figure.suptitle('Player Performance', fontsize=12)	
	# For Sine Function
	axis[0, 0].plot(df_gps['North'], df_gps['East'])
	axis[0, 0].set_title("Player Path")
	  
	# For Cosine Function
	axis[0, 1].plot(df_gps['time'], df_gps['smoothed_velocity'])
	axis[0, 1].set_title("Velocity vs Time")
	  
	# For Tangent Function
	axis[1, 0].plot(df_gps['time'], df_gps['smoothed_heading'])
	axis[1, 0].set_title("Heading vs Time")
	  
	# For Tanh Function
	axis[1, 1].plot(df_gps['time'], df_gps['altitude'])
	axis[1, 1].set_title("Test Numbers")
	  
	# Combine all the operations and display


	gmap = gmplot.GoogleMapPlotter(df_gps['latitude'][0], df_gps['longitude'][0], 20)
	gmap.heatmap(df_gps['latitude'], df_gps['longitude'])
	
	
	
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
	
	
	path = os.getcwd()
	log_path = path + "\\Data\\"
	listdir = os.listdir(path)
	if 'Data' not in listdir:
		os.mkdir(log_path)
	os.mkdir(log_path + dt_string)
	os.chdir(log_path + dt_string)
	#print(path)
	#print(log_path)
	#print(os.listdir(path))
	#print(os.listdir(log_path))
	gmap.draw(dt_string + ".html")
	webbrowser.open(dt_string + ".html") 
	plt.savefig( dt_string +'.png')
	df_gps.to_csv( dt_string +'.csv')
	os.chdir(path)

	plt.show()

if __name__ == "__main__":
	print(__file__)
	filename = '2022-03-08-16-59-51.csv'

	df = pd.read_csv(filename)
	#print(df.head())
	print(df.columns)
	show_data(df)
