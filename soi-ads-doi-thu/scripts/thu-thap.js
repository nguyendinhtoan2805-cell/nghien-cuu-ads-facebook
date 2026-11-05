// Thu thập ads từ Thư viện quảng cáo Meta (facebook.com/ads/library).
// Dán TOÀN BỘ file này vào javascript_tool trên một trang Thư viện vừa tải xong, TRƯỚC KHI cuộn.
// Chạy lại không sao: dữ liệu đã lấy được giữ nguyên tới khi tải lại trang.
//
// Hàm có sẵn sau khi chạy:
//   await __soiAdsThem(url)        → lấy trang đầu (≤30 nhóm) của URL khác mà không chuyển trang
//   __soiAdsTomTat()               → tiến độ theo từng nguồn: tổng Meta ghi, đã lấy, còn trang sau không
//   __soiAdsDong(tu, so)           → mảng dòng gọn để lưu bản chụp (mọi nguồn, hạng tính riêng từng nguồn)
//   __soiAdsChiTiet([id, ...])     → chữ đầy đủ mọi bản + link video/ảnh/thẻ
// Nguồn nào `con_trang_sau: true` thì mở chính URL đó, chạy lại file này và cuộn chuột thật.
(async () => {
  const S = (window.__soiAds = window.__soiAds || { nhom: [], daThay: {}, nguon: {}, hook: false });

  const nguonCua = (u) => { const m = String(u).match(/view_all_page_id=(\d+)/); if (m) return 'page:' + m[1]; const q = String(u).match(/[?&]q=([^&]+)/); return q ? 'q:' + decodeURIComponent(q[1]) : 'khac'; };

  function khop(t, i) {
    let d = 0;
    for (; i < t.length; i++) {
      const c = t[i];
      if (c === '"') { i++; while (i < t.length && t[i] !== '"') { if (t[i] === '\\') i++; i++; } continue; }
      if (c === '[' || c === '{') d++;
      else if (c === ']' || c === '}') { d--; if (d === 0) return i; }
    }
    return -1;
  }

  function layNhom(t, nguon) {
    const N = (S.nguon[nguon] = S.nguon[nguon] || { tong: null, conTrang: null, da: 0 });
    let p = 0;
    while ((p = t.indexOf('"search_results_connection":', p)) !== -1) {
      const o = t.indexOf('{', p);
      const e = khop(t, o);
      if (e < 0) break;
      try {
        const j = JSON.parse(t.slice(o, e + 1));
        if (typeof j.count === 'number' && N.tong === null) N.tong = j.count;
        if (j.page_info) N.conTrang = !!j.page_info.has_next_page;
        for (const ed of j.edges || []) {
          const cr = (ed.node && ed.node.collated_results) || [];
          if (!cr.length) continue;
          const k = nguon + '|' + (cr[0].collation_id || cr[0].ad_archive_id);
          if (S.daThay[k]) continue;
          S.daThay[k] = 1;
          N.da++;
          S.nhom.push({ cr, nguon, hang: N.da });
        }
      } catch (err) { /* không phải JSON hợp lệ, bỏ qua */ }
      p = e + 1;
    }
  }

  if (!S.hook) {
    const oo = XMLHttpRequest.prototype.open, os = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (m, u) { this.__u = u; return oo.apply(this, arguments); };
    XMLHttpRequest.prototype.send = function () {
      this.addEventListener('load', () => {
        try { if (/graphql/.test(this.__u) && this.responseText.indexOf('collated_results') !== -1) layNhom(this.responseText, nguonCua(location.href)); } catch (e) {}
      });
      return os.apply(this, arguments);
    };
    S.hook = true;
  }

  window.__soiAdsThem = async (url) => {
    const html = await (await fetch(url, { credentials: 'include' })).text();
    const ng = nguonCua(url);
    layNhom(html, ng);
    const N = S.nguon[ng] || {};
    return { nguon: ng, tong_theo_meta: N.tong, da_lay_nhom: N.da, con_trang_sau: N.conTrang };
  };

  if (!S.nguon[nguonCua(location.href)]) await window.__soiAdsThem(location.href);

  const ngay = (s) => (s ? new Date(s * 1000).toISOString().slice(0, 10) : null);
  const homNay = Date.now() / 1000;
  const nt = { FACEBOOK: 'F', INSTAGRAM: 'I', MESSENGER: 'M', AUDIENCE_NETWORK: 'A', THREADS: 'T' };
  const mien = (u) => { try { return u ? new URL(u).hostname.replace(/^www\./, '') : null; } catch (e) { return null; } };
  const gon = (s, n) => (s || '').replace(/\s*\n+\s*/g, ' / ').slice(0, n);

  window.__soiAdsTomTat = () => Object.entries(S.nguon).map(([k, N]) => ({ nguon: k, tong_theo_meta: N.tong, da_lay_nhom: N.da, con_trang_sau: N.conTrang }));

  // Một nhóm = một nội dung. Các bản trong nhóm thường là CÙNG nội dung được lên lại ở chiến dịch khác
  // (URL media mỗi lần tải lên đều khác, nên không dùng URL để đoán "khác hình"; muốn biết thì xem thật).
  window.__soiAdsDong = (tu = 0, so = 50) => S.nhom.slice(tu, tu + so).map(({ cr, nguon, hang }) => {
    const a = cr[0], sn = a.snapshot || {};
    const than = new Set(cr.map((x) => ((x.snapshot || {}).body || {}).text || ''));
    const ngayLen = cr.map((x) => x.start_date).filter(Boolean).sort((p, q) => p - q);
    const dau = ngayLen[0], cuoi = ngayLen[ngayLen.length - 1];
    return {
      nguon, hang,
      id: a.ad_archive_id,
      nhom_id: a.collation_id,
      page: a.page_name,
      page_id: a.page_id,
      follow: sn.page_like_count,
      so_ban: a.collation_count || cr.length,
      ban_khac_chu: than.size,
      so_lan_len: new Set(ngayLen.map(ngay)).size,
      bat_dau: ngay(dau),
      lan_len_cuoi: ngay(cuoi),
      tuoi_ngay: dau ? Math.floor((homNay - dau) / 86400) : null,
      dinh_dang: sn.display_format,
      so_the: (sn.cards || []).length,
      nen_tang: (a.publisher_platform || []).map((p) => nt[p] || p).join(''),
      cta: sn.cta_type,
      link: mien(sn.link_url),
      chu: gon(((sn.body || {}).text) || (sn.cards && sn.cards[0] && sn.cards[0].body) || '', 160),
    };
  });

  // Một nhóm có thể nằm ở nhiều nguồn (fanpage + từ khoá): gộp theo nhóm, giữ bản có nhiều biến thể nhất.
  const nhomTheoId = (ids) => {
    const gap = {};
    for (const { cr } of S.nhom) {
      if (!cr.some((x) => ids.includes(x.ad_archive_id))) continue;
      const k = cr[0].collation_id || cr[0].ad_archive_id;
      if (!gap[k] || cr.length > gap[k].length) gap[k] = cr;
    }
    return Object.values(gap);
  };

  window.__soiAdsChiTiet = (ids) => nhomTheoId(ids).map((cr) => cr.map((x) => {
    const sn = x.snapshot || {};
    return {
      id: x.ad_archive_id,
      bat_dau: ngay(x.start_date),
      dinh_dang: sn.display_format,
      chu: ((sn.body || {}).text) || '',
      tieu_de: sn.title, mo_ta: sn.link_description, cta: sn.cta_text, link: sn.link_url,
      video: (sn.videos || []).map((v) => ({ hd: v.video_hd_url || v.video_sd_url, anh_bia: v.video_preview_image_url })),
      anh: (sn.images || []).map((i) => i.original_image_url || i.resized_image_url),
      the: (sn.cards || []).map((c) => ({ tieu_de: c.title, chu: c.body, anh: c.original_image_url || c.resized_image_url, video: c.video_hd_url || c.video_sd_url, link: c.link_url })),
    };
  }));

  return window.__soiAdsTomTat();
})();
