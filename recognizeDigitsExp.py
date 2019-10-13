import os
import cv2
import numpy as np
from tkinter import *
from threading import Thread
from keras.models import load_model

def thresh_fn():

    def setThreshold():
        global thresh_value
        if t.get() in range(0,255):
            thresh_value = t.get()

    window = Tk()
    t = IntVar()
    window.geometry("250x200")
    window.title("Set Threshold")
    Label(window,text="Change Threshold here: (0 <= value <= 255)").pack()
    Entry(window,textvariable=t).pack()
    Button(window,text="Set Threshold",command=setThreshold).pack()
    window.mainloop()

def roi_fn():

    def setROI():
        global roi_top, roi_bottom, roi_left, roi_right
        roi_top = top.get()
        roi_bottom = bottom.get()
        roi_left = left.get()
        roi_right = right.get()

    window = Tk()
    window.geometry("300x300")
    left = IntVar()
    right = IntVar()
    top = IntVar()
    bottom = IntVar()
    window.title('Set ROI')
    Label(window,text="Change Rectangle parameters here:").pack()
    Label(window,text="Top left corner:").pack()
    Label(window,text="x:").pack()
    Entry(window,textvariable=left).pack()
    Label(window,text="y:").pack()
    Entry(window,textvariable=top).pack()
    Label(window,text="Bottom right corner:").pack()
    Label(window,text="x:").pack()
    Entry(window,textvariable=right).pack()
    Label(window,text="y:").pack()
    Entry(window,textvariable=bottom).pack()
    Button(window,text="Set ROI",command=setROI).pack()
    window.mainloop()



def cv_fn():
    
    model = None
    # loading pre-trained model
    if os.path.exists('MNIST_Digits.h5'):
        model = load_model('MNIST_Digits.h5')

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if model:
        print('Model Loaded!')
    else:
        return print('Model not found! Get the model file(.h5) from here - https://github.com/gauravc6/Digit-Recognizer.git')

    print('Initializing Capture...')
    print('Hit Esc. to stop capture!')
    # grab the first camera input device
    cam = cv2.VideoCapture(0)

    # main loop
    while True:
        #get current frame
        _, frame = cam.read()

        # flip frame to change from mirrored view
        frame = cv2.flip(frame,1)

        # creating a copy to display shapes and text
        frame_copy = frame.copy()

        # grabbing ROI from the frame
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]

        # apply grayscale,threshold,dilate and reshape to ROI
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(roi,thresh_value,255,cv2.THRESH_BINARY_INV)
        dilate = cv2.dilate(thresh,kernel=kernel)
        roi = cv2.resize(roi,(28,28),interpolation=cv2.INTER_CUBIC)
        roi = np.expand_dims(roi,axis=2)
        roi = np.expand_dims(roi,axis=0)

        # display model predictions on frame
        cv2.putText(frame_copy,f"I see a ... {model.predict_classes(roi)[0]}?",(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        # display ROI rectangle on frame
        cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,255,0), 3)

        cv2.imshow("Digit Recognizer",frame_copy)

        cv2.imshow("ROI",dilate)

        # use Esc. to stop capture
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print("Keyboard interrupt detected. Capture stopped!")
            break


    # release camera
    cam.release()
    #destroy all open windows
    cv2.destroyAllWindows()


if __name__=='__main__':

    # setting up region of interest(ROI) in top right corner
    roi_top = 62
    roi_bottom = 250
    roi_left = 450
    roi_right = 640

    thresh_value = 50

    kernel = np.ones((3,3),np.uint8)

    Thread(target=thresh_fn).start()
    Thread(target=roi_fn).start()
    Thread(target=cv_fn).start()
