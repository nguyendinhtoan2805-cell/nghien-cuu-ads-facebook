# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""CÀI SKILL SOI ADS ĐỐI THỦ vào Claude — 1 lệnh cài mọi skill trong thư mục này.

    uv run cai-dat-skill.py              chép từng skill vào ~/.claude/skills/<tên skill> (Mac và Windows; dùng cho máy nhân sự)
    uv run cai-dat-skill.py --lien-ket   tạo liên kết thay vì chép (máy người phát triển: sửa ở đây là Claude dùng ngay; Windows cần quyền)

Chạy lại lệnh này mỗi khi có bản skill mới: bản cũ trong ~/.claude/skills được thay bằng bản mới.
Sau khi cài: mở lại Claude để nhận skill.
"""
import os, shutil, sys
from pathlib import Path

GOC = Path(__file__).resolve().parent
DICH = Path.home() / ".claude" / "skills"
CU = []  # tên skill cũ cần gỡ khi cài bản mới (chưa có)
BO_QUA = shutil.ignore_patterns("node_modules", ".venv", "__pycache__", ".DS_Store")


def xoa(p):
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.exists():
        shutil.rmtree(p)


def main():
    lien_ket = "--lien-ket" in sys.argv
    skills = sorted(d for d in GOC.iterdir() if (d / "SKILL.md").exists())
    if not skills:
        sys.exit("Không thấy skill nào (thư mục con có SKILL.md) cạnh file này")
    DICH.mkdir(parents=True, exist_ok=True)
    for ten in CU:
        if (DICH / ten).exists() or (DICH / ten).is_symlink():
            xoa(DICH / ten); print(f"  gỡ skill cũ: {ten}")
    for s in skills:
        d = DICH / s.name
        xoa(d)
        if lien_ket:
            os.symlink(s, d, target_is_directory=True)
        else:
            shutil.copytree(s, d, ignore=BO_QUA)
        print(f"  {'liên kết' if lien_ket else 'chép'}: {s.name} → {d}")
    print(f"XONG — đã cài {len(skills)} skill. Mở lại Claude để nhận skill.")


if __name__ == "__main__":
    main()
