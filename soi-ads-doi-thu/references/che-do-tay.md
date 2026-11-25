# Chế độ tay: người dùng tự lấy dữ liệu, AI phân tích

Dùng khi AI **không điều khiển được trình duyệt** (ChatGPT, Codex không có công cụ trình duyệt, Claude trên web). Người dùng chạy script thu thập trong Chrome của chính họ, tải file về rồi đưa cho AI. Phần thống kê, giải mã, báo cáo giữ nguyên như chế độ tự động.

AI dẫn người dùng **từng bước, mỗi lần một việc**, chờ họ báo xong rồi mới nói bước sau. Người dùng có thể không rành kỹ thuật: nói rõ bấm phím gì, thấy gì là đúng.

## 1. Chuẩn bị (một lần)

- Máy tính có **Chrome** (hoặc Edge, Cốc Cốc), đã đăng nhập Facebook.
- File `thu-thap.js` (và `xem-media.js` nếu xem media) nằm trong thư mục `scripts/` của skill. Đưa file cho người dùng tải (ChatGPT: tạo file để tải về; Codex: chỉ đường dẫn trên máy), hoặc họ lấy trong zip của skill.
- Nói trước một lần: khi mở Console, Facebook hiện cảnh báo lớn **"Dừng lại!"**. Đó là cảnh báo chuẩn chống lừa đảo: chỉ dán code từ nguồn mình tin. `thu-thap.js` **chỉ đọc** danh sách ads đang hiện và tải file về máy, không gửi dữ liệu đi đâu, không đăng gì lên Facebook. Người dùng có quyền mở file ra đọc trước khi dán.

## 2. Lấy dữ liệu một fanpage

| Bước | Người dùng làm | Đúng khi thấy |
|---|---|---|
| 1 | Mở link Thư viện của fanpage (AI đưa link theo `page_id` trong hồ sơ, mẫu ở `thu-vien-meta.md` mục 1) | Trang hiện "~N kết quả" và danh sách ads |
| 2 | Mở Console: **F12** rồi chọn thẻ **Console** (Mac: **Cmd + Option + J**) | Khung gõ lệnh có dấu `>` |
| 3 | Lần đầu, Chrome chặn dán: gõ tay `allow pasting` rồi Enter (Chrome tiếng Việt có thể là `cho phép dán`) | Hết dòng cảnh báo chặn dán |
| 4 | Mở `thu-thap.js` bằng Notepad / TextEdit, chọn hết (Ctrl+A / Cmd+A), copy, dán vào Console, Enter. **Chưa cuộn trang trước bước này** | Dòng `[soi ads] page:…: đã lấy N nhóm` |
| 5 | Đóng Console hoặc để nguyên, **cuộn chuột xuống cuối trang**, chờ ads tải thêm, cuộn tiếp | Console báo `HẾT trang` (hoặc trang không tải thêm nữa) |
| 6 | Gõ `__soiAdsLuu("Tên đối thủ")` rồi Enter. Tên đối thủ lấy đúng như cột "Đối thủ" trong hồ sơ | Trình duyệt tải về file `YYYY-MM-DD-ten-doi-thu.json` |

Đối thủ có nhiều fanpage: làm lại bảng trên cho từng fanpage, **cùng một tên đối thủ**. Mỗi fanpage ra một file (trình duyệt có thể tự thêm "(1)", "(2)" vào tên): `thong-ke.py` tự gộp các file cùng đối thủ, cùng ngày.

Kết quả của `__soiAdsLuu` có `canh_bao` khi còn trang chưa cuộn hết: bảo người dùng cuộn tiếp rồi gõ lại lệnh, xoá file thiếu.

## 3. AI nhận file

1. Người dùng gửi các file `.json` mới **và** các bản chụp cũ của cùng đối thủ (thư mục `du-lieu/` trong dự án) để so lần trước.
2. Đặt tất cả vào một thư mục, chạy `python3 -I <skill>/scripts/thong-ke.py <thư mục>` như Bước 3 của `SKILL.md`.
3. Kiểm: số dòng mỗi file khớp số người dùng thấy ở Console; `nguon[].con_trang_sau` đều `false`. Có `true` thì ghi "bản chụp thiếu" vào Giới hạn của báo cáo.

