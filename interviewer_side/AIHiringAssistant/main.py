import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.home_page import HomePage
# from ui.user_page import UserPage # No longer needed
from ui.session_selection_page import SessionSelectionPage
from ui.alignment_page import AlignmentPage
from ui.ml_result_page import MlResultPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Based Hiring Assistant (Video Processing Mode)")
        self.setGeometry(100, 100, 1400, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self)
        self.session_selection_page = SessionSelectionPage(self)
        self.alignment_page = AlignmentPage(self)
        self.ml_result_page = MlResultPage(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.session_selection_page)
        self.stack.addWidget(self.alignment_page)
        self.stack.addWidget(self.ml_result_page)

        self.stack.setCurrentWidget(self.home_page)

    def go_to_session_selection_page(self):
        self.session_selection_page.load_sessions() # Refresh list
        self.stack.setCurrentWidget(self.session_selection_page)

    def go_to_alignment_page(self, user_data, video_path):
        self.alignment_page.set_session(user_data, video_path)
        self.stack.setCurrentWidget(self.alignment_page)

    def go_to_ml_result_page(self, user_data, session_path, csv_path=None):
        self.ml_result_page.process_session(user_data, session_path, csv_path)
        self.stack.setCurrentWidget(self.ml_result_page)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
