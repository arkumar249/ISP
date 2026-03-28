"""
AI Hiring Assistant - Camera Handler
Manages all webcam operations on a separate thread for GUI responsiveness.
Uses MediaPipe for face detection and frontal gaze verification.
"""

import cv2
import numpy as np
import threading
import queue
import logging
from pathlib import Path
from typing import Optional, Callable, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    # Check if the solutions API is available (older mediapipe versions)
    if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'face_mesh'):
        MEDIAPIPE_AVAILABLE = True
    else:
        MEDIAPIPE_AVAILABLE = False
except ImportError:
    MEDIAPIPE_AVAILABLE = False


class FaceStatus(Enum):
    """Enum representing face alignment status."""
    NO_FACE = "no_face"
    NOT_FRONTAL = "not_frontal"
    ALIGNED = "aligned"


class CameraHandler:
    """
    Handles camera operations on a separate thread.
    Provides face detection, frontal gaze verification, and video recording.
    """
    
    def __init__(self, camera_index: int = 1):
        """
        Initialize the CameraHandler.
        
        Args:
            camera_index: Index of the camera to use (default 0 for primary webcam).
        """
        self.camera_index = camera_index
        self.capture: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.is_recording = False
        
        # Threading components
        self._thread: Optional[threading.Thread] = None
        self._frame_queue: queue.Queue = queue.Queue(maxsize=2)
        self._command_queue: queue.Queue = queue.Queue()
        self._stop_event = threading.Event()
        
        # Recording components
        self._video_writer: Optional[cv2.VideoWriter] = None
        self._record_path: Optional[Path] = None
        
        # Face detection - try MediaPipe first, fallback to Haar Cascade
        self.face_mesh = None
        self.mp_face_mesh = None
        
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
            except Exception:
                self.face_mesh = None
        
        # Always initialize Haar Cascade as fallback
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Status callback
        self._status_callback: Optional[Callable[[FaceStatus], None]] = None
        self._current_status = FaceStatus.NO_FACE
        
        # Frame dimensions
        self.frame_width = 640
        self.frame_height = 480
    
    def set_status_callback(self, callback: Callable[[FaceStatus], None]):
        """Set callback function for face status updates."""
        self._status_callback = callback
    
    def start(self) -> bool:
        """
        Start the camera and processing thread.
        
        Returns:
            True if camera started successfully, False otherwise.
        """
        if self.is_running:
            return True
        
        # Initialize camera
        self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        
        if not self.capture.isOpened():
            # Try without DirectShow
            self.capture = cv2.VideoCapture(self.camera_index)
        
        if not self.capture.isOpened():
            return False
        
        # Set camera properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        
        # Get actual dimensions
        self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Start processing thread
        self._stop_event.clear()
        self.is_running = True
        self._thread = threading.Thread(target=self._processing_loop, daemon=True)
        self._thread.start()
        
        return True
    
    def stop(self):
        """Stop the camera and processing thread."""
        if not self.is_running:
            return
        
        # Stop recording if active
        if self.is_recording:
            self.stop_recording()
        
        # Signal thread to stop
        self._stop_event.set()
        self.is_running = False
        
        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        
        # Release camera
        if self.capture:
            self.capture.release()
            self.capture = None
        
        # Clean up MediaPipe
        if self.face_mesh:
            self.face_mesh.close()
    
    @staticmethod
    def _ensure_bgr(frame: np.ndarray) -> np.ndarray:
        """
        Normalize any frame to 3-channel BGR.
        Handles grayscale (1-ch), BGRA (4-ch), and passthrough for BGR (3-ch).
        """
        if frame is None:
            return frame
        if len(frame.shape) == 2:
            # Single-channel grayscale → BGR
            return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        channels = frame.shape[2] if len(frame.shape) == 3 else 0
        if channels == 1:
            # Explicit single-channel → BGR
            return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif channels == 4:
            # BGRA → BGR
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        # Already 3-channel (BGR) — pass through
        return frame

    def _processing_loop(self):
        """Main processing loop running on separate thread."""
        while not self._stop_event.is_set():
            if self.capture is None or not self.capture.isOpened():
                break
            
            ret, frame = self.capture.read()
            if not ret:
                continue
            
            # Normalize frame to 3-channel BGR (thermal cameras may output grayscale)
            frame = self._ensure_bgr(frame)
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect face and check orientation (wrapped for safety)
            try:
                status = self._detect_face_status(frame)
            except Exception as e:
                logger.warning("Face detection error: %s", e)
                status = FaceStatus.NO_FACE
            
            # Update status if changed
            if status != self._current_status:
                self._current_status = status
                if self._status_callback:
                    try:
                        self._status_callback(status)
                    except Exception as e:
                        logger.warning("Status callback error: %s", e)
            
            # Write frame if recording
            if self.is_recording and self._video_writer:
                try:
                    # VideoWriter crashes if frame dimensions don't exactly match initialization
                    if hasattr(self, '_record_width') and hasattr(self, '_record_height'):
                        record_frame = cv2.resize(frame, (self._record_width, self._record_height))
                        self._video_writer.write(record_frame)
                    else:
                        self._video_writer.write(frame)
                except Exception as e:
                    logger.error(f"Recording error: {e}")
            
            # Put frame in queue for display (drop old frames)
            try:
                if self._frame_queue.full():
                    try:
                        self._frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                self._frame_queue.put_nowait(frame.copy())
            except queue.Full:
                pass
    
    def _detect_face_status(self, frame: np.ndarray) -> FaceStatus:
        """
        Detect face and determine if it's properly aligned and looking forward.
        
        Args:
            frame: BGR image frame from camera.
            
        Returns:
            FaceStatus indicating alignment state.
        """
        if MEDIAPIPE_AVAILABLE and self.face_mesh:
            return self._detect_with_mediapipe(frame)
        else:
            return self._detect_with_cascade(frame)
    
    def _detect_with_mediapipe(self, frame: np.ndarray) -> FaceStatus:
        """Detect face status using MediaPipe Face Mesh."""
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return FaceStatus.NO_FACE
        
        # Get face landmarks
        landmarks = results.multi_face_landmarks[0].landmark
        
        # Check if face is frontal using key landmarks
        # Nose tip (index 1), left eye center (index 33), right eye center (index 263)
        nose = landmarks[1]
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        
        # Check horizontal alignment (face not turned left/right)
        eye_distance = abs(right_eye.x - left_eye.x)
        nose_to_left = abs(nose.x - left_eye.x)
        nose_to_right = abs(nose.x - right_eye.x)
        
        # Nose should be roughly centered between eyes
        horizontal_ratio = min(nose_to_left, nose_to_right) / max(nose_to_left, nose_to_right) if max(nose_to_left, nose_to_right) > 0 else 0
        
        # Check vertical alignment (face not tilted up/down)
        # Using chin (index 152) and forehead (index 10)
        chin = landmarks[152]
        forehead = landmarks[10]
        
        # Check if face is within acceptable range
        face_center_x = (left_eye.x + right_eye.x) / 2
        face_center_y = (forehead.y + chin.y) / 2
        
        # Face should be roughly centered in frame
        is_centered_x = 0.3 < face_center_x < 0.7
        is_centered_y = 0.2 < face_center_y < 0.8
        
        # Check if looking straight (ratio should be close to 1.0 for frontal face)
        is_frontal = horizontal_ratio > 0.75
        
        if is_frontal and is_centered_x and is_centered_y:
            return FaceStatus.ALIGNED
        elif is_centered_x and is_centered_y:
            return FaceStatus.NOT_FRONTAL
        else:
            return FaceStatus.NO_FACE
    
    def _detect_with_cascade(self, frame: np.ndarray) -> FaceStatus:
        """Fallback face detection using Haar Cascade."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            return FaceStatus.NO_FACE
        
        # Check if face is centered
        x, y, w, h = faces[0]
        face_center_x = (x + w / 2) / frame.shape[1]
        face_center_y = (y + h / 2) / frame.shape[0]
        
        is_centered = 0.3 < face_center_x < 0.7 and 0.2 < face_center_y < 0.8
        
        if is_centered:
            return FaceStatus.ALIGNED
        else:
            return FaceStatus.NOT_FRONTAL
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Get the latest frame from the camera (thread-safe).
        
        Returns:
            BGR image frame or None if no frame available.
        """
        try:
            return self._frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_current_status(self) -> FaceStatus:
        """Get the current face alignment status."""
        return self._current_status
    
    def start_recording(self, output_path: Path) -> bool:
        """
        Start recording video to the specified path.
        
        Args:
            output_path: Path where the MP4 file should be saved.
            
        Returns:
            True if recording started successfully.
        """
        if self.is_recording:
            return False
        
        if not self.is_running:
            return False
            
        # Get actual frame size from a real frame (camera props are often wrong for thermal)
        frame = self.get_frame()
        if frame is not None:
            actual_h, actual_w = frame.shape[:2]
        else:
            actual_w, actual_h = self.frame_width, self.frame_height
            
        # Codecs require even dimensions
        width = int(actual_w) if int(actual_w) % 2 == 0 else int(actual_w) - 1
        height = int(actual_h) if int(actual_h) % 2 == 0 else int(actual_h) - 1
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        self._video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            30.0,  # FPS
            (width, height)
        )
        
        if not self._video_writer.isOpened():
            self._video_writer = None
            return False
            
        # Save exact recording dimensions to resize frames before writing
        self._record_width = width
        self._record_height = height
        
        self._record_path = output_path
        self.is_recording = True
        return True
    
    def stop_recording(self) -> Optional[Path]:
        """
        Stop recording and return the path to the saved file.
        
        Returns:
            Path to the recorded file, or None if no recording was active.
        """
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        if self._video_writer:
            self._video_writer.release()
            self._video_writer = None
        
        saved_path = self._record_path
        self._record_path = None
        
        return saved_path
    
    def is_camera_available(self) -> bool:
        """Check if the camera is available and working."""
        if self.capture and self.capture.isOpened():
            return True
        
        # Try to open camera briefly
        test_capture = cv2.VideoCapture(self.camera_index)
        is_available = test_capture.isOpened()
        test_capture.release()
        
        return is_available
    
    def get_frame_size(self) -> Tuple[int, int]:
        """Get the current frame dimensions."""
        return (self.frame_width, self.frame_height)
