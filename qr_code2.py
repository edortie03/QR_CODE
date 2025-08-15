# qr_generate.py
import argparse
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

EC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

def build_qr(
    data: str,
    out_path: str = "qr.png",
    ec_level: str = "M",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    version: int | None = None,
) -> str:
    if not data or not data.strip():
        raise ValueError("Content is empty. Provide some text or a URL.")

    if ec_level not in EC_MAP:
        raise ValueError(f"Invalid error correction '{ec_level}'. Use one of: L, M, Q, H")

    # Auto-fit if version is None; otherwise use fixed version (1–40)
    qr = qrcode.QRCode(
        version=version,
        error_correction=EC_MAP[ec_level],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data.strip())
    qr.make(fit=(version is None))

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Ensure directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    img.save(out_path)
    return os.path.abspath(out_path)

def parse_args():
    p = argparse.ArgumentParser(
        description="Offline QR code generator (no backend)."
    )
    p.add_argument(
        "-c", "--content",
        required=True,
        help="Text to encode (URL, Wi-Fi string, etc.)"
    )
    p.add_argument(
        "-o", "--out",
        default="qr.png",
        help="Output image path (e.g., output/myqr.png)"
    )
    p.add_argument(
        "-e", "--error",
        default="M",
        choices=["L", "M", "Q", "H"],
        help="Error correction level (L=7%%, M=15%%, Q=25%%, H=30%%). Default M."
    )
    p.add_argument(
        "-s", "--box-size",
        type=int,
        default=10,
        help="Pixel size of each QR module. Default 10."
    )
    p.add_argument(
        "-b", "--border",
        type=int,
        default=4,
        help="Border (quiet zone) in modules. Default 4."
    )
    p.add_argument(
        "--fill",
        default="black",
        help="Foreground color (e.g., black, #000000)."
    )
    p.add_argument(
        "--back",
        default="white",
        help="Background color (e.g., white, #FFFFFF)."
    )
    p.add_argument(
        "-v", "--version",
        type=int,
        default=None,
        help="QR version 1–40 (higher stores more). Omit for auto-fit."
    )
    return p.parse_args()

def main():
    args = parse_args()
    try:
        out = build_qr(
            data=args.content,
            out_path=args.out,
            ec_level=args.error,
            box_size=args.box_size,
            border=args.border,
            fill_color=args.fill,
            back_color=args.back,
            version=args.version,
        )
        print(f"Saved QR to: {out}")
    except Exception as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
