// Bài kiểm cho scripts/thu-thap.js, giả lập trang Thư viện Meta. Chạy: node --test tests/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import vm from 'node:vm';

const GOC = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = readFileSync(join(GOC, 'soi-ads-doi-thu/scripts/thu-thap.js'), 'utf8');
const THONG_KE = join(GOC, 'soi-ads-doi-thu/scripts/thong-ke.py');

const nhom = (id, ngay, conTrang) => ({
  collated_results: [{
    ad_archive_id: String(id), collation_id: 'n' + id, collation_count: 1, page_id: '1', page_name: 'Hãng A - Trang chính',
    start_date: Math.floor(Date.parse(ngay) / 1000), publisher_platform: ['FACEBOOK'],
    snapshot: { body: { text: 'Chữ ads ' + id }, display_format: 'VIDEO', cta_type: 'MESSAGE_PAGE', page_like_count: 1000 },
  }],
});
const html = (ids, conTrang) => '<script>x={"search_results_connection":' + JSON.stringify({
  count: 30, page_info: { has_next_page: conTrang }, edges: ids.map((i) => ({ node: nhom(i, '2026-01-01') })),
}) + '}</script>';

async function trang({ conTrang = false } = {}) {
  const tai = [];
  const log = [];
  class XHR { open() {} send() {} addEventListener() {} }
  const ctx = {
    location: { href: 'https://www.facebook.com/ads/library/?active_status=active&country=VN&search_type=page&view_all_page_id=1' },
    XMLHttpRequest: XHR,
    fetch: async () => ({ text: async () => html([101, 102, 103], conTrang) }),
    Blob, URL: { createObjectURL: (b) => { tai.push({ blob: b }); return 'blob:x'; }, revokeObjectURL() {} },
    document: { createElement: () => ({ click() { tai[tai.length - 1].ten = this.download; } }), body: { appendChild() {}, removeChild() {} } },
    console: { log: (...a) => log.push(a.join(' ')) },
    Date, Intl, JSON, Math, Object, Set, String, Number, Array, Promise, setTimeout,
  };
  ctx.window = ctx;
  vm.createContext(ctx);
  await vm.runInContext(SCRIPT, ctx);
  return { w: ctx, tai, log };
}

test('ban chụp đúng định dạng thong-ke.py', async () => {
  const { w } = await trang();
  const b = w.__soiAdsBanChup('Hãng A');
  assert.equal(b.doi_thu, 'Hãng A');
  assert.match(b.ngay_chup, /^\d{4}-\d{2}-\d{2}$/);
  assert.equal(b.ads.length, 3);
  assert.deepEqual(b.nguon.map((n) => [n.page_id, n.page, n.tong_theo_meta]), [['1', 'Hãng A - Trang chính', 30]]);
  assert.ok(b.nguon[0].url.includes('view_all_page_id=1'));
});

test('__soiAdsLuu tải file tên YYYY-MM-DD-<slug>.json', async () => {
  const { w, tai } = await trang();
  const kq = w.__soiAdsLuu('Hãng Đức Anh');
  assert.equal(tai.length, 1);
  assert.match(tai[0].ten, /^\d{4}-\d{2}-\d{2}-hang-duc-anh\.json$/);
  assert.equal(kq.so_nhom, 3);
  assert.equal(kq.canh_bao, undefined);
});

test('còn trang sau thì cảnh báo, vẫn cho tải', async () => {
  const { w, tai } = await trang({ conTrang: true });
  const kq = w.__soiAdsLuu('Hãng A');
  assert.equal(tai.length, 1);
  assert.match(kq.canh_bao, /chưa cuộn hết/);
});

test('có dòng tiến độ cho người chạy tay ở Console', async () => {
  const { log } = await trang();
  assert.ok(log.some((l) => /đã lấy 3 nhóm/.test(l)));
});

test('file tải về chạy được thong-ke.py', async () => {
  const { w, tai } = await trang();
  w.__soiAdsLuu('Hãng A');
  const dir = mkdtempSync(join(tmpdir(), 'soi-ads-'));
  writeFileSync(join(dir, tai[0].ten), await tai[0].blob.text());
  const r = spawnSync('python3', ['-I', THONG_KE, dir], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Hãng A/);
});
