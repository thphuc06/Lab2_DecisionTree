# Tiến độ — Role A (Data Lead & Integrator)

> Owner: Trần Hoàng Phúc (Role A). Ngoài owner, chỉ agent đang làm task Role A
> hoặc task integration/final-audit được người dùng giao rõ mới sửa file này.
> Agent: đọc file này sau khi xác định phạm vi theo `AGENT.md` Mục 0 và cập
> nhật ngay sau mỗi mốc đáng kể, đồng thời kiểm tra lại trước khi bàn giao.

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-09-01)_
- Trạng thái: đã hoàn tất audit nộp bài cuối ở mức source, số liệu và nội dung; report không còn TODO/placeholder. Các file draft từng được nhắc trong nhật ký cũ chỉ là sản phẩm trung gian và đã được xóa sau khi nội dung chuẩn được tích hợp vào LaTeX.
- Bị chặn bởi: không có blocker kỹ thuật trong workspace; chỉ còn kiểm tra danh tính, media và đóng gói do con người đối chiếu trực tiếp với đề gốc.

## Đã xong
- [x] Tải dataset qua `ucimlrepo` (id=697), lưu `data/raw/data.csv`
- [x] Chạy `df.shape`, `df.info()`, `df.isnull().sum()` — xác nhận số liệu thực tế
- [x] Xác định cột categorical mã hóa số, ghi `docs/feature_types.md`
- [x] Viết `src/data.py`: `load_and_preprocess()` + `get_train_test()`
- [x] EDA: phân bố target, thống kê mô tả, heatmap tương quan (5 hình, `notebooks/01_eda.ipynb`)
- [x] Gộp `results.csv` cuối dự án, vẽ `figures/comparison.png` — B/C/D/E đã xong M0-M3, đã gộp qua `notebooks/06_comparison.ipynb`
- [x] Tích hợp mục b/c (Introduction, Dataset Description) vào report chính; xóa bản nháp trung gian sau audit cuối
- [x] Tích hợp mục g/h (Comparison of Results, Conclusion) vào report chính; xóa bản nháp trung gian sau audit cuối
- [x] Tích hợp `origin/main` `a29d356` vào Role E, tạo `requirements-lock.txt` canonical và tái lập artifact E hai lần độc lập
- [x] Chạy audit cuối toàn repository: notebook/CSV/PNG/link/dependency, tái tính độc lập số liệu M0–M3, LaTeX compile và render trực quan toàn bộ PDF A4

## Quyết định đã chốt
_(Ghi các lựa chọn kỹ thuật đã quyết — để agent phiên sau không hỏi lại hoặc tự đổi ý)_
- Số feature đếm thực tế: `df.shape` = (4424, 37) → **36 feature + 1 cột `Target`**. Xác nhận chênh lệch 36 (UCI) vs 34 (bài báo): 2 cột dư là `Previous qualification (grade)` và `Admission grade`. `isnull().sum().sum()` = 0.
- Tên cột thực tế khác doc tóm tắt: `Marital Status` (không phải "Marital status"), `Nacionality` (không phải "Nationality") — `src/data.py` dùng đúng tên thật.
- One-hot: `Marital Status` (6), `Application mode` (18), `Course` (17), `Previous qualification` (17). Giữ nguyên mã số: `Mother's/Father's qualification` (29/34), `Mother's/Father's occupation` (32/46), `Nacionality` (21), `Application order` (ordinal). Chi tiết + lý do: `docs/feature_types.md`.
- Sau one-hot: **90 cột feature**. Split: `train_test_split(test_size=0.2, stratify=y, random_state=42)` → train (3539, 90), test (885, 90), tỉ lệ 3 lớp giữ nguyên ở cả 2 tập.
- Smoke test: `DecisionTreeClassifier(random_state=42)` trên output của `get_train_test()` cho test acc = 0.6689 — khớp khoảng kỳ vọng 0.65–0.72 ở `AGENT.md` §3. Accuracy này chỉ là sanity check, không tự nó chứng minh không có leakage; leakage được kiểm soát bằng split cố định và chỉ fit trên train.

## Việc tiếp theo
- Trưởng nhóm thực hiện các cổng con người/ngoài workspace: xác minh tên–MSSV–giảng viên–ngày nộp, kiểm tra video/đường dẫn chia sẻ và tạo gói `2.zip` đúng đề.
- Người dùng review toàn bộ diff rồi tự `git add` / `git commit` / `git push` theo `AGENT.md`; agent không thực hiện ba thao tác này.
- Commit `0969118` ghi nhầm `[C]` nhưng là công việc Role E. Không dùng prefix đó để tính contribution; nếu nhóm vẫn muốn sửa lịch sử đã công bố, chỉ con người thực hiện quy trình phối hợp trong runbook vì thao tác này viết lại 23 commit hậu duệ.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

> Các entry dưới đây là snapshot lịch sử tại thời điểm được ghi. Khi số trang,
> phiên bản, TODO hoặc trạng thái cũ khác phần đầu file, phần **Trạng thái hiện
> tại** và artifact canonical mới nhất được ưu tiên.

### 2026-09-01 — chuẩn hóa toàn bộ hệ Markdown trước bàn giao
- Đã làm gì: audit 15 file Markdown theo đúng vai trò từng tài liệu; hoàn thiện README, sửa quy trình Git/agent, contribution, provenance, heading hierarchy và trạng thái progress.
- Kết quả: không còn placeholder owner/template hiện hành; link, H1/heading, code fence, model-ID schema và wording safety gate đều đạt. Các việc chưa tick chỉ còn ở runbook/đóng gói do con người thực hiện.
- Vướng gì / để lại cho phiên sau: không có finding Markdown kỹ thuật mở.

