#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
import math

def generate_svg_logo(output_path, text="FP", icon_type="text"):
    """
    Generate a professional SVG logo for the Forguncy plugin.
    """
    icons = {
        "gantt": '''
            <rect x="10" y="15" width="20" height="6" rx="1" fill="white" opacity="0.9"/>
            <rect x="25" y="25" width="25" height="6" rx="1" fill="white" opacity="0.9"/>
            <rect x="15" y="35" width="30" height="6" rx="1" fill="white" opacity="0.9"/>
        ''',
        "chart": '''
            <rect x="12" y="35" width="8" height="15" rx="1" fill="white" opacity="0.9"/>
            <rect x="28" y="20" width="8" height="30" rx="1" fill="white" opacity="0.9"/>
            <rect x="44" y="28" width="8" height="22" rx="1" fill="white" opacity="0.9"/>
        ''',
        "db": '''
            <ellipse cx="32" cy="18" rx="20" ry="8" fill="none" stroke="white" stroke-width="3"/>
            <path d="M12 18 v24 c0 4.4 9 8 20 8 s20 -3.6 20 -8 v-24" fill="none" stroke="white" stroke-width="3"/>
            <path d="M12 30 c0 4.4 9 8 20 8 s20 -3.6 20 -8" fill="none" stroke="white" stroke-width="3"/>
        ''',
        "gear": '''
            <path d="M32 22a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 15a5 5 0 1 1 0-10 5 5 0 0 1 0 10z" fill="white"/>
            <path d="M42 30.5l3.5-2 1.5 2.5-3.5 2c.2.8.2 1.7 0 2.5l3.5 2-1.5 2.5-3.5-2c-.5.6-1 1.2-1.7 1.7l2 3.5-2.5 1.5-2-3.5c-.8.2-1.7.2-2.5 0l-2 3.5-2.5-1.5 2-3.5c-.6-.5-1.2-1-1.7-1.7l-3.5 2-1.5-2.5 3.5 2c-.2-.8-.2-1.7 0-2.5l-3.5-2 1.5-2.5 3.5 2c.5-.6 1-1.2 1.7-1.7l-2-3.5 2.5-1.5 2 3.5c.8-.2 1.7-.2 2.5 0l2-3.5 2.5 1.5-2 3.5c.6.5 1.2 1 1.7 1.7z" fill="white"/>
        '''
    }

    icon_content = icons.get(icon_type, "")
    text_y = 52 if icon_content else 38
    font_size = 14 if icon_content else 24
    
    svg_template = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#4E73DF;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#224ABE;stop-opacity:1" />
        </linearGradient>
    </defs>
    <rect width="64" height="64" rx="12" fill="url(#grad)"/>
    {icon_content}
    <text x="32" y="{text_y}" font-family="Arial, sans-serif" font-size="{font_size}" font-weight="bold" fill="white" text-anchor="middle" opacity="0.9">{text}</text>
</svg>'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_template)
    print(f"✅ SVG Logo generated with type '{icon_type}' at: {output_path}")
    return svg_template

