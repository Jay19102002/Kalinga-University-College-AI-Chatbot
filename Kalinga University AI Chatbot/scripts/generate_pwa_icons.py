import os
import math
from PIL import Image, ImageDraw, ImageFont

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public")
os.makedirs(PUBLIC_DIR, exist_ok=True)

def create_pwa_icon(size: int, is_maskable: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = int(size * 0.1) if is_maskable else int(size * 0.04)
    radius = int(size * 0.22) if not is_maskable else 0

    # Draw rounded background gradient simulation
    top_color = (29, 78, 216)    # #1d4ed8 Blue
    bot_color = (67, 56, 202)    # #4338ca Indigo

    for y in range(margin, size - margin):
        t = (y - margin) / float(size - 2 * margin)
        r = int(top_color[0] * (1 - t) + bot_color[0] * t)
        g = int(top_color[1] * (1 - t) + bot_color[1] * t)
        b = int(top_color[2] * (1 - t) + bot_color[2] * t)
        
        # Row line within rounded rect
        draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255), width=1)

    # Apply mask for smooth rounded corners if not full-bleed maskable
    if not is_maskable:
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=255)
        
        # Apply mask
        img.putalpha(mask)
        draw = ImageDraw.Draw(img)

    # Inner Glow Border
    if not is_maskable:
        draw.rounded_rectangle(
            [margin + 2, margin + 2, size - margin - 2, size - margin - 2],
            radius=radius - 2,
            outline=(255, 255, 255, 90),
            width=max(2, int(size * 0.015))
        )

    # Draw Bot / Shield Emblem in Center
    center_x = size / 2
    center_y = size / 2

    # Draw University Graduation Cap / Shield Accent
    scale = size / 512.0
    
    # Antenna
    antenna_w = max(2, int(12 * scale))
    antenna_top = center_y - 120 * scale
    antenna_bot = center_y - 75 * scale
    draw.line([(center_x, antenna_top), (center_x, antenna_bot)], fill=(255, 255, 255, 240), width=antenna_w)
    ant_ball_r = int(14 * scale)
    draw.ellipse([center_x - ant_ball_r, antenna_top - ant_ball_r, center_x + ant_ball_r, antenna_top + ant_ball_r], fill=(96, 165, 250, 255), outline=(255, 255, 255, 255), width=max(1, int(3 * scale)))

    # Bot Head Outer Box
    head_w = 200 * scale
    head_h = 140 * scale
    head_left = center_x - head_w / 2
    head_top = center_y - 75 * scale
    head_right = center_x + head_w / 2
    head_bot = head_top + head_h
    head_r = int(32 * scale)

    draw.rounded_rectangle([head_left, head_top, head_right, head_bot], radius=head_r, fill=(255, 255, 255, 245))

    # Bot Face Visor (Dark Cyan / Navy)
    visor_margin = 18 * scale
    v_left = head_left + visor_margin
    v_top = head_top + visor_margin
    v_right = head_right - visor_margin
    v_bot = head_bot - visor_margin
    v_r = int(20 * scale)
    draw.rounded_rectangle([v_left, v_top, v_right, v_bot], radius=v_r, fill=(15, 23, 42, 255))

    # Friendly Cyan Glowing Eyes
    eye_radius = int(18 * scale)
    eye_offset = 42 * scale
    eye_y = (v_top + v_bot) / 2
    
    # Left Eye
    draw.ellipse([center_x - eye_offset - eye_radius, eye_y - eye_radius, center_x - eye_offset + eye_radius, eye_y + eye_radius], fill=(56, 189, 248, 255))
    # Eye highlight
    draw.ellipse([center_x - eye_offset - eye_radius * 0.4, eye_y - eye_radius * 0.7, center_x - eye_offset + eye_radius * 0.2, eye_y - eye_radius * 0.1], fill=(255, 255, 255, 230))

    # Right Eye
    draw.ellipse([center_x + eye_offset - eye_radius, eye_y - eye_radius, center_x + eye_offset + eye_radius, eye_y + eye_radius], fill=(56, 189, 248, 255))
    # Eye highlight
    draw.ellipse([center_x + eye_offset - eye_radius * 0.4, eye_y - eye_radius * 0.7, center_x + eye_offset + eye_radius * 0.2, eye_y - eye_radius * 0.1], fill=(255, 255, 255, 230))

    # KU Badge / Lettering below
    badge_y = center_y + 110 * scale
    badge_w = 140 * scale
    badge_h = 38 * scale
    draw.rounded_rectangle(
        [center_x - badge_w/2, badge_y - badge_h/2, center_x + badge_w/2, badge_y + badge_h/2],
        radius=int(14 * scale),
        fill=(255, 255, 255, 230)
    )

    # University "KU" text
    try:
        font_size = int(22 * scale)
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    text = "KALINGA"
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((center_x - tw / 2, badge_y - th / 2 - 2 * scale), text, fill=(29, 78, 216), font=font)
    except Exception:
        pass

    return img

