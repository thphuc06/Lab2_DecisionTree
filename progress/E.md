# Tiến độ — Role E (Improvement 3: Early-warning Feature Selection)

> Owner: Mai Phương Thùy (Role E). Ngoài owner, chỉ agent đang làm task Role E
> hoặc task integration/final-audit được người dùng giao rõ mới sửa file này.
> Agent: đọc file này sau khi xác định phạm vi theo `AGENT.md` Mục 0 và cập
> nhật ngay sau mỗi mốc đáng kể, đồng thời kiểm tra lại trước khi bàn giao.

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-09-01)_
- Trạng thái: hoàn tất; code/notebook/artifact M3 và f.3 đã được đối chiếu trong audit toàn report, không còn việc kỹ thuật mở.
- Bị chặn bởi: không.

## Đã xong
- [x] Loại đúng 12 cột HK1+HK2 (xem `AGENT.md` Mục 3), giữ 24 feature còn lại
- [x] Train M3, gọi `evaluate_model()` từ `src/evaluate.py`
- [x] So sánh Gini/MDI M0 vs M3 theo feature gốc — `figures/E_feature_importance.png`, `outputs/E_feature_importance_comparison.csv`
- [x] Held-out grouped permutation importance: 885 test rows, 30 repeats, seed 42, scorer accuracy — `figures/E_feature_importance_permutation.png`, `outputs/E_feature_importance_permutation.csv`
- [x] Xuất tree, confusion matrix và classification report M3
- [x] Snapshot raw row M0/M1/M2a/M2b và hash 11 artifact D trước/sau evaluation
- [x] Run A/Run B độc lập, validator PASS, execution count 1→10, không stored error/path máy cá nhân
- [x] Tích hợp `main` tại `a29d356`, bảo vệ handoff D `6d558b1` và resolve tài liệu dùng chung
- [x] Tạo `requirements-lock.txt`, kernel `lab2-canonical` và lệnh chạy không ghi timing metadata
- [x] Bàn giao số liệu/artifact canonical để B và các role dùng trong pha viết report
- [x] Hoàn thiện mục f.3 bằng tiếng Anh: mô tả phương pháp, model setting/cây M3, accuracy/error rate, confusion matrix, Gini/MDI, grouped permutation importance, giải thích trade-off và lưu ý đạo đức; không còn `\todo` trong section Role E
- [x] Cài MiKTeX 25.12, biên dịch `docs/report/report.pdf` thành công và kiểm tra trực quan toàn bộ trang f.3

**Trạng thái bàn giao:** mọi section report đã hoàn tất. Slide/video do nhóm quản lý ngoài workspace và phải được đối chiếu với số canonical trước khi đóng gói.

## Quyết định đã chốt
- Accuracy M3 so với M0: 0,5412 so với 0,6689; giảm 0,1277 (12,77 điểm phần trăm) sau khi loại thông tin kết quả hai học kỳ trong thí nghiệm kiểm soát này.
- Có loại thêm `International` (đa cộng tuyến với `Nationality`) không: Không. M3 chính thức chỉ loại đúng 12 cột bắt buộc để giữ thí nghiệm dễ đối chiếu và còn đúng 24 feature gốc.
- Gini/MDI là train-derived; grouped permutation là kiểm tra bổ sung trên held-out test. Không dùng importance để tune M3 và không diễn giải causal.

## Việc tiếp theo
- Không còn việc Role E trong workspace. Nhóm kiểm tra media/đóng gói theo `Cac_Cong_Viec_Can_Phai_Lam.md`; người dùng review rồi tự commit/push.

## Manifest bàn giao code E

