import cv2
import numpy as np
import pdb
import matplotlib.cm as cm
from sound_output import start_sound_output, sound_process
from multiprocessing import Process, Pipe

def find_faces(input):

    faces = frontal_faces_cascade.detectMultiScale(input, 1.3, 5)

    #if np.asarray(faces).size == 0:
        #faces = profile_faces_cascade.detectMultiScale(input, 1.3, 5)

    centers = []
    for (x,y,w,h) in faces:
        centers.append((int(x + (w/2)), int(y + (h/2))))

    return centers, faces

def draw_faces(grayscale_frame, frame, faces, centers):

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if len(centers) > 0:
            cv2.circle(frame,centers[0],5,(0,0,255),2)
        roi_gray = grayscale_frame[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
        #smiles = smile_cascade.detectMultiScale(roi_gray)
        #for (ex, ey, ew, eh) in smiles:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            

    return frame

def color_frame(frame, scale, centers):

    if len(centers) > 0:
        factor = int((centers[0][1] - frame.shape[1] / 2) / 10)
    else:
        factor = 0

    #factor = scale * factor
    factor = factor

    frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    b = np.roll(np.squeeze((cm.prism(np.arange(256))[:,2]*255).astype(np.uint8)), factor)
    g = np.roll(np.squeeze((cm.prism(np.arange(256))[:,1]*255).astype(np.uint8)), factor)
    r = np.roll(np.squeeze((cm.prism(np.arange(256))[:,0]*255).astype(np.uint8)), factor)

    frame_b = cv2.LUT(frame_grayscale, b)
    frame_g = cv2.LUT(frame_grayscale, g)
    frame_r = cv2.LUT(frame_grayscale, r)

    frame = cv2.merge((frame_b,frame_g,frame_r))

    return frame

def main():
    lstFoundFaces = []
    lstFoundCenters = []
    cv2.namedWindow("Video")
    frames = 0
    #parent_conn, child_conn = Pipe()
    #p = Process(target=sound_process, args=(child_conn,))
    #p.start()
    start_sound_output()
    while True:
        frames += 1

        _, frame = cap.read()
        frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        centers, faces = find_faces(frame_grayscale)

        if len(centers) > 0:
            print(int(centers[0][1] - frame.shape[1] / 2))

        if np.asarray(faces).size == 0:
            faces = lstFoundFaces
            centers = lstFoundCenters
        else:
            lstFoundFaces = faces
            lstFoundCenters = centers

        cv2.imshow("Video", draw_faces(frame_grayscale, color_frame(frame, frames, centers), faces, centers));

        k = cv2.waitKey(5) & 0xFF


if __name__ == '__main__':
	
    #frontal_faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    frontal_faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
    #frontal_faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
    #frontal_faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt_tree.xml')
    #smile_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_smile.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
    #profile_faces_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_profileface.xml')


    cap = cv2.VideoCapture(0)

    main()
