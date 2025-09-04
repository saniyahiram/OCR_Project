import os, sys, traceback
from pathlib import Path

print("Python exe:", sys.executable)
print("CWD:", os.getcwd())

image_path = r"C:\Users\saniy\OneDrive\Pictures\Screenshots\OCR_Project\screenshots\prescription.jpg"
p = Path(image_path)
print("Image path:", image_path)
print("Exists:", p.exists())
if p.exists():
    print("Size (bytes):", p.stat().st_size)

try:
    from PIL import Image
    import numpy as np
    print("PIL import: OK")
    try:
        img = Image.open(image_path)
        print("PIL open: OK -> size:", img.size, "mode:", img.mode)
        img = img.convert("RGB")
        arr = np.array(img)
        print("Numpy array shape:", arr.shape)
    except Exception as e:
        print("PIL failed to open image:")
        traceback.print_exc()
except Exception as e:
    print("PIL import FAILED:")
    traceback.print_exc()

try:
    import imageio.v3 as iio
    print("imageio import: OK")
    try:
        ii = iio.imread(image_path)
        import numpy as np
        print("imageio read success -> shape:", np.array(ii).shape)
    except Exception as e:
        print("imageio failed to read image:")
        traceback.print_exc()
except Exception as e:
    print("imageio import FAILED:")
    traceback.print_exc()

try:
    import easyocr
    print("easyocr import OK")
    reader = easyocr.Reader(['en','hi'], gpu=False)
    print("EasyOCR reader inited OK")
    # try passing numpy array (if created above)
    try:
        results = reader.readtext(arr)  # if arr exists
    except NameError:
        results = reader.readtext(image_path)
    print("OCR detections:", len(results))
    for i, det in enumerate(results, 1):
        try:
            bbox, text, score = det
            print(f"{i:02d}. {text} | {score:.2f}")
        except Exception:
            print(i, det)
except Exception as e:
    print("easyocr import/init/ocr FAILED:")
    traceback.print_exc()