- Base Role E: `0969118`; implementation Role E: `33b21fa`; integration main: `a29d356`; handoff Role D được bảo vệ: `6d558b1`.
- Environment: Python 3.14.0; NumPy 2.3.4; pandas 2.3.3; SciPy 1.17.1; scikit-learn 1.9.0; Matplotlib 3.11.1; seaborn 0.13.2; imbalanced-learn 0.14.2; ucimlrepo 0.0.7; joblib 1.5.3; threadpoolctl 3.6.0; nbformat 5.11.1; nbconvert 7.17.1; IPython 9.17.0; ipykernel 7.3.0. `pip check`: PASS.
- Lock canonical: `requirements-lock.txt` SHA-256 `41105bcc92fa60b4fb08978b19b69077909bc3fae817cc55b418a2c7c54354f7`.
- M3 full precision: train accuracy 1.0; test accuracy 0.5412429378531074; error rate 0.4587570621468926; precision macro 0.49208976226946116; recall macro 0.4943895183808582; macro-F1 0.49305009179124043; ROC-AUC macro 0.6253549801464316; recall Dropout/Enrolled/Graduate 0.5316901408450704 / 0.3270440251572327 / 0.6244343891402715; depth 30; leaves 963.
- Protected non-M3 raw-row SHA-256 trước/sau: `2d5d37b708195d0560757698f0a0b731eb77296dad077045f391d17fc3374d15`.
- Hai Run All liên tiếp trên integration main có cùng hash cho notebook, `results.csv`, classification report M3, hai CSV importance và bốn PNG E. Notebook có 22 cell, 10 code cell, execution 1→10, không lỗi và không timing metadata.
- `outputs/results.csv` SHA-256: `63009e839fac73d3460da31a612e3435fb8fd332419cf1b698ae6fee99e02007`; đúng một row cho mỗi M0/M1/M2a/M2b/M3.

Artifact E canonical SHA-256:

- `notebooks/05_improve_features.ipynb`: `f3ed11764e888fa6716b7ca8f698c734d7544ec62feccd9a4334de9d51d07339`
- `outputs/classification_report_M3.txt`: `9a4df1e72e522e9be43f3d262b8f35dbfdcafa17578fb361257bf8aeb5644a8b`
- `outputs/E_feature_importance_comparison.csv`: `119d56393bcb2ab366a6f42e72af1126694f20bc8b72a41361cadd82f4f1f631`
- `outputs/E_feature_importance_permutation.csv`: `7f3c32662d98e5af35849da19a97b479e1c868c473666367fc14abbb9034056c`
- `figures/E_cm_M3.png`: `b02d913eb8e39410c03c6b07e4e3e516eb0463d43e635a64d17705e4976e6067`
- `figures/E_tree_M3.png`: `d59cea8c64f616702dfdd88b3bb16119154495f29a1b5fbabe24d107ea77440a`
- `figures/E_feature_importance.png`: `f7c1d3b5e955f9fae92cb80bf797fa3a721c57e9998fa65a122a5c3e2dce822a`
- `figures/E_feature_importance_permutation.png`: `eac66257924cc89c9a7e0f187aa1421dd60cda2f3b48b6e61f1dffa0933b957b`

Trong audit cuối, notebook D được Run All bằng kernel canonical để khép execution count 1→13, không đổi code thí nghiệm hay artifact; SHA-256 hiện tại là `41b9590a6f58535a50f778767a1e563382dfd2a65a3751405851fe58e8b8e3cb`. `results.csv`, hai classification report và sáu hình D giữ nguyên byte. Không lưu hash của README/progress/report source ở đây vì các tài liệu đó tiếp tục được đồng bộ trong vòng audit cuối; dùng Git diff và manifest bản nộp để kiểm tra phiên bản cuối.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

> Các entry dưới đây là snapshot lịch sử tại thời điểm được ghi. Khi số trang,
> phiên bản, TODO hoặc trạng thái cũ khác phần đầu file, phần **Trạng thái hiện
> tại** và artifact canonical mới nhất được ưu tiên.

### 2026-09-01 — chuẩn hóa metadata progress cuối
- Đã làm gì: điền owner thật, loại entry template rỗng và làm mềm cách mô tả chênh lệch M3 thành kết quả sau khi loại feature trong thí nghiệm kiểm soát.
- Kết quả: progress Role E không còn placeholder; attribution, metric và availability caveat khớp report/runbook canonical.
- Vướng gì / để lại cho phiên sau: không.

