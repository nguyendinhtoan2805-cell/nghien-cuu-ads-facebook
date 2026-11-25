#!/usr/bin/env python3
"""Thống kê và so sánh bản chụp ads đối thủ.

Cách chạy:
    python3 -I thong-ke.py <thư mục dữ liệu> [--ngay YYYY-MM-DD] [--loc "regex"]

Thư mục dữ liệu chứa các file bản chụp tên `YYYY-MM-DD-<doi-thu>.json`:
    {"doi_thu": "...", "ngay_chup": "YYYY-MM-DD",
     "nguon": [{"page_id": "...", "page": "...", "url": "...", "tong_theo_meta": 25}],
     "ads": [<các dòng từ __soiAdsDong()>]}

Lấy bản mới nhất của mỗi đối thủ (hoặc bản đúng --ngay) làm hiện tại, bản liền trước làm mốc so.
--loc: chỉ giữ ads có chữ khớp regex (không phân biệt hoa thường), dùng khi fanpage bán nhiều ngành.
In ra Markdown để dán vào báo cáo.
"""
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

# Ngưỡng khởi điểm để gắn mức (xem references/do-manh.md). Chỉnh sau vài lần chụp.
NGUONG = {
    "nhom_dang_chay": (30, 10),   # >= mạnh, >= vừa, còn lại nhẹ
    "moi_30_ngay": (10, 3),
    "ti_le_nhan_ban": (0.25, 0.1),   # nhóm đã lên lại cùng nội dung cách lần đầu >14 ngày
    "ti_le_ben_90": (0.3, 0.1),
}
NEN_TANG = {"F": "Facebook", "I": "Instagram", "M": "Messenger", "A": "Audience Network", "T": "Threads"}


def muc(gia_tri, khoa):
    cao, vua = NGUONG[khoa]
    return "Mạnh" if gia_tri >= cao else "Vừa" if gia_tri >= vua else "Nhẹ"


