"""
AI Hiring Assistant - OCEAN Assessment Page
Interactive personality assessment with gradient scale buttons.
Aesthetic: Neo-Corporate Futurism
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QProgressBar,
    QGraphicsDropShadowEffect, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient


# OCEAN Questions with trait mapping
OCEAN_QUESTIONS = [
    # Openness (10)
    {"text": "I have a vivid imagination", "trait": "Openness", "id": 1},
    {"text": "I am interested in abstract ideas", "trait": "Openness", "id": 2},
    {"text": "I enjoy artistic and creative experiences", "trait": "Openness", "id": 3},
    {"text": "I like to experiment with new things", "trait": "Openness", "id": 4},
    {"text": "I enjoy thinking about philosophical questions", "trait": "Openness", "id": 5},
    {"text": "I appreciate beauty in art and nature", "trait": "Openness", "id": 6},
    {"text": "I am curious about many different things", "trait": "Openness", "id": 7},
    {"text": "I prefer variety over routine", "trait": "Openness", "id": 8},
    {"text": "I enjoy learning about unfamiliar topics", "trait": "Openness", "id": 9},
    {"text": "I value unconventional ideas", "trait": "Openness", "id": 10},
    
    # Conscientiousness (10)
    {"text": "I am always prepared", "trait": "Conscientiousness", "id": 11},
    {"text": "I pay attention to details", "trait": "Conscientiousness", "id": 12},
    {"text": "I complete tasks thoroughly", "trait": "Conscientiousness", "id": 13},
    {"text": "I like order and organization", "trait": "Conscientiousness", "id": 14},
    {"text": "I follow through on my commitments", "trait": "Conscientiousness", "id": 15},
    {"text": "I am diligent in my work", "trait": "Conscientiousness", "id": 16},
    {"text": "I plan ahead and think before acting", "trait": "Conscientiousness", "id": 17},
    {"text": "I strive for excellence in what I do", "trait": "Conscientiousness", "id": 18},
    {"text": "I am self-disciplined", "trait": "Conscientiousness", "id": 19},
    {"text": "I manage my time effectively", "trait": "Conscientiousness", "id": 20},
    
    # Extraversion (10)
    {"text": "I feel comfortable around people", "trait": "Extraversion", "id": 21},
    {"text": "I start conversations with strangers", "trait": "Extraversion", "id": 22},
    {"text": "I enjoy being the center of attention", "trait": "Extraversion", "id": 23},
    {"text": "I feel energized by social gatherings", "trait": "Extraversion", "id": 24},
    {"text": "I am talkative", "trait": "Extraversion", "id": 25},
    {"text": "I enjoy meeting new people", "trait": "Extraversion", "id": 26},
    {"text": "I am enthusiastic and high-energy", "trait": "Extraversion", "id": 27},
    {"text": "I prefer group activities over solo activities", "trait": "Extraversion", "id": 28},
    {"text": "I express my feelings openly", "trait": "Extraversion", "id": 29},
    {"text": "I take the lead in group situations", "trait": "Extraversion", "id": 30},
    
    # Agreeableness (10)
    {"text": "I am interested in other people's problems", "trait": "Agreeableness", "id": 31},
    {"text": "I like to help others", "trait": "Agreeableness", "id": 32},
    {"text": "I try to understand how others feel", "trait": "Agreeableness", "id": 33},
    {"text": "I am cooperative with others", "trait": "Agreeableness", "id": 34},
    {"text": "I trust people easily", "trait": "Agreeableness", "id": 35},
    {"text": "I avoid conflicts when possible", "trait": "Agreeableness", "id": 36},
    {"text": "I treat everyone with kindness", "trait": "Agreeableness", "id": 37},
    {"text": "I consider others' needs before my own", "trait": "Agreeableness", "id": 38},
    {"text": "I am forgiving of others' mistakes", "trait": "Agreeableness", "id": 39},
    {"text": "I believe in the goodness of people", "trait": "Agreeableness", "id": 40},
    
    # Neuroticism (10)
    {"text": "I often feel stressed or anxious", "trait": "Neuroticism", "id": 41},
    {"text": "I worry about things", "trait": "Neuroticism", "id": 42},
    {"text": "I get upset easily", "trait": "Neuroticism", "id": 43},
    {"text": "I experience mood swings", "trait": "Neuroticism", "id": 44},
    {"text": "I am easily overwhelmed", "trait": "Neuroticism", "id": 45},
    {"text": "I take things personally", "trait": "Neuroticism", "id": 46},
    {"text": "I feel insecure at times", "trait": "Neuroticism", "id": 47},
    {"text": "I dwell on negative experiences", "trait": "Neuroticism", "id": 48},
    {"text": "I react emotionally to problems", "trait": "Neuroticism", "id": 49},
    {"text": "I feel overwhelmed by difficult situations", "trait": "Neuroticism", "id": 50}
]


class TraitBadge(QLabel):
    """Colored badge for OCEAN traits."""
    
    COLORS = {
        "Openness": ("#a855f7", "rgba(168, 85, 247, 0.15)"),
        "Conscientiousness": ("#00d4ff", "rgba(0, 212, 255, 0.15)"),
        "Extraversion": ("#ffd700", "rgba(255, 215, 0, 0.15)"),
        "Agreeableness": ("#00ffa3", "rgba(0, 255, 163, 0.15)"),
        "Neuroticism": ("#ff6b6b", "rgba(255, 107, 107, 0.15)")
    }
    
    def __init__(self, trait: str, parent=None):
        super().__init__(trait, parent)
        color, bg = self.COLORS.get(trait, ("#00d4ff", "rgba(0, 212, 255, 0.15)"))
        self.setStyleSheet(f"""
            color: {color};
            font-size: 11px;
            font-weight: 600;
            background: {bg};
            padding: 6px 14px;
            border-radius: 12px;
            letter-spacing: 1px;
        """)


class ScaleButton(QPushButton):
    """Rating scale button with gradient selection."""
    
    def __init__(self, value: int, parent=None):
        super().__init__(str(value), parent)
        self.value = value
        self.is_selected = False
        self.setFixedSize(56, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()
    
    def _update_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                                stop:0 #00d4ff, stop:1 #a855f7);
                    color: #0a0a0f;
                    border: none;
                    border-radius: 28px;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(0, 212, 255, 120))
            self.setGraphicsEffect(shadow)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(37, 37, 50, 0.6);
                    color: #adb5bd;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 28px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(0, 212, 255, 0.15);
                    border: 1px solid #00d4ff;
                    color: #00d4ff;
                }
            """)
            self.setGraphicsEffect(None)
    
    def set_selected(self, selected: bool):
        self.is_selected = selected
        self._update_style()


