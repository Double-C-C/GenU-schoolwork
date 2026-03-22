#!/usr/bin/env python3
"""
terminal-screenshot render.py
生成终端风格命令行截图（黑底白字，提示符绿色）
用法：python3 render.py --user <username> --host <hostname> --output <out.png> --content <text>
"""

import argparse
import sys
from PIL import Image, ImageDraw, ImageFont

DEFAULT_USER = "user"
DEFAULT_HOST = "ubuntu"
BG_COLOR = (20, 20, 20)
PROMPT_COLOR = (0, 255, 0)
TEXT_COLOR = (200, 200, 200)
FONT_SIZE = 18
PADDING = 20
LINE_SPACING = 6
WIDTH = 900
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def render(lines, username, hostname, output_path):
    font = load_font(FONT_SIZE)
    line_height = FONT_SIZE + LINE_SPACING
    height = len(lines) * line_height + PADDING * 2

    img = Image.new("RGB", (WIDTH, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    prompt_prefix = f"{username}@{hostname}:"

    for i, line in enumerate(lines):
        y = PADDING + i * line_height
        color = PROMPT_COLOR if line.startswith(prompt_prefix) else TEXT_COLOR
        draw.text((PADDING, y), line, font=font, fill=color)

    img.save(output_path)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate terminal screenshot")
    parser.add_argument("--user", default=DEFAULT_USER, help="Username for prompt")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Hostname for prompt")
    parser.add_argument("--output", default="/tmp/terminal_out.png", help="Output image path")
    parser.add_argument("--content", default=None, help="Terminal content (newline separated)")
    parser.add_argument("--file", default=None, help="Read terminal content from file")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    elif args.content:
        lines = args.content.split("\n")
    else:
        print("Error: --content or --file required", file=sys.stderr)
        sys.exit(1)

    render(lines, args.user, args.host, args.output)


if __name__ == "__main__":
    main()
