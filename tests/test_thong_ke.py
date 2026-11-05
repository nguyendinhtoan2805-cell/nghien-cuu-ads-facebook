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

    def test_nhom_tat_som_thanh_doi_chung(self):
        self.assertIn("Đối chứng (đã tắt)", self.out)
        self.assertIn("`199`", self.out)

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


if __name__ == "__main__":
    unittest.main()
