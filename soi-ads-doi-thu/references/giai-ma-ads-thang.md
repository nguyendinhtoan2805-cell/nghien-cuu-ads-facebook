# Giải mã ads thắng: vì sao ads của họ chạy tốt

Thư viện không có số đo hiệu quả. Câu "vì sao ads này chạy tốt" được trả lời bằng **đối chứng**: so ads thắng với ads yếu **của chính đối thủ đó**. Điều ads thắng có mà ads yếu không có là ứng viên lý do. Điều cả hai cùng có chỉ là phong cách của hãng, không giải thích được vì sao ads thắng.

## 1. Chọn ads thắng và đối chứng

`thong-ke.py` in sẵn mục **Ads thắng và đối chứng** theo luật dưới. Luật nằm ở hàm `vai()` trong script, sửa ở đó.

| Vai | Điều kiện | Mức chắc |
|---|---|---|
| **Thắng rõ** | Nhân bản (lên lại sau >14 ngày) **và** hạng ≤5 trong fanpage | cao |
| **Thắng** | Bền >60 ngày và hạng ≤10 · hoặc nhân bản và hạng ≤15 · hoặc mới ≤30 ngày mà đã hạng ≤3 | vừa |
| **Thắng (yếu)** | Như "Thắng" theo độ bền, nhưng đối thủ không lên ads nào trong 30 ngày (chạy treo): ads bền có thể chỉ là ads bị bỏ quên | thấp |
| **Đối chứng** | Nửa dưới bảng hạng của fanpage, chỉ lên một lần, không nhân bản, **đã chạy ≥14 ngày** · hoặc nhóm **chắc chắn** tắt sau ≤14 ngày: tuổi lúc chụp trước + số ngày giữa hai lần chụp ≤14 (hàm `tat_som()`). Muốn có loại đối chứng này thì chụp lại sau 5–7 ngày | |

Ngưỡng hạng co theo cỡ fanpage: "hạng ≤10" và "hạng ≤3" không vượt quá 1/3 số nhóm của trang, "hạng ≤5" không vượt quá một nửa. Fanpage dưới 3 nhóm thì không xét vai.

Ghép cặp: mỗi ads thắng lấy 1–2 đối chứng **cùng sản phẩm hoặc cùng góc**, cùng định dạng nếu được. Script không biết sản phẩm, nên ghép cặp là việc của người phân tích sau khi đọc chữ. Không có đối chứng cùng sản phẩm thì ghép cùng định dạng và hạ mức chắc một bậc.

**Cụm cùng nội dung:** một nội dung có thể được tải lên thành nhiều nhóm (chiến dịch, tệp khác nhau). Script in bảng "Cụm cùng chữ ở nhiều nhóm" và không chọn thành viên của cụm làm đối chứng. Xem media để xác nhận cùng video (cùng thời lượng, cùng khung ở mốc 0,3s · 3s · 50%). Đã cùng video thì:

- Cả cụm là **một** nội dung: tính tổng số nhóm, tổng số bản, hạng tốt nhất. Một nội dung trải 4 nhóm là tín hiệu thắng dù từng nhóm hạng thấp.
- Hạng chênh nhau trong cụm là do ngân sách, tệp nhắm, chiến dịch. **Không** dùng làm bằng chứng về nội dung.

**Lệch tuổi:** ads vài ngày tuổi chưa kịp leo hạng, nên đứng cuối bảng chưa chắc là yếu. Script không chọn ads dưới 14 ngày làm đối chứng (`TUOI_DOI_CHUNG`). Nếu đối chứng còn lại vẫn trẻ hơn ads thắng rất nhiều (ví dụ 20 ngày so với 300 ngày), hạ mức chắc mọi giả thuyết của đối thủ đó một bậc và ghi vào mục Giới hạn của báo cáo. Đối thủ đang lên ads dồn dập (đa số nhóm dưới 30 ngày) thường không đủ đối chứng: chụp lại sau 2–3 tuần.

Nhóm đã tắt không còn trong bộ lọc "đang chạy". Muốn xem lại thì mở `facebook.com/ads/library/?id=<id>`.

Đối thủ chạy dưới 6 nhóm thì không đủ đối chứng: chỉ ghi "đặc điểm ads thắng", không ghi "vì sao".

## 2. Xem đủ sâu trước khi giải mã

Ads thắng cần xem kỹ hơn ads thường:

- **Video:** dải khung mỗi 1,5–2 giây hết video (`__daiKhung` trong `scripts/xem-media.js`), không chỉ 4 mốc.
- **Lời thoại:** bóc lời bằng `scripts/boc-loi.py` khi người dùng cho tải video. Với video có người nói, lời thoại là nửa nội dung. Không được tải thì ghi "chưa nghe lời" và chỉ giải mã phần hình, chữ.
- **Chữ:** chữ đầy đủ của mọi bản, tiêu đề, mô tả link, nút CTA.
- **Ảnh, carousel:** từng thẻ theo thứ tự (`__xemAnh`).

Đối chứng xem ở mức thường: 4 mốc (0,3s · 3s · 50% · cuối) và chữ đầy đủ.

## 3. Mười lớp giải mã

Mỗi lớp ghi ba thứ: **thấy gì** (nguyên văn, mốc giây, số thẻ) → **cơ chế** (vì sao lớp này khiến người xem dừng lại, tin, hoặc nhắn tin) → **đối chứng có không**.

