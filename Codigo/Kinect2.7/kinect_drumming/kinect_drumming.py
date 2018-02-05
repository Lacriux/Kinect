#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

import mido
from mido import Message

import time
import sys

threshold = 500
current_depth = 130

notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def show_depth():
	global threshold
	global current_depth

	depth, timestamp = freenect.sync_get_depth()	
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth

def show_depth2():
	global threshold
	global current_depth
	
	new_depth = current_depth + 25
	
	depth, timestamp = freenect.sync_get_depth()	
	depth = 255 * np.logical_and(depth >= new_depth - threshold, depth <= new_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth

def show_depth3():
	global threshold
	global current_depth
	
	new_depth = current_depth + 50
	
	depth, timestamp = freenect.sync_get_depth()	
	depth = 255 * np.logical_and(depth >= new_depth - threshold, depth <= new_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth

def get_video():
	video,_ = freenect.sync_get_video()

	return video
	
def show_video(image, image_name):	
	cv2.namedWindow(image_name)
	
def find_centroid(imagen, imagen2):
	#http://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv

	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours, hier = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)	
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < 100000:
			cv2.drawContours(imagen,[cnt],0,(200,255,200),2)
			
			#centroide	
			#http://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html#gsc.tab=0
			M = cv2.moments(cnt)
			
			if (int(M['m00'])!=0):
				centro = (int(M['m10']/M['m00'])+ 25,int(M['m01']/M['m00']))						
				cv2.circle(imagen, centro, 16, (255,255,255), -1)
				cv2.circle(imagen2, centro, 16, (255,255,255), -1)
				list_centros.append(centro)	
	
	return {'img':imagen, 'centr':list_centros, 'img2': imagen2}



def draw_lines_p(imagen): #draws lines to divide the camara for user
	
	#vetical lines
	cv2.line(imagen,(213,0),(213,480),(255,250,250),2)
	
	cv2.line(imagen,(426,0),(426,480),(255,250,250),2)
	
	return imagen

def draw_lines_m(imagen): #draws lines to divide the camara for user
	
	#vetical lines
	cv2.line(imagen,(160,0),(160,480),(250,250,250),2)
	cv2.line(imagen,(320,0),(320,480),(250,250,250),2)
	cv2.line(imagen,(480,0),(480,480),(250,250,250),2)
	
	#horizontal lines
	cv2.line(imagen, (0, 240), (640, 240), (255,250,250),2)

	return imagen

def draw_lines_g(imagen): #draws lines to divide the camera for user
	
	#vertical lines
	cv2.line(imagen,(160,0),(160,480),(250,250,250),2)
	cv2.line(imagen,(320,0),(320,480),(250,250,250),2)
	cv2.line(imagen,(480,0),(480,480),(250,250,250),2)
	
	#horizontal lines
	cv2.line(imagen,(0,120),(640,120),(250,250,250),2)
	cv2.line(imagen,(0,240),(640,240),(250,250,250),2)
	cv2.line(imagen,(0,360),(640,360),(250,250,250),2)

	return imagen


def get_cuadrantes_p(centroides):
	
	#  |  | 
	# 1| 2| 3
	#  |  | 
	
	cuadrantes = []
	for i in range(len(centroides)):
		x = centroides[i][0]
		y = centroides[i][1]
	
		if (x < 213):
			cuadrantes.append(1)
		elif (x < 426):
			cuadrantes.append(2)
		else:
			cuadrantes.append(3)

	
	return cuadrantes

def get_cuadrantes_g(centroides):
	
	# 1 | 2 | 3 | 4
	#---------------
	# 5 | 6 | 7 | 8
	#---------------
	# 9 |10 |11 |12
	#---------------
	#13 |14 |15 |16
	
	cuadrantes = []
	for i in range(len(centroides)):
		x = centroides[i][0]
		y = centroides[i][1]
	
		if (x < 160):
			if (y < 120):
				cuadrantes.append(1)
			elif (y < 240):
				cuadrantes.append(5)
			elif (y < 360):
				cuadrantes.append(9)
			else:
				cuadrantes.append(13)
		elif (x < 320):
			if (y < 120):
				cuadrantes.append(2)
			elif (y < 240):
				cuadrantes.append(6)
			elif (y < 360):
				cuadrantes.append(10)
			else:
				cuadrantes.append(14)
		elif (x < 480):
			if (y < 120):
				cuadrantes.append(3)
			elif (y < 240):
				cuadrantes.append(7)
			elif (y < 360):
				cuadrantes.append(11)
			else:
				cuadrantes.append(15)
		else:
			if (y < 120):
				cuadrantes.append(4)
			elif (y < 240):
				cuadrantes.append(8)
			elif (y < 360):
				cuadrantes.append(12)
			else:
				cuadrantes.append(16)
	
	return cuadrantes

def get_cuadrantes_m(centroides):
	
	# 1 | 2 | 3 | 4 |
	#----------------
	# 5 | 6 | 7 | 8 |
	
	cuadrantes = []
	for i in range(len(centroides)):
		x = centroides[i][0]
		y = centroides[i][1]
	
		if (y < 240):
			if (x < 160):
				cuadrantes.append(1)
			elif (x < 320):
				cuadrantes.append(2)
			elif (x < 480):
				cuadrantes.append(3)
			else:
				cuadrantes.append(4)
		else:
			if (x < 160):
				cuadrantes.append(5)
			elif (x < 320):
				cuadrantes.append(6)
			elif (x < 480):
				cuadrantes.append(7)
			else:
				cuadrantes.append(8)
	
	return cuadrantes

def show_image(imagen, mensaje):
	
	cv2.imshow(mensaje, imagen)

def flip_image(imagen):
	#mirror image
	#http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
	
	imagen = cv2.flip(imagen,1)
	
	return imagen

def send_midi_message_p(cuadrantes, volume, nota_inicial=60):
	global t0, t1
	#   |   | 
	# 1	| 2 | 3	
	#   |   | 
	
	#midi objects
	#https://mido.readthedocs.org/en/latest/
	
	#definicion de notas
	f4 = Message("note_on", note=nota_inicial, velocity=volume)
	f40 = Message("note_off", note=nota_inicial, velocity=volume)
	
	g4 = Message("note_on", note=(nota_inicial+2), velocity=volume)
	g40 = Message("note_off", note=(nota_inicial+2), velocity=volume)

	a4 = Message("note_on", note=(nota_inicial+4), velocity=volume)
	a40 = Message("note_off", note=(nota_inicial+4), velocity=volume)
	
	
	if (1 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)	
	
	if (2 in cuadrantes):
		output.send(g4)
	else:
		output.send(g40)
		
	if (3 in cuadrantes):
		output.send(a4)
	else:
		output.send(a40)

def send_midi_message_g(cuadrantes, volume, nota_inicial=60):
	global t0, t1
	# 1 | 2 | 3 | 4
	#---------------
	# 5 | 6 | 7 | 8
	#---------------
	# 9 |10 |11 |12
	#---------------
	#13 |14 |15 |16
	
	#midi objects
	#https://mido.readthedocs.org/en/latest/
	
	#definicion de notas
	c4 = Message("note_on", note=nota_inicial, velocity=volume)
	c40 = Message("note_off", note=nota_inicial, velocity=volume)

	c4s = Message("note_on", note=nota_inicial+1, velocity=volume)
	c4s0 = Message("note_off", note=nota_inicial+1, velocity=volume)
	
	d4 = Message("note_on", note=(nota_inicial+2), velocity=volume)
	d40 = Message("note_off", note=(nota_inicial+2), velocity=volume)

	d4s = Message("note_on", note=(nota_inicial+3), velocity=volume)
	d4s0 = Message("note_off", note=(nota_inicial+3), velocity=volume)

	e4 = Message("note_on", note=(nota_inicial+4), velocity=volume)
	e40 = Message("note_off", note=(nota_inicial+4), velocity=volume)

	f4 = Message("note_on", note=(nota_inicial+5), velocity=volume)
	f40 = Message("note_off", note=(nota_inicial+5), velocity=volume)
	
	f4s = Message("note_on", note=(nota_inicial+6), velocity=volume)
	f4s0 = Message("note_off", note=(nota_inicial+6), velocity=volume)

	g4 = Message("note_on", note=(nota_inicial+7), velocity=volume)
	g40 = Message("note_off", note=(nota_inicial+7), velocity=volume)
	
	g4s = Message("note_on", note=(nota_inicial+8), velocity=volume)
	g4s0 = Message("note_off", note=(nota_inicial+8), velocity=volume)

	a4 = Message("note_on", note=(nota_inicial+9), velocity=volume)
	a40 = Message("note_off", note=(nota_inicial+9), velocity=volume)
	
	a4s = Message("note_on", note=(nota_inicial+10), velocity=volume)
	a4s0 = Message("note_off", note=(nota_inicial+10), velocity=volume)
	
	b4 = Message("note_on", note=(nota_inicial+11), velocity=volume)
	b40 = Message("note_off", note=(nota_inicial+11), velocity=volume)
	
	c5 = Message("note_on", note=(nota_inicial+12), velocity=volume)
	c50 = Message("note_off", note=(nota_inicial+12), velocity=volume)

	c5s = Message("note_on", note=nota_inicial+13, velocity=volume)
	c5s0 = Message("note_off", note=nota_inicial+13, velocity=volume)
	
	d5 = Message("note_on", note=(nota_inicial+14), velocity=volume)
	d50 = Message("note_off", note=(nota_inicial+14),velocity=volume)
	
	if (1 in cuadrantes):
		output.send(c4)
	else:
		output.send(c40)

	if (2 in cuadrantes):
		output.send(c4s)
	else:
		output.send(c4s0)	
	
	if (3 in cuadrantes):
		output.send(d4)
	else:
		output.send(d40)

	if (4 in cuadrantes):
		output.send(d4s)
	else:
		output.send(d4s0)
		
	if (5 in cuadrantes):
		output.send(e4)
	else:
		output.send(e40)
		
	if (6 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)

	if (7 in cuadrantes):
		output.send(f4s)
	else:
		output.send(f4s0)
		
	if (8 in cuadrantes):
		output.send(g4)
	else:
		output.send(g40)

	if (9 in cuadrantes):
		output.send(g4s)
	else:
		output.send(g4s0)
		
	if (10 in cuadrantes):
		output.send(a4)
	else:
		output.send(a40)

	if (11 in cuadrantes):
		output.send(a4s)
	else:
		output.send(a4s0)
		
	if (12 in cuadrantes):
		output.send(b4)
	else:
		output.send(b40)
		
	if (13 in cuadrantes):
		output.send(c5)
	else:
		output.send(c50)

	if (14 in cuadrantes):
		output.send(c5s)
	else:
		output.send(c5s0)

	if (15 in cuadrantes):
		output.send(d5)
	else:
		output.send(d50)
		
def send_midi_message_m(cuadrantes, volume, nota_inicial=60):
	# 1 | 2 | 3 | 4 
	#---------------
	# 5 | 6 | 7 | 8 
	
	#definicion de notas
	c4 = Message("note_on", note=nota_inicial, velocity=volume)
	c40 = Message("note_off", note=nota_inicial, velocity=volume)
	
	d4 = Message("note_on", note=(nota_inicial+2), velocity=volume)
	d40 = Message("note_off", note=(nota_inicial+2), velocity=volume)

	e4 = Message("note_on", note=(nota_inicial+4), velocity=volume)
	e40 = Message("note_off", note=(nota_inicial+4), velocity=volume)
	
	f4 = Message("note_on", note=(nota_inicial+5), velocity=volume)
	f40 = Message("note_off", note=(nota_inicial+5), velocity=volume)
	
	g4 = Message("note_on", note=(nota_inicial+7), velocity=volume)
	g40 = Message("note_off", note=(nota_inicial+7), velocity=volume)
	
	a4 = Message("note_on", note=(nota_inicial+9), velocity=volume)
	a40 = Message("note_off", note=(nota_inicial+9), velocity=volume)
	
	b4 = Message("note_on", note=(nota_inicial+11), velocity=volume)
	b40 = Message("note_off", note=(nota_inicial+11), velocity=volume)
	
	c5 = Message("note_on", note=(nota_inicial+12), velocity=volume)
	c50 = Message("note_off", note=(nota_inicial+12), velocity=volume)
	
	d5 = Message("note_on", note=(nota_inicial+14), velocity=volume)
	d50 = Message("note_off", note=(nota_inicial+14), velocity=volume)
	
	if (1 in cuadrantes):
		output.send(c4)
	else:
		output.send(c40)	
	
	if (2 in cuadrantes):
		output.send(d4)
	else:
		output.send(d40)
		
	if (3 in cuadrantes):
		output.send(e4)
	else:
		output.send(e40)
		
	if (4 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)
		
	if (5 in cuadrantes):
		output.send(g4)
	else:
		output.send(g40)
		
	if (6 in cuadrantes):
		output.send(a4)
	else:
		output.send(a40)
		
	if (7 in cuadrantes):
		output.send(b4)
	else:
		output.send(b40)
		
	if (8 in cuadrantes):
		output.send(c5)
	else:
		output.send(c50)
		
	if (9 in cuadrantes):
		output.send(d5)
	else:
		output.send(d50)

def send_midi_message_m2(cuadrantes, volume, nota_inicial=60):
	# 1 | 2 | 3 | 4 
	#---------------
	# 5 | 6 | 7 | 8 
	
	#definicion de notas
	c4 = Message("note_on", note=nota_inicial, velocity=volume)
	c40 = Message("note_off", note=nota_inicial, velocity=volume)
	
	d4 = Message("note_on", note=(nota_inicial+2), velocity=volume)
	d40 = Message("note_off", note=(nota_inicial+2), velocity=volume)

	e4 = Message("note_on", note=(nota_inicial+3), velocity=volume)
	e40 = Message("note_off", note=(nota_inicial+3), velocity=volume)
	
	f4 = Message("note_on", note=(nota_inicial+5), velocity=volume)
	f40 = Message("note_off", note=(nota_inicial+5), velocity=volume)
	
	g4 = Message("note_on", note=(nota_inicial+7), velocity=volume)
	g40 = Message("note_off", note=(nota_inicial+7), velocity=volume)
	
	a4 = Message("note_on", note=(nota_inicial+8), velocity=volume)
	a40 = Message("note_off", note=(nota_inicial+8), velocity=volume)
	
	b4 = Message("note_on", note=(nota_inicial+10), velocity=volume)
	b40 = Message("note_off", note=(nota_inicial+10), velocity=volume)
	
	c5 = Message("note_on", note=(nota_inicial+12), velocity=volume)
	c50 = Message("note_off", note=(nota_inicial+12), velocity=volume)
	
	d5 = Message("note_on", note=(nota_inicial+14), velocity=volume)
	d50 = Message("note_off", note=(nota_inicial+14), velocity=volume)
	
	if (1 in cuadrantes):
		output.send(c4)
	else:
		output.send(c40)	
	
	if (2 in cuadrantes):
		output.send(d4)
	else:
		output.send(d40)
		
	if (3 in cuadrantes):
		output.send(e4)
	else:
		output.send(e40)
		
	if (4 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)
		
	if (5 in cuadrantes):
		output.send(g4)
	else:
		output.send(g40)
		
	if (6 in cuadrantes):
		output.send(a4)
	else:
		output.send(a40)
		
	if (7 in cuadrantes):
		output.send(b4)
	else:
		output.send(b40)
		
	if (8 in cuadrantes):
		output.send(c5)
	else:
		output.send(c50)
		
	if (9 in cuadrantes):
		output.send(d5)
	else:
		output.send(d50)

def define_note (str_nota):

	if(str_nota == "c"):
		return 60
	elif(str_nota == "d"):
		return 62
	elif(str_nota == "d#"):
		return 63
	elif(str_nota == "e"):
		return 64
	elif(str_nota == "f"):
		return 65
	elif(str_nota == "f#"):
		return 66
	elif(str_nota == "g"):
		return 67
	elif(str_nota == "g#"):
		return 68
	elif(str_nota == "a"):
		return 69
	elif(str_nota == "a#"):
		return 70
	elif(str_nota == "b"):
		return 71
	else:
		print "ERROR: La nota no es correcta"
		return 0

def define_lineas(str_divisiones):
	if(str_divisiones == "p"):
		#imagen_lineas = draw_lines_p(image2)
		imagen_lineas = draw_lines_p(image3)
		return 1
	elif(str_divisiones == "m" or str_divisiones == "m2"):
		#imagen_lineas = draw_lines_m(image2)
		imagen_lineas = draw_lines_m(image3)
		return 1
	elif(str_divisiones == "g"):
		#imagen_lineas = draw_lines_g(image2)
		imagen_lineas = draw_lines_g(image3)
		return 1
	else:
		print "ERROR"
		return 0


def cambiarNotas(str_nota, com):

	if str_nota == "c":
		if com == 100:
			print "no se puede bajar mas el tono"
			return "c"
		if com == 117:
			return "d"
	elif str_nota == "d":
		if com == 100:
			return "c"
		if com == 117:
			return "d#"
	elif(str_nota == "d#"):
		if com == 100:
			return "d"
		if com == 117:
			return "e"
	elif(str_nota == "e"):
		if com == 100:
			return "d#"
		if com == 117:
			return "f"
	elif(str_nota == "f"):
		if com == 100:
			return "e"
		if com == 117:
			return "f#"
	elif(str_nota == "f#"):
		if com == 100:
			return "f"
		if com == 117:
			return "g"
	elif(str_nota == "g"):
		if com == 100:
			return "f#"
		if com == 117:
			return "g#"
	elif(str_nota == "g#"):
		if com == 100:
			return "g"
		if com == 117:
			return "a"
	elif(str_nota == "a"):
		if com == 100:
			return "g#"
		if com == 117:
			return "a#"
	elif(str_nota == "a#"):
		if com == 100:
			return "a"
		if com == 117:
			return "b"
	elif(str_nota == "b"):
		if com == 100:
			return "a#"
		if com == 117:
			print "No se puede subir mas la nota"
			return "b"

def cambiar_divisiones(com):
		if com == 112:
			print "Ya esta en modo 1x3"
			return "p"
		if com == 109:
			print "cambiando a modo 2x2 diatonco mayor"
			return "m"
		if com == 110:
			print "cambiado a modo 2x2 diatonico menor"
			return "m2"
		if com == 103:
			print "cambiando a 4x4"
			return "g"

def imprimir_notas_m(image, nota_inicial):
	if nota_inicial == 60:
		aux = 0
	elif nota_inicial == 62:
		aux = 2
	elif nota_inicial == 63:
		aux = 3
	elif nota_inicial == 64:
		aux = 4
	elif nota_inicial == 65:
		aux = 5
	elif nota_inicial == 66:
		aux = 6
	elif nota_inicial == 67:
		aux = 7
	elif nota_inicial == 68:
		aux = 8
	elif nota_inicial == 69:
		aux = 9
	elif nota_inicial == 70:
		aux = 10
	elif nota_inicial == 71:
		aux = 11

	notas2 = [notas[aux], notas[aux+2], notas[aux+4], notas[aux+5], notas[aux+7], notas[aux+9], notas[aux+11], notas[aux]]
	
	cv2.putText(image,notas2[0], (0,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[1], (160,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[2], (320,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[3], (480,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[4], (0,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[5], (160,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[6], (320,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[7], (480,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)

def imprimir_notas_g(image, nota_inicial):
	if nota_inicial == 60:
		aux = 0
	elif nota_inicial == 62:
		aux = 2
	elif nota_inicial == 63:
		aux = 3
	elif nota_inicial == 64:
		aux = 4
	elif nota_inicial == 65:
		aux = 5
	elif nota_inicial == 66:
		aux = 6
	elif nota_inicial == 67:
		aux = 7
	elif nota_inicial == 68:
		aux = 8
	elif nota_inicial == 69:
		aux = 9
	elif nota_inicial == 70:
		aux = 10
	elif nota_inicial == 71:
		aux = 11

	notas2 = [notas[aux], notas[aux+1], notas[aux+2], notas[aux+3], notas[aux+4], notas[aux+5], notas[aux+6], notas[aux+7], notas[aux+8], notas[aux+9], notas[aux+10], notas[aux+11], notas[aux+12], notas[aux+13], notas[aux+14]]
	
	cv2.putText(image,notas2[0], (0,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[1], (160,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[2], (320,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[3], (480,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[4], (0,230), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[5], (160,230), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[6], (320,230), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[7], (480,230), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[8], (0,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[9], (160,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[10], (320,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[11], (480,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[12], (0,470), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[13], (160,470), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
	cv2.putText(image,notas2[14], (320,470), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)

def imprimir_notas_n(image, nota_inicial):
	if nota_inicial == 60:
		aux = 0
	elif nota_inicial == 62:
		aux = 2
	elif nota_inicial == 63:
		aux = 3
	elif nota_inicial == 64:
		aux = 4
	elif nota_inicial == 65:
		aux = 5
	elif nota_inicial == 66:
		aux = 6
	elif nota_inicial == 67:
		aux = 7
	elif nota_inicial == 68:
		aux = 8
	elif nota_inicial == 69:
		aux = 9
	elif nota_inicial == 70:
		aux = 10
	elif nota_inicial == 71:
		aux = 11

	notas2 = [notas[aux], notas[aux+2], notas[aux+3], notas[aux+5], notas[aux+7], notas[aux+8], notas[aux+10], notas[aux]]
	
	cv2.putText(image,notas2[0], (0,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[1], (160,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[2], (320,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[3], (480,230), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[4], (0,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[5], (160,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[6], (320,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)
	cv2.putText(image,notas2[7], (480,470), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 3)

def calc_vol(cuadrantes, cuadrantes2, cuadrantes3):
	vol = 42
	if cuadrantes2:
		vol = 84
	if cuadrantes:
		vol = 127
	return vol

if __name__ == "__main__":
	print "Presione 'q' para salir"
	print "Para subir el tono presione u"
	print  "Para bajarlo presione d"
	print "Para cambiar de modo use las teclas p, m, g\np: 1x3 (Modo Opus)\nm: 2x4(Modo diatonico mayor) \nn: 2x4(Modo diatonico menor) \ng: 4x4(Modo Cromatico)"
	
	str_nota = 'c'
	str_divisiones = "g"
		
	output = mido.open_output()
	blank_image = np.zeros((480,640,3), np.uint8)

	while 1:
		
		image = show_depth()
		image4 = show_depth2()
		image5 = show_depth3()
		
		image = flip_image(image)
		image4 = flip_image(image4)
		image5 = flip_image(image5)

		image2 = get_video()
		image2 = flip_image(image2)
		
		rslt_fc = find_centroid(image, image2)
		rslt_fc2 = find_centroid(image4, image2)
		rslt_fc3 = find_centroid(image5, image2)
		
		image = rslt_fc['img']
		image2 = rslt_fc['img2']
		centroides = rslt_fc['centr']

		image4 = rslt_fc2['img']
		centroides2 = rslt_fc2['centr']

		image5 = rslt_fc3['img']
		centroides3 = rslt_fc3['centr']

		image3 = cv2.addWeighted(image2,0.5,blank_image,0.5,3)

		bool_lineas = define_lineas(str_divisiones)

		nota_inicial = define_note(str_nota)
		
		if not (nota_inicial and bool_lineas):
			print "Saliendo"
			break
		
		if str_divisiones == "m":
			#imprimir_notas_m(image2, nota_inicial)
			imprimir_notas_m(image3, nota_inicial)
		if str_divisiones == "m2":
			#imprimir_notas_n(image2, nota_inicial)
			imprimir_notas_n(image3, nota_inicial)
		if str_divisiones == "g":
			#imprimir_notas_g(image2, nota_inicial)
			imprimir_notas_g(image3, nota_inicial)
		
		if centroides or centroides2 or centroides3:
			if(str_divisiones == "p"):
				str_nota = 'f'
				cuadrantes = get_cuadrantes_p(centroides)
				cuadrantes2 = get_cuadrantes_p(centroides2)
				cuadrantes3 = get_cuadrantes_p(centroides3)
				volume = calc_vol(cuadrantes, cuadrantes2, cuadrantes3)
				send_midi_message_p(cuadrantes, volume, nota_inicial)
			elif(str_divisiones == "m"):
				cuadrantes = get_cuadrantes_m(centroides)
				cuadrantes2 = get_cuadrantes_m(centroides2)
				cuadrantes3 = get_cuadrantes_m(centroides3)
				volume = calc_vol(cuadrantes, cuadrantes2, cuadrantes3)
				send_midi_message_m(cuadrantes3, volume, nota_inicial)
			elif(str_divisiones == "m2"):
				cuadrantes = get_cuadrantes_m(centroides)
				cuadrantes2 = get_cuadrantes_m(centroides2)
				cuadrantes3 = get_cuadrantes_m(centroides3)
				volume = calc_vol(cuadrantes, cuadrantes2, cuadrantes3)
				send_midi_message_m2(cuadrantes3, volume, nota_inicial)
			elif(str_divisiones == "g"):
				cuadrantes = get_cuadrantes_g(centroides)
				cuadrantes2 = get_cuadrantes_g(centroides2)
				cuadrantes3 = get_cuadrantes_g(centroides3)
				volume = calc_vol(cuadrantes, cuadrantes2, cuadrantes3);
				send_midi_message_g(cuadrantes3, volume, nota_inicial)

		#show_image(image, "vol max")
		#show_video(image, "vol max")

		#show_image(image4, "vol med")
		#show_video(image4, "vol med")

		#show_image(image5, "vol min")
		#show_video(image5, "vol min")
	
		show_image(image3, "video")
		show_video(image3, "video")

		com = cv2.waitKey(10)
		
		if ('u' == chr(com & 255) or 'd' == chr(com & 255)):
			str_nota = cambiarNotas(str_nota, com)

		if ('p' == chr(com & 255) or 'm' == chr(com &255) or 'n' == chr(com & 255) or 'g' == chr(com & 255)):
			str_divisiones = cambiar_divisiones(com)
			
		if 'q' == chr(com & 255):
			break
			output.close()
