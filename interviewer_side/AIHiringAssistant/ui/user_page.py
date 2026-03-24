from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ui.theme import Theme

class UserPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.capture_mode = "image"  # default

        # Apply Global Theme
        self.setStyleSheet(Theme.global_style())

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Container Card
        card = QFrame()
        card.setStyleSheet(Theme.card_style())
        card.setFixedSize(450, 420)
        
        # Add slight shadow to card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255, 40)) # Soft cyan glow
        shadow.setOffset(0, 5)
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # -------- Title --------
        title = QLabel("Session Information")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold; 
            color: {Theme.COLOR_TEXT_MAIN};
            margin-bottom: 10px;
        """)

        # -------- Inputs --------
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Applicant Name")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("User ID")

        for field in (self.name_input, self.id_input):
            field.setFixedHeight(45)
            field.setStyleSheet(Theme.input_style())

        # -------- Buttons --------
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)

        image_btn = QPushButton("Capture Image")
        video_btn = QPushButton("Capture Video")

        for btn in (image_btn, video_btn):
            btn.setFixedHeight(50)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(Theme.button_primary())

            # Button Shadow
            btn_shadow = QGraphicsDropShadowEffect()
            btn_shadow.setBlurRadius(15)
            btn_shadow.setColor(QColor(0, 212, 255, 80))
            btn_shadow.setOffset(0, 3)
            btn.setGraphicsEffect(btn_shadow)

        image_btn.clicked.connect(self.select_image_mode)
        video_btn.clicked.connect(self.select_video_mode)

        # -------- Layout --------
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.name_input)
        layout.addWidget(self.id_input)
        layout.addSpacing(20)
        btn_layout.addWidget(image_btn)
        btn_layout.addWidget(video_btn)
        layout.addLayout(btn_layout)
        layout.addStretch()

        main_layout.addWidget(card)

    # -----------------------------------

    def select_image_mode(self):
        self.capture_mode = "image"
        self.proceed()

    def select_video_mode(self):
        self.capture_mode = "video"
        self.proceed()

    def proceed(self):
        user_data = {
            "name": self.name_input.text().strip(),
            "id": self.id_input.text().strip()
        }

        if not user_data["name"] or not user_data["id"]:
            return  # (later we’ll show validation message)

        self.main_window.go_to_alignment_page(
            user_data,
            self.capture_mode
        )

