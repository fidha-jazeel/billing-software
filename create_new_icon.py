"""
Create a new billing icon for the application
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_billing_icon():
    """Create a modern billing/invoice icon"""
    
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create image with transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Purple-teal gradient background circle
        padding = size // 8
        circle_bbox = [padding, padding, size - padding, size - padding]
        
        # Draw circle background with purple color
        draw.ellipse(circle_bbox, fill='#7c3aed')
        
        # Draw document/invoice icon
        doc_padding = size // 4
        doc_width = size - (2 * doc_padding)
        doc_height = int(doc_width * 1.3)
        doc_top = (size - doc_height) // 2
        doc_left = doc_padding
        
        # Document rectangle (white)
        doc_bbox = [doc_left, doc_top, doc_left + doc_width, doc_top + doc_height]
        draw.rectangle(doc_bbox, fill='white', outline='#e0e0e0', width=max(1, size//64))
        
        # Draw lines on document (representing text/items)
        line_padding = size // 12
        line_width = doc_width - (2 * line_padding)
        line_height = max(1, size // 32)
        line_spacing = size // 12
        
        # Header line (thicker - represents invoice title)
        if size >= 32:
            header_y = doc_top + line_padding
            draw.rectangle(
                [doc_left + line_padding, header_y, 
                 doc_left + line_padding + line_width, header_y + line_height + 1],
                fill='#7c3aed'
            )
        
        # Body lines (representing invoice items)
        num_lines = 2 if size < 64 else 3
        for i in range(num_lines):
            line_y = doc_top + line_padding + (line_spacing * (i + 1.5))
            if line_y + line_height < doc_top + doc_height - line_padding:
                draw.rectangle(
                    [doc_left + line_padding, line_y, 
                     doc_left + line_padding + line_width * 0.7, line_y + max(1, line_height - 1)],
                    fill='#94a3b8'
                )
        
        # Add currency symbol or $ sign for larger icons
        if size >= 48:
            # Draw a small teal circle in the corner
            badge_size = size // 4
            badge_x = size - padding - badge_size
            badge_y = size - padding - badge_size
            draw.ellipse(
                [badge_x, badge_y, badge_x + badge_size, badge_y + badge_size],
                fill='#14b8a6'
            )
            
            # Draw $ or ₹ symbol
            if size >= 64:
                try:
                    font_size = badge_size // 2
                    # Use a simple font
                    symbol = "$"
                    text_bbox = draw.textbbox((0, 0), symbol)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    text_x = badge_x + (badge_size - text_width) // 2
                    text_y = badge_y + (badge_size - text_height) // 2 - text_bbox[1]
                    draw.text((text_x, text_y), symbol, fill='white')
                except:
                    pass
        
        images.append(img)
    
    # Save as ICO file
    output_file = 'billing_app.ico'
    images[0].save(
        output_file,
        format='ICO',
        sizes=[(s, s) for s in sizes]
    )
    
    print(f"✓ Created {output_file} with sizes: {sizes}")
    print(f"  Icon features:")
    print(f"  - Purple circle background (#7c3aed)")
    print(f"  - White document/invoice")
    print(f"  - Teal currency badge (#14b8a6)")
    print(f"  - Modern minimal design")
    
    # Also save largest as PNG for preview
    images[-1].save('billing_app_preview.png')
    print(f"✓ Created billing_app_preview.png (256x256) for preview")

if __name__ == "__main__":
    create_billing_icon()
