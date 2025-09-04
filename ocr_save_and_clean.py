import easyocr
import re
from pathlib import Path

# ===== CONFIG =====
IMAGE_PATH = r"C:\Users\saniy\OneDrive\Pictures\Screenshots\OCR_Project\screenshots\prescription.jpg"
RAW_OUT   = "ocr_output_raw.txt"
CLEAN_OUT = "ocr_output_clean.txt"
LANGS     = ['en', 'hi']          # languages passed to EasyOCR
CONF_THRESH = 0.50                # keep lines with confidence >= this
MIN_LEN = 3                       # drop very short noisy tokens

# ===== OCR =====
reader = easyocr.Reader(LANGS, gpu=False)
results = reader.readtext(IMAGE_PATH)

# ===== Save raw results (full detections) =====
with open(RAW_OUT, "w", encoding="utf-8") as rf:
    rf.write("OCR RAW RESULTS\n")
    rf.write(f"Image: {IMAGE_PATH}\n\n")
    for i, det in enumerate(results, 1):
        try:
            bbox, text, prob = det
        except Exception:
            # fallback if different format
            text = det[1] if len(det) > 1 else str(det)
            prob = det[2] if len(det) > 2 else 0.0
        rf.write(f"{i:02d}. {text}  ({prob:.2f})\n")

# ===== Cleaning heuristics =====
def is_useful(text: str, prob: float) -> bool:
    # basic confidence threshold
    if prob < CONF_THRESH:
        return False

    txt = text.strip()
    if len(txt) < MIN_LEN:
        return False

    # remove lines that look like mostly punctuation or single-symbol garbage
    if re.fullmatch(r'[\W_]+', txt):
        return False

    # keep if contains letters or digits (medical terms often contain both)
    if not re.search(r'[\w\d]', txt):
        return False

    # optionally: filter out extremely numeric-only garbage (e.g., '()' handled above)
    # allow numbers with units: '500mg', '120/80', etc.
    if re.fullmatch(r'\d{1,2}$', txt):  # lone small numbers (likely noise)
        return False

    return True

# ===== Produce cleaned file with two sections =====
with open(CLEAN_OUT, "w", encoding="utf-8") as cf:
    cf.write("OCR CLEANED RESULTS\n")
    cf.write(f"Image: {IMAGE_PATH}\n\n")
    cf.write("Kept lines (confidence >= {:.2f}):\n".format(CONF_THRESH))

    kept = []
    for i, det in enumerate(results, 1):
        bbox, text, prob = det
        if is_useful(text, prob):
            line = f"{text}  ({prob:.2f})"
            kept.append((prob, text))
            cf.write(line + "\n")

    # If nothing kept, lower threshold once (helpful sometimes)
    if not kept:
        cf.write("\nNo lines met the threshold. Falling back to a relaxed filter:\n")
        for i, det in enumerate(results, 1):
            bbox, text, prob = det
            txt = text.strip()
            if len(txt) >= MIN_LEN and not re.fullmatch(r'[\W_]+', txt):
                cf.write(f"{text}  ({prob:.2f})\n")

print("✅ Done.")
print(f"Raw results -> {Path(RAW_OUT).resolve()}")
print(f"Cleaned results -> {Path(CLEAN_OUT).resolve()}")
print(f"Kept {len(kept)} lines with confidence >= {CONF_THRESH:.2f}")
