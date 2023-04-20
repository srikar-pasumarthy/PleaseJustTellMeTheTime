from specific_person_fr import *
from gui import *

#Boolean indicating if model is done training
training = False

def main():
    #Create gui window 
    gui().create()
    
    #Train Model function will begin video capture once completed
    faceRecognition.trainModel()

if __name__ == "__main__":
    main()
