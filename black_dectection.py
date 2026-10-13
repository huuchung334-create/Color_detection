# import numpy as np
# import cv2

# def get_orange_limits(b, g, r):
#     """Nhận ba số nguyên B, G, R (0..255), trả hai ngưỡng HSV màu cam.

#     Ví dụ: get_orange_limits(0, 140, 255). Nới S/V để chịu thay đổi
#     ánh sáng; giới hạn Hue để giảm nhận nhầm màu đỏ và vàng.
#     """
#     channels = (b, g, r)
#     if any(isinstance(c, (bool, np.bool_)) or
#            not isinstance(c, (int, np.integer)) or not 0 <= c <= 255
#            for c in channels):
#         raise ValueError("B, G, R phải là số nguyên trong khoảng 0..255")
#     sample = np.array([[channels]], dtype=np.uint8)
#     hue, sat, val = map(int, cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)[0, 0])
#     if not 5 <= hue <= 25 or sat < 40 or val < 40:
#         raise ValueError("Hãy chọn mẫu màu cam rõ, ví dụ B=0, G=140, R=255")
#     lower = np.array([max(5, hue - 7), max(40, int(sat * 0.4)),
#                       max(40, int(val * 0.25))], dtype=np.uint8)
#     upper = np.array([min(25, hue + 7), 255, 255], dtype=np.uint8)
#     return lower, upper


# def detect_orange_ball(frame, lower, upper, min_area=300):
#     """Trả (mask sạch, contour bóng hoặc None); diện tích tính bằng pixel.

#     Chỉ giữ vùng cam lớn, tương đối tròn. Mask hiển thị là vùng đã chọn,
#     không phải toàn bộ pixel vượt ngưỡng màu trong nền.
#     """
#     blurred = cv2.GaussianBlur(frame, (5, 5), 0)
#     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, lower, upper)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     candidates = []
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area < min_area:
#             continue
#         perimeter = cv2.arcLength(contour, True)
#         if perimeter == 0:
#             continue
#         _, _, width, height = cv2.boundingRect(contour)
#         circularity = 4 * np.pi * area / (perimeter * perimeter)
#         (_, _), radius = cv2.minEnclosingCircle(contour)
#         circle_fill = area / (np.pi * radius * radius)
#         # Nới vừa phải vì bàn tay có thể che một phần quả bóng.
#         if 0.6 <= width / height <= 1.5 and circularity >= 0.45 and circle_fill >= 0.5:
#             candidates.append(contour)
#     clean_mask = np.zeros_like(mask)
#     if not candidates:
#         return clean_mask, None
#     ball = max(candidates, key=cv2.contourArea)
#     cv2.drawContours(clean_mask, [ball], -1, 255, cv2.FILLED)
#     return clean_mask, ball


# def get_limits(color, hue_tol=10, s_tol_ratio=0.5, v_tol_ratio=0.5, s_min_floor=15, v_min_floor=15):
#     """
#     Input:
#         color - BGR list/tuple, vd [0,0,0], [0,255,0], [190,225,245]...
#         hue_tol - độ nới cho Hue (mặc định 10)
#         s_tol_ratio, v_tol_ratio - tỉ lệ nới cho S, V dựa theo giá trị đo được
#         s_min_floor, v_min_floor - biên dưới tối thiểu cho khoảng S, V (tránh quá hẹp)
#     Output:
#         lowerLimit, upperLimit - np.array HSV dùng cho cv2.inRange
#     """
#     c = np.uint8([[color]])
#     hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
#     hue, sat, val = int(hsvC[0][0][0]), int(hsvC[0][0][1]), int(hsvC[0][0][2])

#     # --- Case 1: Đen tuyệt đối (V rất thấp) ---
#     if val < 40:
#         return np.array([0, 0, 0]), np.array([180, 255, 60])

#     # --- Case 2: Trắng tuyệt đối (S rất thấp, V rất cao) ---
#     if sat < 25 and val > 220:
#         return np.array([0, 0, 200]), np.array([180, 50, 255])

#     # --- Case 3: Xám thuần (S rất thấp, V trung bình) ---
#     if sat < 25:
#         v_tol = max(int(val * v_tol_ratio), v_min_floor)
#         return (np.array([0, 0, max(val - v_tol, 0)]),
#                 np.array([180, 50, min(val + v_tol, 255)]))

#     # --- Case 4: Mọi màu có sắc (từ pastel/nhạt đến đậm) — công thức thích nghi ---
#     # S, V tolerance tỉ lệ theo chính giá trị đo được, thay vì ép cứng 100-255
#     s_tol = max(int(sat * s_tol_ratio), s_min_floor)
#     v_tol = max(int(val * v_tol_ratio), v_min_floor)

#     lower_h = max(hue - hue_tol, 0)
#     upper_h = min(hue + hue_tol, 180)
#     lower_s = max(sat - s_tol, 0)
#     upper_s = min(sat + s_tol, 255)
#     lower_v = max(val - v_tol, 0)
#     upper_v = min(val + v_tol, 255)

#     lowerLimit = np.array([lower_h, lower_s, lower_v])
#     upperLimit = np.array([upper_h, upper_s, upper_v])

#     return lowerLimit, upperLimit