### 2026-09-01 — audit nộp bài cuối và đồng bộ tài liệu
- Đã làm gì: đối chiếu đề gốc, source LaTeX, toàn bộ artifact, số liệu M0–M3, Git/progress và tài liệu Markdown; loại năm draft trung gian sau khi xác nhận nội dung chuẩn đã có trong report chính.
- Kết quả: phần report và code không còn việc kỹ thuật mở; các đầu việc còn lại đều là xác minh danh tính, media và đóng gói theo đề gốc.
- Vướng gì / để lại cho phiên sau: con người phải thực hiện các cổng ngoài workspace và tự commit/push sau khi review.

### 2026-08-30 (phiên 17) — resolve merge conflict giữa local (A) và origin/main (nhánh Role E)
- Đã làm gì: Người dùng `git pull` sau khi commit 2 việc trước đó (fix bảng A6 lần 1, tạo Phancong.md) thì gặp `git pull` báo local changes ở `progress/A.md` sẽ bị ghi đè — hướng dẫn người dùng commit trước rồi pull lại. Sau khi pull, git tự merge sạch hầu hết file (kể cả `progress/A.md`, `c_dataset.tex`, `AGENT.md` — không conflict vì 2 bên sửa khác vùng/khác nội dung tương thích), chỉ còn đúng 2 file conflict thật: `docs/02-DATASET-VA-CONG-VIEC.md` và `docs/report/report.pdf` (binary).
  - `docs/02`: phát hiện bên `origin/main` (nhánh Role E, có vẻ do 1 agent khác chạy audit "release-readiness" độc lập) đã **tự tìm ra và sửa đúng y hệt 2 giá trị sai** ở bảng A6 mà tôi đã sửa trước đó (0,791 và 0,910) — khớp 100%, cross-verify tốt. Khác nhau ở cách trình bày: tôi sắp lại thứ tự bảng giảm dần, họ giữ nguyên vị trí gốc chỉ sửa số. Vì 2 cách khác nhau, git để sót 1 dòng trùng lặp ("Nationality↔International") ngoài vùng conflict marker — không chỉ chọn 1 bên mà phải dựng lại tay: giữ cấu trúc gốc (theo họ, đơn giản hơn) + xoá dòng trùng + dùng ghi chú giải thích của họ (chính xác hơn, khớp đúng code M3 thật — không loại cột theo correlation).
  - `report.pdf`: không merge tay file nhị phân, mà **compile lại từ đầu** từ `.tex` đã merge — cách chắc chắn đúng nhất.
- Kết quả: Compile lại sạch hoàn toàn — 3 pass exit 0, 0 lỗi, 0 undefined ref/citation, **0 overfull hbox** (tốt hơn cả trước, nhờ merge mang theo `\emergencystretch` từ nhánh kia). `report.pdf` 22 trang. Đã xem lại trang bảng A6/Table 4 (mục c) — số liệu khớp nhau hoàn toàn giữa `docs/02` và `c_dataset.tex`.
- Vướng gì / để lại cho phiên sau: Không có blocker kỹ thuật. Ghi chú: nhánh Role E (tag `[E]`, git author `Arthern-30062006ww`) tự sửa `AGENT.md`/`README.md`/`docs/03` — cùng kiểu tự cấp quyền như D từng làm trước đây; nội dung hợp lý (mở rộng đúng phạm vi file Role A để cover `requirements-lock.txt`, làm rõ 5 cấu hình model) nên không revert, chỉ ghi nhận lại đây để minh bạch.

### 2026-08-30 — audit release-readiness cuối trước pha report/slide/video
- Đã làm gì: Fetch lại remote và xác nhận `origin/main` vẫn ở `a29d356`; rà toàn bộ diff merge; chạy pipeline notebook 01→06 hai vòng trong môi trường lock; sửa portability, số liệu/tài liệu stale và nguồn nondeterminism của pandas Styler; kiểm tra JSON/UTF-8, link Markdown, dependency LaTeX, inventory CSV/TXT/PNG và số liệu model; compile/render report thật.
- Kết quả: Cả hai full pipeline đều exit 0 và mọi artifact dữ liệu/output/hình giữ nguyên bit-for-bit; notebook 02/04 sau khi cố định Styler UUID tiếp tục có hash ổn định qua hai lượt riêng. Sáu notebook có execution count lần lượt 1→11, 1→13, 1→12, 1→13, 1→10, 1→5; không stored error/warning/timing metadata hay đường dẫn máy cá nhân. `pip check` và lock dry-run PASS. `results.csv` có đúng 5 model/16 cột với metric canonical. Có đúng 22 PNG hợp lệ. `report.pdf` là A4, 22 trang; log 0 error, 0 undefined citation/reference, 0 overfull box; toàn bộ trang đã render và kiểm tra trực quan, không còn trang references mồ côi.
- Vướng gì / để lại cho phiên sau: Không còn blocker kỹ thuật. Merge vẫn ở trạng thái chưa commit vì `AGENT.md` cấm agent chạy `git add`/`git commit`/`git push`; người dùng phải thực hiện ba thao tác đó. Report hiện là khung kỹ thuật khỏe nhưng vẫn còn placeholder đỏ ở a/d/e/f1/f2/f3, đúng phạm vi của pha viết tiếp theo.

