import numpy as np
import cv2
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
object_detector = cv2.createBackgroundSubtractorMOG2(history = 100, varThreshold = 30)
# camera  = cv2.VideoCapture(2);
# cv2.startWindowThread()
# while(True):
#     ret, frame = camera.read()
#     if not ret:
#         break
#     frame = cv2.resize(frame, (640, 480))
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# camera.release()
# cv2.destroyAllWindows()


#
# cv2.startWindowThread()
#
# # open webcam video stream
# cap = cv2.VideoCapture(1)
#
# # the output will be written to output.avi
#
# while (True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # resizing for faster detection
#     frame = cv2.resize(frame, (640, 480))
#     # using a greyscale picture, also for faster detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#
#     # detect people in the image
#     # returns the bounding boxes for the detected objects
#     boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
#
#     boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
#
#     for (xA, yA, xB, yB) in boxes:
#         # display the detected boxes in the colour picture
#         cv2.rectangle(frame, (xA, yA), (xB, yB),
#                       (0, 255, 0), 2)
#
#     # Write the output video
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# # and release the output
# # finally, close the window
# cv2.destroyAllWindows()
# cv2.waitKey(1)

# def faceDetect(frame):
#     faces = face.detectMultiScale(frame,1.3,minNeighbors=3)
#     for (xA, yA, xB, yB) in faces:
#         cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
#     return frame

def motionDetect(frame):
    rect_count = 0
    fg_mask = object_detector.apply(frame)
    
    contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 500:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rect_count += 1
    return frame,rect_count

def proceesor(frame):

    #gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
    # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    return frame, len(boxes)
