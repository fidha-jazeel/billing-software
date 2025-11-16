"""
Travel Agency Billing Software Icon Generator
Creates a professional icon with purple/teal theme matching the application design.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_travel_icon():
    """Create a professional travel agency icon with purple/teal theme."""
    
    # Create image sizes
    sizes = [512, 256, 128, 64, 32, 16]
    
    # Colors from our application theme
    purple = "#7c3aed"  # Primary purple
    lavender = "#a78bfa"  # Light purple
    teal = "#14b8a6"  # Teal accent
    dark = "#1a1a1a"  # Dark background
    white = "#ffffff"
    
    for size in sizes:
        # Create new image with transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw circular background with gradient effect
        # Outer circle (purple)
        margin = int(size * 0.05)
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill=purple, outline=lavender, width=int(size*0.02))
        
        # Inner circle (dark)
        inner_margin = int(size * 0.15)
        draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], 
                     fill=dark, outline=teal, width=int(size*0.015))
        
        # Draw stylized airplane/travel symbol
        center_x, center_y = size // 2, size // 2
        
        # Airplane body (simplified)
        if size >= 64:
            # Draw plane symbol
            plane_size = int(size * 0.4)
            plane_x1 = center_x - plane_size // 2
            plane_y1 = center_y
            plane_x2 = center_x + plane_size // 2
            plane_y2 = center_y
            
            # Fuselage
            draw.line([(plane_x1, plane_y1), (plane_x2, plane_y2)], 
                     fill=white, width=max(2, int(size*0.04)))
            
            # Wings
            wing_len = int(plane_size * 0.6)
            draw.line([(center_x, plane_y1 - wing_len//2), 
                      (center_x, plane_y1 + wing_len//2)], 
                     fill=teal, width=max(2, int(size*0.03)))
            
            # Tail
            tail_size = int(plane_size * 0.25)
            draw.line([(plane_x1, plane_y1), 
                      (plane_x1 - tail_size//2, plane_y1 - tail_size)], 
                     fill=lavender, width=max(1, int(size*0.02)))
        
        # Add currency symbol for billing
        if size >= 32:
            try:
                # Try to use a system font
                font_size = int(size * 0.3)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Draw rupee or dollar symbol
                symbol = "₹"
                bbox = draw.textbbox((0, 0), symbol, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                text_x = center_x - text_width // 2
                text_y = center_y + int(size * 0.2)
                
                draw.text((text_x, text_y), symbol, fill=lavender, font=font)
            except:
                pass
        
        # Save as PNG
        filename = f"travel_icon_{size}x{size}.png"
        img.save(filename, 'PNG')
        print(f"✓ Created {filename}")
    
    # Create ICO file with multiple sizes
    try:
        images = []
        for size in [256, 128, 64, 32, 16]:
            img = Image.open(f"travel_icon_{size}x{size}.png")
            images.append(img)
        
        images[0].save('travel_billing.ico', format='ICO', 
                      sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)],
                      append_images=images[1:])
        print("✓ Created travel_billing.ico")
    except Exception as e:
        print(f"⚠️  Could not create ICO file: {e}")
    
    print("\n✅ All icon files created successfully!")
    print("\nIcon files created:")
    print("  - travel_icon_512x512.png (main icon)")
    print("  - travel_icon_256x256.png")
    print("  - travel_icon_128x128.png")
    print("  - travel_icon_64x64.png")
    print("  - travel_icon_32x32.png")
    print("  - travel_icon_16x16.png")
    print("  - travel_billing.ico (Windows icon)")

if __name__ == "__main__":
    print("🎨 Generating Travel Agency Billing Software Icons...")
    print("Theme: Purple (#7c3aed) + Teal (#14b8a6)\n")
    
    try:
        create_travel_icon()
    except ImportError:
        print("❌ Error: PIL (Pillow) library not found!")
        print("Please install it: pip install Pillow")
        print("Then run this script again.")
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
