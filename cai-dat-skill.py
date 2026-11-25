# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""CÀI SKILL SOI ADS ĐỐI THỦ vào Claude — 1 lệnh cài mọi skill trong thư mục này.

    uv run cai-dat-skill.py              chép từng skill vào ~/.claude/skills/<tên skill> (Mac và Windows; dùng cho máy nhân sự)
    uv run cai-dat-skill.py --lien-ket   tạo liên kết thay vì chép (máy người phát triển: sửa ở đây là Claude dùng ngay; Windows cần quyền)
    uv run cai-dat-skill.py --codex      cài cho Codex (OpenAI) vào ~/.agents/skills thay vì Claude
    uv run cai-dat-skill.py --zip-chatgpt   tạo file soi-ads-doi-thu-skill.zip để tải lên ChatGPT (mục Skills)

Chạy lại lệnh này mỗi khi có bản skill mới: bản cũ trong ~/.claude/skills được thay bằng bản mới.
Sau khi cài: mở lại Claude để nhận skill.
"""
import os, shutil, sys
from pathlib import Path

GOC = Path(__file__).resolve().parent
DICH_CLAUDE = Path.home() / ".claude" / "skills"
DICH_CODEX = Path.home() / ".agents" / "skills"  # theo tài liệu Codex hiện hành (bản cũ dùng ~/.codex/skills)
CU = []  # tên skill cũ cần gỡ khi cài bản mới (chưa có)
BO_QUA = shutil.ignore_patterns("node_modules", ".venv", "__pycache__", ".DS_Store")


def xoa(p):
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.exists():
        shutil.rmtree(p)


def zip_chatgpt(skills):
    """Mỗi skill một file zip, gốc zip là thư mục skill (có SKILL.md) — dạng ChatGPT nhận khi tải skill lên."""
    import zipfile
    for s in skills:
        out = GOC / f"{s.name}-skill.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(s.rglob("*")):
                if f.is_file() and not any(p in ("__pycache__", "node_modules", ".venv") for p in f.parts) and f.name != ".DS_Store":
                    z.write(f, Path(s.name) / f.relative_to(s))
        print(f"  zip: {out}")
    print("XONG — tải file zip này lên ChatGPT (mục Skills).")


def main():
    lien_ket = "--lien-ket" in sys.argv
    skills = sorted(d for d in GOC.iterdir() if (d / "SKILL.md").exists())
    if not skills:
        sys.exit("Không thấy skill nào (thư mục con có SKILL.md) cạnh file này")
    if "--zip-chatgpt" in sys.argv:
        return zip_chatgpt(skills)
    DICH = DICH_CODEX if "--codex" in sys.argv else DICH_CLAUDE
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
    print(f"XONG — đã cài {len(skills)} skill vào {DICH}. Mở lại {'Codex' if DICH == DICH_CODEX else 'Claude'} để nhận skill.")


if __name__ == "__main__":
    main()
