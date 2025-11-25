"""
Utility functions for styling widgets and applying themes
"""
from travel_billing_software.config import COLORS, FONTS, LAYOUT_CONFIG, BUTTON_CONFIG


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
    """Get label stylesheet with customizable options."""
    font_size = FONTS[f'size_{size}']
    font_weight = FONTS['weight_bold'] if bold else FONTS['weight_normal']
    text_color = COLORS.get(color, COLORS['text_secondary'])
    
    return f"""
        QLabel {{
            color: {text_color};
            font-size: {font_size};
            font-weight: {font_weight};
            font-family: '{FONTS['family_primary']}', Arial, sans-serif;
        }}
    """


def get_input_style():
    """Get standard input field stylesheet."""
    return f"""
        QLineEdit {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-weight: {FONTS['weight_semibold']};
        }}
        QLineEdit:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
    """


def get_dateedit_style():
    """Get date edit widget stylesheet."""
    return f"""
        QDateEdit {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-weight: {FONTS['weight_semibold']};
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
    """Get combobox (dropdown) stylesheet."""
    return f"""
        QComboBox {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-weight: {FONTS['weight_semibold']};
        }}
        QComboBox:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: {COLORS['accent_primary']};
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {COLORS['text_secondary']};
            margin-right: 5px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            selection-background-color: {COLORS['accent_primary']};
            border: 1px solid {COLORS['border_primary']};
        }}
    """


def get_spinbox_style():
    """Get spinbox stylesheet."""
    return f"""
        QDoubleSpinBox {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border_primary']};
            border-radius: {LAYOUT_CONFIG['input_radius']};
            padding: 5px;
            font-weight: {FONTS['weight_semibold']};
        }}
        QDoubleSpinBox:focus {{
            border: 1px solid {COLORS['border_focus']};
        }}
        QDoubleSpinBox::up-button {{
            background-color: {COLORS['accent_primary']};
            border-radius: 2px;
        }}
        QDoubleSpinBox::down-button {{
            background-color: {COLORS['accent_primary']};
            border-radius: 2px;
        }}
    """


def get_button_style(button_type='save'):
    """Get button stylesheet based on type."""
    config = BUTTON_CONFIG['colors'].get(button_type, BUTTON_CONFIG['colors']['save'])
    
    return f"""
        QPushButton {{
            background-color: {config['bg']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: {LAYOUT_CONFIG['button_radius']};
            padding: {BUTTON_CONFIG['padding']};
            font-weight: {BUTTON_CONFIG['font_weight']};
            font-size: {BUTTON_CONFIG['font_size']};
        }}
        QPushButton:hover {{
            background-color: {config['hover']};
        }}
        QPushButton:pressed {{
            background-color: {config['pressed']};
        }}
    """


def get_table_style():
    """Get table widget stylesheet."""
    return f"""
        QTableWidget {{
            background-color: {COLORS['primary_bg']};
            alternate-background-color: {COLORS['tertiary_bg']};
            gridline-color: {COLORS['grid_lines']};
            color: {COLORS['text_secondary']};
            border: none;
        }}
        QTableWidget::item {{
            padding: 5px;
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
        }}
        QTableWidget::item:selected {{
            background-color: {COLORS['accent_secondary']};
            color: {COLORS['text_primary']};
        }}
        QHeaderView::section {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_primary']};
            padding: 8px;
            border: 1px solid {COLORS['border_primary']};
            border-bottom: 2px solid {COLORS['accent_primary']};
            font-weight: {FONTS['weight_bold']};
        }}
        QTableWidget QTableCornerButton::section {{
            background-color: {COLORS['secondary_bg']};
            border: 1px solid {COLORS['border_primary']};
        }}
        QTableWidget::verticalHeader {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text_secondary']};
        }}
    """


def get_scrollarea_style():
    """Get scroll area stylesheet."""
    return f"""
        QScrollArea {{
            background-color: {COLORS['primary_bg']};
            border: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {COLORS['secondary_bg']};
            width: 12px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['accent_primary']};
            min-height: 20px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {COLORS['accent_secondary']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """


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
            font-size: {FONTS['size_normal']};
            font-weight: {FONTS['weight_semibold']};
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
