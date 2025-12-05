"""
Utility functions for styling widgets and applying themes
Dynamic Version: Adapts to Font Size and Theme Color from ConfigManager
"""
from travel_billing_software.config.config import COLORS, LAYOUT_CONFIG, cm

def get_base_font_size():
    """Fetch the current font size setting from the manager."""
    return cm.get_app_settings().get("font_size", 12)

def get_frame_style():
    """Get standard frame stylesheet."""
    return f"""
        QFrame {{
            background-color: {COLORS['secondary_bg']};
            border-radius: {LAYOUT_CONFIG['border_radius']};
            border: 1px solid {COLORS['border_primary']};
            padding: 15px;
        }}
    """

def get_label_style(bold=False, size='normal', color='text_secondary'):
    """Get label stylesheet with dynamic font size."""
    base_size = get_base_font_size()
    
    # Scale font size based on type
    size_map = {
        'title': int(base_size * 2),       # e.g., 24px
        'heading': int(base_size * 1.4),   # e.g., 16px
        'subheading': int(base_size * 1.2),# e.g., 14px
        'normal': base_size,               # e.g., 12px
        'small': int(base_size * 0.9),     # e.g., 10px
    }
    
    final_size = size_map.get(size, base_size)
    weight = "bold" if bold else "normal"
    text_color = COLORS.get(color, COLORS['text_secondary'])
    
    return f"""
        QLabel {{
            color: {text_color};
            font-size: {final_size}px;
            font-weight: {weight};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
    """

def get_input_style():
    """Get standard input field stylesheet with dynamic sizing."""
    base_size = get_base_font_size()
    
    return f"""
        QLineEdit {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-size: {base_size}px;
            min-height: {base_size + 10}px; /* Auto-scale height */
        }}
        QLineEdit:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
    """

def get_dateedit_style():
    base_size = get_base_font_size()
    return f"""
        QDateEdit {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-size: {base_size}px;
            min-height: {base_size + 10}px;
        }}
        QDateEdit:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
        QDateEdit::drop-down {{
            border: none;
            background-color: {COLORS['accent_primary']};
        }}
    """

def get_combobox_style():
    base_size = get_base_font_size()
    return f"""
        QComboBox {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-size: {base_size}px;
            min-height: {base_size + 10}px;
        }}
        QComboBox:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: {COLORS['accent_primary']};
        }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            selection-background-color: {COLORS['accent_primary']};
            border: 1px solid {COLORS['border_primary']};
        }}
    """

def get_spinbox_style():
    base_size = get_base_font_size()
    return f"""
        QDoubleSpinBox, QSpinBox {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-size: {base_size}px;
            min-height: {base_size + 10}px;
        }}
        QDoubleSpinBox:focus, QSpinBox:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
        QDoubleSpinBox::up-button, QSpinBox::up-button {{
            background-color: {COLORS['accent_primary']};
            width: 15px;
        }}
        QDoubleSpinBox::down-button, QSpinBox::down-button {{
            background-color: {COLORS['accent_primary']};
            width: 15px;
        }}
    """

def get_button_style(button_type='save'):
    """Get button stylesheet based on type with dynamic sizing."""
    base_size = get_base_font_size()
    
    # Map types to colors
    btn_colors = {
        'save': COLORS["success"],
        'pdf': COLORS["danger"],
        'print': COLORS["info"],
        'share': COLORS["teal"],
        'add': COLORS["accent_primary"],
        'delete': COLORS["danger"],
    }
    
    bg = btn_colors.get(button_type, COLORS['accent_primary'])
    
    return f"""
        QPushButton {{
            background-color: {bg};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: {LAYOUT_CONFIG['button_radius']};
            padding: 8px 16px;
            font-weight: bold;
            font-size: {base_size}px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent_secondary']};
        }}
    """

def get_table_style():
    """Get table widget stylesheet with dynamic font."""
    base_size = get_base_font_size()
    return f"""
        QTableWidget {{
            background-color: {COLORS['primary_bg']};
            alternate-background-color: {COLORS['tertiary_bg']};
            gridline-color: {COLORS['grid_lines']};
            color: {COLORS['text_secondary']};
            border: none;
            font-size: {base_size}px;
        }}
        QTableWidget::item {{
            padding: 5px;
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
        }}
        QHeaderView::section {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_primary']};
            padding: 8px;
            border: 1px solid {COLORS['border_primary']};
            border-bottom: 2px solid {COLORS['accent_primary']};
            font-weight: 600;
            font-size: 15px;
        }}
    """

def get_scrollarea_style():
    return f"""
        QScrollArea {{
            background-color: {COLORS['primary_bg']};
            border: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {COLORS['secondary_bg']};
            width: 12px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['accent_primary']};
            min-height: 20px;
            border-radius: 6px;
        }}
    """

# ==================== RESTORED HELPER FUNCTIONS ====================

def get_sidebar_style():
    """Get sidebar frame stylesheet."""
    return f"""
        QFrame {{
            background-color: {COLORS['primary_bg']};
            border-right: 1px solid {COLORS['border_secondary']};
        }}
    """

def get_sidebar_button_style(is_active=False):
    """Get sidebar button stylesheet."""
    base_size = get_base_font_size()
    bg_color = COLORS['accent_primary'] if is_active else 'transparent'
    text_color = COLORS['text_primary'] if is_active else COLORS['text_muted']
    
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: {LAYOUT_CONFIG['button_radius']};
            padding: 12px;
            text-align: left;
            font-size: {base_size}px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_primary']};
        }}
    """

def apply_fixed_width_label(label, width):
    """Apply fixed width to a label."""
    label.setFixedWidth(width)
    label.setStyleSheet(get_label_style(bold=True, size='normal'))

def apply_minimum_width_widget(widget, width):
    """Apply minimum width to a widget."""
    widget.setMinimumWidth(width)