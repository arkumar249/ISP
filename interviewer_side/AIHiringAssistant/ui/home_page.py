from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ui.theme import Theme

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # --- Apply Global Theme ---
        self.setStyleSheet(Theme.global_style())

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        # --- Dashboard Title ---
        title_container = QFrame()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(5)
        
        self.title = QLabel("Interviewer's Dashboard")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {Theme.COLOR_TEXT_MAIN};
            letter-spacing: -0.5px;
        """)

        self.subtitle = QLabel("Automated Facial Data & Alignment System")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(f"""
            font-size: 16px;
            color: {Theme.COLOR_TEXT_SEC};
            font-weight: 500;
        """)

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)
        
        # --- Action Button ---
        self.start_btn = QPushButton("Initialize Session Scan")
        self.start_btn.setFixedSize(260, 50)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet(Theme.button_primary())
        
        # Add slight shadow to button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 100)) # Cyan glow
        shadow.setOffset(0, 4)
        self.start_btn.setGraphicsEffect(shadow)
        
        self.start_btn.clicked.connect(self.main_window.go_to_session_selection_page)

        layout.addStretch()
        layout.addWidget(title_container)
        layout.addSpacing(20)
        layout.addWidget(self.start_btn)
        layout.addStretch()