### 2026-08-30 — tích hợp Role E với main và khóa môi trường canonical
- Đã làm gì: Merge `origin/main` `a29d356` vào branch `role-e-final-thuy` ở chế độ chưa commit; resolve tài liệu chung; tạo `requirements-lock.txt`; đồng bộ manifest/lock trong `README.md`, `AGENT.md`, `docs/02` và `docs/03`; cập nhật provenance E sang handoff D `6d558b1`.
- Kết quả: `pip check` PASS; Role E Run All hai lần bằng kernel `.venv` định danh cho kết quả bit-for-bit giống nhau; notebook execution 1→10, không stored error/timing metadata; 11 artifact D bất biến và các artifact report/A từ `main` không bị thay đổi bởi quá trình chạy E.
- Vướng gì / để lại cho phiên sau: Không còn blocker kỹ thuật. Người dùng cần tự `git add`/`git commit`/`git push`; agent không được chạy ba lệnh này theo `AGENT.md`.

### 2026-08-30 (phiên 7) — tạo khung LaTeX cho report (docs/report/)
- Đã làm gì: Theo yêu cầu người dùng, tạo `docs/report/` chứa `report.tex` (master file), `references.bib` (13 reference đã gộp từ tất cả bản nháp b/c, f1, f2, f3, g/h — không bịa thêm), `README.md` hướng dẫn compile + bản đồ sở hữu, và 10 file `sections/*.tex` khớp đúng cấu trúc a-i của đề gốc (3.4). Đã **điền đầy đủ tiếng Anh** 4 mục thuộc quyền A (b, c, g, h) — dịch từ bản Việt đã fact-check, giữ nguyên số liệu đã sửa lỗi. 6 mục còn lại (a, d, e, f1, f2, f3) để **khung + `\todo{}` placeholder** trỏ đúng file nguồn Việt đã audit cho từng role tự dịch, không tự điền thay.
- Kiểm tra kỹ thuật: không có LaTeX trên máy này nên **chưa compile thử được thật** — đã bù bằng cách tự kiểm tra thủ công: (1) không còn `_` chưa escape ngoài phần đối số lệnh (`\input`/`\includegraphics`), (2) sửa 5 URL trong `.bib` bị thiếu bọc `\url{}` (URL có `_` sẽ vỡ compile nếu không bọc), (3) đếm ngoặc `{}` cân bằng ở cả 11 file `.tex` + `references.bib`, (4) mọi `\ref{}` đều có `\label{}` khớp, (5) mọi `\cite{}` đều có entry trong `.bib`, (6) số cột bảng khớp header/data ở cả 3 bảng.
- Vướng gì / để lại cho phiên sau: **Chưa compile thật lần nào** — việc đầu tiên khi có máy có LaTeX (hoặc Overleaf) là chạy thử ngay, vì kiểm tra tay không thay thế được compile thật 100%. Cũng lưu ý README đã note rõ rằng đây là quyết định thay thế kế hoạch "Google Doc chung" cũ trong `docs/02` Phần E1.

### 2026-08-30 (phiên 8) — cài LaTeX (MiKTeX) và compile thật khung report
- Đã làm gì: Theo yêu cầu người dùng, cài MiKTeX qua `winget install MiKTeX.MiKTeX`, bật auto-install package thiếu (`initexmf --set-config-value=[MPM]AutoInstall=1`), rồi compile thật `docs/report/report.tex` (pdflatex → bibtex → pdflatex → pdflatex).
- **Bug thật tìm được qua compile (không phải qua đọc tay):**
  1. BibTeX **không coi `%` là comment** — nó quét tìm ký tự `@` bất kỳ đâu trong file. Dòng comment đầu `references.bib` viết "add new @entries" làm bibtex vỡ ngay entry đầu tiên ("I was expecting a `{' or a `('"). Đã sửa: viết lại toàn bộ đoạn giải thích không dùng ký tự `@` (kể cả khi mô tả chính lỗi này — bị dính lại 1 lần nữa lúc sửa, phải viết "at-sign" thay vì gõ trực tiếp).
  2. Style `plainnat.bst` **tự động bọc `\url{...}`** quanh trường `url` khi sinh bibliography. Tôi lại tự bọc thêm 1 lớp `\url{}` nữa trong `.bib` (làm theo lo ngại lúc soát tay tuần trước) → `\url{\url{...}}` lồng đôi → catcode xử lý đệ quy → "TeX capacity exceeded, input stack size=10000", compile chết, không ra PDF. Đã sửa: bỏ lớp `\url{}` tôi tự thêm ở cả 5 URL, giữ URL thô (style tự xử lý catcode `_` đúng cách).
  3. (Nhân tiện) thêm `author`/`year` cho 5 entry `@misc` để hết warning "empty year"/"need author or key" của plainnat.bst.
