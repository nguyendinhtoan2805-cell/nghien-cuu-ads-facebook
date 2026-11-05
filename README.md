# Nghiên cứu ads Facebook: skill soi ads đối thủ cho Claude

Skill cho **Claude** soi quảng cáo Facebook, Instagram của đối thủ qua [Thư viện quảng cáo Meta](https://www.facebook.com/ads/library/). Phiên bản: xem `PHIEN-BAN.txt`.

Mỗi lần chạy, Claude:

1. **Thu thập** mọi ads đang chạy theo từng fanpage và lưu bản chụp, để lần sau so được đối thủ đổi gì.
2. **Ước lượng độ mạnh** khi không có số chi tiêu: thứ hạng hiển thị, nhịp ra ads, ads bền, ads thắng được nhân bản sang chiến dịch mới.
3. **Xem video và ảnh thật**: dải khung mỗi 2 giây, bóc lời thoại tiếng Việt (khi bạn cho tải video).
4. **Giải mã vì sao ads thắng chạy tốt**: so ads thắng với ads yếu của chính đối thủ đó qua 10 lớp (người xem, hook, lời hứa, cơ chế, bằng chứng, rào cản, ưu đãi, nhịp kịch bản, tay nghề, đòn tâm lý), rồi gom thành công thức của từng đối thủ.
5. **Viết báo cáo**: họ đang chạy nội dung gì, vì sao chạy tốt, khoảng trống mình đánh được, giả thuyết test cho ads của mình.

Skill là **quy trình chung**, không chứa dữ liệu thương hiệu nào. Đối thủ, nơi lưu và luật nội dung của bạn nằm trong **hồ sơ theo dõi** trong dự án của bạn: lần đầu chạy, Claude tạo hồ sơ từ mẫu `soi-ads-doi-thu/mau/ho-so-theo-doi.md` cùng bạn.

## Cài

Cần: app Claude (thẻ **Code**) hoặc Claude Code có trình duyệt (trình duyệt có sẵn trong app, hoặc Claude in Chrome), Python 3, và [uv](https://docs.astral.sh/uv/) nếu muốn bóc lời thoại.

```bash
git clone https://github.com/nguyendinhtoan2805-cell/nghien-cuu-ads-facebook.git
cd nghien-cuu-ads-facebook
uv run cai-dat-skill.py
```

Hoặc tải zip ở mục **Releases**, giải nén rồi chạy lệnh cuối. Cài xong thì **mở lại Claude**.

Nhận bản mới: `git pull` (hoặc giải nén zip mới đè lên) rồi chạy lại `uv run cai-dat-skill.py`.

## Dùng

Nói với Claude trong dự án của bạn, ví dụ:

- *"Soi ads Facebook của đối thủ A và B."*
- *"Vì sao ads của đối thủ A đang chạy tốt?"*
- *"Chụp lại ads đối thủ tháng này, so với lần trước."*

Nên đăng nhập Facebook trong trình duyệt Claude dùng. Claude sẽ hỏi trước khi tải video về máy để bóc lời.

## Bên trong

| Đường dẫn | Là gì |
|---|---|
| `soi-ads-doi-thu/SKILL.md` | Quy trình 8 bước, mỗi bước có điều kiện "xong khi" |
| `soi-ads-doi-thu/references/` | Thao tác Thư viện Meta · ước lượng độ mạnh · giải mã ads thắng · phân tích nội dung và mẫu báo cáo |
| `soi-ads-doi-thu/scripts/thu-thap.js` | Chạy trong tab Thư viện: gom ads của fanpage thành dòng gọn |
| `soi-ads-doi-thu/scripts/xem-media.js` | Chạy trong tab Thư viện: lưới video, dải khung, ảnh carousel |
| `soi-ads-doi-thu/scripts/thong-ke.py` | Thống kê bản chụp, chọn ads thắng và đối chứng, so lần trước |
| `soi-ads-doi-thu/scripts/boc-loi.py` | Tải video (khi được phép) và bóc lời bằng faster-whisper |
| `tests/` | Bài kiểm cho `thong-ke.py`, dữ liệu mẫu giả |

## Giới hạn

- Thư viện Meta không có chi tiêu, lượt hiển thị ở Việt Nam. Độ mạnh và "vì sao chạy tốt" là **suy luận có căn cứ**, luôn kèm mức chắc chắn, không phải số đo.
- Ngưỡng Mạnh/Vừa/Nhẹ là ngưỡng khởi điểm cho SME Việt Nam (`NGUONG` trong `thong-ke.py`), nên chỉnh sau vài lần chụp.
- Báo cáo về đối thủ là tài liệu nội bộ. Dùng để học nguyên lý, không chép chữ hay hình của họ.

## Phát triển

```bash
python3 -I -m unittest discover -s tests
node --check soi-ads-doi-thu/scripts/thu-thap.js soi-ads-doi-thu/scripts/xem-media.js
```

Ra bản mới: sửa `PHIEN-BAN.txt` và `CHANGELOG.md` → commit, push → `gh release create v<x>` kèm zip (`git archive -o nghien-cuu-ads-facebook-v<x>.zip HEAD`).
