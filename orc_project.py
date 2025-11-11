import cv2
import easyocr
import matplotlib.pyplot as plt
import re

# -----------------------------
# 1. 이미지 불러오기
# -----------------------------
img_path = "images/fire1.jpg"
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"이미지를 불러올 수 없습니다: {img_path}")

# -----------------------------
# 2. OCR 적용 (원본 이미지 그대로)
# -----------------------------
reader = easyocr.Reader(['en', 'ko'])
results = reader.readtext(img)

# -----------------------------
# 3. OCR 오류 후처리 함수
# -----------------------------
def correct_ocr_errors(text):
    corrections = {
        'O': '0',
        'E': '0',
        'I': '1',
        'l': '1',
        ' ': ''
    }
    for k, v in corrections.items():
        text = text.replace(k, v)
    return text

# -----------------------------
# 4. 내용연한(유효기간) 추출
# -----------------------------
expiry_texts = []

# 정규식 패턴
patterns = [
    r'\d{4}0?\d{1,2}월',               # 203008월
    r'\d{4}[-./]\d{1,2}[-./]\d{1,2}',  # 2025-11-11
    r'\d{2}[-./]\d{1,2}[-./]\d{1,2}'   # 23.05.01
]

for bbox, text, prob in results:
    text_corr = correct_ocr_errors(text)
    
    for pat in patterns:
        match = re.search(pat, text_corr)
        if match:
            expiry_texts.append(match.group())

# 포맷 변환 (예: 203008월 → 2030년 8월)
formatted_expiry = []
for t in expiry_texts:
    m = re.match(r'(\d{4})0?(\d{1,2})월', t)
    if m:
        formatted_expiry.append(f"{m.group(1)}년 {int(m.group(2))}월")
    else:
        formatted_expiry.append(t)

print("추출된 내용연한:", formatted_expiry)

# -----------------------------
# 5. 결과 시각화
# -----------------------------
output_img = img.copy()
for bbox, text, prob in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple([int(x) for x in top_left])
    bottom_right = tuple([int(x) for x in bottom_right])
    
    # 날짜/내용연한이면 빨간색, 아니면 초록색
    text_corr = correct_ocr_errors(text)
    color = (0,0,255) if any(re.search(p, text_corr) for p in patterns) else (0,255,0)
    
    cv2.rectangle(output_img, top_left, bottom_right, color, 2)
    cv2.putText(output_img, text, (top_left[0], top_left[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

plt.figure(figsize=(12,6))
plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
