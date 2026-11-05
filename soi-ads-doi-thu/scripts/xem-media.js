// Xem video và ảnh ads ngay trong tab Thư viện quảng cáo Meta.
// Chạy SAU thu-thap.js và SAU KHI đã lưu bản chụp: các hàm dưới thay giao diện trang
// (window.__soiAds vẫn giữ). Muốn thu thập tiếp thì tải lại trang.
//
//   __xemLuoi([id, ...], {cot: 4, cao: 330})    → lưới video (hoặc ảnh) đầu của mỗi nhóm, mỗi ô ghi 6 số cuối ID
//   await __tua(giay | (d) => d * 0.5)          → tua mọi video trong lưới tới cùng một mốc, rồi chụp màn hình
//   await __daiKhung(id, {buoc: 2, cot: 6, rong: 160, ban: 0, tu: 0, den: 30})
//                                               → dải khung của một video: mỗi `buoc` giây một khung, ghi mốc giây.
//                                                 Dài hơn màn hình thì cuộn chuột thật rồi chụp tiếp (scrollTo không ăn).
//                                                 Muốn đọc chữ trên màn hình: một đoạn `tu`–`den`, ít cột, `rong` lớn
//   __xemAnh([id, ...], {cot: 3})               → mọi ảnh và thẻ carousel theo thứ tự
//   await __linkVideo([id, ...])                → [{id, url, mb}] để xin phép tải và ghi ra file cho boc-loi.py (link hết hạn sau vài ngày)
(() => {
  if (!window.__soiAdsChiTiet) return 'Chạy scripts/thu-thap.js trước';
  const ct = (ids) => window.__soiAdsChiTiet(ids);
  const videoCua = (b) => (b.video[0] && b.video[0].hd) || (b.the.find((t) => t.video) || {}).video || null;
  const anhCua = (b) => [...b.anh, ...b.the.map((t) => t.anh)].filter(Boolean);
  const dau = (nhom) => nhom.find((b) => videoCua(b)) || nhom[0];
  const nhan = (id) => '…' + String(id).slice(-6);
  const css = '<style>body{margin:0;background:#111;color:#eee;font:13px system-ui}.l{display:grid;gap:6px;padding:6px}'
    + '.o{position:relative;background:#000}.o b{position:absolute;left:4px;top:4px;background:#000c;padding:1px 5px;border-radius:3px;z-index:2}'
    + '.o video,.o img,.o canvas{width:100%;display:block;object-fit:contain}</style>';
  const dung = (html, cot) => {
    document.body.innerHTML = css + `<div class="l" style="grid-template-columns:repeat(${cot},1fr)">${html}</div>`;
    window.scrollTo(0, 0);
  };
  // Chờ một sự kiện của video, tối đa 8 giây (video lỗi thì không treo cả lượt).
  const cho = (v, ev) => new Promise((r) => {
    const t = setTimeout(r, 8000);
    v.addEventListener(ev, () => { clearTimeout(t); r(); }, { once: true });
  });

  window.__xemLuoi = (ids, { cot = 4, cao = 330 } = {}) => {
    const o = ct(ids).map((nhom) => {
      const b = dau(nhom);
      return { id: nhom[0].id, v: videoCua(b), anh: anhCua(b)[0], so_ban: nhom.length };
    });
    dung(o.map((x) => `<div class="o"><b>${nhan(x.id)}</b>${x.v
      ? `<video src="${x.v}" muted preload="auto" style="height:${cao}px"></video>`
      : `<img src="${x.anh || ''}" style="height:${cao}px">`}</div>`).join(''), cot);
    return o.map((x) => ({ id: x.id, loai: x.v ? 'video' : 'anh', so_ban: x.so_ban }));
  };

  window.__tua = async (t) => {
    const vs = [...document.querySelectorAll('.o video')];
    await Promise.all(vs.map(async (v) => {
      if (v.readyState < 1) await cho(v, 'loadedmetadata');
      const g = typeof t === 'function' ? t(v.duration) : t;
      v.currentTime = Math.max(0, Math.min(g, (v.duration || 0) - 0.1));
      await cho(v, 'seeked');
    }));
    return vs.map((v) => ({
      o: v.closest('.o').querySelector('b').textContent,
      giay: +v.currentTime.toFixed(1), dai: +(v.duration || 0).toFixed(1), khung: v.videoWidth + '×' + v.videoHeight,
    }));
  };

  // Một video, nhiều mốc: vẽ từng khung lên canvas (canvas bị "nhiễm" nguồn ngoài nhưng vẫn hiện để chụp).
  window.__daiKhung = async (id, { buoc = 2, cot = 6, rong = 160, ban = null, tu = 0.3, den = Infinity } = {}) => {
    const nhom = ct([id])[0];
    if (!nhom) return 'Không thấy nhóm ' + id;
    const b = ban === null ? dau(nhom) : nhom[ban];
    const src = b && videoCua(b);
    if (!src) return 'Bản này không có video';
    const v = document.createElement('video');
    v.src = src; v.muted = true; v.preload = 'auto';
    await cho(v, 'loadedmetadata');
    await cho(v, 'canplaythrough');
    const d = v.duration || 0, moc = [];
    const het = Math.min(d, den);
    for (let g = tu; g < het; g += buoc) moc.push(g);
    if (den >= d && moc.length && d - moc[moc.length - 1] > 0.8) moc.push(d - 0.3);
    const h = Math.round((rong * v.videoHeight) / (v.videoWidth || 1)) || rong;
    dung(moc.map((g, i) => `<div class="o"><b>${g.toFixed(1)}s</b><canvas id="k${i}" width="${rong}" height="${h}"></canvas></div>`).join(''), cot);
    // Video nằm ngoài trang thì trình duyệt ngừng giải mã giữa chừng và vẽ ra khung đen:
    // gắn vào trang (gần như vô hình), chờ dữ liệu về và chờ khung thật hiện ra rồi mới vẽ.
    v.style.cssText = 'position:fixed;right:0;bottom:0;width:4px;height:4px;opacity:.01;pointer-events:none';
    document.body.appendChild(v);
    const khungMoi = () => new Promise((r) => {
      const t = setTimeout(r, 1500);
      if (v.requestVideoFrameCallback) v.requestVideoFrameCallback(() => { clearTimeout(t); r(); });
      else requestAnimationFrame(() => requestAnimationFrame(() => { clearTimeout(t); r(); }));
    });
    let loi = [];
    for (let i = 0; i < moc.length; i++) {
      const doi = khungMoi();
      v.currentTime = moc[i];
      await cho(v, 'seeked');
      for (let k = 0; k < 40 && v.readyState < 2; k++) await new Promise((r) => setTimeout(r, 250));
      await doi;
      if (v.readyState < 2) loi.push(+moc[i].toFixed(1));
      document.getElementById('k' + i).getContext('2d').drawImage(v, 0, 0, rong, h);
    }
    return { id, ban: b.id, dai: +d.toFixed(1), khung: v.videoWidth + '×' + v.videoHeight, so_khung: moc.length, khung_loi: loi, cao_trang: document.body.scrollHeight };
  };

  window.__xemAnh = (ids, { cot = 3 } = {}) => {
    const o = ct(ids).flatMap((nhom) => anhCua(nhom[0]).map((a, i) => ({ id: nhom[0].id, i: i + 1, a })));
    dung(o.map((x) => `<div class="o"><b>${nhan(x.id)} · ${x.i}</b><img src="${x.a}"></div>`).join(''), cot);
    return o.length;
  };

  // Kèm dung lượng thật (HEAD) để nêu khi xin phép người dùng tải.
  window.__linkVideo = async (ids) => {
    const ds = ct(ids).map((nhom) => ({ id: nhom[0].id, url: videoCua(dau(nhom)) })).filter((x) => x.url);
    for (const x of ds) {
      try { x.mb = +((await fetch(x.url, { method: 'HEAD' })).headers.get('content-length') / 1e6).toFixed(1); } catch (e) { x.mb = null; }
    }
    return ds;
  };

  return ['__xemLuoi', '__tua', '__daiKhung', '__xemAnh', '__linkVideo'];
})();
