import cv2
import requests
import base64

cap = cv2.VideoCapture(0)  # Access the default webcam (change 0 if using multiple cameras)

while True:
    ret, frame = cap.read()

    if ret:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        cv2.imshow("frame", frame)

        # Encode frame as base64 for transmission
        encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

        # Send frame to Node.js server
        url = 'http://localhost:4000/receive_frame1'  # Replace with your Node.js server endpoint
        response = requests.post(url, data={'frame': encoded_frame})
        print(response.text)  

    cv2.waitKey(1)
cap.release()
