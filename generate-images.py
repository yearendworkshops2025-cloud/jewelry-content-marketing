#!/usr/bin/env python3
"""
Generate images using Gemini Nano Banana (gemini-2.5-flash-image)
"""

import requests
import base64
import json
from pathlib import Path

# API Configuration
GEMINI_API_KEY = "AIzaSyCH3Z0GA--EvxQciPHbFaNhm_hw1TE0Zes"

# Nano Banana model for image generation
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={GEMINI_API_KEY}"

# Output directory
output_dir = Path("/home/student/jewelry-content-marketing/images")
output_dir.mkdir(exist_ok=True)

# Image prompts - ecstatic people using AI for jewelry business
prompts = [
    {
        "name": "hero-woman-laptop",
        "prompt": """A happy elegant businesswoman in her 40s sitting at a wooden desk with a laptop,
        ecstatic expression celebrating success, warm golden lighting, beautiful jewelry pieces displayed on velvet nearby,
        modern boutique interior, successful empowered look, photorealistic warm tones, professional portrait photography"""
    },
    {
        "name": "team-celebration",
        "prompt": """A diverse team of 3 people in a jewelry boutique celebrating while looking at a tablet,
        stylish woman holding handmade jewelry, genuine joy and excitement on faces,
        warm ambient lighting, jewelry display cases in background, photorealistic candid moment, warm golden tones"""
    },
    {
        "name": "woman-phone-success",
        "prompt": """A young creative woman entrepreneur early 30s in a jewelry workshop looking at smartphone with pure joy,
        ecstatic genuine smile, jewelry making tools and pieces around her, natural daylight from window,
        wearing apron, artistic successful look, photorealistic authentic emotion, lifestyle photography"""
    }
]

print("Starting image generation with Gemini Nano Banana...")
print("=" * 50)

headers = {
    "Content-Type": "application/json"
}

for i, img_data in enumerate(prompts, 1):
    print(f"\n[{i}/3] Generating: {img_data['name']}...")

    payload = {
        "contents": [{
            "parts": [{
                "text": img_data['prompt']
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=180)

        if response.status_code != 200:
            error_detail = response.text[:500]
            print(f"    HTTP {response.status_code}: {error_detail}")
            continue

        result = response.json()

        # Look for image data in response
        saved = False
        if "candidates" in result:
            for candidate in result["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "inlineData" in part:
                            mime_type = part["inlineData"].get("mimeType", "image/png")
                            data = part["inlineData"]["data"]

                            image_bytes = base64.b64decode(data)
                            ext = "png" if "png" in mime_type else "jpg" if "jpeg" in mime_type else "webp"
                            filename = f"{img_data['name']}.{ext}"
                            filepath = output_dir / filename

                            with open(filepath, "wb") as f:
                                f.write(image_bytes)

                            print(f"    Saved: {filepath} ({len(image_bytes)} bytes)")
                            saved = True
                            break
                if saved:
                    break

        if not saved:
            if "candidates" in result and result["candidates"]:
                text = result["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
                print(f"    No image. Text: {text[:200]}..." if text else "    No image data")
            else:
                print(f"    Response: {json.dumps(result)[:400]}")

    except Exception as e:
        print(f"    Error: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print(f"Images saved to: {output_dir}")

# List generated images
import os
images = list(output_dir.glob("*.*"))
if images:
    print("\nGenerated images:")
    for img in images:
        print(f"  - {img.name} ({img.stat().st_size} bytes)")
