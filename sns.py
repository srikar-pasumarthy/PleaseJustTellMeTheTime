#import cv2
import face_recognition as fr

def main():
    
    unknown_image = fr.load_image_file("face2.jpg")
    biden_encoding = fr.face_encodings(known_image)[0]
    unknown_encoding = fr.face_encodings(unknown_image)[0]
    results = fr.compare_faces([biden_encoding], unknown_encoding)

    print(results)

if __name__ == "__main__":
    main()