class QuestionWidget(QFrame):
    """Individual question display with rating scale."""
    
    response_changed = pyqtSignal(int, int)  # question_id, value
    
    def __init__(self, question: dict, parent=None):
        super().__init__(parent)
        self.question = question
        self.selected_value = None
        self.buttons = []
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(30, 30, 42, 0.7), 
                                            stop:1 rgba(20, 20, 30, 0.8));
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)
        
        # Header with trait badge
        header = QHBoxLayout()
        
        badge = TraitBadge(self.question["trait"])
        header.addWidget(badge)
        header.addStretch()
        
        q_num = QLabel(f"#{self.question['id']}")
        q_num.setStyleSheet("color: #4a4a5a; font-size: 13px; font-weight: 500;")
        header.addWidget(q_num)
        
        layout.addLayout(header)
        
        # Question text
        text = QLabel(self.question["text"])
        text.setFont(QFont("Segoe UI", 17))
        text.setStyleSheet("color: #f8f9fa;")
        text.setWordWrap(True)
        layout.addWidget(text)
        
        # Scale buttons
        scale_container = QWidget()
        scale_layout = QHBoxLayout(scale_container)
        scale_layout.setSpacing(12)
        scale_layout.setContentsMargins(0, 10, 0, 0)
        
        # Labels
        disagree = QLabel("Disagree")
        disagree.setStyleSheet("color: #6c757d; font-size: 12px;")
        scale_layout.addWidget(disagree)
        
        scale_layout.addStretch()
        
        for i in range(1, 6):
            btn = ScaleButton(i)
            btn.clicked.connect(lambda checked, v=i: self._on_button_clicked(v))
            scale_layout.addWidget(btn)
            self.buttons.append(btn)
        
        scale_layout.addStretch()
        
        agree = QLabel("Agree")
        agree.setStyleSheet("color: #6c757d; font-size: 12px;")
        scale_layout.addWidget(agree)
        
        layout.addWidget(scale_container)
    
    def _on_button_clicked(self, value: int):
        self.selected_value = value
        for btn in self.buttons:
            btn.set_selected(btn.value == value)
        self.response_changed.emit(self.question["id"], value)


