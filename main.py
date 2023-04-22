import face_recognition as fr
from gui import *
import multiprocessing

#Boolean indicating if model is done training
training = False
detected = False

# def main():
    # #Create gui window 
    # gui.create()
   
    
    #Train Model function will begin video capture once completed
   

if __name__ == "__main__":
    p1 = multiprocessing.Process(name='p1', target=gui.create())
    p = multiprocessing.Process(name='p', target=face_recognition.start())
    p1.start()
    p.start()
