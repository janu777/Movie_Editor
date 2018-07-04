import cv2
import os
import time
import video_settings as VS
import moviepy.editor as mpe
import numpy as np
def video_collector(input_path,OUT):
	cap = cv2.VideoCapture(input_path)
	ret, frame = cap.read()
	print(input_path)
	print(ret)
	fps = cap.get(cv2.CAP_PROP_FPS)
	two_seconds=fps*2
	total_frames_collected=0
	collect_flag  = 0
	text = ''
	cv2.namedWindow("VIDEO_EDITOR", cv2.WINDOW_NORMAL)
	while ret:
		ret, frame = cap.read()
		if ret:
			frame = cv2.resize(frame,(VS.width,VS.height),interpolation = cv2.INTER_CUBIC)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,str(text),(100,50), font, 1,(255,255,255),2,cv2.LINE_AA)
			cv2.imshow("VIDEO_EDITOR",frame)

			if (total_frames_collected>=two_seconds):               
				collect_flag=0
				total_frames_collected=0
				text = ''

			key = chr(cv2.waitKey(0) & 255)
			if key == 'q': break
			if key == 'e': 
				text = input()
				collect_flag = 1
				print('edit') 
			if key == 'c' or collect_flag == 1: 
				if collect_flag == 1:
					total_frames_collected+=1
					font = cv2.FONT_HERSHEY_SIMPLEX
					cv2.putText(frame,str(text),(100,50), font, 1,(255,0,255),2,cv2.LINE_AA)
				OUT.write(frame)	
				print('collect')
		else:
			break
		#cap.release()
	cv2.destroyWindow("VIDEO_EDITOR")


def read_key():
	while True:
		cv2.namedWindow("VIDEO_EDITOR", cv2.WINDOW_NORMAL)
		key = chr(cv2.waitKey(0) & 255)
		print(key)

def add_audio(audio_path,video_path,output_path):
	final = mpe.VideoFileClip(video_path)
	audio = mpe.AudioFileClip(audio_path)
	final = final.set_audio(audio)
	final.write_videofile(output_path)

if __name__ == '__main__':
	flag = 0
	audio_path = VS.audio_to_add_path+'/'+VS.audio_name
	video_path = VS.output_video_path+'/'+VS.output_filename
	output_path = VS.output_video_path+'/'+VS.output_video_name
	for videonumber in np.arange(1,15):
		input_path = VS.videos_to_edit_path +'/'+ str(videonumber)+'.mp4'
		print(input_path)
		if flag == 0:
			cap = cv2.VideoCapture(input_path)
			fps = cap.get(cv2.CAP_PROP_FPS)
			ret, frame = cap.read()
			width,height = VS.width,VS.height
			OUT = cv2.VideoWriter(video_path, 0x00000020, fps, (width,height))
			cap.release()
			flag = 1
		video_collector(input_path,OUT)
	#if flag == 1:
	OUT.release()
	add_audio(audio_path,video_path,output_path)

