"""
AI Hiring Assistant - Landing Page
Dramatic entrance with animated gradient background and glowing CTA.
Aesthetic: Neo-Corporate Futurism
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QPen, QBrush


class GlowingButton(QPushButton):
    """Primary CTA button with glow effect."""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_glow()
    
    def _setup_glow(self):
        """Add drop shadow glow effect."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 212, 255, 120))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        """Intensify glow on hover."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 212, 255, 180))
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Reset glow on leave."""
        self._setup_glow()
        super().leaveEvent(event)


class OrbitDot(QWidget):
    """Animated floating dot for visual interest."""
    
    def __init__(self, size=8, color="#00d4ff", parent=None):
        super().__init__(parent)
        self.dot_size = size
        self.dot_color = color
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(self.dot_color)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.dot_size, self.dot_size)


class LandingPage(QWidget):
    """
    Landing page with dramatic gradient background and glowing elements.
    Features floating orbs, gradient text effects, and premium aesthetics.
    """
    
    start_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("landingPage")
        self.setup_ui()
        self._create_floating_elements()
    
    def setup_ui(self):
        """Set up the landing page with dramatic styling."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 80, 60, 60)
        layout.setSpacing(0)
        
        # Top spacer
        layout.addStretch(2)
        
        # Badge / Eyebrow text
        badge_container = QWidget()
        badge_layout = QHBoxLayout(badge_container)
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        badge = QLabel("✦  NEXT-GEN RECRUITMENT PLATFORM  ✦")
        badge.setStyleSheet("""
            color: #00d4ff;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 3px;
            background: rgba(0, 212, 255, 0.1);
            padding: 10px 24px;
            border-radius: 20px;
            border: 1px solid rgba(0, 212, 255, 0.3);
        """)
        badge_layout.addWidget(badge)
        layout.addWidget(badge_container)
        
        layout.addSpacing(30)
        
        # Main heading with gradient effect
        heading_container = QWidget()
        heading_layout = QVBoxLayout(heading_container)
        heading_layout.setSpacing(8)
        heading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # "AI Hiring" line
        line1 = QLabel("AI Hiring")
        line1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line1.setFont(QFont("Segoe UI", 64, QFont.Weight.Bold))
        line1.setStyleSheet("""
            color: #f8f9fa;
            letter-spacing: -2px;
        """)
        heading_layout.addWidget(line1)
        
        # "Assistant" with accent color
        line2 = QLabel("Assistant")
        line2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line2.setFont(QFont("Segoe UI", 64, QFont.Weight.Bold))
        line2.setStyleSheet("""
            color: #00d4ff;
            letter-spacing: -2px;
        """)
        heading_layout.addWidget(line2)
        
        layout.addWidget(heading_container)
        
        layout.addSpacing(24)
        
        # Subtitle
        subtitle = QLabel("Powered by Computer Vision & Personality Analytics")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 18))
        subtitle.setStyleSheet("color: #adb5bd; letter-spacing: 0.5px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(50)
        
        # CTA Button
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.start_button = GlowingButton("Begin Your Journey")
        self.start_button.setFixedSize(280, 64)
        self.start_button.setFont(QFont("Segoe UI", 17, QFont.Weight.DemiBold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00d4ff, stop:1 #a855f7);
                color: #0a0a0f;
                border: none;
                border-radius: 32px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00e5ff, stop:0.5 #00d4ff, stop:1 #a855f7);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #a855f7, stop:1 #00d4ff);
            }
        """)
        self.start_button.clicked.connect(self._on_start_clicked)
        button_layout.addWidget(self.start_button)
        
        layout.addWidget(button_container)
        
        # Bottom spacer
        layout.addStretch(3)
        
        # Footer with features
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setSpacing(50)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        features = [
            ("🔒", "Secure & Private"),
            ("💾", "Local Storage Only"),
            ("🎯", "AI-Powered Analysis")
        ]
        
        for icon, text in features:
            feature_widget = QWidget()
            feature_layout = QHBoxLayout(feature_widget)
            feature_layout.setSpacing(8)
            feature_layout.setContentsMargins(0, 0, 0, 0)
            
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI Emoji", 14))
            
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #6c757d; font-size: 13px;")
            
            feature_layout.addWidget(icon_label)
            feature_layout.addWidget(text_label)
            footer_layout.addWidget(feature_widget)
        
        layout.addWidget(footer)
        
        # Version
        version = QLabel("v2.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: #3a3a4a; font-size: 11px; margin-top: 20px;")
        layout.addWidget(version)
    
    def _create_floating_elements(self):
        """Create decorative floating orbs for visual interest."""
        # Positioned absolutely over the widget
        positions = [
            (50, 100, 12, "#00d4ff"),
            (150, 200, 8, "#a855f7"),
            (80, 400, 6, "#00ffa3"),
        ]
        
        for x, y, size, color in positions:
            dot = OrbitDot(size, color, self)
            dot.move(x, y)
            dot.show()
    
    def _on_start_clicked(self):
        """Handle start button click."""
        self.start_clicked.emit()
    
    def paintEvent(self, event):
        """Paint gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create diagonal gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#0a0a0f"))
        gradient.setColorAt(0.4, QColor("#12121a"))
        gradient.setColorAt(0.7, QColor("#1a1a24"))
        gradient.setColorAt(1.0, QColor("#0f0f18"))
        
        painter.fillRect(self.rect(), gradient)
        
        # Add subtle radial glow in center
        center_x = self.width() // 2
        center_y = self.height() // 2 - 50
        
        # Draw subtle cyan glow
        for i in range(5):
            opacity = 15 - i * 3
            size = 200 + i * 80
            painter.setBrush(QColor(0, 212, 255, opacity))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - size//2, center_y - size//2, size, size)
