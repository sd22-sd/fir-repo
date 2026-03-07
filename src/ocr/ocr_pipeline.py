import os
import subprocess
import cv2
import pytesseract
import numpy as np


# Render/Linux already has poppler in /usr/bin
# Keep this None so system PATH is used
POPPLER_BIN = None


def preprocess_image(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return thresh


def run_ocr_on_pdf(pdf_path, dpi=300):

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    img_folder = os.path.join("output", f"{pdf_name}_imgs")

    os.makedirs(img_folder, exist_ok=True)

    print("📄 Converting PDF pages to images...")

    out_prefix = os.path.join(img_folder, "page")

    # On Render/Linux this works automatically
    pdftoppm = "pdftoppm"

    # If POPPLER_BIN is provided manually
    if POPPLER_BIN:
        pdftoppm = os.path.join(POPPLER_BIN, "pdftoppm")

    cmd = [
        pdftoppm,
        "-png",
        "-r", str(dpi),
        pdf_path,
        out_prefix
    ]

    subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    images = sorted(
        f for f in os.listdir(img_folder)
        if f.lower().endswith(".png")
    )

    print(f"Saved {len(images)} pages to {img_folder}")

    full_text = ""

    for idx, img_name in enumerate(images):

        img_path = os.path.join(img_folder, img_name)

        print(f"OCR processing page {idx+1}...")

        img = cv2.imread(img_path)

        if img is not None:

            h, w = img.shape[:2]

            if max(h, w) > 2500:
                img = cv2.resize(img, None, fx=0.7, fy=0.7)

        processed = preprocess_image(img)

        # No Windows path needed — Render will use system tesseract
        text = pytesseract.image_to_string(
            processed,
            lang="hin+eng",
            config="--oem 3 --psm 6"
        )

        full_text += text + "\n"

        del img
        del processed

    return full_text.strip()