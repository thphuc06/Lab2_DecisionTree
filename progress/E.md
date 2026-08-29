# Tiến độ — Role E (Improvement 3: Early-warning Feature Selection)

> Chỉ [Tên thành viên E] và agent trong phiên làm việc của E được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role E (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-30)_
- Đang làm: Phạm vi code/notebook/artifact M3 đã hoàn thiện và tái lập hai lần độc lập dưới môi trường canonical.
- Bị chặn bởi: Repo chưa có commit lock môi trường dùng chung của Role A/integration owner; lần kiểm tra này dùng môi trường local đúng toàn bộ pin. Đây không chặn artifact E hiện tại nhưng cần xử lý trước lần chạy tổng của cả nhóm.

## Đã xong
- [x] Loại đúng 12 cột HK1+HK2 (xem `AGENT.md` Mục 3), giữ 24 feature còn lại
- [x] Train M3, gọi `evaluate_model()` từ `src/evaluate.py`
- [x] So sánh Gini/MDI M0 vs M3 theo feature gốc — `figures/E_feature_importance.png`, `outputs/E_feature_importance_comparison.csv`
- [x] Held-out grouped permutation importance: 885 test rows, 30 repeats, seed 42, scorer accuracy — `figures/E_feature_importance_permutation.png`, `outputs/E_feature_importance_permutation.csv`
- [x] Xuất tree, confusion matrix và classification report M3
- [x] Snapshot raw row M0/M1/M2a/M2b và hash 11 artifact D trước/sau evaluation
- [x] Run A/Run B độc lập, validator PASS, execution count 1→10, không stored error/path máy cá nhân
- [ ] Hỗ trợ B viết mục Analysis of the Tree nếu cần

**Ngoài phạm vi theo yêu cầu người dùng:** report/References, slide và video; nhóm thực hiện chung ở giai đoạn sau.

## Quyết định đã chốt
- Accuracy M3 so với M0: 0,5412 so với 0,6689; giảm 0,1277 (12,77 điểm phần trăm) do loại thông tin kết quả hai học kỳ.
- Có loại thêm `International` (đa cộng tuyến với `Nationality`) không: Không. M3 chính thức chỉ loại đúng 12 cột bắt buộc để giữ thí nghiệm dễ đối chiếu và còn đúng 24 feature gốc.
- Gini/MDI là train-derived; grouped permutation là kiểm tra bổ sung trên held-out test. Không dùng importance để tune M3 và không diễn giải causal.

## Việc tiếp theo
- Integration owner tạo/commit lock môi trường dùng chung khớp manifest canonical bên dưới.
- Khi nhóm bước sang giai đoạn báo cáo/media, dùng các artifact canonical này làm nguồn số liệu; không chạy lại bằng môi trường khác.

## Manifest bàn giao code E

- Base Role E: `0969118`; handoff Role D được bảo vệ: `76891d6`; environment commit dùng chung: chưa có trong lịch sử hiện tại.
- Environment: Python 3.14.0; NumPy 2.3.4; pandas 2.3.3; SciPy 1.17.1; scikit-learn 1.9.0; Matplotlib 3.11.1; seaborn 0.13.2; imbalanced-learn 0.14.2; ucimlrepo 0.0.7; joblib 1.5.3; threadpoolctl 3.6.0; nbformat 5.11.1; nbconvert 7.17.1; IPython 9.17.0; ipykernel 7.3.0. `pip check`: PASS.
- M3 full precision: train accuracy 1.0; test accuracy 0.5412429378531074; error rate 0.4587570621468926; precision macro 0.49208976226946116; recall macro 0.4943895183808582; macro-F1 0.49305009179124043; ROC-AUC macro 0.6253549801464316; recall Dropout/Enrolled/Graduate 0.5316901408450704 / 0.3270440251572327 / 0.6244343891402715; depth 30; leaves 963.
- Protected non-M3 raw-row SHA-256 trước/sau: `2d5d37b708195d0560757698f0a0b731eb77296dad077045f391d17fc3374d15`.
- Run A/Run B/main có cùng hash cho `results.csv`, classification report M3, hai CSV importance và bốn PNG E. Notebook mỗi run có 22 cell, 10 code cell, execution 1→10, không lỗi.
- README SHA-256 trước/sau: `d6ff9d2590dc21f7cd283f155d0742698f304da2ff13804accc2038502b63f3e` / `54bea65bfe6788b496b872a5cd1cccce6d8d375aee7f867543611dae429df1f6`; diff đồng bộ môi trường canonical và thêm phần Role E, không sửa metric/artifact D.

Artifact E canonical SHA-256:

- `notebooks/05_improve_features.ipynb`: `61bc6cb62ea903eacef977c76fb1f0eba1fc482ddf98f35a729b82b3bbb143e0`
- `outputs/classification_report_M3.txt`: `9a4df1e72e522e9be43f3d262b8f35dbfdcafa17578fb361257bf8aeb5644a8b`
- `outputs/E_feature_importance_comparison.csv`: `119d56393bcb2ab366a6f42e72af1126694f20bc8b72a41361cadd82f4f1f631`
- `outputs/E_feature_importance_permutation.csv`: `7f3c32662d98e5af35849da19a97b479e1c868c473666367fc14abbb9034056c`
- `figures/E_cm_M3.png`: `b02d913eb8e39410c03c6b07e4e3e516eb0463d43e635a64d17705e4976e6067`
- `figures/E_tree_M3.png`: `48f2da501befe82dd8379443d34f53b01243cbd390a89adcc45b2bd3914d7f61`
- `figures/E_feature_importance.png`: `f7c1d3b5e955f9fae92cb80bf797fa3a721c57e9998fa65a122a5c3e2dce822a`
- `figures/E_feature_importance_permutation.png`: `eac66257924cc89c9a7e0f187aa1421dd60cda2f3b48b6e61f1dffa0933b957b`

Artifact D được bảo vệ có hash bất biến ở Run A/Run B/main: notebook D `847a24e6...f1ad9`; report f.2 `69229748...cfbe6`; progress D `bfa39c03...995dc`; classification report M2a/M2b `9193517d...6ef45` / `13eb7d80...d37ed`; sáu hình D lần lượt `a9f9962f...99da8`, `2598e5b3...7d32d`, `887e9439...9977`, `5cf3db3c...6e54e`, `6eb0985c...93add`, `8d57ca1e...9c459`.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

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
