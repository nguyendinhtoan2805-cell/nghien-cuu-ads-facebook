"""Bài kiểm cho scripts/thong-ke.py. Chạy: python3 -I -m unittest discover -s tests (ở thư mục gốc bộ skill)."""
import importlib.util
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SCRIPT = GOC / "soi-ads-doi-thu" / "scripts" / "thong-ke.py"
MAU = Path(__file__).resolve().parent / "mau"
spec = importlib.util.spec_from_file_location("thong_ke", SCRIPT)
tk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tk)
HOM = date(2026, 1, 31)


def ads(**k):
    a = {"hang": 1, "bat_dau": "2025-09-01", "lan_len_cuoi": "2025-09-01", "tuoi_ngay": 152, "so_lan_len": 1}
    a.update(k)
    return a


class Vai(unittest.TestCase):
    def test_nhan_ban_dung_dau_la_thang_ro(self):
        v, _ = tk.vai(ads(lan_len_cuoi="2026-01-20", so_lan_len=3), 10, HOM)
        self.assertEqual(v, "Thắng rõ")

    def test_len_lai_trong_14_ngay_khong_tinh_nhan_ban(self):
        self.assertFalse(tk.la_nhan_ban(ads(lan_len_cuoi="2025-09-10")))

    def test_ben_hang_cao_la_thang(self):
        self.assertEqual(tk.vai(ads(hang=2), 10, HOM)[0], "Thắng")

    def test_chay_treo_ha_xuong_thang_yeu(self):
        self.assertEqual(tk.vai(ads(hang=2), 10, HOM, treo=True)[0], "Thắng (yếu)")

    def test_nguong_hang_co_theo_co_fanpage(self):
        # Trang 9 nhóm: "top 10" co lại thành top 3, hạng 5 không còn là thắng.
        self.assertNotIn(tk.vai(ads(hang=5), 9, HOM)[0], ("Thắng", "Thắng rõ"))
        self.assertEqual(tk.vai(ads(hang=3), 9, HOM)[0], "Thắng")

    def test_fanpage_qua_it_nhom_khong_xet(self):
        self.assertEqual(tk.vai(ads(hang=1, lan_len_cuoi="2026-01-20"), 2, HOM), (None, None))

    def test_moi_vao_top(self):
        self.assertEqual(tk.vai(ads(hang=1, bat_dau="2026-01-25", lan_len_cuoi="2026-01-25", tuoi_ngay=6), 9, HOM)[0], "Thắng")

    def test_nua_duoi_len_mot_lan_la_doi_chung(self):
        self.assertEqual(tk.vai(ads(hang=8, bat_dau="2026-01-10", lan_len_cuoi="2026-01-10", tuoi_ngay=21), 10, HOM)[0], "Đối chứng")

    def test_doi_chung_qua_non_khong_tinh(self):
        # Ads mới lên vài ngày chưa kịp leo hạng: đứng cuối bảng không có nghĩa là yếu.
        self.assertEqual(tk.vai(ads(hang=8, bat_dau="2026-01-25", lan_len_cuoi="2026-01-25", tuoi_ngay=6), 10, HOM), (None, None))
        self.assertEqual(tk.vai(ads(hang=8, bat_dau="2026-01-17", lan_len_cuoi="2026-01-17", tuoi_ngay=14), 10, HOM)[0], "Đối chứng")


class ChayCaScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(MAU)], capture_output=True, text=True, encoding="utf-8")
        cls.out, cls.loi = r.stdout, r.returncode

    def test_chay_khong_loi(self):
        self.assertEqual(self.loi, 0, self.out)

    def test_co_muc_ads_thang(self):
        self.assertIn("**Ads thắng và đối chứng**", self.out)
        self.assertIn("| Thắng rõ | 1 |", self.out)

    def test_tat_giua_hai_lan_chup_xa_khong_lam_doi_chung(self):
        # 199 mới 7 ngày tuổi ở lần chụp 01/01, nhưng hai lần chụp cách 30 ngày:
        # có thể nó đã chạy tới 37 ngày rồi mới tắt, nên không biết là "test rồi bỏ".
        bang_vai = self.out.split("**Ads thắng và đối chứng**")[1].split("**So với")[0]
        self.assertNotIn("`199`", bang_vai)

    def test_so_lan_truoc(self):
        self.assertIn("**So với bản 2026-01-01:**", self.out)

    def test_tach_bat_lai_voi_moi_tinh(self):
        # 102 và 201 bắt đầu trước lần chụp trước: là ads cũ bật lại, không phải nội dung mới.
        self.assertIn("+6 nhóm mới tinh · +2 nhóm cũ bật lại", self.out)
        self.assertIn("1 nhóm thêm bản", self.out)

    def test_cum_cung_chu_khong_lam_doi_chung(self):
        # 105 và 108 cùng chữ "Ads yeu 1": là một nội dung, không được ghép làm đối chứng.
        self.assertIn("**Cụm cùng chữ ở nhiều nhóm**", self.out)
        bang_vai = self.out.split("**Ads thắng và đối chứng**")[1].split("**So với")[0]
        self.assertNotIn("`105`", bang_vai)
        self.assertNotIn("`108`", bang_vai)
        self.assertIn("`106`", bang_vai)

    def test_trang_it_nhom_khong_co_vai(self):
        self.assertNotIn("`201`", self.out.split("**Ads thắng và đối chứng**")[1].split("**So với")[0])


