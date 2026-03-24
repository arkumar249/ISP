from PyQt6.QtGui import QColor, QFont

class Theme:
    # --- PRO COLOR PALETTE (Neo-Corporate Futurism) ---
    COLOR_BG = "#0a0a0f"           # Deep dark background
    COLOR_SURFACE = "rgba(30, 30, 42, 0.8)"  # Dark translucent surface
    COLOR_SURFACE_SOLID = "#1e1e2a" 
    COLOR_PRIMARY = "#00d4ff"      # Cyan
    COLOR_PRIMARY_HOVER = "#00e5ff" # Brighter cyan
    COLOR_ACCENT = "#a855f7"       # Purple 
    COLOR_TEXT_MAIN = "#f8f9fa"    # Bright text
    COLOR_TEXT_SEC = "#adb5bd"     # Dim text
    COLOR_BORDER = "rgba(255, 255, 255, 0.06)"  # Subtle glass border
    
    # Status Colors
    COLOR_SUCCESS = "#00ffa3"      # Neon green
    COLOR_WARNING = "#ffd700"      # Gold
    COLOR_DANGER = "#ff6b6b"       # Bright red
    COLOR_SUCCESS_BG = "rgba(0, 255, 163, 0.1)"
    COLOR_WARNING_BG = "rgba(255, 215, 0, 0.1)"
    COLOR_DANGER_BG = "rgba(255, 107, 107, 0.1)"

    # --- TYPOGRAPHY ---
    FONT_FAMILY = "Segoe UI"
    
    @staticmethod
    def get_font(size=14, weight="normal"):
        return f"font-family: '{Theme.FONT_FAMILY}', sans-serif; font-size: {size}px; font-weight: {weight};"

    # --- COMPONENT STYLES ---
    
    @staticmethod
    def global_style():
        return f"""
            QWidget {{
                background-color: {Theme.COLOR_BG};
                color: {Theme.COLOR_TEXT_MAIN};
                font-family: '{Theme.FONT_FAMILY}', sans-serif;
            }}
            QLabel {{
                color: {Theme.COLOR_TEXT_MAIN};
                background: transparent;
            }}
            QListWidget {{
                background-color: {Theme.COLOR_SURFACE_SOLID};
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 12px;
                padding: 10px;
                color: {Theme.COLOR_TEXT_MAIN};
            }}
            QListWidget::item:selected {{
                background-color: rgba(0, 212, 255, 0.1);
                border: 1px solid rgba(0, 212, 255, 0.3);
                border-radius: 8px;
            }}
        """

    @staticmethod
    def button_primary():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 {Theme.COLOR_PRIMARY}, stop:1 {Theme.COLOR_ACCENT});
                color: #0a0a0f;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 {Theme.COLOR_PRIMARY_HOVER}, stop:1 {Theme.COLOR_ACCENT});
            }}
            QPushButton:pressed {{
                background: {Theme.COLOR_ACCENT};
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }}
        """
        
    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.05);
                color: {Theme.COLOR_TEXT_MAIN};
                font-size: 14px;
                font-weight: 600;
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.2);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.15);
            }}
        """

    @staticmethod
    def button_danger():
        return f"""
            QPushButton {{
                background-color: {Theme.COLOR_DANGER_BG};
                color: {Theme.COLOR_DANGER};
                font-size: 14px;
                font-weight: bold;
                border: 1px solid rgba(255, 107, 107, 0.3);
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 107, 107, 0.2);
                border-color: {Theme.COLOR_DANGER};
            }}
        """

    @staticmethod
    def card_style():
        return f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 {Theme.COLOR_SURFACE}, 
                                        stop:1 rgba(20, 20, 30, 0.9));
            border: 1px solid {Theme.COLOR_BORDER};
            border-radius: 16px;
        """

    @staticmethod
    def input_style():
        return f"""
            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
                background-color: rgba(10, 10, 15, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px 14px;
                color: {Theme.COLOR_TEXT_MAIN};
                font-size: 14px;
            }}
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
                border: 1px solid {Theme.COLOR_PRIMARY};
                background-color: rgba(0, 212, 255, 0.05);
            }}
            QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder {{
                color: {Theme.COLOR_TEXT_SEC};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {Theme.COLOR_TEXT_SEC};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.COLOR_SURFACE_SOLID};
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 8px;
                color: {Theme.COLOR_TEXT_MAIN};
                selection-background-color: rgba(0, 212, 255, 0.2);
                selection-color: {Theme.COLOR_PRIMARY};
            }}
        """

    @staticmethod
    def scrollbar_style():
        return """
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: rgba(255, 255, 255, 0.05);
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.2);
                min-width: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """

    @staticmethod
    def apply_global(app):
        style = Theme.global_style() + "\\n" + Theme.scrollbar_style()
        app.setStyleSheet(style)