- Kết quả: **Compile sạch, 3 pass đều exit 0, không còn `!` error, không còn undefined citation/reference.** `report.pdf` 26 trang, 14.4MB (nặng vì hình cây độ phân giải cao). Đã xem trực tiếp nhiều trang (title/mục a, mục b, 2 hình EDA mục c, trang references, trang TODO heatmap mục c) qua `miktex-pdftoppm` — render đúng, citation/cross-ref/bảng/hình/TODO đỏ đều hiển thị chính xác.
- Đã dọn: xoá hết ảnh preview tạm, thêm `.gitignore` cho `*.aux/*.bbl/*.blg/*.out/*.toc/*.synctex.gz` (giữ lại `report.pdf` — đây là deliverable thật, không ignore).
- Vướng gì / để lại cho phiên sau: Không còn vướng kỹ thuật. `report.pdf` hiện tại còn nhiều `\todo{}` (mục a, d, e, f1, f2, f3) — cần B/C/D/E dịch nội dung của họ rồi compile lại. Bài học rút ra (đáng nhớ cho cả nhóm): **kiểm tra tay kỹ tới đâu cũng không thay được compile thật** — cả 2 bug trên đều là loại lỗi mà review tay không phát hiện ra, chỉ lộ ra khi chạy pdflatex/bibtex thật.

### 2026-08-30 (phiên 16) — cập nhật Phancong.md: Trưởng nhóm chốt quyết định giữ điều khoản AGENT.md
- Đã làm gì: Người dùng (xác nhận là Trưởng nhóm) quyết định **giữ nguyên** điều khoản "ngoại lệ" D tự thêm vào `AGENT.md` Mục 5 (không revert). Cập nhật `Phancong.md`: tick `[x]` 2 mục "Quyết định cùng..." ở phần Role D và Trưởng nhóm, ghi rõ đã chốt giữ nguyên. Không sửa `AGENT.md` (giữ nguyên là quyết định của Trưởng nhóm, không cần thao tác gì thêm).
- Kết quả: `Phancong.md` giờ chỉ còn đúng các việc thật sự cần làm (dịch report B/C/D/E, slide/video E, sửa README của D, điền mục a + đóng gói của Trưởng nhóm) — không còn mục "chờ quyết định" nào.
- Vướng gì / để lại cho phiên sau: Không có.

### 2026-08-30 (phiên 15) — tạo Phancong.md tổng hợp việc còn lại cho cả nhóm
- Đã làm gì: Theo yêu cầu người dùng, tạo `Phancong.md` ở root repo — gộp toàn bộ việc còn lại đã liệt kê rải rác trong phiên (bảng cuối cùng, các lưu ý về docs/02, README, AGENT.md) thành 1 file duy nhất, chia rõ theo từng role (B/C/D/E/Trưởng nhóm), có checkbox để tick tiến độ, và mục "Quy tắc chung" tóm tắt 6 quy tắc mới đã thêm vào AGENT.md/docs/report/README.md trong phiên này.
- Đã đối chiếu lại số `\todo` còn lại từng file trước khi ghi vào Phancong.md (không dùng số nhớ từ trước, tránh sai lệch nếu có gì đổi): a=7, d=6, e=7, f1=7, f2=10, f3=6; b/c/g/h=0.
- Vướng gì / để lại cho phiên sau: Không có. File `Phancong.md` không thuộc quyền sở hữu role nào cụ thể (là tài liệu điều phối chung), mọi role đều có thể tick checkbox khi xong việc của mình.

### 2026-08-30 (phiên 14) — sửa bảng đa cộng tuyến sai trong docs/02 (đã xin xác nhận người dùng)
- Đã làm gì: Người dùng xác nhận muốn sửa lỗi #10 (bảng A6 sai) trong danh sách việc tồn đọng. Sửa `docs/02-DATASET-VA-CONG-VIEC.md` Phần A6: đổi `Nationality↔International` từ 0,912 → **0,791**, đổi `Mother's/Father's occupation` từ 0,724 (hạng 9) → **0,910** (hạng 3 thật), sắp lại đúng thứ tự giảm dần trong bảng (giữ nguyên 10 cặp gốc, không thêm cặp mới ngoài phạm vi yêu cầu). Sửa thêm 1 chỗ trích số cũ (r=0,91 → r=0,79) ở đoạn "Mở rộng" gợi ý bỏ cột `International`. Thêm ghi chú đầu bảng giải thích đã rà soát lại 2026-08-30.
- Xoá khối `\todo{Data-integrity note...}` trong `docs/report/sections/c_dataset.tex` (đúng theo chỉ dẫn "delete once acted on" đã ghi sẵn trong chính khối đó) — giờ `c_dataset.tex` không còn `\todo` nào, hoàn toàn xong.
- Compile lại xác nhận sạch (3 pass exit 0, không lỗi/undefined).
- Vướng gì / để lại cho phiên sau: Không có. Đây là thay đổi trong `docs/02` — file kế hoạch dùng chung, không thuộc riêng role nào, nên không cần xin phép role khác như trường hợp sửa file D trước đây.