class TatSom(unittest.TestCase):
    """Nhóm biến mất giữa hai lần chụp: chỉ chắc là 'tắt sớm' khi tuổi lúc chụp trước + khoảng cách hai lần chụp ≤ 14 ngày."""

    def test_hai_lan_chup_gan(self):
        self.assertTrue(tk.tat_som(ads(tuoi_ngay=5), date(2026, 1, 24), HOM))

    def test_hai_lan_chup_xa(self):
        self.assertFalse(tk.tat_som(ads(tuoi_ngay=5), date(2026, 1, 1), HOM))

    def test_chay_va_in(self):
        import json, tempfile
        d = Path(tempfile.mkdtemp())
        dong = lambda i, hang, tuoi, bd: {**ads(id=i, nhom_id="n" + i, hang=hang, tuoi_ngay=tuoi, bat_dau=bd, lan_len_cuoi=bd),
                                          "nguon": "page:1", "page": "P", "page_id": "1", "chu": "chu " + i}
        ban = lambda ngay, ds: {"doi_thu": "Hang D", "ngay_chup": ngay, "nguon": [{"page_id": "1", "page": "P", "url": "", "tong_theo_meta": len(ds)}], "ads": ds}
        truoc = [dong("1", 1, 3, "2026-01-21"), dong("2", 2, 40, "2025-12-15"), dong("3", 3, 200, "2025-07-08"), dong("4", 4, 200, "2025-07-08")]
        (d / "2026-01-24-hang-d.json").write_text(json.dumps(ban("2026-01-24", truoc)), encoding="utf-8")
        (d / "2026-01-31-hang-d.json").write_text(json.dumps(ban("2026-01-31", [dong("4", 1, 207, "2025-07-08")])), encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(SCRIPT), str(d)], capture_output=True, text=True, encoding="utf-8").stdout
        bang_vai = out.split("**Ads thắng và đối chứng**")[1].split("**So với")[0]
        self.assertIn("`1`", bang_vai)        # 3 ngày + 7 ngày giữa hai lần chụp: chắc chắn tắt sớm
        self.assertNotIn("`2`", bang_vai)     # 40 ngày: không phải đối chứng
        self.assertIn("Từng đứng top 3 lần trước, nay đã tắt", out)
        self.assertIn("`3`", out.split("Từng đứng top 3 lần trước, nay đã tắt")[1])


class GopFileCungNgay(unittest.TestCase):
    """Chạy tay: mỗi fanpage tải một file. Cùng đối thủ, cùng ngày phải gộp thành MỘT bản chụp."""

    def test_gop_hai_fanpage(self):
        import json, tempfile
        d = Path(tempfile.mkdtemp())
        mot = lambda pid, ids: {"doi_thu": "Hang B", "ngay_chup": "2026-02-01",
                                "nguon": [{"page_id": pid, "page": "Trang " + pid, "url": "", "tong_theo_meta": len(ids)}],
                                "ads": [{**ads(id=str(i), nhom_id="n" + str(i), hang=k + 1), "nguon": "page:" + pid,
                                         "page": "Trang " + pid, "page_id": pid} for k, i in enumerate(ids)]}
        (d / "2026-02-01-hang-b.json").write_text(json.dumps(mot("1", [1, 2, 3])), encoding="utf-8")
        (d / "2026-02-01-hang-b (1).json").write_text(json.dumps(mot("2", [4, 5, 3])), encoding="utf-8")
        ban = tk.doc(str(d), None)["Hang B"]
        self.assertEqual(len(ban), 1)
        self.assertEqual(len(ban[0]["nguon"]), 2)
        # nhóm 3 xuất hiện ở cả 2 trang: giữ cả 2 dòng vì hạng tính riêng từng trang
        self.assertEqual(sorted(a["id"] for a in ban[0]["ads"]), ["1", "2", "3", "3", "4", "5"])

    def test_tai_trung_file_khong_nhan_doi(self):
        import json, tempfile
        d = Path(tempfile.mkdtemp())
        b = {"doi_thu": "Hang C", "ngay_chup": "2026-02-01", "nguon": [{"page_id": "9", "page": "P", "url": "", "tong_theo_meta": 1}],
             "ads": [{**ads(id="7"), "nguon": "page:9", "page": "P", "page_id": "9"}]}
        for ten in ("2026-02-01-hang-c.json", "2026-02-01-hang-c (1).json"):
            (d / ten).write_text(json.dumps(b), encoding="utf-8")
        ban = tk.doc(str(d), None)["Hang C"]
        self.assertEqual((len(ban), len(ban[0]["ads"]), len(ban[0]["nguon"])), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()
