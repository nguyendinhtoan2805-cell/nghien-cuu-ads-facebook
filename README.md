# Nghiên cứu ads Facebook: skill soi ads đối thủ cho Claude, ChatGPT, Codex

Skill (chuẩn Agent Skills) soi quảng cáo Facebook, Instagram của đối thủ qua [Thư viện quảng cáo Meta](https://www.facebook.com/ads/library/). Phiên bản: xem `PHIEN-BAN.txt`.

Mỗi lần chạy, AI:

1. **Thu thập** mọi ads đang chạy theo từng fanpage và lưu bản chụp, để lần sau so được đối thủ đổi gì.
2. **Ước lượng độ mạnh** khi không có số chi tiêu: thứ hạng hiển thị, nhịp ra ads, ads bền, ads thắng được nhân bản sang chiến dịch mới.
3. **Xem video và ảnh thật**: dải khung mỗi 2 giây, bóc lời thoại tiếng Việt (khi bạn cho tải video).
4. **Giải mã vì sao ads thắng chạy tốt**: so ads thắng với ads yếu của chính đối thủ đó qua 10 lớp (người xem, hook, lời hứa, cơ chế, bằng chứng, rào cản, ưu đãi, nhịp kịch bản, tay nghề, đòn tâm lý), rồi gom thành công thức của từng đối thủ.
5. **Viết báo cáo**: họ đang chạy nội dung gì, vì sao chạy tốt, khoảng trống mình đánh được, giả thuyết test cho ads của mình.

Skill là **quy trình chung**, không chứa dữ liệu thương hiệu nào. Đối thủ, nơi lưu và luật nội dung của bạn nằm trong **hồ sơ theo dõi** trong dự án của bạn: lần đầu chạy, Claude tạo hồ sơ từ mẫu `soi-ads-doi-thu/mau/ho-so-theo-doi.md` cùng bạn.

## Cài

### Cần có

| Thứ | Để làm gì | Lấy ở đâu |
|---|---|---|
| App **Claude** bản máy tính (thẻ **Code**) hoặc Claude Code | Chạy skill | [claude.ai/download](https://claude.ai/download) |
| Trình duyệt cho Claude: trình duyệt có sẵn trong app, hoặc tiện ích **Claude in Chrome** | Mở Thư viện quảng cáo Meta | Có sẵn trong app · [Chrome Web Store](https://chromewebstore.google.com/) tìm "Claude" |
| **uv** | Chạy lệnh cài (tự lo Python) | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Tài khoản Facebook | Thư viện xem được đủ ads khi đã đăng nhập | |

Dùng ChatGPT hoặc Codex thì xem mục **[Dùng với ChatGPT hoặc Codex](#dùng-với-chatgpt-hoặc-codex)**.

### Từng bước (lần đầu)

1. Cài app Claude, đăng nhập, mở thẻ **Code**.
2. Cài uv. Mở **Terminal** (Mac) hoặc **PowerShell** (Windows), dán đúng một dòng:
   - Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

   Cài xong thì đóng cửa sổ, mở lại.
3. Tải skill: vào mục **Releases** bên phải trang này, tải file `nghien-cuu-ads-facebook-v<x>.zip` ở bản mới nhất, giải nén vào chỗ dễ tìm (ví dụ thư mục Tài liệu).
4. Cài: trong Terminal/PowerShell, gõ `cd ` (có dấu cách) rồi kéo thả thư mục vừa giải nén vào, Enter. Sau đó chạy:

   ```bash
   uv run cai-dat-skill.py
   ```

   Thấy dòng `XONG — đã cài 1 skill` là được.
5. **Thoát hẳn app Claude rồi mở lại.**
6. Tạo một thư mục dự án (ví dụ `Ads đối thủ`), mở thư mục đó trong thẻ Code. Đăng nhập Facebook trong trình duyệt Claude dùng.
7. Gõ thử: *"Soi ads Facebook của đối thủ A"*. Lần đầu Claude sẽ hỏi để tạo **hồ sơ theo dõi** (đối thủ nào, lưu ở đâu, luật nội dung). Công ty đã có hồ sơ sẵn thì chép file đó vào thư mục dự án trước khi gõ.

Biết dùng git thì thay bước 3 bằng:

```bash
git clone https://github.com/nguyendinhtoan2805-cell/nghien-cuu-ads-facebook.git
cd nghien-cuu-ads-facebook
```

### Nhận bản mới

Tải zip bản mới, giải nén đè lên thư mục cũ (hoặc `git pull`), chạy lại `uv run cai-dat-skill.py`, rồi mở lại Claude. Hồ sơ và dữ liệu nằm trong thư mục dự án của bạn nên không bị mất.

### Gặp lỗi

| Lỗi | Cách xử |
|---|---|
| `uv: command not found` / `uv is not recognized` | Chưa mở lại Terminal sau khi cài uv. Đóng, mở lại |
| Claude không nhận skill | Thoát hẳn app (Mac: Cmd+Q) rồi mở lại. Kiểm tra có thư mục `~/.claude/skills/soi-ads-doi-thu` |
| Thư viện chỉ hiện vài ads, đòi đăng nhập | Đăng nhập Facebook trong đúng trình duyệt Claude đang dùng |
| Bóc lời thoại chậm lần đầu | Lần đầu tải mô hình nghe (~0,5 GB). Claude sẽ hỏi trước |

## Dùng với ChatGPT hoặc Codex

| | Claude bản máy tính | ChatGPT bản máy tính có tích hợp Chrome | ChatGPT trên web | Codex |
|---|---|---|---|---|
| Thu thập ads | **Tự động**: AI mở Thư viện, cuộn, lấy hết | **Bán tự động**: AI tự mở, cuộn, dán script; bạn chỉ gõ `allow pasting` một lần trong Console | **Tay**: bạn dán script vào Console, cuộn, tải file JSON gửi ChatGPT. AI dẫn từng bước | Tay, hoặc tự động nếu Codex có công cụ trình duyệt |
| Thống kê, giải mã, báo cáo | ✅ | ✅ (đã chạy thử 25/11/2026) | ✅ | ✅ |
| Xem video, ảnh | AI tự xem | AI tự xem | Bạn chụp màn hình theo mốc AI đưa | Như ChatGPT web |
| Bóc lời thoại | ✅ (khi cho phép tải) | Chưa thử | ❌ ghi "chưa nghe lời" | ✅ |

Chế độ tay chậm hơn nhưng dữ liệu y hệt (thứ hạng, ngày lên, số bản), nên thống kê và giải mã vẫn đủ căn cứ. Hướng dẫn đầy đủ: `soi-ads-doi-thu/references/che-do-tay.md`.

**ChatGPT**

1. Vào mục **Releases**, tải file `soi-ads-doi-thu-skill.zip` (chỉ có skill, gọn để tải lên).
2. Trong ChatGPT mở mục **Skills**, tải file zip lên.
3. Nên tạo một **Project** cho việc soi ads, đưa hồ sơ theo dõi và các file bản chụp cũ (`du-lieu/*.json`) vào project.
4. Gõ `@soi-ads-doi-thu` rồi yêu cầu, ví dụ *"soi ads đối thủ A"*. ChatGPT sẽ dẫn bạn lấy dữ liệu trong Chrome.

**Codex** (trên máy): làm như bước Cài ở trên nhưng chạy `uv run cai-dat-skill.py --codex` (cài vào `~/.agents/skills`), rồi mở lại Codex, gọi bằng `$soi-ads-doi-thu`.

Giao diện ChatGPT và Codex thay đổi nhanh: tên mục có thể khác chút.

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
- `boc-loi.py` (bóc lời thoại) **chưa chạy trên video thật**. Lần đầu dùng nên thử 1–2 video ngắn trước.
- Ngưỡng Mạnh/Vừa/Nhẹ là ngưỡng khởi điểm cho SME Việt Nam (`NGUONG` trong `thong-ke.py`), nên chỉnh sau vài lần chụp.
- Báo cáo về đối thủ là tài liệu nội bộ. Dùng để học nguyên lý, không chép chữ hay hình của họ.

## Phát triển

```bash
python3 -I -m unittest discover -s tests
node --test tests/thu-thap.test.mjs
node --check soi-ads-doi-thu/scripts/thu-thap.js soi-ads-doi-thu/scripts/xem-media.js
```

Ra bản mới: sửa `PHIEN-BAN.txt`, `CHANGELOG.md` và dòng phiên bản trong `SKILL.md` → commit, push → `gh release create v<x>` kèm 2 file: `git archive -o nghien-cuu-ads-facebook-v<x>.zip HEAD` và `uv run cai-dat-skill.py --zip-chatgpt`.