| # | Lớp | Hỏi gì |
|---|---|---|
| 1 | **Người xem và mức nhận biết** | Ads nói với ai. Người đó đang ở mức nào: chưa thấy vấn đề · thấy vấn đề · đang tìm giải pháp · đang so sản phẩm · sắp mua. Câu hoặc hình nào cho biết điều đó |
| 2 | **Hook 0–3 giây** | Loại hook: nhận diện bản thân ("con bạn có đang ngồi thế này?") · nỗi đau nhìn thấy được · kết quả · tò mò · trái ngược · giá hoặc ưu đãi · người thật. Khung đầu có gì: mặt người, sản phẩm, vấn đề, chữ. Câu nói đầu tiên là gì |
| 3 | **Lời hứa chính** | Người xem được gì, đo bằng gì, sau bao lâu. Một câu nguyên văn |
| 4 | **Cơ chế** | Sản phẩm làm được lời hứa bằng cách nào: tính năng nào, chứng minh ra sao. Cơ chế là thứ làm lời hứa đáng tin |
| 5 | **Bằng chứng** | Demo trực tiếp · thông số · chứng nhận · khách thật · chuyên gia · số lượng đã bán · so sánh trước và sau. Ghi nguyên văn kèm mốc giây |
| 6 | **Xử lý rào cản** | Ads trả lời những lo ngại nào: giá, chất lượng, độ bền, có vừa với người dùng không, lắp đặt, giao hàng, bảo hành, đổi trả. Liệt kê rào cản kèm câu trả lời trong ads |
| 7 | **Ưu đãi và lý do mua ngay** | Giảm giá, quà, combo, hạn chót, số lượng có hạn. Ưu đãi nằm ở chữ, ở hình hay ở lời nói |
| 8 | **Cấu trúc kịch bản** | Chia nhịp kèm mốc giây: Hook → Vấn đề → Giải pháp → Demo → Bằng chứng → Ưu đãi → CTA (bỏ nhịp không có, thêm nhịp lạ). Sản phẩm xuất hiện ở giây mấy, tên hãng ở giây mấy |
| 9 | **Tay nghề sản xuất** | Kiểu làm: người thật tự quay · studio · ảnh ghép chữ · hoạt hình. Có người nói thẳng vào máy không. Phụ đề, nhịp cắt (số cảnh mỗi 10 giây), nhạc hay giọng, khung 9:16, 1:1 hay 4:5 |
| 10 | **Đòn tâm lý và khớp phễu** | Chỉ ghi đòn **nhìn thấy được trong ads**: bằng chứng xã hội · uy tín chuyên gia · sợ mất · neo giá · khan hiếm · bản sắc ("bố mẹ hiện đại") · hình dung tương lai. CTA và link đích có khớp mức nhận biết ở lớp 1 không |

## 4. Kết luận "vì sao chạy tốt"

Viết 2–3 **giả thuyết**, mỗi giả thuyết một dòng:

| Giả thuyết | Ads thắng có | Đối chứng không có | Mức chắc |
|---|---|---|---|

Mức chắc:

- **cao**: khác biệt có ở ≥2 ads thắng và vắng ở ≥2 đối chứng cùng sản phẩm
- **vừa**: một cặp cùng sản phẩm, hoặc ≥2 cặp lệch sản phẩm
- **thấp**: chỉ quan sát ads thắng, không có đối chứng

Viết theo cách so sánh: "Ads được nhân bản 3 lần khác ads tắt sớm ở chỗ…". Ngân sách, tệp nhắm và mùa vụ có thể giải thích thay cho nội dung. Ghi rõ khi ads thắng cũng là ads ra đúng mùa cao điểm, hoặc là ads duy nhất của sản phẩm bán chạy nhất.

**Đối chiếu chéo giữa các đối thủ:** giả thuyết rút từ một đối thủ phải soát với đối thủ khác trước khi thành nguyên lý. Đối thủ khác thắng mà **không** có yếu tố đó, hoặc có yếu tố đó ở cả ads thắng lẫn đối chứng, thì yếu tố đó không phải lý do: tìm điểm chung rộng hơn. Ví dụ "người dẫn nói trong 5 giây đầu" bị bác khi hãng thứ hai thắng mà không có người dẫn; điểm chung thật là "người dùng sản phẩm xuất hiện sớm". Khi sửa giả thuyết của lần trước, ghi rõ trong báo cáo mới.

## 5. Công thức của đối thủ

Giải mã xong mọi ads thắng của một đối thủ thì gom điểm **lặp lại ở ≥2 ads thắng** thành **công thức** theo 6 ô: người xem · hook · lời hứa · bằng chứng · nhịp kịch bản · CTA. Công thức là "cách họ ra đơn". Điểm chỉ có ở một ads thì ghi là nét riêng, không đưa vào công thức. Có dưới 2 ads thắng thì ghi "chưa đủ ads thắng để thành công thức".

## 6. Chuyển thành việc cho mình

Mỗi giả thuyết mức vừa trở lên chuyển thành một dòng:

| Nguyên lý rút ra | Mình làm khác thế nào | Giả thuyết test |
|---|---|---|

- **Nguyên lý** là cơ chế, không phải nội dung. Ví dụ "hook là tư thế xấu nhìn thấy được trong 1 giây đầu", không phải "quay lại cảnh bé gù lưng giống họ".
- **Giả thuyết test phải thua được**: nêu chỉ số (tỉ lệ xem 3 giây, CTR, giá mỗi tin nhắn), so với ads nào, kỳ vọng tăng hay giảm.
- Áp luật nội dung trong hồ sơ: không chép chữ hay hình của đối thủ, không mượn claim mà mình chưa có căn cứ.

**Xong khi:** mọi ads thắng có đủ 10 lớp điền từ quan sát, mọi giả thuyết có cột đối chứng, và mỗi đối thủ có công thức hoặc dòng "chưa đủ ads thắng".
