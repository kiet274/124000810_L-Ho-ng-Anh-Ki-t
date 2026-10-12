import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Ẩn cửa sổ chính của tkinter
root = tk.Tk()
root.withdraw()

print("Đang mở hộp thoại chọn ảnh...")
# Mở cửa sổ chọn file ảnh từ thư mục
image_path = filedialog.askopenfilename(
    title="Chọn file ảnh",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")]
)

# Kiểm tra nếu người dùng không chọn ảnh
if not image_path:
    print("Bạn chưa chọn ảnh nào. Chương trình dừng lại.")
    exit()

# Đọc ảnh từ đường dẫn đã chọn
img_bgr = cv2.imread(image_path)

if img_bgr is None:
    print("Lỗi: Không thể đọc file ảnh.")
    exit()

# 1. Chuyển ảnh BGR (mặc định OpenCV) sang RGB để hiển thị đúng màu bằng Matplotlib
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# 2. Chuyển ảnh sang màu xám (Grayscale) theo yêu cầu đề bài
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Hiển thị 2 ảnh song song có trục tọa độ (giống hình đề bài)
plt.figure(figsize=(10, 5))

# Ảnh gốc màu
plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.title("True")

# Ảnh màu xám
plt.subplot(1, 2, 2)
plt.imshow(img_gray, cmap='gray')
plt.title("True")

plt.tight_layout()
plt.show()