import os
import time
import cv2
import numpy as np
from PIL import Image
from threading import Thread

path = "TrainingImage"

# Ensure the directory exists
if not os.path.exists(path):
    os.makedirs(path)
    print(f"The directory '{path}' has been created. Please add images to it and rerun the script.")
else:
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

def getImagesAndLabels(path):
    # path of all the files in the folder

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    # empty ID list
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

save_path = "TrainingImageLabel"
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"Directory '{save_path}' created.")


def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    Thread(target = recognizer.train(faces, np.array(Id))).start()
    Thread(target = counter_img("TrainingImage")).start()
    recognizer.save(os.path.join(save_path, "Trainner.yml"))
    print("All Images Trained")


def counter_img(path):
    imgcounter = 1
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        print(str(imgcounter) + " Images Trained", end="\r")
        time.sleep(0.008)
        imgcounter += 1