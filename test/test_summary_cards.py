"""Test to verify summary card update issue"""
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout
import sys
from travel_billing_software.config.config import format_currency, get_currency_symbol


def test_findChildren_issue():
    """Test if findChildren returns too many frames"""
    app = QApplication(sys.argv)
    
    # Create a summary frame similar to the app
    summary_frame = QFrame()
    summary_layout = QVBoxLayout(summary_frame)
    
    # Add 3 child cards
    for i in range(3):
        card = QFrame()
        card_layout = QVBoxLayout(card)
        
        title = QLabel(f"Card {i+1} Title")
        card_layout.addWidget(title)
        
        value = QLabel(format_currency(0))
        value.setProperty('summary_value', True)
        card_layout.addWidget(value)
        
        summary_layout.addWidget(card)
    
    # Test findChildren
    all_frames = summary_frame.findChildren(QFrame)
    print(f"Total QFrames found: {len(all_frames)}")
    print("This includes the parent summary_frame itself and all child cards!")
    
    # The issue: findChildren returns parent + 3 cards = 4 frames
    # But we only want the 3 cards
    
    # Correct way: Get direct children only
    direct_children = [child for child in summary_frame.children() if isinstance(child, QFrame)]
    print(f"\nDirect QFrame children: {len(direct_children)}")
    
    # Even better: Get widgets from layout
    layout_items = []
    for i in range(summary_frame.layout().count()):
        widget = summary_frame.layout().itemAt(i).widget()
        if isinstance(widget, QFrame):
            layout_items.append(widget)
    print(f"QFrames in layout: {len(layout_items)}")
    
    print("\n" + "="*50)
    print("SOLUTION: Use layout().itemAt(i).widget() instead of findChildren(QFrame)")
    print("="*50)

if __name__ == '__main__':
    test_findChildren_issue()
