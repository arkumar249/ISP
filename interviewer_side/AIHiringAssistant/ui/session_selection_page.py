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
             
        if video_files:
            video_file = video_files[0]
            self.selected_video_path = video_file
            details += f"<br><span style='color:{Theme.COLOR_TEXT_SEC};'>Video Source:</span> <span style='color:{Theme.COLOR_TEXT_MAIN};'>{os.path.basename(video_file)}</span><br>"
            details += f"<br><span style='color:{Theme.COLOR_SUCCESS}; font-weight:bold;'>✓ Ready for processing</span>"
        else:
            details += f"<br><span style='color:{Theme.COLOR_DANGER}; font-weight:bold;'>⚠ No video source found</span>"
            
        self.details_label.setText(details)
        
        if self.selected_video_path and self.selected_user_data:
            self.process_btn.setEnabled(True)
        else:
            self.process_btn.setEnabled(False)
            
        if self.selected_user_data:
            self.report_btn.setEnabled(True)
        else:
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
            
        ocean_scores = {'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0}
        summary_path = os.path.join(self.selected_session_path, "summary.json")
        if os.path.exists(summary_path):
            try:
                with open(summary_path, 'r') as f:
                    summary_data = json.load(f)
                    raw_scores = summary_data.get('ocean_scores', {})
                    ocean_scores['O'] = raw_scores.get('Openness', ocean_scores['O'])
                    ocean_scores['C'] = raw_scores.get('Conscientiousness', ocean_scores['C'])
                    ocean_scores['E'] = raw_scores.get('Extraversion', ocean_scores['E'])
                    ocean_scores['A'] = raw_scores.get('Agreeableness', ocean_scores['A'])
                    ocean_scores['N'] = raw_scores.get('Neuroticism', ocean_scores['N'])
            except:
                pass
                
        image_html = ""
        img_path = os.path.join(self.selected_session_path, "aligned_face.jpg")
        if os.path.exists(img_path):
            img_uri = f"file://{img_path}"
            image_html = f"<img src='{img_uri}' width='150' alt='Candidate'>"
        else:
            image_html = f"<div style='color:#bdc3c7; padding:50px 0;'>No Image</div>"
            
        try:
            model = CareerPersonalityModel()
            top_3 = model.get_top_3_profiles(ocean_scores)
            
            job_profile = self.selected_user_data.get('job_profile', '')
            if job_profile:
                suitability = model.get_job_suitability_percentage(ocean_scores, job_profile)
            else:
                suitability = "N/A"
        except Exception as e:
            top_3 = ["Software Engineer", "Data Scientist", "Product Manager"]
            suitability = "75%"
            
        top_3_html = "<ul>" + "".join([f"<li>{prof}</li>" for prof in top_3]) + "</ul>"
        
        name = self.selected_user_data.get('name', 'N/A')
        email = self.selected_user_data.get('email', 'N/A')
        age = self.selected_user_data.get('age', 'N/A')
        job = self.selected_user_data.get('job_profile', 'Not Specified')
        
        html_str = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #2c3e50; line-height: 1.6; background-color: #ffffff; }}
            h1 {{ color: {Theme.COLOR_PRIMARY}; text-align: center; border-bottom: 2px solid #ecf0f1; padding-bottom: 15px; letter-spacing: 1px; font-weight: 300; font-size: 28px; margin-bottom: 30px; }}
            h3 {{ color: #34495e; font-weight: 600; font-size: 18px; margin-top: 0; padding-bottom: 8px; border-bottom: 1px solid #ecf0f1; }}
            .card {{ background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; margin-bottom: 20px; }}
            .highlight-card {{ background-color: #f0f7ff; border: 1px solid #cce5ff; border-left: 5px solid {Theme.COLOR_PRIMARY}; padding: 20px; margin-top: 25px; }}
            .label {{ font-weight: bold; color: #7f8c8d; font-size: 14px; }}
            .value {{ font-weight: 600; color: #2c3e50; font-size: 15px; }}
            .score-box {{ background-color: #ffffff; border: 1px solid #dee2e6; padding: 10px; text-align: center; margin: 5px; }}
            .score-title {{ font-size: 11px; color: #7f8c8d; font-weight: bold; text-transform: uppercase; }}
            .score-val {{ font-size: 18px; color: {Theme.COLOR_PRIMARY}; font-weight: bold; }}
            ul {{ margin-top: 10px; padding-left: 20px; color: #34495e; font-size: 15px; font-weight: 500; }}
            li {{ margin-bottom: 8px; }}
            .suitability {{ font-size: 20px; font-weight: bold; color: #27ae60; background: #e8f8f5; padding: 10px 15px; border-radius: 8px; display: inline-block; margin-top: 15px; }}
        </style>
        </head>
        <body>
            <h1>CANDIDATE EVALUATION REPORT</h1>
            
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 25px;">
                <tr>
                    <td width="30%" valign="top" align="center">
                        <div style="background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px;">
                            {image_html}
                        </div>
                    </td>
                    <td width="5%"></td>
                    <td width="65%" valign="top">
                        <div class="card" style="margin-bottom: 0;">
                            <h3>Candidate Details</h3>
                            <table width="100%" cellpadding="5" cellspacing="0" border="0">
                                <tr>
                                    <td width="35%" class="label">Full Name:</td>
                                    <td class="value">{name}</td>
                                </tr>
                                <tr>
                                    <td class="label">Email Address:</td>
                                    <td class="value">{email}</td>
                                </tr>
                                <tr>
                                    <td class="label">Age:</td>
                                    <td class="value">{age}</td>
                                </tr>
                                <tr>
                                    <td class="label">Target Role:</td>
                                    <td class="value">{job}</td>
                                </tr>
                            </table>
                        </div>
                    </td>
                </tr>
            </table>
            
            <div class="card">
                <h3>OCEAN Personality Profile</h3>
                <p style="color: #7f8c8d; font-size: 13px; margin-top: 0; margin-bottom: 15px;">Extracted from behavioral analysis across interview sessions.</p>
                <table width="100%" cellpadding="5" cellspacing="0" border="0">
                    <tr>
                        <td width="20%" align="center">
                            <div class="score-box">
                                <div class="score-title">Openness</div>
                                <div class="score-val">{float(ocean_scores.get('O',0)):.2f}</div>
                            </div>
                        </td>
                        <td width="20%" align="center">
                            <div class="score-box">
                                <div class="score-title">Conscient.</div>
                                <div class="score-val">{float(ocean_scores.get('C',0)):.2f}</div>
                            </div>
                        </td>
                        <td width="20%" align="center">
                            <div class="score-box">
                                <div class="score-title">Extraversion</div>
                                <div class="score-val">{float(ocean_scores.get('E',0)):.2f}</div>
                            </div>
                        </td>
                        <td width="20%" align="center">
                            <div class="score-box">
                                <div class="score-title">Agreeable.</div>
                                <div class="score-val">{float(ocean_scores.get('A',0)):.2f}</div>
                            </div>
                        </td>
                        <td width="20%" align="center">
                            <div class="score-box">
                                <div class="score-title">Neuroticism</div>
                                <div class="score-val">{float(ocean_scores.get('N',0)):.2f}</div>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            
            <div class="highlight-card">
                <h3 style="border-bottom:none; color: {Theme.COLOR_PRIMARY};">Career Match Analysis</h3>
                
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td width="55%" valign="top">
                            <div class="label" style="margin-bottom: 10px;">Top Recommended Profiles:</div>
                            {top_3_html}
                        </td>
                        <td width="45%" valign="top" align="center" style="border-left: 1px solid #cce5ff; padding-left: 20px;">
                            <div class="label">Suitability for Target Role</div>
                            <div style="font-size: 15px; font-weight: 500; color: #34495e; margin-top: 5px;">{job}</div>
                            <br>
                            <span class="suitability" style="color: #27ae60; border: 2px solid #27ae60; padding: 5px;">{suitability} MATCH</span>
                        </td>
                    </tr>
                </table>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #bdc3c7; font-size: 12px;">
                Generated by AI Hiring Assistant • Date: {os.path.basename(self.selected_session_path)}
            </div>
        </body>
        </html>
        """
        
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle("Candidate Report")
        report_dialog.resize(800, 750)
        report_dialog.setStyleSheet(Theme.global_style())
        
        layout = QVBoxLayout(report_dialog)
        
        text_browser = QTextBrowser()
        text_browser.setHtml(html_str)
        text_browser.setStyleSheet("background-color: white; color: black; border-radius: 8px;")
        layout.addWidget(text_browser)
        
        download_btn = QPushButton("Download PDF")
        download_btn.setFixedHeight(50)
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        download_btn.setStyleSheet(Theme.button_primary())
        
        def on_download():
            file_path, _ = QFileDialog.getSaveFileName(
                report_dialog, "Save PDF Report", 
                f"{name.replace(' ', '_')}_Report.pdf", 
                "PDF Files (*.pdf)"
            )
            if file_path:
                if not file_path.endswith('.pdf'):
                    file_path += '.pdf'
                printer = QPrinter(QPrinter.PrinterMode.ScreenResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(file_path)
                text_browser.document().print(printer)
                QMessageBox.information(report_dialog, "Success", f"Report saved to {{file_path}}")
                
        download_btn.clicked.connect(on_download)
        layout.addWidget(download_btn)
        
        report_dialog.exec()
