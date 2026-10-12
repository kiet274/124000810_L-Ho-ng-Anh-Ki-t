import cv2
import tkinter as tk
from tkinter import filedialog
import os

# 1. Mở hộp thoại chọn video
root = tk.Tk()
root.withdraw()

print("Đang mở hộp thoại chọn video...")
video_path = filedialog.askopenfilename(
    title="Chọn file video",
    filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov"), ("All files", "*.*")]
)

if not video_path:
    print("Bạn chưa chọn video nào. Chương trình dừng lại.")
    exit()

# 2. Khởi tạo bộ nhận diện khuôn mặt và kiểm tra lỗi tải file XML
xml_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml_path)

# Nếu không load được từ thư mục mặc định của opencv, ta thử nạp trực tiếp đường dẫn hoặc thông báo
if face_cascade.empty():
    # Thử tìm file trong thư mục hiện tại nếu bạn copy thủ công vào
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if face_cascade.empty():
    print("LỖI: Không thể tải được file nhận diện khuôn mặt XML!")
    print("Vui lòng tải file 'haarcascade_frontalface_default.xml' bỏ chung vào thư mục project.")
    exit()

# 3. Mở video bằng OpenCV
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Lỗi: Không thể mở file video '{video_path}'")
    exit()

print("--- HƯỚNG DẪN ---")
print("Nhấn phím [S]: Lưu các khuôn mặt đang xuất hiện thành file 0.png, 1.png,...")
print("Nhấn phím [Q] hoặc [ESC]: Thoát chương trình")

while True:
    ret, frame = cap.read()

    # Nếu video chạy hết thì tự động phát lại từ đầu
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Chuyển ảnh sang màu xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Nhận diện các khuôn mặt trong khung hình
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )

    display_frame = frame.copy()
    cropped_faces = []

    # Lặp qua các khuôn mặt tìm được
    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        cropped_faces.append(face_img)

        # Vẽ hình chữ nhật màu xanh lá quanh khuôn mặt
        cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Đếm và hiển thị số lượng khuôn mặt
    face_count = len(faces)
    cv2.putText(
        display_frame, 
        f"So khuon mat: {face_count}", 
        (20, 40), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (0, 255, 0), 
        2
    )

    # Hiển thị video
    cv2.imshow("Bai 3 - Nhan dien & Luu khuon mat", display_frame)

    key = cv2.waitKey(30) & 0xFF

    # Nếu nhấn phím 'S' hoặc 's': Lưu khuôn mặt ra file 0.png, 1.png,...
    if key == ord('s') or key == ord('S'):
        if face_count > 0:
            for i, face_crop in enumerate(cropped_faces):
                filename = f"{i}.png"
                cv2.imwrite(filename, face_crop)
                print(f"Đã lưu: {filename}")
            print(f"--> Đã lưu thành công {face_count} khuôn mặt!")
        else:
            print("Không tìm thấy khuôn mặt nào trong khung hình hiện tại để lưu.")

    elif key == ord('q') or key == ord('Q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()