def doc(thu_muc, loc):
    theo_dt = defaultdict(list)
    for f in sorted(Path(thu_muc).glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # file hỏng thì báo, không dừng
            print(f"> ⚠️ Bỏ qua {f.name}: {e}\n")
            continue
        if loc:
            r = re.compile(loc, re.I)
            d["ads"] = [a for a in d.get("ads", []) if r.search(a.get("chu") or "")]
        theo_dt[d["doi_thu"]].append(d)
    for dt, ds in theo_dt.items():
        theo_dt[dt] = gop_cung_ngay(ds)
    return theo_dt


def gop_cung_ngay(ds):
    """Gộp các file cùng đối thủ, cùng ngày chụp thành một bản (chạy tay: mỗi fanpage một file).
    Dòng ads khoá theo (nguồn, id): cùng nhóm ở hai fanpage thì giữ cả hai vì hạng tính riêng; tải trùng file thì không nhân đôi."""
    gop = {}
    for d in ds:
        g = gop.setdefault(d["ngay_chup"], {**d, "nguon": [], "ads": [], "_khoa_ads": set(), "_khoa_nguon": set()})
        for n in d.get("nguon", []):
            k = n.get("page_id") or n.get("url") or n.get("page")
            if k not in g["_khoa_nguon"]:
                g["_khoa_nguon"].add(k); g["nguon"].append(n)
        for a in d.get("ads", []):
            k = (a.get("nguon"), a.get("id"))
            if k not in g["_khoa_ads"]:
                g["_khoa_ads"].add(k); g["ads"].append(a)
    for g in gop.values():
        del g["_khoa_ads"], g["_khoa_nguon"]
    return [gop[k] for k in sorted(gop)]


def khoa(a):
    return a.get("nhom_id") or a["id"]


def tinh(ban, ngay_chup):
    ads = ban["ads"]
    n = len(ads)
    hom = date.fromisoformat(ngay_chup)
    tuoi = [a["tuoi_ngay"] for a in ads if a.get("tuoi_ngay") is not None]
    bd = [date.fromisoformat(a["bat_dau"]) for a in ads if a.get("bat_dau")]
    moi = lambda k: sum(1 for x in bd if (hom - x).days <= k)
    test_chu = sum(1 for a in ads if (a.get("ban_khac_chu") or 1) >= 2)
    # Nhân bản: cùng nội dung được lên lại sau >14 ngày (thường là đẩy ads thắng sang chiến dịch/tệp mới).
    nhan_ban = [a for a in ads if la_nhan_ban(a)]
    nhan_ban_30 = [a for a in nhan_ban if (hom - ngay_(a, "lan_len_cuoi")).days <= 30]
    hoat_dong_30 = sum(1 for a in ads if any(ngay_(a, k) and (hom - ngay_(a, k)).days <= 30 for k in ("bat_dau", "lan_len_cuoi")))
    ben = sum(1 for t in tuoi if t > 90)
    return {
        "n": n,
        "tong_ads": sum(a.get("so_ban") or 1 for a in ads),
        "pages": Counter(a["page"] for a in ads),
        "follow": {a["page"]: a.get("follow") for a in ads},
        "dinh_dang": Counter(a.get("dinh_dang") for a in ads),
        "nen_tang": Counter(c for a in ads for c in (a.get("nen_tang") or "")),
        "cta": Counter(a.get("cta") for a in ads),
        "link": Counter(a.get("link") for a in ads if a.get("link")),
        "moi7": moi(7), "moi30": moi(30), "moi90": moi(90),
        "trung_vi_tuoi": statistics.median(tuoi) if tuoi else None,
        "tuoi_nhom": Counter(
            "≤7 ngày" if t <= 7 else "8–30" if t <= 30 else "31–90" if t <= 90 else "91–365" if t <= 365 else ">365"
            for t in tuoi),
        "thang": Counter(x.strftime("%Y-%m") for x in bd if (hom - x).days <= 183),
        "test_chu": test_chu, "ben": ben,
        "nhan_ban": len(nhan_ban), "nhan_ban_30": len(nhan_ban_30), "hoat_dong_30": hoat_dong_30,
        "ti_le_nhan_ban": len(nhan_ban) / n if n else 0,
        "ti_le_ben": ben / n if n else 0,
    }


def ngay_(a, k):
    return date.fromisoformat(a[k]) if a.get(k) else None


def la_nhan_ban(a):
    bd, cuoi = ngay_(a, "bat_dau"), ngay_(a, "lan_len_cuoi")
    return bool(bd and cuoi and (cuoi - bd).days > 14)


TUOI_DOI_CHUNG = 14  # ngày tối thiểu để một ads hạng thấp được làm đối chứng


def vai(a, so_nhom_trang, hom, treo=False):
    """Vai của một nhóm ads: (vai, lý do) hoặc (None, None). Luật: references/giai-ma-ads-thang.md mục 1.
    treo=True khi đối thủ không lên ads nào trong 30 ngày: ads bền khi đó có thể chỉ là ads bị bỏ quên."""
    hang = a.get("hang") or 999
    bd = ngay_(a, "bat_dau")
    tuoi = a.get("tuoi_ngay") or 0
    nb = la_nhan_ban(a)
    if so_nhom_trang < 3:  # fanpage quá ít nhóm: đứng đầu không nói lên gì
        return None, None
    # Ngưỡng hạng co theo số nhóm của fanpage: trang 9 nhóm thì "top 10" là cả trang.
    tren = lambda k, chia: max(1, min(k, so_nhom_trang // chia))
    if nb and hang <= tren(5, 2):
        return "Thắng rõ", f"nhân bản ({a.get('so_lan_len') or '?'} lần lên) + hạng {hang}/{so_nhom_trang}"
    if tuoi > 60 and hang <= tren(10, 3):
        if treo:
            return "Thắng (yếu)", f"bền {tuoi} ngày + hạng {hang}/{so_nhom_trang}, nhưng đối thủ đang chạy treo"
        return "Thắng", f"bền {tuoi} ngày + hạng {hang}/{so_nhom_trang}"
    if nb and hang <= tren(15, 1):
        return "Thắng", f"nhân bản + hạng {hang}/{so_nhom_trang}"
    if bd and (hom - bd).days <= 30 and hang <= tren(3, 3):
        return "Thắng", f"mới {(hom - bd).days} ngày đã hạng {hang}/{so_nhom_trang}"
    # Đối chứng phải chạy đủ lâu để có cơ hội leo hạng: ads vài ngày tuổi đứng cuối chưa chắc là yếu (bài học lần chụp 06/11/2026).
    if hang > so_nhom_trang / 2 and (a.get("so_lan_len") or 1) <= 1 and not nb and tuoi >= TUOI_DOI_CHUNG:
        return "Đối chứng", f"hạng {hang}/{so_nhom_trang}, lên 1 lần, {tuoi} ngày"
    return None, None


THU_TU_VAI = ["Thắng rõ", "Thắng", "Thắng (yếu)", "Đối chứng (đã tắt)", "Đối chứng"]


def bang(counter, ten=None, tong=None):
    tong = tong or sum(counter.values()) or 1
    return " · ".join(f"{(ten or {}).get(k, k)} {v} ({round(v * 100 / tong)}%)" for k, v in counter.most_common())


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    thu_muc, ngay, loc = args[0], None, None
    if "--ngay" in args:
        ngay = args[args.index("--ngay") + 1]
    if "--loc" in args:
        loc = args[args.index("--loc") + 1]
    du_lieu = doc(thu_muc, loc)
    if not du_lieu:
        print("Không có bản chụp nào trong thư mục.")
        sys.exit(1)

    tong_hop = []
    print(f"# Thống kê ads đối thủ{' (lọc: ' + loc + ')' if loc else ''}\n")
    for dt, ds in du_lieu.items():
        if ngay:
            ds = [d for d in ds if d["ngay_chup"] <= ngay]
            if not ds:
                continue
        hien, truoc = ds[-1], (ds[-2] if len(ds) > 1 else None)
        s = tinh(hien, hien["ngay_chup"])
        tong_hop.append((dt, hien["ngay_chup"], s))
        s["bien_dong"] = None
        print(f"## {dt} · chụp {hien['ngay_chup']}\n")
        print(f"- **Đang chạy:** {s['n']} nhóm nội dung · {s['tong_ads']} ads (tính cả bản biến thể)")
        for p, c in s["pages"].most_common():
            f = s["follow"].get(p)
            print(f"  - {p}: {c} nhóm · {f:,} follow" if f else f"  - {p}: {c} nhóm")
        print(f"- **Định dạng:** {bang(s['dinh_dang'])}")
        print(f"- **Nền tảng** (một ads có thể chạy nhiều nơi): " + " · ".join(f"{NEN_TANG.get(k, k)} {v}/{s['n']}" for k, v in s["nen_tang"].most_common()))
        print(f"- **CTA:** {bang(s['cta'])}")
        if s["link"]:
            print(f"- **Link đích:** {bang(s['link'])}")
        print(f"- **Ads mới:** 7 ngày {s['moi7']} · 30 ngày {s['moi30']} · 90 ngày {s['moi90']}")
        print(f"- **Tuổi ads:** trung vị {s['trung_vi_tuoi']:.0f} ngày · " + " · ".join(f"{k} {v}" for k, v in sorted(s['tuoi_nhom'].items(), key=lambda x: ['≤7 ngày', '8–30', '31–90', '91–365', '>365'].index(x[0]))) if s["trung_vi_tuoi"] is not None else "- **Tuổi ads:** không có dữ liệu")
        y, m = map(int, hien["ngay_chup"][:7].split("-"))
        thang6 = [f"{(y * 12 + m - 1 - i) // 12}-{(y * 12 + m - 1 - i) % 12 + 1:02d}" for i in range(5, -1, -1)]
        print(f"- **Nhịp ra ads (6 tháng, chỉ tính ads còn chạy):** " + " · ".join(f"{k[2:]}: {s['thang'].get(k, 0)}" for k in thang6))
        print(f"- **Lên ads trong 30 ngày** (mới + nhân bản lại): {s['hoat_dong_30']} nhóm")
        print(f"- **Nhân bản ads cũ** (lên lại cùng nội dung sau >14 ngày): {s['nhan_ban']}/{s['n']} nhóm ({s['ti_le_nhan_ban']:.0%}), {s['nhan_ban_30']} nhóm nhân bản trong 30 ngày qua")
        print(f"- **Test chữ** (các bản trong nhóm khác chữ): {s['test_chu']}/{s['n']} nhóm · khác hình chỉ biết khi xem media")
        print(f"- **Ads bền (>90 ngày):** {s['ben']}/{s['n']} ({s['ti_le_ben']:.0%})\n")

        print("**Top 10 theo lượt hiển thị** (thứ hạng Meta xếp trong từng fanpage):\n")
        print("| Hạng | Fanpage | Bắt đầu | Lên lại gần nhất | Tuổi | Bản | Định dạng | Nền tảng | Chữ mở đầu |")
        print("|---|---|---|---|---|---|---|---|---|")
        for a in sorted(hien["ads"], key=lambda x: x.get("hang", 999))[:10]:
            chu = (a.get("chu") or "").replace("|", "/")[:70]
            print(f"| {a.get('hang')} | {a['page'][:28]} | {a.get('bat_dau')} | {a.get('lan_len_cuoi') if a.get('lan_len_cuoi') != a.get('bat_dau') else '–'} | {a.get('tuoi_ngay')} | {a.get('so_ban')} | {a.get('dinh_dang')} | {a.get('nen_tang')} | {chu} |")
        print()

        ra = []
        if truoc:
            cu = {khoa(a): a for a in truoc["ads"]}
            moi_ = {khoa(a): a for a in hien["ads"]}
            ra = [cu[k] for k in cu if k not in moi_]

        # Ads thắng và đối chứng: đầu vào cho bước giải mã "vì sao chạy tốt".
        hom = date.fromisoformat(hien["ngay_chup"])
        so_trang = Counter(a.get("nguon") or a["page"] for a in hien["ads"])
        treo = s["hoat_dong_30"] == 0
        dong = []
        for a in hien["ads"]:
            v, ly_do = vai(a, so_trang[a.get("nguon") or a["page"]], hom, treo)
            if v:
                dong.append((v, ly_do, a))
        for a in ra:
            if (a.get("tuoi_ngay") or 0) <= 14:
                dong.append(("Đối chứng (đã tắt)", f"tắt sau ≤{a.get('tuoi_ngay')} ngày", a))
        dong.sort(key=lambda x: (THU_TU_VAI.index(x[0]), x[2].get("hang") or 999))

        # Cụm cùng chữ: một nội dung có thể được tải lên thành nhiều nhóm (chiến dịch, tệp khác nhau).
        # Cùng chữ thường là cùng video, nhưng phải xem media để chắc. Hạng chênh trong cụm là do ngân sách/tệp, không do nội dung.
        cum = defaultdict(list)
        for a in hien["ads"]:
            chu = re.sub(r"\s+", " ", (a.get("chu") or "")).strip().lower()
            if chu:
                cum[(chu[:120], a.get("dinh_dang"))].append(a)
        cum = [v for v in cum.values() if len(v) >= 2]
        if cum:
            print("**Cụm cùng chữ ở nhiều nhóm** (coi như một nội dung khi xét thắng; không ghép làm đối chứng của nhau):\n")
            print("| Số nhóm | Tổng bản | Các hạng | Định dạng | Chữ mở đầu |")
            print("|---|---|---|---|---|")
            for v in sorted(cum, key=lambda x: min(a.get("hang") or 999 for a in x)):
                hang = ", ".join(str(a.get("hang")) for a in sorted(v, key=lambda a: a.get("hang") or 999))
                print(f"| {len(v)} | {sum(a.get('so_ban') or 1 for a in v)} | {hang} | {v[0].get('dinh_dang')} | {(v[0].get('chu') or '').replace('|', '/')[:60]} |")
            print()
        id_cum = {a["id"]: len(v) for v in cum for a in v}
        dong = [(v, ly + (f", cùng chữ với {id_cum[a['id']] - 1} nhóm khác" if a["id"] in id_cum else ""), a)
                for v, ly, a in dong if not (v == "Đối chứng" and a["id"] in id_cum)]
        dem = Counter(v for v, _, _ in dong)
        print("**Ads thắng và đối chứng** (luật ở references/giai-ma-ads-thang.md mục 1; ghép cặp cùng sản phẩm khi giải mã):\n")
        if not dong:
            print("- Không có nhóm nào đạt luật.\n")
        else:
            print(" · ".join(f"{k} {dem[k]}" for k in THU_TU_VAI if dem.get(k)) + "\n")
            print("| Vai | Hạng | Fanpage | Lý do | ID | Định dạng | Chữ mở đầu |")
            print("|---|---|---|---|---|---|---|")
            da_in = Counter()
            for v, ly_do, a in dong:
                if v.startswith("Đối chứng") and da_in[v] >= 8:
                    continue
                da_in[v] += 1
                chu = (a.get("chu") or "").replace("|", "/")[:60]
                print(f"| {v} | {a.get('hang')} | {a['page'][:24]} | {ly_do} | `{a['id']}` | {a.get('dinh_dang')} | {chu} |")
            if s["n"] < 6:
                print("\n> Dưới 6 nhóm: không đủ đối chứng, chỉ ghi đặc điểm ads thắng.")
            print()

        if truoc:
            vao = [moi_[k] for k in moi_ if k not in cu]
            them_ban = [(cu[k], moi_[k]) for k in moi_ if k in cu and (moi_[k].get("so_ban") or 1) > (cu[k].get("so_ban") or 1)]
            # Nhóm "mới" mà bắt đầu trước lần chụp trước = ads cũ được bật lại, không phải nội dung mới.
            bat_lai = [a for a in vao if a.get("bat_dau") and a["bat_dau"] < truoc["ngay_chup"]]
            moi_tinh = [a for a in vao if a not in bat_lai]
            print(f"**So với bản {truoc['ngay_chup']}:** +{len(moi_tinh)} nhóm mới tinh · +{len(bat_lai)} nhóm cũ bật lại · −{len(ra)} nhóm đã tắt · {len(them_ban)} nhóm thêm bản\n")
            if bat_lai:
                print(f"- Bật lại: {len(bat_lai)} nhóm ads cũ quay lại danh sách đang chạy (bắt đầu từ {min(a['bat_dau'] for a in bat_lai)}). Bật lại hàng loạt trước một mốc sale là dấu hiệu tăng tốc")
                for a in sorted(bat_lai, key=lambda x: x.get("hang", 999))[:8]:
                    print(f"  - hạng {a.get('hang')} · `{a['id']}` · bắt đầu {a.get('bat_dau')} · {(a.get('chu') or '')[:60]}")
            if them_ban:
                print(f"- Thêm bản: " + " · ".join(f"`{m['id']}` {c.get('so_ban') or 1}→{m.get('so_ban') or 1}" for c, m in sorted(them_ban, key=lambda x: x[1].get("hang", 999))[:8]))
            vao = moi_tinh
            s["bien_dong"] = (len(moi_tinh), len(bat_lai), len(them_ban), truoc["ngay_chup"])
            if ra:
                ngan = [a for a in ra if (a.get("tuoi_ngay") or 0) <= 14]
                print(f"- Đã tắt: {len(ra)} nhóm, trong đó {len(ngan)} nhóm sống ≤14 ngày lúc chụp trước (dấu hiệu test rồi bỏ)")
                for a in ra[:8]:
                    print(f"  - `{a['id']}` · {a.get('bat_dau')} · {(a.get('chu') or '')[:60]}")
            if vao:
                print(f"- Mới: {len(vao)} nhóm")
                for a in sorted(vao, key=lambda x: x.get("hang", 999))[:8]:
                    print(f"  - hạng {a.get('hang')} · `{a['id']}` · {a.get('dinh_dang')} · {(a.get('chu') or '')[:60]}")
            print()

    if len(tong_hop) > 1:
        print("## Bảng so độ mạnh giữa các đối thủ\n")
        print("*Mức Mạnh/Vừa/Nhẹ theo ngưỡng khởi điểm ở references/do-manh.md. Đây là ước lượng tương đối, không phải số tiền.*\n")
        print("| Đối thủ | Nhóm đang chạy | Nội dung mới 30 ngày | Lên ads 30 ngày | Nhân bản ads cũ | Ads bền >90 ngày | Video | Từ lần chụp trước: mới · bật lại · thêm bản |")
        print("|---|---|---|---|---|---|---|---|")
        for dt, ng, s in tong_hop:
            vid = s["dinh_dang"].get("VIDEO", 0)
            bd = "{} · {} · {} (từ {})".format(*s["bien_dong"]) if s.get("bien_dong") else "chưa có lần trước"
            print(f"| {dt} | {s['n']} · {muc(s['n'], 'nhom_dang_chay')} | {s['moi30']} · {muc(s['moi30'], 'moi_30_ngay')} | {s['hoat_dong_30']} · {muc(s['hoat_dong_30'], 'moi_30_ngay')} | {s['ti_le_nhan_ban']:.0%} · {muc(s['ti_le_nhan_ban'], 'ti_le_nhan_ban')} | {s['ti_le_ben']:.0%} · {muc(s['ti_le_ben'], 'ti_le_ben_90')} | {round(vid * 100 / (s['n'] or 1))}% | {bd} |")
        print()


if __name__ == "__main__":
    main()
