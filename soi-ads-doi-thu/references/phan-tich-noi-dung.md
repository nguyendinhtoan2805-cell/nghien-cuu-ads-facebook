# Phân tích nội dung và mẫu báo cáo

## 1. Chọn ads để xem

Với mỗi đối thủ:

1. **Ads thắng** (mục "Ads thắng và đối chứng" của `thong-ke.py`): xem sâu và giải mã theo [`giai-ma-ads-thang.md`](giai-ma-ads-thang.md).
2. **Đối chứng**: 1–2 ads cho mỗi ads thắng, ghép cặp theo `giai-ma-ads-thang.md` mục 1.
3. **Ads tiêu biểu khác**: top 5 theo hạng, ads mới ≤30 ngày có hạng cao, và ads mở góc nội dung lạ. Mỗi ads một phiếu ngắn (mục 3). Tối đa khoảng 15 ads mỗi đối thủ, tính cả hai nhóm trên.

Ads còn lại chỉ xếp vào **bản đồ nội dung** (mục 2).

## 2. Bản đồ nội dung

Xếp **mọi** nhóm ads đang chạy vào hai bảng, đếm số nhóm mỗi ô. Đánh dấu ô có ads thắng.

- **Sản phẩm × Góc nội dung:** đối thủ dồn lực vào sản phẩm nào, đánh bằng góc nào. Đặt tên góc bằng chính việc ads làm, ví dụ: nỗi đau tư thế · đầu tư dài hạn · bằng chứng khách thật · chứng nhận và kỹ thuật · quà tặng · khuyến mãi theo mùa · kéo về cửa hàng · bán phụ kiện · demo tính năng. Gom về 5–8 góc, đặt tên mới khi không khớp.
- **Góc × Kiểu sáng tạo:** cùng một góc nhưng làm bằng kiểu nào. Kiểu: người thật review · demo sản phẩm · so sánh · kể chuyện gia đình · chuyên gia nói · cắt từ livestream · ảnh sản phẩm kèm chữ · album hoặc carousel thông số.

Dưới hai bảng, viết 3–5 dòng **"Họ đang nói gì"**: các thông điệp lặp lại nhiều nhất, xếp theo số nhóm và theo hạng tốt nhất. Mỗi dòng dẫn 1–2 câu nguyên văn.

## 3. Phiếu ngắn cho ads tiêu biểu

Tách ba lớp: **thấy được** (chữ, hình, mốc giây) → **diễn giải** (vì sao có tác dụng hay không) → **cần kiểm** (điều chưa đủ bằng chứng).

| Mục | Ghi gì |
|---|---|
| Nhận diện | ID (có link), fanpage, hạng, vai, ngày chạy, tuổi, số bản, định dạng và thời lượng, nền tảng, CTA |
| Sản phẩm và tệp nhắm | Mẫu nào. Ads nói với ai, dựa trên chữ và hình (gọi theo mã tệp của dự án nếu có) |
| Hook chữ | Nguyên văn câu đầu. Nằm trong khoảng 125 ký tự đầu hay không |
| Hook hình | Khung 0–3 giây hoặc ảnh đầu đã **xem thật**: cảnh gì, chữ trên màn hình gì |
| Thông điệp chính | Một câu |
| Bằng chứng | Thông số, chứng nhận, khách thật, chuyên gia, so sánh. Ghi nguyên văn |
| Ưu đãi | Mức giảm, quà, điều kiện, thời hạn |
| Diễn biến video | Nhịp cảnh theo mốc giây, có người nói hay không, phụ đề, CTA cuối |
| Biến thể | Xem cạnh nhau mốc 0,3s và 3s của các bản. Giống hệt là **nhân bản** (ghi các ngày lên lại); khác chữ hoặc khác hình là **test**, ghi khác ở đâu |
| **Điểm mạnh** | 2–3 ý, mỗi ý có căn cứ quan sát được |
| **Điểm yếu, rủi ro** | 1–3 ý: lời hứa quá mức, chữ dài, hook chậm, thiếu demo, rủi ro chính sách |
| **Bài học cho mình** | Học được gì · tránh gì · khoảng trống nào mình đánh được |

Ads thắng không dùng phiếu này mà dùng bảng 10 lớp của `giai-ma-ads-thang.md`.

Dự án có khung chấm hook hoặc chấm video riêng (ghi trong hồ sơ theo dõi) thì chấm thêm theo khung đó.

Ưu nhược điểm là **nhận định biên tập**. Ghi "có thể", "dễ khiến" khi chưa có số đo. Không suy ra CTR hay doanh số.

## 4. Mẫu báo cáo

```
# Ads Facebook đối thủ: <các đối thủ> · <ngày chụp>
(khối cảnh báo: chỉ dùng nội bộ, theo luật thương hiệu trong hồ sơ)
(khối giới hạn: không có chi tiêu; đã xem video nào, khung nào; đã nghe lời video nào)

## 1. Tóm tắt 30 giây
3–5 gạch: ai đang mạnh nhất, vì sao ads thắng của họ chạy tốt (một câu), đổi hướng gì so với lần trước, khoảng trống đáng đánh nhất

## 2. Độ mạnh
Bảng so đối thủ (từ thong-ke.py) + nhận định tổ hợp tín hiệu kèm mức chắc chắn

## 3. Thay đổi so với lần chụp trước
Mới · tắt · thêm bản. Bỏ mục này ở lần chụp đầu

## 4. Họ đang chạy nội dung gì
Hai bảng bản đồ nội dung + "Họ đang nói gì"

## 5. Vì sao ads của họ chạy tốt
Mỗi đối thủ: công thức 6 ô → từng ads thắng (bảng 10 lớp + đối chứng đã ghép) → bảng giả thuyết kèm mức chắc

## 6. Ads tiêu biểu khác
Phiếu ngắn (mục 3), xếp theo hạng. Kèm ảnh khung hook nếu dự án cho lưu ảnh

## 7. Khoảng trống và việc nên làm
Bảng nguyên lý → mình làm khác thế nào → giả thuyết test (giai-ma-ads-thang.md mục 6), rồi bảng khoảng trống đối thủ chưa đánh → cần kiểm gì trước (luật nội dung, dữ liệu thật)

## 8. Nguồn
Link fanpage trong Thư viện, link từng ads, file bản chụp, lệnh thống kê đã chạy, file lời thoại
```