def create_png_logo(output_path, text="FP", icon_type="text", size=(100, 100)):
    """
    Generate a PNG logo with specified size.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("⚠️ PIL (Pillow) not found. Skipping PNG generation.")
        return

    width, height = size
    
    # Create high-res image for anti-aliasing (2x)
    scale = 4
    w, h = width * scale, height * scale
    
    # Create background with gradient
    # Gradient colors: #4E73DF -> #224ABE
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle background
    # We draw a gradient and then mask it with rounded rectangle
    
    # 1. Create gradient layer
    gradient = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    
    r1, g1, b1 = (78, 115, 223) # #4E73DF
    r2, g2, b2 = (34, 74, 190)  # #224ABE
    
    # Vertical gradient
    for y in range(h):
        r = int(r1 + (r2 - r1) * y / h)
        g = int(g1 + (g2 - g1) * y / h)
        b = int(b1 + (b2 - b1) * y / h)
        gradient_draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # 2. Create mask for rounded corners
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(min(w, h) * 0.2) # 20% radius
    mask_draw.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
    
    # 3. Apply mask to gradient
    img = Image.composite(gradient, Image.new('RGBA', (w, h), (0, 0, 0, 0)), mask)
    draw = ImageDraw.Draw(img)
    
    # 4. Draw Icon Content (Simplified for PIL)
    # We use simple shapes relative to canvas size
    content_color = (255, 255, 255, 230) # White with 90% opacity
    
    if icon_type == "gantt":
        # Draw 3 bars
        # Bar 1
        draw.rounded_rectangle(
            [(w*0.15, h*0.25), (w*0.45, h*0.35)], 
            radius=h*0.02, fill=content_color
        )
        # Bar 2
        draw.rounded_rectangle(
            [(w*0.4, h*0.40), (w*0.8, h*0.50)], 
            radius=h*0.02, fill=content_color
        )
        # Bar 3
        draw.rounded_rectangle(
            [(w*0.25, h*0.55), (w*0.7, h*0.65)], 
            radius=h*0.02, fill=content_color
        )
        
    elif icon_type == "chart":
        # Draw 3 columns
        # Col 1
        draw.rounded_rectangle([(w*0.2, h*0.55), (w*0.32, h*0.8)], radius=w*0.02, fill=content_color)
        # Col 2
        draw.rounded_rectangle([(w*0.44, h*0.3), (w*0.56, h*0.8)], radius=w*0.02, fill=content_color)
        # Col 3
        draw.rounded_rectangle([(w*0.68, h*0.45), (w*0.8, h*0.8)], radius=w*0.02, fill=content_color)
        
    elif icon_type == "db":
        # Draw cylinder
        # Top ellipse
        draw.ellipse([(w*0.2, h*0.2), (w*0.8, h*0.4)], outline=content_color, width=int(w*0.05))
        # Body lines
        draw.line([(w*0.2, h*0.3), (w*0.2, h*0.7)], fill=content_color, width=int(w*0.05))
        draw.line([(w*0.8, h*0.3), (w*0.8, h*0.7)], fill=content_color, width=int(w*0.05))
        # Bottom arc
        draw.arc([(w*0.2, h*0.6), (w*0.8, h*0.8)], 0, 180, fill=content_color, width=int(w*0.05))
        
    elif icon_type == "gear":
        # Simplified gear: circle with dash outline or just a cog symbol
        # Draw a thick circle for now
        draw.ellipse([(w*0.25, h*0.25), (w*0.75, h*0.75)], outline=content_color, width=int(w*0.1))
        # Draw spokes
        draw.line([(w*0.5, h*0.15), (w*0.5, h*0.85)], fill=content_color, width=int(w*0.08))
        draw.line([(w*0.15, h*0.5), (w*0.85, h*0.5)], fill=content_color, width=int(w*0.08))

    # 5. Draw Text
    # Calculate font size based on icon presence
    has_icon = icon_type != "text"
    
    # Font size logic
    target_font_size = int(h * (0.22 if has_icon else 0.4))
    
    try:
        # Try to use Arial Bold
        font = ImageFont.truetype("arialbd.ttf", target_font_size)
    except:
        try:
            # Fallback to default or load_default
            font = ImageFont.load_default()
            # Default font is very small, might need scaling up or just accept it
            # If load_default is used, we can't scale it easily in old PIL, but newer PIL supports size
            # Let's try loading a system font if on Windows
            if sys.platform == "win32":
                font = ImageFont.truetype("arial.ttf", target_font_size)
        except:
             font = ImageFont.load_default()

    # Calculate text position
    # If icon exists, text is at bottom
    # If no icon, text is centered
    
    text_y = h * 0.82 if has_icon else h * 0.5
    
    # Draw text centered
    # newer Pillow has anchor='mm' for middle-middle
    try:
        draw.text((w/2, text_y), text, fill=(255, 255, 255, 240), anchor="mm", font=font)
    except:
        # Fallback for older Pillow
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(((w - text_w)/2, text_y - text_h/2), text, fill=(255, 255, 255, 240), font=font)

    # 6. Resize down to target size (High Quality)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"✅ PNG Logo generated: {output_path} ({width}x{height})")

def main():
    parser = argparse.ArgumentParser(description="Forguncy Plugin Logo Generator")
    parser.add_argument("project_path", help="Path to the plugin project root")
    parser.add_argument("--text", default="FP", help="Text to display in the logo (default: FP)")
    parser.add_argument("--type", choices=["text", "gantt", "chart", "db", "gear"], default="text", 
                        help="Icon type (gantt: APS/Industrial, chart: Analytics, db: Data, gear: Tools)")
    parser.add_argument("--sync", action="store_true", help="Automatically find and overwrite existing logos in the project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    resources_path = project_path / "Resources"
    
    # 1. Generate PluginLogo.png (100x100) - For PluginConfig.json
    create_png_logo(resources_path / "PluginLogo.png", args.text, args.type, size=(100, 100))
    
    # 2. Generate CommandIcon.png (16x16) - For C# Attributes [Icon]
    create_png_logo(resources_path / "CommandIcon.png", args.text, args.type, size=(16, 16))
    
    # 3. Generate SVG (Optional, for reference)
    generate_svg_logo(resources_path / "icon.svg", args.text, args.type)

    print("\n🎉 Logo generation complete!")
    print("👉 Next Step:")
    print("   1. Update PluginConfig.json: \"image\": \"Resources/PluginLogo.png\"")
    print("   2. Update C# [Icon] Attribute: [Icon(\"pack://application:,,,/YourProject;component/Resources/CommandIcon.png\")]")

if __name__ == "__main__":
    main()
