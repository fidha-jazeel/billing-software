"""
Script to generate application icon for Travel Agency Billing Software.
Creates a purple-themed icon with travel/billing symbolism.
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_app_icon():
        """Create a modern purple-themed application icon."""
        # Create image with transparent background
        size = 512
        icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Purple gradient background circle
        center = size // 2
        radius = size // 2 - 20
        
        # Draw main circle with purple color
        draw.ellipse(
            [(center - radius, center - radius), (center + radius, center + radius)],
            fill='#7c3aed',  # Purple from theme
            outline='#a78bfa',  # Lavender outline
            width=8
        )
        
        # Draw inner circle
        inner_radius = radius - 40
        draw.ellipse(
            [(center - inner_radius, center - inner_radius), 
             (center + inner_radius, center + inner_radius)],
            fill='#1a1a1a',  # Dark background
            outline='#14b8a6',  # Teal accent
            width=6
        )
        
        # Draw "₹" symbol in the center
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", 200)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Draw rupee/dollar symbol
        text = "₹"
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2 - 20
        
        # Draw text with glow effect
        for offset in range(3, 0, -1):
            draw.text(
                (text_x, text_y),
                text,
                fill=f'rgba(168, 139, 250, {offset * 30})',  # Lavender glow
                font=font
            )
        
        # Main text
        draw.text((text_x, text_y), text, fill='#ffffff', font=font)
        
        # Draw small document icon at bottom
        doc_width = 60
        doc_height = 80
        doc_x = center - doc_width // 2
        doc_y = center + inner_radius - doc_height - 30
        
        # Document rectangle
        draw.rounded_rectangle(
            [(doc_x, doc_y), (doc_x + doc_width, doc_y + doc_height)],
            radius=5,
            fill='#14b8a6',  # Teal
            outline='#ffffff',
            width=3
        )
        
        # Document lines
        line_y = doc_y + 15
        for _ in range(3):
            draw.line(
                [(doc_x + 10, line_y), (doc_x + doc_width - 10, line_y)],
                fill='#ffffff',
                width=3
            )
            line_y += 15
        
        # Save icon in multiple sizes
        output_dir = os.path.dirname(__file__)
        
        # Save full size
        icon.save(os.path.join(output_dir, 'app_icon.png'))
        print("✓ Created app_icon.png (512x512)")
        
        # Save ICO file with multiple sizes
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        icon.save(
            os.path.join(output_dir, 'app_icon.ico'),
            format='ICO',
            sizes=icon_sizes
        )
        print("✓ Created app_icon.ico (multi-size)")
        
        # Save smaller PNG versions
        for size_tuple in [(256, 256), (128, 128), (64, 64)]:
            small_icon = icon.resize(size_tuple, Image.Resampling.LANCZOS)
            filename = f'app_icon_{size_tuple[0]}x{size_tuple[1]}.png'
            small_icon.save(os.path.join(output_dir, filename))
            print(f"✓ Created {filename}")
        
        print("\n✅ All icon files created successfully!")
        print(f"📁 Location: {output_dir}")
        return True
    
    if __name__ == "__main__":
        create_app_icon()

except ImportError:
    print("⚠️  PIL (Pillow) not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    print("✓ Pillow installed. Please run this script again.")
