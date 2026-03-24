"""
AI Hiring Assistant - Premium Dark Theme Stylesheet
Aesthetic Direction: Neo-Corporate Futurism
- Glassmorphism effects with frosted transparency
- Gradient mesh backgrounds and accent glows
- Refined typography with distinctive font choices
- Subtle micro-animations and hover effects
- Luxury tech brand feel with AI undertones
"""

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE - Deep Space with Electric Accents
# ═══════════════════════════════════════════════════════════════════════════════

# Primary - Deep cosmic darkness
VOID_BLACK = "#0a0a0f"
OBSIDIAN = "#12121a"
CHARCOAL_DEPTH = "#1a1a24"
SLATE_MIST = "#252532"

# Accent - Electric cyan with warm gold highlights
ELECTRIC_CYAN = "#00d4ff"
CYAN_GLOW = "#00e5ff"
WARM_GOLD = "#ffd700"
SUNSET_CORAL = "#ff6b6b"
AURORA_GREEN = "#00ffa3"
VIOLET_PULSE = "#a855f7"

# Neutrals - Refined silver tones
SILVER_100 = "#f8f9fa"
SILVER_200 = "#e9ecef"
SILVER_300 = "#dee2e6"
SILVER_400 = "#ced4da"
SILVER_500 = "#adb5bd"
SILVER_600 = "#6c757d"

# Semantic
SUCCESS_GLOW = "#00ffa3"
ERROR_FLAME = "#ff4757"
WARNING_AMBER = "#ffa502"

# Gradients (for reference in code)
GRADIENT_PRIMARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d4ff, stop:1 #a855f7)"
GRADIENT_WARM = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffd700, stop:1 #ff6b6b)"
GRADIENT_AURORA = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00ffa3, stop:1 #00d4ff)"

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL APPLICATION STYLESHEET
# ═══════════════════════════════════════════════════════════════════════════════

