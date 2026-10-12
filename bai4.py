import cv2
import numpy as np

# Tên file ảnh quả bóng của bạn
image_path = "bong.png"  

# 1. Đọc ảnh gốc
img = cv2.imread(image_path)
if img is None:
    print(f"Lỗi: Không tìm thấy file ảnh '{image_path}'!")
    exit()

h_img, w_img, _ = img.shape

# Cắt bỏ hoàn toàn phần chữ tiêu đề phía trên, chỉ giữ lại phần dưới chứa các quả bóng
crop_y1 = int(h_img * 0.30)
img_cropped = img[crop_y1:, :]

# 2. Chuyển vùng ảnh đã cắt về ảnh xám (Grayscale)
gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)

# 3. Chuyển ảnh về ĐEN TRẮNG (Binary Thresholding)
# Các phần tối hơn ngưỡng 230 (chính là các quả bóng) sẽ chuyển thành màu TRẮNG, nền trắng thành ĐEN
_, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

# Hiển thị cửa sổ ảnh đen trắng để bạn dễ dàng quan sát
cv2.imshow("Anh Da Chuyen Ve Den Trang (Binary)", thresh)

# 4. Tìm các đường viền (contours) trên ảnh đen trắng vừa tạo
contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

ball_count = 0
display_img = img_cropped.copy()

# 5. Lọc diện tích để đếm chính xác từng quả bóng
for c in contours:
    area = cv2.contourArea(c)
    
    # Khoảng diện tích phù hợp với kích thước quả bóng (đã nới rộng để bắt đủ cả bóng sáng lẫn bóng tối)
    if 500 < area < 80000:  
        ball_count += 1
        
        # Vẽ khoanh tròn màu xanh và đánh số thứ tự đỏ
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(display_img, (int(x), int(y)), int(radius), (0, 255, 0), 2)
        cv2.putText(display_img, str(ball_count), (int(x) - 10, int(y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# 6. In kết quả chuẩn ra màn hình Terminal
print(f"========================================")
print(f" Tổng số quả bóng đếm được chính xác là: {ball_count}")
print(f"========================================")

# Hiển thị ảnh kết quả khoanh vùng bóng cuối cùng
cv2.imshow("Ket Qua Dem Bong", display_img)
cv2.waitKey(0)
cv2.destroyAllWindows()