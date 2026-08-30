# Tiến độ — Role E (Improvement 3: Early-warning Feature Selection)

> Chỉ [Tên thành viên E] và agent trong phiên làm việc của E được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role E (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-30)_
- Đang làm: Phạm vi code/notebook/artifact M3 và audit tích hợp cuối đã hoàn tất dưới môi trường canonical.
- Bị chặn bởi: —. Role A/Integrator đã tích hợp `main` mới, khóa môi trường và xác minh lại toàn repository trước pha report/media.

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

**Pha tiếp theo (chưa bắt đầu):** hoàn thiện report/References, slide và video từ các artifact canonical; không cần thay đổi thí nghiệm M3.

## Quyết định đã chốt
- Accuracy M3 so với M0: 0,5412 so với 0,6689; giảm 0,1277 (12,77 điểm phần trăm) do loại thông tin kết quả hai học kỳ.
- Có loại thêm `International` (đa cộng tuyến với `Nationality`) không: Không. M3 chính thức chỉ loại đúng 12 cột bắt buộc để giữ thí nghiệm dễ đối chiếu và còn đúng 24 feature gốc.
- Gini/MDI là train-derived; grouped permutation là kiểm tra bổ sung trên held-out test. Không dùng importance để tune M3 và không diễn giải causal.

## Việc tiếp theo
- Khi nhóm bước sang giai đoạn báo cáo/media, dùng các artifact canonical này làm nguồn số liệu; không chạy lại bằng môi trường khác.
- Sau khi người dùng review, tự hoàn tất merge commit và push branch theo quy ước repo.

## Manifest bàn giao code E

- Base Role E: `0969118`; implementation Role E: `33b21fa`; integration main: `a29d356`; handoff Role D được bảo vệ: `6d558b1`.
- Environment: Python 3.14.0; NumPy 2.3.4; pandas 2.3.3; SciPy 1.17.1; scikit-learn 1.9.0; Matplotlib 3.11.1; seaborn 0.13.2; imbalanced-learn 0.14.2; ucimlrepo 0.0.7; joblib 1.5.3; threadpoolctl 3.6.0; nbformat 5.11.1; nbconvert 7.17.1; IPython 9.17.0; ipykernel 7.3.0. `pip check`: PASS.
- Lock canonical: `requirements-lock.txt` SHA-256 `a2e41b2e0286ca9987881ec3a68c7c092c0ca18ce85077832a59cbb223192a0f`.
- M3 full precision: train accuracy 1.0; test accuracy 0.5412429378531074; error rate 0.4587570621468926; precision macro 0.49208976226946116; recall macro 0.4943895183808582; macro-F1 0.49305009179124043; ROC-AUC macro 0.6253549801464316; recall Dropout/Enrolled/Graduate 0.5316901408450704 / 0.3270440251572327 / 0.6244343891402715; depth 30; leaves 963.
- Protected non-M3 raw-row SHA-256 trước/sau: `2d5d37b708195d0560757698f0a0b731eb77296dad077045f391d17fc3374d15`.
- Hai Run All liên tiếp trên integration main có cùng hash cho notebook, `results.csv`, classification report M3, hai CSV importance và bốn PNG E. Notebook có 22 cell, 10 code cell, execution 1→10, không lỗi và không timing metadata.
- `outputs/results.csv` SHA-256: `63009e839fac73d3460da31a612e3435fb8fd332419cf1b698ae6fee99e02007`; đúng một row cho mỗi M0/M1/M2a/M2b/M3.
- README SHA-256: `15f78b6861d781cbca20490de8f32356eef4261065d91e670daaff00dc3a6701`; tài liệu dùng kernel `.venv` định danh và lock canonical, giữ đủ hướng dẫn Role D/E.

Artifact E canonical SHA-256:

- `notebooks/05_improve_features.ipynb`: `f3ed11764e888fa6716b7ca8f698c734d7544ec62feccd9a4334de9d51d07339`
- `outputs/classification_report_M3.txt`: `9a4df1e72e522e9be43f3d262b8f35dbfdcafa17578fb361257bf8aeb5644a8b`
- `outputs/E_feature_importance_comparison.csv`: `119d56393bcb2ab366a6f42e72af1126694f20bc8b72a41361cadd82f4f1f631`
- `outputs/E_feature_importance_permutation.csv`: `7f3c32662d98e5af35849da19a97b479e1c868c473666367fc14abbb9034056c`
- `figures/E_cm_M3.png`: `b02d913eb8e39410c03c6b07e4e3e516eb0463d43e635a64d17705e4976e6067`
- `figures/E_tree_M3.png`: `d59cea8c64f616702dfdd88b3bb16119154495f29a1b5fbabe24d107ea77440a`
- `figures/E_feature_importance.png`: `f7c1d3b5e955f9fae92cb80bf797fa3a721c57e9998fa65a122a5c3e2dce822a`
- `figures/E_feature_importance_permutation.png`: `eac66257924cc89c9a7e0f187aa1421dd60cda2f3b48b6e61f1dffa0933b957b`

Trong audit cuối, notebook D chỉ được chuẩn hóa output Styler để tái lập bit-for-bit, không đổi code thí nghiệm hay artifact D; hash notebook hiện tại là `3b69b94085aeeabcc96314260d6a978c61e1984ab8e8c8f1f159076f121b016e`. Các file D được bảo vệ còn lại giữ nguyên: report f.2 `4617abb3edcdba47a655ec6c5303219e1430628bf77e7155a5962a91ae717f31`; progress D `a2fe6582ef4ccc79b75f43401d37a8085c9af4a26c285636cc9f417bf73097cb`; classification report M2a/M2b `9193517df55d52aad0056ccc43ba9ed84ce3ff6f88ccf3f44e808ccdf36ef45c` / `13eb7d80813f31f9dd63465c8d60da989237a35e4a65285b9a0e6553f81d37ed`; sáu hình D lần lượt `a9f9962fe1fefedcef310f310d502a6a54155c8e289f16e6b536c17d18b99da8`, `2598e5b30ae70461b36829b4e1aa8b41f9eded9f61484390b26817f0f097d32d`, `887e94393a0a53489e0ebb654773bffa96079932049285457dd535504a4af977`, `5cf3db3c72d79e5921bdb357a10f96d4eb35b598c7cab5b5c2089bcf3156e54e`, `6eb0985ce38760306e18ccc46c572020084c88596efebf0e77669d060a993add`, `8d57ca1e203f2a07fb23a2895efdb3afdc4420c189dda27931d6b2d62109c459`.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

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

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
