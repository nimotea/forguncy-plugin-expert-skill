#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

def generate_svg_logo(output_path, text="FP", icon_type="text"):
    """
    Generate a professional SVG logo for the Forguncy plugin.
    """
    # ... (same icons and logic)
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
            <path d="M42 30.5l3.5-2 1.5 2.5-3.5 2c.2.8.2 1.7 0 2.5l3.5 2-1.5 2.5-3.5-2c-.5.6-1 1.2-1.7 1.7l2 3.5-2.5 1.5-2-3.5c-.8.2-1.7.2-2.5 0l-2 3.5-2.5-1.5 2-3.5c-.6-.5-1.2-1-1.7-1.7l-3.5 2-1.5-2.5 3.5-2c-.2-.8-.2-1.7 0-2.5l-3.5-2 1.5-2.5 3.5 2c.5-.6 1-1.2 1.7-1.7l-2-3.5 2.5-1.5 2 3.5c.8-.2 1.7-.2 2.5 0l2-3.5 2.5 1.5-2 3.5c.6.5 1.2 1 1.7 1.7z" fill="white"/>
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

def try_generate_png(project_path, svg_content, name="icon.png", sync=False):
    """
    Attempt to generate a PNG version of the logo.
    If sync is True, it will attempt to find existing logos in the project and overwrite them.
    """
    project_path = Path(project_path)
    resources_path = project_path / "Resources"
    output_path = resources_path / name
    
    # Sync logic: find existing logo files
    target_paths = [output_path]
    if sync:
        print("🔍 Sync mode enabled. Searching for existing logos to overwrite...")
        # Common Forguncy logo names
        common_names = ["PluginLogo.png", "Icon.png", "icon.png", "logo.png"]
        for root, dirs, files in os.walk(project_path):
            if "bin" in dirs: dirs.remove("bin")
            if "obj" in dirs: dirs.remove("obj")
            for file in files:
                if file in common_names:
                    found_path = Path(root) / file
                    if found_path not in target_paths:
                        target_paths.append(found_path)
                        print(f"  Found existing logo: {found_path.relative_to(project_path)}")

    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([0, 0, 128, 128], radius=24, fill=(78, 115, 223))
        
        try:
            font = ImageFont.truetype("arialbd.ttf", 48)
        except:
            font = ImageFont.load_default()
            
        draw.text((64, 64), "FP", fill=(255, 255, 255), anchor="mm", font=font)
        
        for path in target_paths:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            img.save(path, "PNG")
            print(f"✅ PNG Logo generated at: {path}")
        
    except ImportError:
        print("⚠️ PIL (Pillow) not found. Skipping PNG generation.")
    except Exception as e:
        print(f"⚠️ Failed to generate PNG: {e}")

def main():
    parser = argparse.ArgumentParser(description="Forguncy Plugin Logo Generator")
    parser.add_argument("project_path", help="Path to the plugin project root")
    parser.add_argument("--text", default="FP", help="Text to display in the logo (default: FP)")
    parser.add_argument("--type", choices=["text", "gantt", "chart", "db", "gear"], default="text", 
                        help="Icon type (gantt: APS/Industrial, chart: Analytics, db: Data, gear: Tools)")
    parser.add_argument("--name", default="icon.svg", help="Logo filename (default: icon.svg)")
    parser.add_argument("--png", action="store_true", default=True, help="Also generate a PNG version for PluginConfig.json")
    parser.add_argument("--sync", action="store_true", help="Automatically find and overwrite existing logos in the project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    resources_path = project_path / "Resources"
    output_path = resources_path / args.name
    
    svg_content = generate_svg_logo(output_path, args.text, args.type)
    
    if args.png:
        try_generate_png(args.project_path, svg_content, sync=args.sync)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
