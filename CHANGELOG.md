# Thay đổi

## 3.0 · 05/11/2026

- **Giải mã ads thắng** (`references/giai-ma-ads-thang.md`): trả lời "vì sao ads của họ chạy tốt" bằng đối chứng với ads yếu cùng hãng, 10 lớp giải mã, giả thuyết kèm mức chắc, công thức của từng đối thủ, giả thuyết test cho mình.
- `thong-ke.py` tự chọn **ads thắng và đối chứng** (hàm `vai()`), ngưỡng hạng co theo cỡ fanpage, hạ ads bền của đối thủ chạy treo xuống "Thắng (yếu)", nhóm tắt sớm thành đối chứng.
- `xem-media.js` mới: lưới video, tua đồng loạt, **dải khung** một video mỗi 2 giây, ảnh carousel, lấy link video.
- `boc-loi.py` mới: tải video (chỉ máy chủ media Facebook) và bóc lời tiếng Việt bằng faster-whisper.
- `thong-ke.py` tách **ads cũ bật lại** với **ads mới tinh** khi so lần trước, đếm nhóm thêm bản, gom **cụm cùng chữ** ở nhiều nhóm (không ghép làm đối chứng của nhau).
- `__daiKhung` gắn video vào trang và chờ khung thật trước khi vẽ (bản đầu ra khung đen ở video dài), báo `khung_loi`, xem được một đoạn `tu`–`den` để đọc chữ trên màn hình. `__linkVideo` kèm dung lượng thật.
- Bản đồ nội dung thêm bảng Góc × Kiểu sáng tạo và mục "Họ đang nói gì". Mẫu báo cáo 8 mục.
- Đóng gói: lệnh cài, bài kiểm, README.

## 2.1 · 03/11/2026

- Đọc đúng nhóm ads: các bản trong nhóm thường là cùng nội dung lên lại, không phải test. Thêm chỉ số nhân bản ads thắng, lên ads 30 ngày.
- Sửa làm tròn phần trăm, hiện đủ 6 tháng nhịp ra ads, gộp nhóm trùng giữa các nguồn.

## 2.0 · 03/11/2026

- Viết lại thành quy trình chung + hồ sơ theo dõi riêng từng dự án, lưu bản chụp và so lần trước.
