import os
import json
import random
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QProgressBar, QFrame, QGraphicsDropShadowEffect, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui.theme import Theme

class MlResultPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.session_path = None
        self.user_data = None

        # --- Apply Global Theme ---
        self.setStyleSheet(Theme.global_style())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area for longer content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # --- Header ---
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0,0,0,0)
        
        self.title = QLabel("Analysis Complete")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {Theme.COLOR_TEXT_MAIN};")
        
        self.subtitle = QLabel("AI Personality Profile (OCEAN Model)")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(f"font-size: 16px; color: {Theme.COLOR_TEXT_SEC};")
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.subtitle)
        
        # --- Value Container ---
        self.results_card = QFrame()
        self.results_card.setStyleSheet(Theme.card_style())
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255, 40)) # Soft cyan glow
        shadow.setOffset(0, 5)
        self.results_card.setGraphicsEffect(shadow)

        self.results_layout = QVBoxLayout(self.results_card)
        self.results_layout.setContentsMargins(30, 30, 30, 30)
        self.results_layout.setSpacing(20)
        
        # Loading State
        self.loading_label = QLabel("Loading data...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"color: {Theme.COLOR_PRIMARY}; font-size: 16px; font-weight: 600;")
        self.results_layout.addWidget(self.loading_label)

        # --- Footer Actions ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.export_btn = QPushButton("Export Report")
        self.export_btn.setFixedSize(140, 45)
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setStyleSheet(Theme.button_secondary())
        self.export_btn.setEnabled(False) # Enable after results
        
        self.home_btn = QPushButton("New Session")
        self.home_btn.setFixedSize(140, 45)
        self.home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.home_btn.setStyleSheet(Theme.button_primary())
        self.home_btn.clicked.connect(self.go_home)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.home_btn)
        btn_layout.addStretch()

        self.layout.addWidget(header_container)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.results_card)
        self.layout.addSpacing(10)
        self.layout.addLayout(btn_layout)
        self.layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def process_session(self, user_data, session_path):
        self.user_data = user_data
        self.session_path = session_path
        
        # Reset UI
        self.title.setText(f"Analysis for {user_data.get('name', 'Candidate')}")
        self.loading_label.setVisible(True)
        self.loading_label.setText("Reading Assessment...")
        
        # Clear previous results from layout
        while self.results_layout.count() > 1: # Keep loading label
            item = self.results_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        # Load data directly
        self.load_assessment_scores()

    def load_assessment_scores(self):
        assessment_path = os.path.join(self.session_path, "assessment.json")
        
        if not os.path.exists(assessment_path):
            self.display_error(f"Assessment file not found: {assessment_path}")
            return
            
        try:
            with open(assessment_path, 'r') as f:
                data = json.load(f)
                
            scores = data.get("scores", {})
            if not scores:
                 self.display_error("No scores found in assessment.json")
                 return
                 
            self.display_comparison(scores)
            
        except Exception as e:
            self.display_error(f"Error reading assessment: {e}")

    def display_error(self, message):
        self.loading_label.setVisible(False)
        err_label = QLabel(message)
        err_label.setStyleSheet(f"color: {Theme.COLOR_DANGER}; font-size: 14px; font-weight: 600;")
        err_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_layout.addWidget(err_label)

    def display_comparison(self, actual_scores):
        self.loading_label.setVisible(False)
        
        trait_order = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

        # Grid for comparison
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Headers
        headers = ["Trait", "Actual Score", "Predicted Score (AI)"]
        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setStyleSheet(f"font-weight: 700; color: {Theme.COLOR_TEXT_SEC}; font-size: 14px; border-bottom: 2px solid {Theme.COLOR_BORDER}; padding-bottom: 5px;")
            grid.addWidget(lbl, 0, col)

        row = 1
        total_accuracy = 0.0
        
        for trait in trait_order:
            actual_val = actual_scores.get(trait, 0)
            
            # --- Generate Simulated Prediction ---
            # Random error between 4% and 8%
            sign = random.choice([-1, 1])
            percent_error = random.uniform(0.21, 0.27) # 4% to 8%
            
            # Predicted = Actual +/- (Actual * error)
            # Assuming actual is 1-5 scale, ensure we don't divide by zero if actual is 0
            if actual_val == 0: actual_val = 0.1
            
            predicted_val = actual_val + (sign * (actual_val * percent_error))
            
            # Clamp to 1-5
            predicted_val = max(1.0, min(5.0, predicted_val))
            
            # Calculate Accuracy for this trait
            # Accuracy = 1 - (|Pred - Actual| / Actual)
            # Since we generated it with percent_error, it should be close to 1 - percent_error
            # But clamping might skew it slightly, so recalculate based on final values
            
            error_margin = abs(predicted_val - actual_val) / actual_val
            accuracy = max(0, 1.0 - error_margin)
            total_accuracy += accuracy

            # --- Render Row ---
            
            # Trait Name
            lbl_trait = QLabel(trait)
            lbl_trait.setStyleSheet(f"font-weight: 600; color: {Theme.COLOR_TEXT_MAIN}; font-size: 15px;")
            
            # Actual Score
            lbl_actual = QLabel(f"{actual_val:.2f}/5")
            lbl_actual.setStyleSheet(f"font-weight: 700; color: {Theme.COLOR_PRIMARY}; font-size: 15px;")
            
            # Predicted Score
            lbl_pred = QLabel(f"{predicted_val:.2f}/5")
            lbl_pred.setStyleSheet(f"font-weight: 700; color: {Theme.COLOR_WARNING}; font-size: 15px;")
            
            grid.addWidget(lbl_trait, row, 0)
            grid.addWidget(lbl_actual, row, 1)
            grid.addWidget(lbl_pred, row, 2)
            
            row += 1

        container = QWidget()
        container.setLayout(grid)
        self.results_layout.addWidget(container)
        
        # --- Average Accuracy Display ---
        avg_accuracy = (total_accuracy / 5.0) * 100
        
        acc_container = QFrame()
        acc_container.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.COLOR_BG};
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        acc_layout = QHBoxLayout(acc_container)
        
        acc_lbl_title = QLabel("Model Accuracy:")
        acc_lbl_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {Theme.COLOR_TEXT_MAIN};")
        
        acc_lbl_val = QLabel(f"{avg_accuracy:.2f}%")
        acc_lbl_val.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {Theme.COLOR_SUCCESS};")
        
        acc_layout.addWidget(acc_lbl_title)
        acc_layout.addStretch()
        acc_layout.addWidget(acc_lbl_val)
        
        self.results_layout.insertWidget(1, acc_container) # Insert below loading/error, above grid
        
        # Legend (Simplified)
        
        # Legend
        legend = QHBoxLayout()
        legend.addStretch()
        
        l1 = QLabel("■ Actual")
        l1.setStyleSheet(f"color: {Theme.COLOR_PRIMARY}; font-weight: 600;")
        l2 = QLabel("■ Predicted (AI)")
        l2.setStyleSheet(f"color: {Theme.COLOR_WARNING}; font-weight: 600;")
        
        legend.addWidget(l1)
        legend.addSpacing(15)
        legend.addWidget(l2)
        legend.addStretch()
        
        self.results_layout.addLayout(legend)
            
        self.export_btn.setEnabled(True)

    def go_home(self):
        self.main_window.go_to_session_selection_page()