### 2026-09-01 — audit f.3 và attribution cuối
- Đã làm gì: đối chiếu metric/importance/cây/confusion matrix M3, làm rõ giả định thời điểm có feature và đồng bộ trạng thái report/media. Xác minh commit `0969118` là công việc Role E dù subject ghi nhầm `[C]`.
- Kết quả: không còn finding mở thuộc Role E; attribution trong nội dung report không dựa vào prefix commit sai. Việc đổi subject của commit đã công bố chỉ là tùy chọn Git-history do con người phối hợp thực hiện theo runbook.
- Vướng gì / để lại cho phiên sau: không.

### 2026-08-30 — hoàn thiện report f.3 của Role E
- Đã làm gì: Đọc lại toàn bộ đề gốc 6 trang, hướng dẫn/phân quyền, source dùng chung, notebook M3, kết quả CSV/classification report và bốn hình E; chuyển nội dung đã kiểm chứng thành section LaTeX hoàn chỉnh. Cài MiKTeX 25.12 theo chế độ user, cài các package cần thiết và chạy chuỗi biên dịch LaTeX/BibTeX.
- Kết quả: Mục f.3 có đủ bốn thành phần đề yêu cầu, thêm bảng exclusion/model setting, bảng metric M0–M3, bảng class-level, cây M3, confusion matrix, Gini/MDI và grouped permutation importance. `report.pdf` biên dịch thành công 30 trang; cross-reference/citation ổn định, không có LaTeX error, undefined reference/citation hoặc overfull box. Đã render và kiểm tra trực quan các trang 21–25; xác nhận 0 `\todo` trong f.3.
- Vướng gì / để lại cho phiên sau: Role E không còn blocker. Toàn report vẫn còn placeholder thuộc Role lead/B/D trong a/d/e/f.2; Role E không sửa các file ngoài quyền sở hữu.

### 2026-08-30 — audit tích hợp cuối trước pha report/media
- Đã làm gì: Chạy lại pipeline canonical 01→06, kiểm tra độc lập schema/metrics/hash/artifact, chuẩn hóa metadata notebook và đối chiếu toàn bộ tài liệu chung với kết quả thật.
- Kết quả: M3 giữ nguyên toàn bộ metric và artifact phân tích; notebook execution 1→10, không error/warning/timing/path máy cá nhân. Hash manifest phía trên là trạng thái canonical hiện tại. Thay đổi duy nhất ngoài E có liên quan là chuẩn hóa cách render Styler của notebook D, không đổi metric hay hình D.
- Vướng gì / để lại cho phiên sau: Không có blocker kỹ thuật. Pha report chỉ cần chuyển nội dung đã kiểm chứng vào section f.3 và dùng đúng số liệu/artifact này.

### 2026-08-30 — Tích hợp Role E với main mới nhất
- Đã làm gì: Role A/Integrator merge `origin/main` `a29d356` vào branch E ở chế độ chưa commit; resolve README và tài liệu Git theo artifact thật; cập nhật provenance sang handoff D `6d558b1`; tạo lock đầy đủ cho Python 3.14.0; đăng ký kernel `lab2-canonical`; đổi lệnh canonical sang `python -m nbconvert` với kernel định danh và `record_timing=False`.
- Kết quả: Hai Run All liên tiếp PASS và bit-for-bit giống nhau cho 9 file E, gồm chính notebook. Notebook có execution 1→10, 0 stored error, 0 timing metadata và 8 thông báo PASS. `results.csv` có đúng một row cho mỗi model; metric M3 giữ nguyên. Kiểm tra SHA-256 độc lập xác nhận 11 artifact D bất biến ở cả hai run.
- Vướng gì / để lại cho phiên sau: Không còn blocker kỹ thuật. Repo đang dừng trước merge commit theo quy ước chỉ người dùng được `git add`/`git commit`/`git push`.