GLOBAL_STYLESHEET = f"""
/* ══════════════════════════════════════════════════════════════════════════════
   GLOBAL RESET & BASE STYLES
   ══════════════════════════════════════════════════════════════════════════════ */

QMainWindow, QWidget {{
    background-color: {VOID_BLACK};
    color: {SILVER_200};
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', sans-serif;
    font-size: 14px;
    letter-spacing: 0.3px;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   PRIMARY BUTTONS - Gradient Glow Effect
   ══════════════════════════════════════════════════════════════════════════════ */

QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                stop:0 {ELECTRIC_CYAN}, stop:1 {VIOLET_PULSE});
    color: {VOID_BLACK};
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.5px;
    min-width: 120px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                stop:0 {CYAN_GLOW}, stop:0.5 {ELECTRIC_CYAN}, stop:1 {VIOLET_PULSE});
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                stop:0 {VIOLET_PULSE}, stop:1 {ELECTRIC_CYAN});
    padding: 15px 28px 13px 28px;
}}

QPushButton:disabled {{
    background: {SLATE_MIST};
    color: {SILVER_600};
}}

/* Secondary Button Style */
QPushButton[secondary="true"] {{
    background: transparent;
    border: 2px solid {SILVER_500};
    color: {SILVER_200};
}}

QPushButton[secondary="true"]:hover {{
    border-color: {ELECTRIC_CYAN};
    color: {ELECTRIC_CYAN};
    background: rgba(0, 212, 255, 0.1);
}}

/* Ghost Button */
QPushButton[ghost="true"] {{
    background: transparent;
    border: none;
    color: {SILVER_400};
}}

QPushButton[ghost="true"]:hover {{
    color: {ELECTRIC_CYAN};
    background: rgba(0, 212, 255, 0.05);
}}

/* ══════════════════════════════════════════════════════════════════════════════
   INPUT FIELDS - Glassmorphism Style
   ══════════════════════════════════════════════════════════════════════════════ */

QLineEdit, QSpinBox {{
    background: rgba(37, 37, 50, 0.6);
    color: {SILVER_100};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 15px;
    selection-background-color: {ELECTRIC_CYAN};
    selection-color: {VOID_BLACK};
}}

QLineEdit:focus, QSpinBox:focus {{
    border: 1px solid {ELECTRIC_CYAN};
    background: rgba(37, 37, 50, 0.8);
}}

QLineEdit:hover, QSpinBox:hover {{
    border: 1px solid rgba(0, 212, 255, 0.4);
}}

QLineEdit[error="true"] {{
    border: 1px solid {ERROR_FLAME};
    background: rgba(255, 71, 87, 0.1);
}}

QLineEdit::placeholder {{
    color: {SILVER_600};
}}

/* ══════════════════════════════════════════════════════════════════════════════
   COMBO BOX - Elegant Dropdown
   ══════════════════════════════════════════════════════════════════════════════ */

QComboBox {{
    background: rgba(37, 37, 50, 0.6);
    color: {SILVER_100};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 15px;
    min-width: 150px;
}}

QComboBox:hover {{
    border: 1px solid rgba(0, 212, 255, 0.4);
}}

QComboBox:focus {{
    border: 1px solid {ELECTRIC_CYAN};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 15px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid {ELECTRIC_CYAN};
    margin-right: 12px;
}}

QComboBox QAbstractItemView {{
    background: {CHARCOAL_DEPTH};
    color: {SILVER_100};
    selection-background-color: rgba(0, 212, 255, 0.2);
    selection-color: {ELECTRIC_CYAN};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 5px;
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    padding: 10px 15px;
    border-radius: 6px;
}}

QComboBox QAbstractItemView::item:hover {{
    background: rgba(0, 212, 255, 0.1);
}}

/* ══════════════════════════════════════════════════════════════════════════════
   LABELS - Typography Hierarchy
   ══════════════════════════════════════════════════════════════════════════════ */

QLabel {{
    color: {SILVER_300};
    font-size: 14px;
    background: transparent;
}}

QLabel[heading="true"] {{
    font-size: 42px;
    font-weight: 700;
    color: {SILVER_100};
    letter-spacing: -0.5px;
}}

QLabel[subheading="true"] {{
    font-size: 18px;
    font-weight: 400;
    color: {SILVER_500};
    letter-spacing: 0.2px;
}}

QLabel[caption="true"] {{
    font-size: 12px;
    color: {SILVER_600};
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

QLabel[error="true"] {{
    color: {ERROR_FLAME};
    font-size: 12px;
    font-weight: 500;
}}

QLabel[success="true"] {{
    color: {SUCCESS_GLOW};
    font-weight: 600;
}}

QLabel[warning="true"] {{
    color: {WARNING_AMBER};
    font-weight: 600;
}}

QLabel[accent="true"] {{
    color: {ELECTRIC_CYAN};
}}

/* ══════════════════════════════════════════════════════════════════════════════
   CARDS & FRAMES - Glassmorphism Containers
   ══════════════════════════════════════════════════════════════════════════════ */

QFrame[card="true"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(37, 37, 50, 0.8), 
                                stop:1 rgba(26, 26, 36, 0.9));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
}}

QFrame[card="true"]:hover {{
    border: 1px solid rgba(0, 212, 255, 0.2);
}}

QFrame[glowCard="true"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(37, 37, 50, 0.9), 
                                stop:1 rgba(26, 26, 36, 0.95));
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   SCROLL AREAS - Minimal Scrollbars
   ══════════════════════════════════════════════════════════════════════════════ */

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: rgba(255, 255, 255, 0.15);
    border-radius: 4px;
    min-height: 40px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ELECTRIC_CYAN};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   PROGRESS BAR - Gradient Fill
   ══════════════════════════════════════════════════════════════════════════════ */

QProgressBar {{
    border: none;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    height: 12px;
    text-align: center;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                stop:0 {ELECTRIC_CYAN}, stop:1 {VIOLET_PULSE});
    border-radius: 6px;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   RADIO BUTTONS & CHECKBOXES - Custom Styled
   ══════════════════════════════════════════════════════════════════════════════ */

QRadioButton {{
    color: {SILVER_300};
    spacing: 10px;
    font-size: 14px;
}}

QRadioButton::indicator {{
    width: 22px;
    height: 22px;
    border-radius: 11px;
    border: 2px solid {SILVER_500};
    background: transparent;
}}

QRadioButton::indicator:hover {{
    border: 2px solid {ELECTRIC_CYAN};
}}

QRadioButton::indicator:checked {{
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                                fx:0.5, fy:0.5,
                                stop:0 {ELECTRIC_CYAN}, stop:0.6 {ELECTRIC_CYAN}, 
                                stop:0.7 transparent);
    border: 2px solid {ELECTRIC_CYAN};
}}

/* ══════════════════════════════════════════════════════════════════════════════
   SLIDERS - Gradient Track with Glowing Handle
   ══════════════════════════════════════════════════════════════════════════════ */

QSlider::groove:horizontal {{
    border: none;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {ELECTRIC_CYAN};
    border: none;
    width: 20px;
    height: 20px;
    margin: -7px 0;
    border-radius: 10px;
}}

QSlider::handle:horizontal:hover {{
    background: {CYAN_GLOW};
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                stop:0 {ELECTRIC_CYAN}, stop:1 {VIOLET_PULSE});
    border-radius: 3px;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   TEXT BROWSER - Code/JSON Display
   ══════════════════════════════════════════════════════════════════════════════ */

QTextBrowser {{
    background: rgba(10, 10, 15, 0.9);
    color: {AURORA_GREEN};
    border: 1px solid rgba(0, 255, 163, 0.2);
    border-radius: 12px;
    padding: 20px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.5;
    selection-background-color: rgba(0, 255, 163, 0.3);
}}

/* ══════════════════════════════════════════════════════════════════════════════
   GROUP BOX - Section Containers
   ══════════════════════════════════════════════════════════════════════════════ */

QGroupBox {{
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    margin-top: 16px;
    padding-top: 24px;
    font-weight: 500;
    background: transparent;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 10px;
    color: {ELECTRIC_CYAN};
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   MESSAGE BOX - Styled Dialogs
   ══════════════════════════════════════════════════════════════════════════════ */

QMessageBox {{
    background: {CHARCOAL_DEPTH};
}}

QMessageBox QLabel {{
    color: {SILVER_200};
    font-size: 14px;
}}

QMessageBox QPushButton {{
    min-width: 100px;
    padding: 10px 20px;
}}

/* ══════════════════════════════════════════════════════════════════════════════
   TOOLTIPS - Floating Info Cards
   ══════════════════════════════════════════════════════════════════════════════ */

QToolTip {{
    background: {CHARCOAL_DEPTH};
    color: {SILVER_200};
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE-SPECIFIC STYLES (to be applied directly in widgets)
# ═══════════════════════════════════════════════════════════════════════════════

LANDING_PAGE_STYLE = f"""
QWidget#landingPage {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {VOID_BLACK}, 
                                stop:0.5 {OBSIDIAN},
                                stop:1 {CHARCOAL_DEPTH});
}}
"""

CAMERA_FRAME_ALIGNED = f"""
QFrame {{
    background: {VOID_BLACK};
    border-radius: 16px;
    border: 3px solid {AURORA_GREEN};
}}
"""

CAMERA_FRAME_WARNING = f"""
QFrame {{
    background: {VOID_BLACK};
    border-radius: 16px;
    border: 3px solid {WARNING_AMBER};
}}
"""

CAMERA_FRAME_ERROR = f"""
QFrame {{
    background: {VOID_BLACK};
    border-radius: 16px;
    border: 3px solid {ERROR_FLAME};
}}
"""

CAMERA_FRAME_DEFAULT = f"""
QFrame {{
    background: {VOID_BLACK};
    border-radius: 16px;
    border: 3px solid rgba(255, 255, 255, 0.1);
}}
"""


def get_scale_button_style(value: int, is_selected: bool = False) -> str:
    """Generate style for OCEAN scale buttons with gradient based on value."""
    if is_selected:
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 {ELECTRIC_CYAN}, stop:1 {VIOLET_PULSE});
                color: {VOID_BLACK};
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }}
        """
    else:
        return f"""
            QPushButton {{
                background: rgba(37, 37, 50, 0.6);
                color: {SILVER_200};
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(0, 212, 255, 0.15);
                border: 1px solid {ELECTRIC_CYAN};
                color: {ELECTRIC_CYAN};
            }}
        """


def get_trait_badge_style(trait: str) -> str:
    """Generate badge style based on OCEAN trait."""
    colors = {
        "Openness": (VIOLET_PULSE, "rgba(168, 85, 247, 0.15)"),
        "Conscientiousness": (ELECTRIC_CYAN, "rgba(0, 212, 255, 0.15)"),
        "Extraversion": (WARM_GOLD, "rgba(255, 215, 0, 0.15)"),
        "Agreeableness": (AURORA_GREEN, "rgba(0, 255, 163, 0.15)"),
        "Neuroticism": (SUNSET_CORAL, "rgba(255, 107, 107, 0.15)"),
    }
    color, bg = colors.get(trait, (ELECTRIC_CYAN, "rgba(0, 212, 255, 0.15)"))
    return f"""
        color: {color};
        font-size: 13px;
        font-weight: 600;
        background-color: {bg};
        padding: 6px 16px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    """
