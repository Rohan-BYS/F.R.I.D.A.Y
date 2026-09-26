"""
F.R.I.D.A.Y. Vision Module (Eyes).
Captures images from the local webcam using OpenCV.
"""

import base64
from typing import Optional
from friday_engine.logger import logger

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


class VisionEngine:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        
    def capture_frame(self, return_base64: bool = True) -> Optional[str]:
        """Activate the webcam, capture a single frame, and return it as base64 or bytes."""
        if not CV2_AVAILABLE:
            logger.error("opencv-python is not installed. Cannot use Vision Engine.")
            return None
            
        logger.info(f"Activating webcam (index {self.camera_index})...")
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            logger.error(f"Failed to open webcam at index {self.camera_index}.")
            return None
            
        try:
            # Read a few frames to let the camera auto-adjust exposure
            for _ in range(5):
                cap.read()
                
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to read frame from webcam.")
                return None
                
            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            
            if return_base64:
                return base64.b64encode(buffer).decode('utf-8')
            return buffer.tobytes()
            
        finally:
            cap.release()