### 2026-08-30 (phiên 13) — audit độc lập lần 2 (subagent) + sửa 6 lỗi mới tìm được
- Đã làm gì: Theo yêu cầu người dùng, chạy 1 subagent audit độc lập toàn bộ 4 file đã điền của A (b/c/g/h) — kiểm tra 4 tiêu chí: khớp đề gốc, số liệu chuẩn xác (re-verify từ `outputs/*`, tự tính lại từ `data/raw/data.csv`), logic nhận xét, ý nghĩa thực tế. Tự verify lại độc lập từng finding (không tin ngay) trước khi sửa.
- Kết quả — xác nhận đúng cả 6 lỗi, đã sửa hết:
  1. `g_comparison.tex`: "~1.35× M0" (Enrolled recall) → tính lại đúng là **~1.21×** (0,4654/0,3836).
  2. `g_comparison.tex`: "M2b raises Enrolled precision (0,3234→0,4044)" — **0,3234 là của M2a, không phải M0**. M0 thật (từ `classification_report_M0.txt`) là **0,3567**. Sửa lại đúng baseline.
  3. `c_dataset.tex`: hoán đổi Graduate% giữa 2 ngành thấp nhất — ghi "33 ... và 9119 ... chỉ 8,2% và 8,3%" nhưng tính lại từ data thật thì 33→8,3%, 9119→8,2% (ngược thứ tự). Đã sửa đúng thứ tự.
  4. `c_dataset.tex` Table `tab:c-corr`: r của Mother's/Father's occupation ghi 0,911, tính chính xác lại là **0,9105 → làm tròn 0,910** (không phải 0,911). Sửa cả trong bảng và trong `\todo` note.
  5. `c_dataset.tex`: "lower than the three pairs above" nhưng lúc đó đã liệt kê 4 cặp (credited/enrolled/occupation/approved), không phải 3 — sửa thành "four pairs".
  6. **Lỗi nặng nhất** — `h_conclusion.tex`: trích luật Dropout chỉ bằng 1 điều kiện (`2nd sem approved ≤ 1.5`) và luật Graduate chỉ 2 điều kiện, nhưng đối chiếu `outputs/rules_M0.txt`/`docs/report_draft_d_e.md` thì luật Dropout thật có **9 điều kiện AND với nhau**, luật Graduate có **16 điều kiện** — chỉ trích 1-2/9-16 điều kiện rồi nói "gần như chắc chắn Dropout" là đơn giản hoá sai lệch (không hẳn bịa như lần trước, nhưng gây hiểu lầm tương tự). Đã sửa: nêu rõ đây là 1 điều kiện dễ đọc nhất trong chuỗi 9/16 điều kiện, không phải đủ để kết luận một mình — đồng thời nối được thêm luận điểm hay: chuỗi điều kiện dài chính là bằng chứng cụ thể cho overfitting đã bàn ở đoạn trên.
- Compile lại xác nhận sạch (3 pass exit 0, không lỗi/undefined). Đã xem lại trang h_conclusion mới xác nhận đúng.
- Đánh giá tổng thể của subagent (không phải tôi tự nhận xét): phần "khớp đề gốc" và "ý nghĩa thực tế" đều đạt (DONE), phần compile/hình/table-traceability đều ổn — chỉ 2 nhóm lỗi trên (số liệu + 1 chỗ logic) cần sửa, đã sửa xong.
- Vướng gì / để lại cho phiên sau: Không có. Bài học lặp lại (lần thứ 3 trong phiên này): **luôn tự verify lại bằng code, kể cả những con số "nghe hợp lý" hoặc đã tưởng là đã kiểm tra kỹ ở lượt trước** — 2 lượt fact-check trước cũng để lọt 6 lỗi này.

### 2026-08-30 (phiên 12) — thêm luật "số liệu phải truy được nguồn" vào AGENT.md
- Đã làm gì: Người dùng hỏi AGENT.md đã có luật đảm bảo số liệu phải từ code/hình artifact, không bịa, chưa — kiểm tra thì chỉ có 1 dòng hẹp cho riêng role A (Mục 0 bước 2, về `df.shape`/`df.info()`), không có luật chung cho việc VIẾT báo cáo. Thêm 1 dòng mới vào bảng Mục 2 (áp dụng mọi role): mọi số liệu trong `docs/report/sections/*.tex` phải verify được từ (a) output code thật hoặc (b) bảng/hình đã có mặt ngay trong báo cáo — không suy diễn "nghe hợp lý", không copy từ `docs/02` mà không re-verify. Đúc kết trực tiếp từ 2 lượt lỗi thật đã gặp trong phiên này (lỗi bịa luật Dropout ở h_conclusion, và số liệu không tra được từ hình ở c_dataset).
- Kết quả: `AGENT.md` Mục 2 giờ có đủ 3 luật mới liên quan tới chất lượng báo cáo (chữ trong hình tiếng Anh, không nhắc tên file/hàm, số liệu phải truy được nguồn). Đã kiểm tra bảng markdown không bị vỡ cú pháp.
- Vướng gì / để lại cho phiên sau: Không có.

### 2026-08-30 (phiên 11) — thêm bảng số liệu, sửa lỗi "số liệu không thấy từ đâu ra"
- Đã làm gì: Theo góp ý người dùng ("phần nhận xét nhiều số liệu quá mà nhìn biểu đồ không thấy số từ đâu ra"), rà lại `c_dataset.tex`: đúng là nhiều số (Gini importance rank 1/3/6/24, các giá trị r=0.945/0.911/0.904/0.791) được trích trong văn bản nhưng **không hình nào đang gắn kèm thực sự hiển thị được** — heatmap không có số in trên ô, còn bảng feature importance của M0 thì chưa từng xuất hiện ở mục c (chỉ có ở mục f.3 của E, xuất hiện sau). Không phải số bịa (đã verify từ trước), nhưng đúng là không tra được tại chỗ.
- Đã sửa: thêm **2 bảng mới** vào `c_dataset.tex` — Table 3 "Top-10 features by Gini importance in M0" (kèm dòng Scholarship holder hạng 24 để đối chiếu) đặt trước đoạn đầu tiên trích số importance; Table 4 "Highest Pearson correlations" liệt kê đúng 5 cặp được nhắc trong văn bản heatmap. Sửa cả 4 chỗ trích số (Tuition rank 3, Scholarship rank 24, Course rank 6, 2nd sem approved rank 1, và đoạn heatmap) để trỏ `\ref{}` về đúng bảng thay vì chỉ khẳng định suông.
- Compile lại xác nhận sạch (3 pass exit 0, không lỗi/undefined), xem lại 3 trang mẫu qua `miktex-pdftoppm` — cả 2 bảng mới hiển thị đúng, mọi số trong văn bản giờ tra được ngay tại chỗ.
- Vướng gì / để lại cho phiên sau: Không có. Lưu ý: nếu B/C/D/E cũng trích số liệu (VD nhắc "feature importance", "correlation") trong phần của họ mà không có bảng/hình đi kèm tại chỗ, nên áp dụng cùng cách sửa (thêm bảng nhỏ hoặc `\ref{}` về bảng/hình đã có).

