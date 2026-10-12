import cv2
import numpy as np
import os

# Tên file ảnh biển số xe của bạn (Lưu ảnh vào chung thư mục với tên 'bienso.png')
image_path = "bienso.png"  

# 1. Đọc ảnh gốc
img = cv2.imread(image_path)
if img is None:
    print(f"Lỗi: Không tìm thấy file ảnh '{image_path}'! Hãy kiểm tra lại tên file.")
    exit()

# 2. Chuyển ảnh về màu xám (Grayscale)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# 3. ĐƯA ẢNH VỀ TRẮNG ĐEN (Binary Thresholding bằng phương pháp Otsu)
# Chuyển chữ đen trên nền trắng thành các nét chữ trắng rõ nét trên nền đen
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Hiển thị cửa sổ ảnh TRẮNG ĐEN để quan sát rõ kết quả chuyển đổi
cv2.imshow("Anh Bien So Trang Den (Binary)", thresh)

# 4. Tìm các đường viền (contours) trên ảnh trắng đen vừa tạo
contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

h_img, w_img = gray.shape
character_contours = []

# 5. Lọc các contour hợp lệ theo kích thước tiêu chuẩn của ký tự trên biển số
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    
    # Điều kiện lọc chiều cao, chiều rộng phù hợp với chữ/số trên biển
    if (h > 0.4 * h_img) and (h < 0.98 * h_img) and (w < 0.8 * h) and (w * h > 30):
        character_contours.append((x, y, w, h))

# 6. Sắp xếp các ký tự theo thứ tự từ TRÁI sang PHẢI dựa vào tọa độ x
character_contours = sorted(character_contours, key=lambda item: item[0])

# Tạo thư mục chứa các file ảnh ký tự được crop ra
output_dir = "cropped_chars"
os.makedirs(output_dir, exist_ok=True)

display_img = img.copy()
print(f"Đã tìm thấy và tách thành công {len(character_contours)} ký tự từ ảnh trắng đen.")

# 7. Tiến hành crop từng ký tự và lưu ra file ảnh (.png)
for i, (x, y, w, h) in enumerate(character_contours):
    # Cắt vùng chứa ký tự từ ảnh gốc
    char_crop = img[y:y+h, x:x+w]
    
    # Lưu file vào thư mục cropped_chars với tên 0.png, 1.png, 2.png,...
    filename = os.path.join(output_dir, f"{i}.png")
    cv2.imwrite(filename, char_crop)
    print(f"Đã lưu: {filename}")
    
    # Vẽ khung xanh quanh ký tự và đánh số thứ tự trên ảnh gốc để kiểm tra
    cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(display_img, str(i), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# 8. Hiển thị kết quả khoanh vùng trực quan
cv2.imshow("Ket Qua Khoanh Vung Ky Tu Bien So", display_img)
cv2.waitKey(0)
cv2.destroyAllWindows()