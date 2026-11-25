# Ước lượng độ mạnh ads đối thủ

Thư viện không có chi tiêu. Độ mạnh được **suy từ hành vi chạy ads**, mỗi kết luận phải dẫn tín hiệu cụ thể. Gọi đúng tên: "tín hiệu đổ ngân sách mạnh", "dấu hiệu chạy duy trì", không viết "họ chi X triệu" hay "ads này hiệu quả".

## 1. Bảy tín hiệu

| # | Tín hiệu | Lấy từ | Đọc thế nào |
|---|---|---|---|
| 1 | **Thứ hạng hiển thị** | `hang` | Ads ở top 5 là ads Meta đang phân phối nhiều nhất của fanpage. Phân tích kỹ nhất nhóm này |
| 2 | **Quy mô** | số nhóm, tổng ads, số fanpage chạy song song | Nhiều nhóm và nhiều fanpage cho thấy ngân sách rộng, có thể chia theo tệp hoặc vùng |
| 3 | **Nhịp ra ads** | ads mới 7/30/90 ngày, biểu đồ theo tháng | Ra đều mỗi tuần nghĩa là có đội làm creative liên tục. Dồn một tháng rồi im là chạy theo mùa |
| 4 | **Độ bền** | `tuoi_ngay` (tính từ bản lên sớm nhất), ads >90 ngày | Người chạy ads hiếm khi giữ ads lỗ hàng tháng. Ads bền mà **còn ở top hạng** là tín hiệu thắng mạnh. Ads bền nhưng không có gì mới là chạy treo, không phải mạnh |
| 5 | **Nhân bản và test** | `so_ban`, `so_lan_len`, `lan_len_cuoi`, `ban_khac_chu` | Các bản trong một nhóm thường là **cùng nội dung lên lại** ở chiến dịch khác. Lên lại sau >14 ngày là **nhân bản ads thắng** sang chiến dịch hoặc tệp mới, tín hiệu dồn tiền mạnh nhất có được. Bản khác chữ là test thông điệp. Khác hình chỉ biết khi xem media: URL ảnh/video luôn khác nhau giữa các lần tải lên |
| 6 | **Độ phủ nền tảng** | `nen_tang` | Chỉ F hoặc FM thường là ads tin nhắn, ngân sách gọn. FIAM là phân phối rộng, thường đi với ngân sách lớn hơn hoặc Advantage+ |
| 7 | **Thay đổi giữa hai lần chụp** | `thong-ke.py` | Nhóm **chắc chắn** chỉ sống ≤14 ngày (tuổi lúc chụp trước + số ngày giữa hai lần chụp ≤14) là test rồi bỏ; hai lần chụp cách xa thì không biết nhóm tắt sớm hay muộn. Nhóm từng đứng top 3 mà nay tắt: tìm lý do (hết hàng, hết đợt sale, ads mỏi). Nhóm mới vào top hạng ngay là đang dồn tiền. Nhóm "mới" có ngày bắt đầu trước lần chụp trước là **ads cũ bật lại**; nhóm cũ tăng số bản là **thêm bản**. Hai việc này không làm tăng "ads mới 30 ngày" nhưng là đổ thêm tiền thật |

## 2. Ngưỡng khởi điểm

Đặt trong `scripts/thong-ke.py` (`NGUONG`). Đây là ngưỡng cho một thương hiệu SME tại Việt Nam, nên chỉnh sau 2–3 lần chụp khi đã thấy dải thật của ngành.

| Tín hiệu | Mạnh | Vừa | Nhẹ |
|---|---|---|---|
| Nhóm đang chạy | ≥30 | 10–29 | <10 |
| Ads mới 30 ngày | ≥10 | 3–9 | <3 |
| Lên ads 30 ngày (mới + nhân bản) | ≥10 | 3–9 | <3 |
| Tỉ lệ nhóm nhân bản ads cũ | ≥25% | 10–24% | <10% |
| Tỉ lệ ads >90 ngày | ≥30% | 10–29% | <10% |

So giữa các đối thủ **trong cùng một lần chụp** có giá trị hơn so với ngưỡng tuyệt đối.

## 3. Đọc tổ hợp tín hiệu

| Tổ hợp | Nhận định gợi ý |
|---|---|
| Nhiều nhóm · nhiều ads mới · test cao | Đang **mở rộng và đổ ngân sách**, tìm creative mới liên tục |
| Top hạng là ads được nhân bản lại · ít nội dung mới | **Dồn tiền vào vài ads thắng** và nhân sang chiến dịch mới. Đối thủ đã biết ads nào ra đơn |
| Ads bền chiếm đa số · 0 lên ads trong 30 ngày | **Chạy treo**: ads cũ tự chạy, không ai làm mới. Kiểm thêm fanpage khác của họ trước khi kết luận ngân sách thấp |
| Ít nhóm · ads cũ ở top hạng · gần như không có ads mới | **Tập trung tiền vào vài ads thắng**, duy trì |
| Ít nhóm · ads cũ · hạng thấp · không có ads mới | Ngân sách thấp hoặc đang ngưng ngành hàng này |
| Nhiều nhóm chắc chắn tắt sau ≤14 ngày | Test nhiều nhưng **chưa tìm ra ads thắng** |
| Ads mới đồng loạt cùng một góc nội dung | Đang **đổi hướng thông điệp**, đáng theo dõi kỹ ở lần chụp sau |
| Nhịp tăng vọt trước một mốc (mùa tựu trường, Tết, ngày sale) | Chạy theo mùa vụ. Đối chiếu lịch mùa vụ của dự án |
| Bật lại hàng loạt ads cũ · thêm bản cho ads thắng · không có nội dung mới | **Tăng tốc bằng hàng đã thắng** trước một mốc bán. Chụp lại sau mốc để xem họ tắt gì, giữ gì |

Mọi nhận định ghi kèm **mức chắc chắn** (cao, vừa, thấp) và tín hiệu nào dẫn tới nó.

Từ độ mạnh của cả hãng xuống từng ads: vai **thắng / đối chứng** của mỗi nhóm ở [`giai-ma-ads-thang.md`](giai-ma-ads-thang.md) mục 1.
