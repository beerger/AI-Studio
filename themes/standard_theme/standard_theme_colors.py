# theme_colors.py

"""
This file defines all color constants used in the application theme.
Each color includes comments describing its purpose and where it is applied.
Modify these values to create a new theme.
"""

# General Colors
PRIMARY_BACKGROUND = "rgb(40, 44, 52)"  # Overall background for widgets and panels
SECONDARY_BACKGROUND = "rgb(33, 37, 43)"  # Slightly lighter background for contrast
ACCENT_BACKGROUND = "rgb(40, 44, 52)"  # Hover states and active elements
HIGHLIGHT_BACKGROUND = "rgb(189, 147, 249)"  # Selected tabs or emphasized states

# Border Colors
DEFAULT_BORDER = "rgb(44, 49, 58)"  # Default or inactive borders
HOVER_BORDER = "rgb(64, 71, 88)"  # Borders for hover states
FOCUS_BORDER = "rgb(91, 101, 124)"  # Borders for focused states
HIGHLIGHT_BORDER = "rgb(255, 121, 198)"  # Emphasized or selected states
# Used in:
#   hoverContainer:hover
#   QTabBar::tab:selected
#   NetworkConnectionLine

# Text Colors
PRIMARY_TEXT = "rgb(221, 221, 221)"  # Default text color for most UI elements
SECONDARY_TEXT = "rgb(113, 126, 149)"  # Muted or less prominent text
HIGHLIGHT_TEXT = "rgb(255, 255, 255)"  # Selected or emphasized text
SELECTION_TEXT = "rgb(255, 121, 198)"
# Used in:
#   QWidget
#   QLineEdit::selection

# Scroll and Slider Colors
SCROLL_GROOVE_BACKGROUND = "rgb(52, 59, 72)"  # Background for scroll grooves
SCROLL_HANDLE_START = "rgb(189, 147, 249)"  # Gradient start for scroll handles
SCROLL_HANDLE_END = "rgb(189, 147, 249)"  # Gradient end for scroll handles

SLIDER_GROOVE = "rgb(52, 59, 72)"  # Background for slider grooves
SLIDER_HANDLE = "rgb(189, 147, 249)"  # Background for slider handles

# Button Colors
BUTTON_BACKGROUND = "rgb(52, 59, 72)"  # Default button background
BUTTON_HOVER_BACKGROUND = "rgb(57, 65, 80)"  # Button background on hover
BUTTON_HOVER_BORDER  = "rgb(61, 70, 86)"
BUTTON_PRESSED_BACKGROUND = "rgb(35, 40, 49)"  # Button background when pressed
BUTTON_PRESSED_BORDER = "rgb(43, 50, 61)"

# Miscellaneous Colors
TOOLTIP_BACKGROUND = "rgba(33, 37, 43, 180)"  # Background for tooltips
CATEGORY_DIVIDER = "rgb(44, 49, 58)"  # For dividers like QFrame lines

# Check Box
TICK_WIDGET_BACKGROUND = "rgb(44, 49, 60)"  # Background for check box and radio buttons
TICK_WIDGET_BORDER = "rgb(52, 59, 72)"  # Border for check box and radio buttons

# Combo Box
COMBO_BOX_SEPARATOR = "rgba(39, 44, 54, 150)"  # Separator line between arrow and text
COMBO_BOX_SELECTION = "rgb(33, 37, 43)"  # Background for selected item in combo box

PANE_BORDER = "rgb(44, 49, 58)" # Bottom border for panes

# Network Connection Line
NETWORK_CONNECTION_LINE = "rgb(255, 121, 198)"  # Color for network connection lines

STATUS_BAR = "rgb(44, 49, 58)"  # Status bar background color

LINK_LABEL = "rgb(189, 147, 249)"  # Link color for QLabel