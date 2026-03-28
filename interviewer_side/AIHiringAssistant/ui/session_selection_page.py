import os
import json
import glob
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QSplitter, QFrame, QGraphicsDropShadowEffect,
    QDialog, QTextBrowser, QFileDialog, QMessageBox
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ui.theme import Theme
from core.career_model import CareerPersonalityModel

class SessionSelectionPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_session_path = None
        self.selected_video_path = None
        self.selected_user_data = None

        # --- Apply Global Theme ---
        self.setStyleSheet(Theme.global_style() + f"""
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # --- Title ---
        title = QLabel("Session Selection")
        title.setStyleSheet(f"""
            font-size: 26px; 
            font-weight: 700; 
            color: {Theme.COLOR_TEXT_MAIN};
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # --- Main Content (Splitter) ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Theme.COLOR_BORDER};
            }}
        """)
        
        # Left: Session List
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 20, 0)
        left_layout.setSpacing(10)
        
        list_label = QLabel("Available Sessions")
        list_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Theme.COLOR_TEXT_SEC};")
        
        self.session_list = QListWidget()
        self.session_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.session_list.itemClicked.connect(self.on_session_selected)
        
        left_layout.addWidget(list_label)
        left_layout.addWidget(self.session_list)
        
        # Right: Details & Action
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 0, 0, 0)
        right_layout.setSpacing(15)

        details_header = QLabel("Session Details")
        details_header.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Theme.COLOR_TEXT_SEC};")
        
        # Details Pane (Card Style)
        self.details_frame = QFrame()
        self.details_frame.setStyleSheet(f"""
            QFrame {{
                {Theme.card_style()}
            }}
        """)
        
        # Subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255, 40)) # Soft cyan glow
        shadow.setOffset(0, 5)
        self.details_frame.setGraphicsEffect(shadow)

        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(20, 20, 20, 20)
        
        self.details_label = QLabel("Select a session to view details.")
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.details_label.setStyleSheet(f"""
            font-size: 14px; 
            color: {Theme.COLOR_TEXT_MAIN}; 
            border: none;
            background: transparent;
        """)
        
        details_layout.addWidget(self.details_label)
        details_layout.addStretch()

        # Action Buttons
        self.report_btn = QPushButton("SHOW REPORT")
        self.report_btn.setEnabled(False)
        self.report_btn.setFixedHeight(50)
        self.report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.report_btn.setStyleSheet(Theme.button_secondary())
        self.report_btn.clicked.connect(self.show_report_dialog)

        self.process_btn = QPushButton("Start Processing")
        self.process_btn.setEnabled(False)
        self.process_btn.setFixedHeight(50)
        self.process_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.process_btn.setStyleSheet(Theme.button_primary())
        self.process_btn.clicked.connect(self.process_session)
        
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.setFixedHeight(50)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet(Theme.button_secondary())
        self.refresh_btn.clicked.connect(self.load_sessions)
        
        right_layout.addWidget(details_header)
        right_layout.addWidget(self.details_frame, 2)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.report_btn)
        right_layout.addWidget(self.refresh_btn)
        right_layout.addWidget(self.process_btn)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        self.load_sessions()

    def load_sessions(self):
        self.session_list.clear()
        self.process_btn.setEnabled(False)
        self.report_btn.setEnabled(False)
        self.details_label.setText("Select a session to view details.")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_data_dir = os.path.join(base_dir, "user_data")
        
        if not os.path.exists(user_data_dir):
            self.details_label.setText(f"User data directory not found: {user_data_dir}")
            return

        sessions = [f.path for f in os.scandir(user_data_dir) if f.is_dir()]
        sessions.sort(key=lambda x: os.path.getmtime(x), reverse=True) 
        
        for session_path in sessions:
            folder_name = os.path.basename(session_path)
            display_name = folder_name
            reg_path = os.path.join(session_path, "registration.json")
            if os.path.exists(reg_path):
                try:
                    with open(reg_path, 'r') as f:
                        data = json.load(f)
                        user_name = data.get('name', 'Unknown')
                        display_name = f"{user_name} ({folder_name})"
                except:
                    pass
            
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, session_path)
            self.session_list.addItem(item)

    def on_session_selected(self, item):
        session_path = item.data(Qt.ItemDataRole.UserRole)
        self.selected_session_path = session_path
        
        reg_path = os.path.join(session_path, "registration.json")
        video_files = glob.glob(os.path.join(session_path, "*.mp4")) + \
                      glob.glob(os.path.join(session_path, "*.avi"))
        
        # HTML formatting using Theme colors
        details = f"<b style='font-size:15px; color:{Theme.COLOR_TEXT_MAIN};'>{os.path.basename(session_path)}</b><br><hr style='border: 1px solid {Theme.COLOR_BORDER};'><br>"
        
        self.selected_user_data = None
        self.selected_video_path = None
        
        if os.path.exists(reg_path):
            try:
                with open(reg_path, 'r') as f:
                    data = json.load(f)
                    self.selected_user_data = data
                    details += f"<span style='color:{Theme.COLOR_TEXT_SEC};'>Name:</span> <span style='color:{Theme.COLOR_TEXT_MAIN}; font-weight:600;'>{data.get('name', 'N/A')}</span><br>"
                    details += f"<span style='color:{Theme.COLOR_TEXT_SEC};'>ID:</span> <span style='color:{Theme.COLOR_TEXT_MAIN}; font-weight:600;'>{data.get('id', 'N/A')}</span><br>"
                    details += f"<span style='color:{Theme.COLOR_TEXT_SEC};'>Email:</span> <span style='color:{Theme.COLOR_TEXT_MAIN}; font-weight:600;'>{data.get('email', 'N/A')}</span><br>"
            except Exception as e:
                details += f"<span style='color:{Theme.COLOR_DANGER};'>Error loading registration: {e}</span><br>"
        else:
             details += f"<span style='color:{Theme.COLOR_WARNING};'>No registration.json found.</span><br>"
             
        summary_path = os.path.join(session_path, "summary.json")
        is_processed = False
        if os.path.exists(summary_path):
            try:
                with open(summary_path, 'r') as f:
                    summary_data = json.load(f)
                if summary_data.get("ocean_scores"):
                    is_processed = True
            except: pass

        if video_files:
            video_file = video_files[0]
            self.selected_video_path = video_file
            details += f"<br><span style='color:{Theme.COLOR_TEXT_SEC};'>Video Source:</span> <span style='color:{Theme.COLOR_TEXT_MAIN};'>{os.path.basename(video_file)}</span><br>"
            if is_processed:
                details += f"<br><span style='color:{Theme.COLOR_SUCCESS}; font-weight:bold;'>✓ Processing Complete</span>"
            else:
                details += f"<br><span style='color:{Theme.COLOR_SUCCESS}; font-weight:bold;'>✓ Ready for processing</span>"
        else:
            details += f"<br><span style='color:{Theme.COLOR_DANGER}; font-weight:bold;'>⚠ No video source found</span>"
            
        self.details_label.setText(details)
        
        if self.selected_video_path and self.selected_user_data and not is_processed:
            self.process_btn.setVisible(True)
            self.process_btn.setEnabled(True)
        else:
            self.process_btn.setVisible(False)
            self.process_btn.setEnabled(False)
            
        if is_processed:
            self.report_btn.setVisible(True)
            self.report_btn.setEnabled(True)
        else:
            self.report_btn.setVisible(False)
            self.report_btn.setEnabled(False)

    def process_session(self):
        if self.selected_user_data and self.selected_video_path:
            self.main_window.go_to_alignment_page(
                self.selected_user_data, 
                self.selected_video_path
            )

    def show_report_dialog(self):
        if not self.selected_session_path or not self.selected_user_data:
            return
            
        safe_name = self.selected_user_data.get('name', 'Candidate').replace(' ', '_')
        if not safe_name: safe_name = "Candidate"
        pdf_path = os.path.join(self.selected_session_path, f"{safe_name}_Report.pdf")
        
        if os.path.exists(pdf_path):
            try:
                os.startfile(os.path.abspath(pdf_path))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open PDF: {e}")
        else:
            QMessageBox.information(self, "Not Found", "PDF Report not found for this session. It may not be fully processed yet.")