### 2026-08-30 (phiên 10) — hình tiếng Anh, dọn tên file/hàm khỏi văn bản báo cáo, thêm luật AGENT.md
- Đã làm gì (3 việc, theo yêu cầu người dùng):
  1. **Hình tiếng Anh**: `notebooks/01_eda.ipynb` và `notebooks/06_comparison.ipynb` có title/label matplotlib bằng tiếng Việt ("Ti le Target theo...", "Phan bo lop Target"...) — patch 15 chuỗi (10+5) sang tiếng Anh, chạy lại cả 2 notebook, xuất lại toàn bộ 6 hình của A. Kiểm tra chéo hình của B/C/D (đã có sẵn tiếng Anh, không cần sửa).
  2. **Dọn văn bản báo cáo**: xoá hết tham chiếu tên file/đường dẫn/hàm nội bộ repo (`src/data.py`, `get_train_test()`, `df.shape`, `outputs/*.csv`, `docs/02-...md`, v.v.) khỏi phần văn bản thật của `c_dataset.tex`, `g_comparison.tex`, `a_group_intro.tex` — thay bằng mô tả tiếng Anh thường hoặc citation thật (`\citep{realinho2022predicting}` thay vì "Section A5 của docs/02"). Giữ nguyên tham chiếu trong khối `\todo{}` và comment đầu file (ghi chú nội bộ, sẽ xoá trước khi nộp). Tiện phát hiện và sửa 1 lỗi lặp câu ("Enrolled is minority class...") bị trùng 2 lần do sót từ lần sửa trước.
  3. **Thêm luật vào `AGENT.md`** (Mục 2, theo yêu cầu rõ ràng của người dùng): 2 dòng mới — (a) chữ trong hình matplotlib phải tiếng Anh, (b) văn bản báo cáo (`docs/report/sections/*.tex`) không được nhắc tên file/hàm nội bộ repo, trỏ sang `docs/report/README.md` để biết chi tiết.
- Compile lại xác nhận: sạch, 3 pass exit 0, không lỗi/undefined, overfull hbox giảm còn 13 (từ 16). Đã xem lại 2 trang mẫu qua `miktex-pdftoppm` xác nhận hình English + văn bản đã dọn đúng.
- Vướng gì / để lại cho phiên sau: Không có. Lưu ý cho phiên sau: khi B/C/D/E tự điền phần `\todo{}` của họ, nhắc họ đọc luật mới trong `AGENT.md` Mục 2 (không nhắc tên file/hàm trong văn bản thật).

### 2026-08-30 (phiên 9) — sửa format: caption ngắn lại, tràn lề bảng
- Đã làm gì: Theo góp ý người dùng ("figure đánh giá nằm dưới, đừng để phần comment đánh giá nằm ở phần chú thích figure"), viết lại toàn bộ 5 hình trong `c_dataset.tex` và hình `comparison.png` trong `g_comparison.tex`: caption giờ chỉ mô tả hình (1 câu), phần nhận xét/phân tích chuyển thành đoạn văn thường ngay trước/sau hình. Thêm quy tắc này vào `README.md` để B/C/D/E theo khi tự điền phần của họ.
- Compile lại xác nhận (không chỉ đọc code): phát hiện thêm 2 bảng trong `g_comparison.tex` bị tràn lề thật (168pt và 119pt too wide, xem `Overfull \hbox` trong log) — bảng 10 cột (`tab:g1`) quá rộng ở font `\small`, bảng "Why" 3 cột (`tab:g2`) dùng cột `l` không wrap được chữ dài. Đã sửa: bảng số bọc `\resizebox{\textwidth}{!}{...}`, bảng chữ đổi cột `l`→`p{4.3cm}`/`p{6.3cm}`. Recompile xác nhận 2 chỗ tràn nặng đã hết hoàn toàn (chỉ còn các overfull nhỏ <70pt, mức bình thường của LaTeX, 1 chỗ còn lại là do placeholder TODO dài ở trang tiêu đề, sẽ tự hết khi điền tên khóa học thật). Tiện thể sửa 2 chỗ `\texttt{outputs/E_feature_importance_comparison.csv}` dài không ngắt được dòng → đổi sang `\url{}` để tự ngắt ở dấu `/`.
- Kết quả: `report.pdf` giờ 25 trang (giảm 1 trang so với trước do gọn caption), compile sạch, đã xem lại 4 trang mẫu qua `miktex-pdftoppm` xác nhận đúng.
- Vướng gì / để lại cho phiên sau: Không có.

