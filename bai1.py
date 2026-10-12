import cv2

# Mở camera mặc định của máy tính (0 là webcam chính)
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có mở thành công không
if not cap.isOpened():
    print("Lỗi: Không thể mở camera.")
    exit()

print("--- HƯỚNG DẪN ---")
print("Nhấn phím [Q] để thoát chương trình.")

while True:
    # Đọc từng khung hình (frame) từ camera
    ret, frame = cap.read()

    # Kiểm tra nếu đọc khung hình thất bại
    if not ret:
        print("Lỗi: Không thể đọc khung hình từ camera.")
        break

    # Chuyển ảnh màu từ camera (BGR) sang ảnh xám (Grayscale)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Hiển thị ảnh gốc màu
    cv2.imshow("Camera - Anh Goc (Color)", frame)
    
    # Hiển thị ảnh sau khi chuyển sang màu xám
    cv2.imshow("Camera - Anh Xam (Grayscale)", gray_frame)

    # Chờ phím bấm trong 30 mili-giây. Nếu nhấn phím 'q' hoặc 'Q', thoát vòng lặp
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng tất cả các cửa sổ hiển thị
cap.release()
cv2.destroyAllWindows()