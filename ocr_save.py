import easyocr

# Adjust to your actual image path
image_path = r"C:\Users\saniy\OneDrive\Pictures\Screenshots\OCR_Project\screenshots\prescription.jpg"

reader = easyocr.Reader(['en'])
results = reader.readtext(image_path)

with open("ocr_output.txt", "w", encoding="utf-8") as f:
    for bbox, text, prob in results:
        line = f"{text} ({prob:.2f})\n"
        print(line.strip())
        f.write(line)

print("✅ OCR results saved to ocr_output.txt")

