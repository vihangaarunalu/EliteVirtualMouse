import cv2

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()  # Read frame
    if not ret:
        break

    cv2.imshow("Webcam Test", frame)  # Display frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()  # Release webcam
cv2.destroyAllWindows()  # Close all OpenCV windows