class AssessmentPage(QWidget):
    """
    Full OCEAN personality assessment with interactive scale buttons.
    Premium question cards with trait badges and progress tracking.
    """
    
    assessment_complete = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.responses = {}
        self.question_widgets = []
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header (fixed)
        header = QWidget()
        header.setStyleSheet("background: #0a0a0f;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(60, 30, 60, 20)
        header_layout.setSpacing(12)
        
        step_label = QLabel("STEP 4 OF 5")
        step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        step_label.setStyleSheet("""
            color: #00d4ff;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(step_label)
        
        heading = QLabel("Personality Assessment")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        heading.setStyleSheet("color: #f8f9fa; letter-spacing: -1px;")
        header_layout.addWidget(heading)
        
        subtitle = QLabel("Rate each statement on a scale of 1 (Disagree) to 5 (Agree)")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #6c757d; font-size: 15px;")
        header_layout.addWidget(subtitle)
        
        # Progress bar
        progress_container = QHBoxLayout()
        progress_container.setContentsMargins(100, 15, 100, 0)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 50)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #00d4ff, stop:1 #a855f7);
                border-radius: 3px;
            }
        """)
        progress_container.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("0 / 50")
        self.progress_label.setStyleSheet("color: #6c757d; font-size: 13px; margin-left: 15px;")
        progress_container.addWidget(self.progress_label)
        
        header_layout.addLayout(progress_container)
        
        main_layout.addWidget(header)
        
        # Scrollable questions area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00d4ff;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(80, 20, 80, 30)
        content_layout.setSpacing(20)
        
        for q in OCEAN_QUESTIONS:
            widget = QuestionWidget(q)
            widget.response_changed.connect(self._on_response)
            self.question_widgets.append(widget)
            content_layout.addWidget(widget)
        
        # Submit button at bottom
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(0, 30, 0, 30)
        
        self.submit_button = QPushButton("Complete Assessment →")
        self.submit_button.setFixedSize(260, 56)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
        self.submit_button.setEnabled(False)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00d4ff, stop:1 #a855f7);
                color: #0a0a0f;
                border: none;
                border-radius: 28px;
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
        self.submit_button.clicked.connect(self._on_submit)
        button_layout.addWidget(self.submit_button)
        
        content_layout.addWidget(button_container)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def _on_response(self, question_id: int, value: int):
        self.responses[question_id] = value
        count = len(self.responses)
        self.progress_bar.setValue(count)
        self.progress_label.setText(f"{count} / 50")
        
        if count == 50:
            self.submit_button.setEnabled(True)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 212, 255, 120))
            self.submit_button.setGraphicsEffect(shadow)
    
    def _on_submit(self):
        # Group responses by trait
        grouped = {
            "Openness": [],
            "Conscientiousness": [],
            "Extraversion": [],
            "Agreeableness": [],
            "Neuroticism": []
        }
        
        for q in OCEAN_QUESTIONS:
            if q["id"] in self.responses:
                grouped[q["trait"]].append(self.responses[q["id"]])
        
        self.assessment_complete.emit(grouped)
    
    def start(self):
        """Reset and start assessment."""
        pass
    
    def reset(self):
        """Reset all responses."""
        self.responses = {}
        self.progress_bar.setValue(0)
        self.progress_label.setText("0 / 50")
        self.submit_button.setEnabled(False)
        self.submit_button.setGraphicsEffect(None)
        
        for widget in self.question_widgets:
            widget.selected_value = None
            for btn in widget.buttons:
                btn.set_selected(False)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0a0a0f"))
        gradient.setColorAt(1.0, QColor("#0f0f18"))
        painter.fillRect(self.rect(), gradient)
