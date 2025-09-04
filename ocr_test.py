import easyocr

reader = easyocr.Reader(['en', 'hi'])  # English + Hindi, add other langs if needed
image_path = r"screenshots\prescription.jpg"

results = reader.readtext(image_path)

for detection in results:
    print(detection[1])