### 2026-08-30 — Hoàn thiện code E theo kế hoạch canonical
- Đã làm gì: Dựng môi trường đúng Python 3.14.0/scikit-learn 1.9.0 và toàn bộ pin; thêm environment fail-fast, provenance, snapshot raw non-M3 rows, hash 11 artifact D, portable output path, Gini/MDI caveat và held-out grouped permutation importance vào notebook. Đồng bộ đúng đoạn Role E trong README/AGENT/docs kỹ thuật; không tạo hoặc sửa report, slide, video.
- Kết quả: Run A và Run B trên hai bản sao/kernel độc lập đều PASS và tạo artifact bit-for-bit giống nhau. Main run cũng khớp toàn bộ hash. M3 giữ nguyên metric canonical; permutation CSV có 72 row (36 M0 + 24 M3 available + 12 M3 unavailable), dùng 30 repeats/seed 42/accuracy và giữ one-hot group hợp lệ. Non-M3 raw row cùng 11 artifact D bất biến.
- Vướng gì / để lại cho phiên sau: Chưa có commit lock môi trường dùng chung do A/integration owner sở hữu. Report/References, slide và video được người dùng loại khỏi phạm vi lần này.

### 2026-08-29 — Kiểm tra tích hợp E sau commit D
- Đã làm gì: Đối chiếu lịch sử `outputs/results.csv`, xác nhận commit E `04ee0bd` từng tái sinh nhầm hai dòng M2a/M2b theo môi trường khác và commit D `76891d6` đã phục hồi số canonical. Chạy lại sạch 9/9 code cell của notebook E trên HEAD hiện tại, kiểm tra hash hai dòng M2a/M2b trước/sau, schema/độ duy nhất của 5 model, artifact và hình ảnh E.
- Kết quả: Tất cả quality gate PASS; không có cell lỗi. M3 giữ nguyên test accuracy 0,5412, macro-F1 0,4931, depth 30 và 963 leaf. Hash M2a/M2b trước và sau lần chạy E giống hệt nhau (`0cbb1ad1...138848b0`), nên notebook E hiện không còn ghi đè hay làm thay đổi kết quả Role D. `results.csv` có đúng một dòng cho mỗi M0/M1/M2a/M2b/M3 và đúng author.
- Vướng gì / để lại cho phiên sau: Artifact canonical của D dùng scikit-learn 1.9.0, còn môi trường kiểm tra E hiện dùng 1.8.0; không ảnh hưởng lần chạy E hoặc dữ liệu D, nhưng nhóm vẫn nên khóa một môi trường chung trước lần chạy tổng cuối.

### 2026-08-29 — Rà soát sau cập nhật Role D
- Đã làm gì: Kiểm tra commit mới nhất của D; xác nhận D không sửa pipeline dùng chung hay notebook E. Chạy lại toàn bộ 9 code cell của `05_improve_features.ipynb`; bổ sung bảng phiên bản môi trường, fingerprint split/target, guardrail lọc cột, kiểm tra feature thực sự được cây sử dụng và đối soát dòng M3 trong `results.csv`.
- Kết quả: Tất cả quality gate PASS. M3 vẫn loại đúng 12 feature, giữ 24 feature gốc/78 cột mã hóa, test accuracy 0,5412 và macro-F1 0,4931. Biểu đồ importance nay gộp các dummy one-hot về feature UCI gốc và dùng chung trục x; thêm file số liệu `outputs/E_feature_importance_comparison.csv`. Không thay đổi metric chính thức hay file của role khác.
- Vướng gì / để lại cho phiên sau: Repo hiện ghi artifact D được tạo bằng scikit-learn 1.9.0, còn artifact E được tái lập bằng 1.8.0; nhóm nên chốt một phiên bản trước lần chạy tổng cuối. Đây là việc tích hợp chung, không phải lỗi logic của M3.

### 2026-08-29
- Đã làm gì: Đọc đề gốc, đặc tả kỹ thuật, quy ước repo; kiểm tra pipeline A–D; hoàn thiện và chạy toàn bộ `05_improve_features.ipynb`.
- Kết quả: M3 dùng 24 feature gốc/78 cột sau one-hot, test accuracy 0,5412, error rate 0,4588, macro-F1 0,4931; đã sinh cây, confusion matrix, classification report, biểu đồ importance và dòng M3 trong `results.csv`. Tất cả quality gates của notebook đều PASS. A–C tái lập được; D có sai khác nhẹ theo phiên bản scikit-learn nên cần Role D khóa phiên bản trước khi bàn giao cuối.
- Vướng gì / để lại cho phiên sau: Phần code/notebook không còn vướng; report, slide và video để sau theo yêu cầu hiện tại.