### 2026-08-30 (phiên 6) — audit chéo báo cáo B/C/D/E + sửa lỗi của D (có xin phép người dùng)
- Đã làm gì: Theo yêu cầu người dùng, chạy 4 subagent song song audit `docs/report_draft_d_e.md` (B), `docs/report_draft_f1_pruning.md` (C), `docs/report_draft_f2_imbalance.md` (D), và nội dung trong `notebooks/05_improve_features.ipynb` (E) — cùng phương pháp đã dùng cho A: OCR từng hình đối chiếu caption, verify từng số liệu về `outputs/results.csv`/classification report/artifact thật.
- Kết quả: B, C, E hoàn toàn sạch (0 lỗi/~40, ~40, ~12 số liệu kiểm tra). D có 2 lỗi nhỏ, đã tự verify lại độc lập (không chỉ tin subagent) và **đã sửa trực tiếp trong `docs/report_draft_f2_imbalance.md`** theo yêu cầu rõ ràng của người dùng ("nếu thực sự lỗi thì sửa dùm luôn"):
  1. "recall Graduate giảm 0,91 điểm phần trăm" → sửa thành **0,90** (0,7647→0,7557 = 0,9050pp, làm tròn đúng là 0,90 không phải 0,91).
  2. Mô tả cơ chế SMOTE ép kiểu one-hot: "giá trị nội suy... bị làm tròn về 0" → sửa thành **"cắt cụt (truncate)"** — đối chiếu trực tiếp log in ra của chính notebook D (cell 17) xác nhận cơ chế thật là `.astype(int)` truncate, không phải round(); bằng chứng thực nghiệm là `sum_greater_than_one_rate = 0.0%` ở cả 4 nhóm one-hot, chỉ khớp với truncate chứ không khớp với round-to-nearest.