def create_svg():
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1d4ed8" />
      <stop offset="100%" stop-color="#4338ca" />
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0f172a" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Outer Rounded Shield -->
  <rect x="24" y="24" width="464" height="464" rx="100" fill="url(#bgGrad)" filter="url(#shadow)"/>
  <rect x="28" y="28" width="456" height="456" rx="96" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="6"/>

  <!-- Antenna -->
  <line x1="256" y1="135" x2="256" y2="180" stroke="#ffffff" stroke-width="12" stroke-linecap="round"/>
  <circle cx="256" cy="135" r="16" fill="url(#cyanGrad)" stroke="#ffffff" stroke-width="4"/>

  <!-- Bot Head -->
  <rect x="156" y="180" width="200" height="145" rx="36" fill="#ffffff" filter="url(#shadow)"/>
  
  <!-- Visor -->
  <rect x="176" y="198" width="160" height="108" rx="24" fill="#0f172a"/>
  
  <!-- Glowing Eyes -->
  <circle cx="216" cy="252" r="18" fill="url(#cyanGrad)"/>
  <circle cx="212" cy="246" r="5" fill="#ffffff"/>

  <circle cx="296" cy="252" r="18" fill="url(#cyanGrad)"/>
  <circle cx="292" cy="246" r="5" fill="#ffffff"/>

  <!-- Ear Nods -->
  <rect x="142" y="224" width="14" height="56" rx="7" fill="#60a5fa"/>
  <rect x="356" y="224" width="14" height="56" rx="7" fill="#60a5fa"/>

  <!-- Kalinga Badge -->
  <rect x="166" y="356" width="180" height="42" rx="16" fill="#ffffff" filter="url(#shadow)"/>
  <text x="256" y="385" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="20" fill="#1d4ed8" text-anchor="middle" letter-spacing="2">KALINGA AI</text>
</svg>'''
    with open(os.path.join(PUBLIC_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Generated favicon.svg")

def main():
    print("Generating PWA icons...")
    create_svg()

    # 192x192
    icon_192 = create_pwa_icon(192)
    icon_192.save(os.path.join(PUBLIC_DIR, "pwa-192.png"))
    print("Generated pwa-192.png")

    # 512x512
    icon_512 = create_pwa_icon(512)
    icon_512.save(os.path.join(PUBLIC_DIR, "pwa-512.png"))
    print("Generated pwa-512.png")

    # 512x512 maskable
    maskable_512 = create_pwa_icon(512, is_maskable=True)
    maskable_512.save(os.path.join(PUBLIC_DIR, "maskable-icon-512.png"))
    print("Generated maskable-icon-512.png")

    # Apple touch icon (180x180)
    apple_icon = create_pwa_icon(180)
    apple_icon.save(os.path.join(PUBLIC_DIR, "apple-touch-icon.png"))
    print("Generated apple-touch-icon.png")

if __name__ == "__main__":
    main()
