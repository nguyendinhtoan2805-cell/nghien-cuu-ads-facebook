# Thay đổi

## 3.2.1 · 25/11/2026

Sửa sau lần chạy thử thật trên ChatGPT bản máy tính (tích hợp Chrome):

- **Sửa lỗi "đối chứng đã tắt"**: trước đây nhóm biến mất giữa hai lần chụp bị coi là "test rồi bỏ" chỉ theo tuổi lúc chụp trước, quên khoảng cách hai lần chụp. Ads thắng hạng 1 chạy tiếp gần 3 tuần rồi mới tắt cũng bị xếp làm đối chứng. Nay dùng `tat_som()`: tuổi lúc chụp trước + số ngày giữa hai lần chụp ≤14.
- Thống kê in thêm **"Từng đứng top 3 lần trước, nay đã tắt"**.
- SKILL.md: **cấm thay `thu-thap.js` bằng đọc giao diện** rồi báo số; thêm chế độ **bán tự động** (AI điều khiển Chrome nhưng dán script qua Console); Bước 7 sửa cả `cap_nhat` của hồ sơ.
- Chế độ tay: lưu ý tắt bộ gõ tiếng Việt khi gõ `allow pasting`. README tách ChatGPT bản máy tính (bán tự động) với ChatGPT web (tay).

## 3.2 · 25/11/2026

- **Dùng được với ChatGPT và Codex.** SKILL.md có bước chọn chế độ: **tự động** (AI điều khiển trình duyệt) hoặc **tay** (người dùng chạy script trong Chrome, AI phân tích). Hướng dẫn chế độ tay mới: `references/che-do-tay.md`.
- `thu-thap.js`: thêm `__soiAdsBanChup`, `__soiAdsLuu` (tải bản chụp về máy thành file JSON đúng định dạng), `__soiAdsLuuChiTiet`, và dòng tiến độ trong Console. Bài kiểm mới `tests/thu-thap.test.mjs` giả lập trang Thư viện.
- `thong-ke.py` tự **gộp các file cùng đối thủ, cùng ngày** (chạy tay mỗi fanpage một file; tải trùng không nhân đôi).
- Lệnh cài: `--codex` (cài vào `~/.agents/skills`), `--zip-chatgpt` (tạo zip để tải lên ChatGPT).

## 3.1 · 25/11/2026

- **Đối chứng phải chạy ≥14 ngày** (`TUOI_DOI_CHUNG` trong `thong-ke.py`): ads vài ngày tuổi chưa kịp leo hạng nên không còn bị chọn làm đối chứng. Tài liệu thêm mục **Lệch tuổi** (đối chứng trẻ hơn ads thắng nhiều thì hạ mức chắc) và **Đối chiếu chéo giữa các đối thủ** trước khi rút nguyên lý.
- README: hướng dẫn cài từng bước cho người mới (Mac, Windows), bảng lỗi hay gặp, cách nhận bản mới.

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