- Lưu ý: đây là lần đầu A sửa trực tiếp file thuộc quyền role khác (`docs/report_draft_f2_imbalance.md` là D's) — làm vậy vì người dùng **yêu cầu rõ ràng và trực tiếp** ("sửa dùm luôn đi"), không phải A tự quyết. Nên báo cho D biết đã có người sửa 2 chỗ nhỏ trong file này.
- Vướng gì / để lại cho phiên sau: Không có.

### 2026-08-30 (phiên 5) — soát lỗi số liệu/nhận xét trong 2 bản nháp báo cáo
- Đã làm gì: Theo yêu cầu người dùng "OCR hình + kiểm tra nhận xét có sơ sài không", đọc lại từng hình trong `figures/` và tự tính lại (không tin theo tài liệu cũ) các số liệu đã trích dẫn trong `docs/report_draft_b_c.md` và `docs/report_draft_g_h.md`.
- Kết quả — tìm và sửa **4 lỗi thật**:
  1. Caption Hình c.3: "hai ngành gần như không có Graduate" — quá lời, số thật là 8,2%/8,3% (không phải ~0%). Đã sửa dùng số chính xác.
  2. Caption Hình c.5: trích r=0,912 cho `Nacionality`↔`International` và r=0,724 cho `Mother's/Father's occupation` từ bảng A6 cũ trong `docs/02`, nhưng tự tính lại trên `data/raw/data.csv` thật ra là **r=0,791** và **r=0,911**. Bảng A6 của `docs/02` sai — đã note lại trong file để nhóm biết cập nhật, không chỉ tự sửa một chiều.
  3. **Lỗi nặng nhất**: mục h Conclusion trích "luật ở mục e: chưa đóng học phí + trượt gần hết môn HK2 → Dropout" — bịa, không khớp luật Dropout thật của B (luật thật dùng `2nd sem approved`, `Mother's occupation`, `Marital Status`, không hề có điều kiện học phí). Đã đọc lại `docs/report_draft_d_e.md` và sửa bằng đúng luật thật (Dropout: `2nd sem approved ≤ 1.5`; Graduate: có điều kiện `Tuition fees up to date > 0.5`).
  4. Mục g giải thích M3: trích "3 trong 5 feature quan trọng nhất của M0" nhưng lấy nhầm bảng permutation importance của **bài báo gốc** (docs/02 A5) thay vì Gini importance thật của chính cây M0 nhóm train. Kiểm tra `outputs/E_feature_importance_comparison.csv` (số liệu thật của E): `1st sem approved` chỉ hạng 9 trong M0 thật, không phải top-5. Đã sửa dùng đúng top-5 thật (2nd sem approved hạng 1, 2nd sem grade hạng 2, Tuition fees hạng 3, 2nd sem enrolled hạng 4, Admission grade hạng 5) và note rõ 2 bảng khác nguồn/khác thuật toán nên khác thứ hạng.
  5. Caption Hình c.2: claim "Scholarship holder nằm trong top-5 bài báo gốc" — sai, top-5 gốc không có feature này; M0 thật xếp nó hạng 24. Đã sửa, đồng thời thêm giải thích vì sao chênh lệch % lớn trên biểu đồ không đồng nghĩa importance cao trong cây (có thể do trùng thông tin với feature mạnh hơn).
- Bài học rút ra: khi trích số liệu từ tài liệu kế hoạch (`docs/02`) hoặc suy diễn hợp lý (nghe "có vẻ đúng"), **phải verify lại bằng code trên dữ liệu/artifact thật** trước khi đưa vào báo cáo, không được tin tài liệu cũ hoặc trực giác. Ba lỗi 2 và 5 xuất phát từ việc tin `docs/02` không kiểm chứng lại; lỗi 3 xuất phát từ việc suy diễn luật "nghe hợp lý" thay vì đọc đúng luật B đã trích.
- Vướng gì / để lại cho phiên sau: Không vướng. Cả 2 file đã re-verify toàn bộ số liệu và ảnh sau khi sửa.

### 2026-08-30 (phiên 4)
- Đã làm gì: Tự audit lại `docs/report_draft_b_c.md` và `docs/report_draft_g_h.md`, phát hiện cả 2 file mô tả số liệu từ hình bằng lời nhưng **không gắn ảnh thật** (khác chuẩn C/D đã làm — luôn có `![...]` + chú thích ngay dưới). Đã sửa: gắn đủ 6 hình (5 hình EDA của A + `comparison.png`) vào đúng vị trí liên quan trong mục c và g, mỗi hình có caption "Hình c.N/g.1" giải thích cụ thể. Bổ sung thêm 1 đoạn mới "Đa cộng tuyến giữa các feature" ở mục c (trước đó có hình heatmap nhưng chưa hề được nhắc tới ở đâu cả trong bản nháp).
- Kết quả: Đã verify tất cả 6 đường dẫn ảnh tồn tại thật (`../figures/...` từ `docs/`). Không còn hình nào "mồ côi" (tồn tại nhưng không được báo cáo nhắc tới) hay caption nào không có ảnh đi kèm.
- Vướng gì / để lại cho phiên sau: Không có.

### 2026-08-30 (phiên 3)
- Đã làm gì: Xác nhận B/C/D/E đã hoàn thành M0-M3 (`outputs/results.csv` đủ 5 dòng, không trùng/hỏng). Dựng và chạy `notebooks/06_comparison.ipynb` (bảng so sánh đầy đủ, `outputs/comparison_table.csv`, hình 4-panel `figures/comparison.png`, bảng "model tốt nhất theo từng tiêu chí"). Viết bản nháp mục **g. Comparison of Results** và **h. Conclusion** dựa trên số liệu thật, đối chiếu với `docs/report_draft_f1_pruning.md`/`f2_imbalance.md`/notebook E để nhất quán số liệu → lưu `docs/report_draft_g_h.md`.
- Kết quả: Toàn bộ 4 mục báo cáo thuộc phạm vi role A (b, c, g, h) đã có bản nháp đầy đủ, có số liệu thật, sẵn sàng copy vào Google Doc. `src/data.py` xác nhận không bị role nào khác đụng vào (`git log -- src/data.py` chỉ có đúng 1 commit của A).
- Vướng gì / để lại cho phiên sau: Không vướng kỹ thuật. Có 2 vấn đề ngoài phạm vi A cần Trưởng nhóm xử lý (xem "Việc tiếp theo"): (1) attribution sai của commit `0969118`, (2) README/docs/02 mô tả sai môi trường cài đặt (không phải lỗi code, không ảnh hưởng kết quả).

### 2026-08-28 (phiên 2)
- Đã làm gì: Đọc lại toàn bộ `docs/00-DE-BAI-GOC.pdf` (đối chiếu bản gốc, xác nhận `docs/02` không lệch), đọc trực tiếp nội dung 5 hình EDA để lấy số liệu cụ thể, viết bản nháp báo cáo mục **b. Introduction** (lý thuyết decision tree + mục tiêu đồ án, có trích dẫn Quinlan 1986/Breiman 1984/Mitchell 1997/Pedregosa 2011) và **c. Dataset Description** (nguồn, số liệu thực tế, 6 nhóm feature, tiền xử lý, lý do phù hợp decision tree, lưu ý đạo đức) → lưu vào `docs/report_draft_b_c.md`.
- Kết quả: File nháp đầy đủ, có số liệu thật (không phải placeholder), có trích dẫn nguồn. Sẵn sàng để copy vào Google Doc chung.
- Vướng gì / để lại cho phiên sau: Chưa điền mục a (tên nhóm/MSSV/GroupID) — thuộc trách nhiệm Trưởng nhóm, không phải phạm vi A. File nháp viết bằng tiếng Việt theo yêu cầu người dùng phiên này.

### 2026-08-28 (phiên 1)
- Đã làm gì: Cài `ucimlrepo`/`imbalanced-learn`; tải dataset UCI id=697 → `data/raw/data.csv`; viết `src/data.py` (`load_and_preprocess()`, `get_train_test()`) với one-hot cho cột ít giá trị, giữ mã số cho cột nhiều giá trị, stratified split random_state=42; viết `docs/feature_types.md`; dựng và chạy (Restart & Run All qua `nbconvert --execute`) `notebooks/01_eda.ipynb` xuất 5 hình vào `figures/A_*.png`.
- Kết quả: `from src.data import get_train_test` chạy được, trả 4 giá trị đã stratify đúng schema (Definition of Done đạt). Smoke-test DecisionTreeClassifier cho acc trong khoảng kỳ vọng. 5 hình EDA đã xuất: target distribution, correlation heatmap, boxplot curricular units 2nd sem theo target, tuition/scholarship vs target, target theo course.
- Vướng gì / để lại cho phiên sau: Chưa có gì vướng. Notebook đang trỏ `FIG_DIR = Path.cwd().parent / "figures"` — giả định chạy notebook từ trong thư mục `notebooks/` (mặc định của Jupyter), cần lưu ý nếu ai chạy theo cách khác. Chưa viết phần báo cáo (b/c/g/h) vì cần chờ số liệu từ các model khác.
