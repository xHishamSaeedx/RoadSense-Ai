import asyncio
import base64
import cv2
import json
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer

class WebcamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.node_server = "ws://localhost:3000"  # Node.js server address
        self.node_connection = await websockets.connect(self.node_server)

        await self.accept()

        cap = cv2.VideoCapture(0)  # OpenCV for capturing frames

        while True:
            ret, frame = cap.read()  # Capture a frame
            if not ret:
                break

            # Encode frame as base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_as_bytes = base64.b64encode(buffer).decode('utf-8')

            # Send frame to the Node.js server via WebSocket
            await self.node_connection.send(json.dumps({'frame': frame_as_bytes}))

            # Add delay if needed
            await asyncio.sleep(0.1)

        cap.release()

    async def disconnect(self, close_code):
        await self.node_connection.close()
