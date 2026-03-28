"""
AI Hiring Assistant - Face Alignment Page
Premium camera interface with animated status indicators.
Aesthetic: Neo-Corporate Futurism
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QImage, QPixmap, QColor, QPainter, QLinearGradient, QPen, QBrush
import cv2
import numpy as np

from ..camera_handler import CameraHandler, FaceStatus


class StatusIndicator(QWidget):
    """Animated status indicator with glow effect."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = FaceStatus.NO_FACE
        self.pulse_opacity = 100
        self.pulse_direction = 1
        
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self._pulse)
        self.pulse_timer.start(50)
    
    def _pulse(self):
        """Animate the glow pulse."""
        self.pulse_opacity += self.pulse_direction * 8
        if self.pulse_opacity >= 150:
            self.pulse_direction = -1
        elif self.pulse_opacity <= 80:
            self.pulse_direction = 1
        self.update()
    
    def set_status(self, status: FaceStatus):
        self.status = status
        self.update()


class CameraFrame(QFrame):
    """Styled camera preview frame with dynamic border."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(660, 500)
        self._set_default_style()
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
    
    def _set_default_style(self):
        self.setStyleSheet("""
            QFrame {
                background: #0a0a0f;
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
    
    def set_status(self, status: FaceStatus):
        """Update border color based on status."""
        if status == FaceStatus.ALIGNED:
            color = "#00ffa3"
            glow_color = QColor(0, 255, 163, 80)
        elif status == FaceStatus.NOT_FRONTAL:
            color = "#ffa502"
            glow_color = QColor(255, 165, 2, 80)
        else:
            color = "#ff4757"
            glow_color = QColor(255, 71, 87, 80)
        
        self.setStyleSheet(f"""
            QFrame {{
                background: #0a0a0f;
                border-radius: 20px;
                border: 3px solid {color};
            }}
        """)
        
        # Update shadow color
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(glow_color)
        self.setGraphicsEffect(shadow)


class FaceAlignmentPage(QWidget):
    """
    Premium face alignment interface with animated feedback.
    Real-time camera preview with status indicators.
    """
    
    proceed_clicked = pyqtSignal()
    back_clicked = pyqtSignal()
    
    def __init__(self, camera_handler: CameraHandler, parent=None):
        super().__init__(parent)
        self.camera_handler = camera_handler
        self.is_active = False
        
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self._update_preview)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the face alignment page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(12)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        step_label = QLabel("STEP 2 OF 5")
        step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        step_label.setStyleSheet("""
            color: #00d4ff;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(step_label)
        
        heading = QLabel("Face Alignment")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        heading.setStyleSheet("color: #f8f9fa; letter-spacing: -1px;")
        header_layout.addWidget(heading)
        
        subtitle = QLabel("Position yourself within the guide and look straight at the camera")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #6c757d; font-size: 15px;")
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header)
        main_layout.addSpacing(30)
        
        # Camera preview
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.camera_frame = CameraFrame()
        camera_inner_layout = QVBoxLayout(self.camera_frame)
        camera_inner_layout.setContentsMargins(3, 3, 3, 3)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(654, 494)
        self.preview_label.setStyleSheet("border-radius: 18px; background: #0a0a0f;")
        camera_inner_layout.addWidget(self.preview_label)
        
        preview_layout.addWidget(self.camera_frame)
        
        # Status indicator
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.setSpacing(12)
        
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #ff4757; font-size: 16px;")
        
        self.status_label = QLabel("Initializing camera...")
        self.status_label.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
        self.status_label.setStyleSheet("color: #adb5bd;")
        
        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.status_label)
        preview_layout.addWidget(status_container)
        
        main_layout.addWidget(preview_container)
        main_layout.addStretch()
        
        # Buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(16)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(140, 52)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #adb5bd;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 26px;
                font-size: 15px;
            }
            QPushButton:hover {
                border-color: #00d4ff;
                color: #00d4ff;
            }
        """)
        self.back_button.clicked.connect(self._on_back_clicked)
        
        self.proceed_button = QPushButton("Proceed to Interview →")
        self.proceed_button.setFixedSize(240, 52)
        self.proceed_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.proceed_button.setFont(QFont("Segoe UI", 15, QFont.Weight.DemiBold))
        self.proceed_button.setEnabled(False)
        self.proceed_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00d4ff, stop:1 #a855f7);
                color: #0a0a0f;
                border: none;
                border-radius: 26px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00e5ff, stop:1 #a855f7);
            }
            QPushButton:disabled {
                background: #252532;
                color: #6c757d;
            }
        """)
        self.proceed_button.clicked.connect(self._on_proceed_clicked)
        
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.proceed_button)
        main_layout.addWidget(button_container)
    
    def start(self):
        """Start camera and face detection."""
        self.is_active = True
        self.camera_handler.set_status_callback(self._on_face_status_changed)
        
        if not self.camera_handler.start():
            self.status_label.setText("Camera not available")
            self.status_label.setStyleSheet("color: #ff4757;")
            self.status_dot.setStyleSheet("color: #ff4757;")
            return
        
        self.preview_timer.start(33)
    
    def stop(self):
        """Stop camera preview."""
        self.is_active = False
        self.preview_timer.stop()
    
    def _update_preview(self):
        """Update camera preview."""
        if not self.is_active:
            return
        
        frame = self.camera_handler.get_frame()
        if frame is None:
            return
        
        # Draw face guide
        frame = self._draw_face_guide(frame)
        
        # Convert to RGB for display — handle any channel format safely
        if len(frame.shape) == 2:
            # Grayscale frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        elif frame.shape[2] == 1:
            rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        h, w, ch = rgb.shape
        q_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img).scaled(
            654, 494,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.preview_label.setPixmap(pixmap)
    
    def _draw_face_guide(self, frame: np.ndarray) -> np.ndarray:
        """Draw oval face guide."""
        overlay = frame.copy()
        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        axes = (130, 175)
        
        status = self.camera_handler.get_current_status()
        if status == FaceStatus.ALIGNED:
            color = (163, 255, 0)  # BGR for #00ffa3
        elif status == FaceStatus.NOT_FRONTAL:
            color = (2, 165, 255)  # BGR for #ffa502
        else:
            color = (87, 71, 255)  # BGR for #ff4757
        
        cv2.ellipse(overlay, center, axes, 0, 0, 360, color, 3)
        
        return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
    
    def _on_face_status_changed(self, status: FaceStatus):
        """Update UI based on face status."""
        if status == FaceStatus.ALIGNED:
            self.status_label.setText("Face Aligned — Looking Straight")
            self.status_label.setStyleSheet("color: #00ffa3;")
            self.status_dot.setStyleSheet("color: #00ffa3;")
            self.proceed_button.setEnabled(True)
            self.camera_frame.set_status(status)
            
            # Add glow to proceed button
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 212, 255, 100))
            self.proceed_button.setGraphicsEffect(shadow)
            
        elif status == FaceStatus.NOT_FRONTAL:
            self.status_label.setText("Please look straight at the camera")
            self.status_label.setStyleSheet("color: #ffa502;")
            self.status_dot.setStyleSheet("color: #ffa502;")
            self.proceed_button.setEnabled(False)
            self.proceed_button.setGraphicsEffect(None)
            self.camera_frame.set_status(status)
            
        else:
            self.status_label.setText("Move into frame")
            self.status_label.setStyleSheet("color: #ff4757;")
            self.status_dot.setStyleSheet("color: #ff4757;")
            self.proceed_button.setEnabled(False)
            self.proceed_button.setGraphicsEffect(None)
            self.camera_frame.set_status(status)
    
    def _on_proceed_clicked(self):
        self.stop()
        self.proceed_clicked.emit()
    
    def _on_back_clicked(self):
        self.stop()
        self.back_clicked.emit()
    
    def paintEvent(self, event):
        """Paint gradient background."""
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#0a0a0f"))
        gradient.setColorAt(0.5, QColor("#0f0f18"))
        gradient.setColorAt(1.0, QColor("#12121a"))
        painter.fillRect(self.rect(), gradient)