## 4. Chữ đầy đủ và media của ads được chọn

Sau khi thống kê chọn ra ads thắng và đối chứng:

1. Người dùng **giữ nguyên tab** vừa thu thập (chưa tải lại trang). Ads thuộc fanpage khác thì mở lại fanpage đó và chạy lại bước 2.1–2.4 (không cần cuộn nếu ads nằm trong 30 nhóm đầu).
2. AI đưa sẵn một dòng lệnh để dán: `__soiAdsLuuChiTiet(["<id1>", "<id2>", …])`. Trình duyệt tải về file chi tiết: chữ đầy đủ mọi bản, tiêu đề, CTA, link ảnh và video.
3. **Xem hình.** Link ảnh, video trong file có hạn dùng và AI trên web thường không mở được. Nhờ người dùng chụp màn hình:
   - Dán thêm `xem-media.js` vào Console, gõ `__xemLuoi(["<id1>", …])`, chờ 4 giây, rồi lần lượt `await __tua(0.3)`, `await __tua(3)`, `await __tua(d => d * 0.5)`, `await __tua(d => d - 1.5)`. Sau mỗi lệnh chụp màn hình gửi AI. Đây là 4 mốc tối thiểu.
   - Ads thắng dạng video cần xem kỹ: `await __daiKhung("<id>", {buoc: 2})`, chụp hết các khung (cuộn nếu dài).
   - Ảnh, carousel: `__xemAnh(["<id>", …], {cot: 2})`, chụp màn hình.
   - Cách đơn giản hơn khi chỉ vài ads: mở `facebook.com/ads/library/?id=<id>`, chụp ở đầu, giây thứ 3, giữa và cuối video.
4. **Lời thoại.** Chế độ tay không bóc lời tự động. Hỏi người dùng có muốn tự nghe hook 5 giây đầu và gõ lại không; không thì ghi "chưa nghe lời". Dùng Codex trên máy thì chạy được `boc-loi.py` như chế độ tự động (vẫn phải xin phép tải).

## 5. Trả kết quả

- Báo cáo viết theo `phan-tich-noi-dung.md` mục 4. Đưa người dùng file `.md` để lưu vào thư mục báo cáo trong hồ sơ.
- Nhắc người dùng **lưu các file `.json` vừa tải** vào thư mục `du-lieu/` của dự án. Lần sau thiếu chúng thì không so được "đối thủ đổi gì".
- Hồ sơ theo dõi cần thêm dòng lịch sử (Bước 7 của `SKILL.md`): đưa nguyên đoạn cần dán, người dùng tự sửa file hồ sơ.

## 6. Lỗi hay gặp

| Người dùng báo | Cách xử |
|---|---|
| Dán vào Console không được | Gõ tay `allow pasting` (hoặc `cho phép dán`) vào dòng có dấu `>` rồi Enter, sau đó dán lại. **Tắt bộ gõ tiếng Việt trước**: gõ Telex thì "allow" thành "allơ" và Chrome không nhận. Phải gõ trong Console của đúng tab đang thu thập |
| `__soiAdsLuu is not defined` | Trang đã tải lại hoặc chưa dán script. Dán lại `thu-thap.js` |
| Console báo `đã lấy` nhưng số không tăng khi cuộn | Cuộn bằng chuột hoặc phím Page Down; đợi 2–3 giây mỗi lần. Dán script **trước** khi cuộn, nếu lỡ cuộn trước thì tải lại trang và làm lại |
| Không thấy file tải về | Xem thư mục Tải về (Downloads); Chrome có thể hỏi "cho phép tải nhiều file" ở thanh địa chỉ |
| Thư viện chỉ hiện vài ads | Chưa đăng nhập Facebook, hoặc đang ở bộ lọc khác: dùng đúng link AI đưa |
