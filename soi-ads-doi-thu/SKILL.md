---
name: soi-ads-doi-thu
description: Soi quảng cáo Facebook của đối thủ qua Thư viện quảng cáo Meta. Thu thập ads đang chạy, ước lượng độ mạnh (thứ hạng hiển thị, nhịp ra ads, nhân bản ads thắng), xem video và ảnh, bóc lời thoại, giải mã vì sao ads thắng của họ chạy tốt bằng cách so với ads yếu, so với lần chụp trước. Dùng khi check, soi hoặc theo dõi ads đối thủ, đọc Ad Library, hỏi vì sao ads đối thủ chạy tốt, hoặc tìm góc ads từ đối thủ.
---

# Soi ads đối thủ

**Phiên bản** 3.0 · 05/11/2026 · Chỉ Facebook / Instagram (Thư viện quảng cáo Meta).

Skill này là **quy trình chung**. Đối thủ, nơi lưu và luật nội dung của từng thương hiệu nằm trong **hồ sơ theo dõi** của dự án, không nằm trong skill.

Thư viện **không có chi tiêu hay lượt hiển thị** ở Việt Nam. Độ mạnh được **suy từ tín hiệu** ([`references/do-manh.md`](references/do-manh.md)). "Vì sao chạy tốt" được trả lời bằng **đối chứng**: so ads thắng với ads yếu của chính đối thủ đó ([`references/giai-ma-ads-thang.md`](references/giai-ma-ads-thang.md)).

## Bước 0: Mở hồ sơ theo dõi

Tìm file `*Hồ sơ theo dõi ads*` trong dự án. Nếu chưa có, tạo từ [`mau/ho-so-theo-doi.md`](mau/ho-so-theo-doi.md) cùng người dùng: hỏi đối thủ, nơi lưu, và lấy link luật thương hiệu từ tài liệu dự án. Đọc hết các link luật, tệp khách, khung chấm ghi trong hồ sơ.

**Xong khi:** biết danh sách đối thủ kèm `page_id`, nơi lưu bản chụp và báo cáo, luật nội dung phải theo, và bản chụp gần nhất (nếu có).

## Bước 1: Xác nhận fanpage

Mọi thao tác Thư viện làm theo [`references/thu-vien-meta.md`](references/thu-vien-meta.md). Đọc file đó trước khi mở trình duyệt.

- Đối thủ chưa có `page_id`, hoặc lần dò gần nhất đã quá 90 ngày: dò fanpage (mục 2 của file tham chiếu), gồm cả trang theo ngành và trang vệ tinh. Ghi vào hồ sơ.
- Người dùng nhắc đối thủ mới: dò và thêm vào hồ sơ trước khi thu thập.

**Xong khi:** mỗi đối thủ trong lần chạy này có ít nhất một fanpage chính đã mở được trong Thư viện.

## Bước 2: Thu thập và lưu bản chụp

Với từng fanpage: mở URL theo `page_id`, chạy [`scripts/thu-thap.js`](scripts/thu-thap.js), cuộn chuột thật tới khi `con_trang_sau` là `false`, rồi xuất `__soiAdsDong` theo lô 50.

Ghi **một file mỗi đối thủ** vào thư mục dữ liệu: `YYYY-MM-DD-<doi-thu>.json`, định dạng ở đầu [`scripts/thong-ke.py`](scripts/thong-ke.py). Gộp các fanpage chính của đối thủ vào cùng file, `hang` giữ theo từng fanpage. Trang vệ tinh chỉ đưa vào khi hồ sơ ghi cần.

**Xong khi:** mọi fanpage đều có `con_trang_sau: false`, và số dòng trong file bằng tổng `da_lay_nhom`.

## Bước 3: Thống kê

```bash
python3 -I <thư mục skill>/scripts/thong-ke.py "<thư mục dữ liệu>" [--loc "<regex>"]
```

Dùng `--loc` khi hồ sơ ghi lọc chữ (fanpage bán nhiều ngành). Script in sẵn: quy mô, định dạng, nền tảng, CTA, nhịp ra ads, tuổi, nhân bản, top 10 theo hạng, **cụm cùng chữ**, **ads thắng và đối chứng**, thay đổi so với lần trước (mới tinh · bật lại · thêm bản · tắt), bảng so độ mạnh.

**Xong khi:** có bảng thống kê cho mọi đối thủ, và đọc được tổ hợp tín hiệu theo `do-manh.md` mục 3 kèm mức chắc chắn.

## Bước 4: Xem media

Chạy [`scripts/xem-media.js`](scripts/xem-media.js) trong tab Thư viện, sau khi đã lưu bản chụp. Chọn ads theo [`references/phan-tich-noi-dung.md`](references/phan-tich-noi-dung.md) mục 1.

- **Ads thắng:** dải khung mỗi 2 giây hết video, mọi thẻ ảnh, chữ đầy đủ mọi bản.
- **Đối chứng và ads tiêu biểu:** 4 mốc (0,3s · 3s · 50% · cuối) và chữ đầy đủ.
- **Lời thoại:** hỏi người dùng **một lần** cho cả lượt: được tải video của ads thắng và đối chứng để bóc lời không (nêu số file, nguồn, dung lượng ước tính). Được thì chạy [`scripts/boc-loi.py`](scripts/boc-loi.py) theo `thu-vien-meta.md` mục 5. Không được thì ghi "chưa nghe lời".

**Xong khi:** mọi ads thắng có dải khung đã xem hết, mọi ads được chọn có ít nhất mốc 0,3s và 3s đã xem, và mọi video đã có lời thoại hoặc ghi "chưa nghe lời".

## Bước 5: Phân tích nội dung

1. **Bản đồ nội dung** (`phan-tich-noi-dung.md` mục 2): xếp mọi nhóm vào hai bảng, viết "Họ đang nói gì".
2. **Giải mã ads thắng** (`giai-ma-ads-thang.md`): ghép cặp đối chứng, điền 10 lớp, viết giả thuyết kèm mức chắc, gom công thức của từng đối thủ, chuyển thành nguyên lý và giả thuyết test cho mình.
3. **Phiếu ngắn** cho ads tiêu biểu còn lại (`phan-tich-noi-dung.md` mục 3).

**Xong khi:** mọi nhóm đang chạy nằm trong bản đồ nội dung; mọi ads thắng có đủ 10 lớp và có cột đối chứng; mỗi đối thủ có công thức hoặc dòng "chưa đủ ads thắng".

## Bước 6: Viết báo cáo

Theo mẫu ở `phan-tich-noi-dung.md` mục 4, lưu vào nơi ghi trong hồ sơ. Áp luật nội dung của hồ sơ cho phần "khoảng trống và việc nên làm". Mỗi gợi ý ghi cần kiểm gì trước khi dùng (dữ liệu thật, claim, quyền hình ảnh).

**Xong khi:** báo cáo có đủ 8 mục (mục 3 được bỏ ở lần chụp đầu), mọi nhận định độ mạnh dẫn tín hiệu, mọi "vì sao chạy tốt" dẫn đối chứng, mọi ưu nhược điểm dẫn quan sát.

## Bước 7: Cập nhật hồ sơ

Thêm một dòng vào lịch sử các lần chụp. Ghi fanpage mới tìm thấy, page đổi tên, ngưỡng cần chỉnh nếu thấy dải thật của ngành khác `do-manh.md`. Báo người dùng link báo cáo và 3 điều đáng chú ý nhất, trong đó có công thức ads thắng của đối thủ mạnh nhất.

**Xong khi:** hồ sơ có dòng của lần chụp này.
