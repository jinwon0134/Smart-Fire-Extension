import cv2
import easyocr
import matplotlib.pyplot as plt

# 1. 이미지 불러오기
img_path = "images/fire1.jpg"
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"이미지를 불러올 수 없습니다: {img_path}")

# 2. OCR 적용 (원본 이미지 그대로)
reader = easyocr.Reader(['en', 'ko'])
results = reader.readtext(img)

# 3. 결과 시각화
output_img = img.copy()
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple([int(x) for x in top_left])
    bottom_right = tuple([int(x) for x in bottom_right])
    cv2.rectangle(output_img, top_left, bottom_right, (0,255,0), 2)
    cv2.putText(output_img, text, (top_left[0], top_left[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

plt.figure(figsize=(12,6))
plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# 4. 텍스트 출력
for bbox, text, prob in results:
    print(f"{text} ({prob:.2f})")
