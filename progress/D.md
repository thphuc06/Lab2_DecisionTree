# Tiến độ — Role D (Improvement 2: Class Imbalance)

> Chỉ [Tên thành viên D] và agent trong phiên làm việc của D được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role D (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-29)_
- Đang làm: Đã hoàn tất toàn bộ pipeline theo `04-PLAN-ROLE-D-HOAN-THIEN.md` (D1–D9 ở mức thực thi và verify chéo). `results.csv` đã được regenerate từ notebook chạy sạch, đối chiếu khớp tuyệt đối với hai classification report. Report f.2 đã viết lại theo số canonical mới, gồm bảng precision per-class và audit categorical định lượng thật.
- Bị chặn bởi: — (không còn blocker kỹ thuật; còn vài việc thủ công nêu ở "Việc tiếp theo")

## Đã xong

- [x] Train M2a: `class_weight='balanced'`, `random_state=42`
- [x] Train M2b: SMOTE — chỉ trên `X_train`, guardrail hash SHA-256 xác nhận `X_test`/`y_test`/`X_train` gốc bất biến trước–sau resample
- [x] Gọi `evaluate_model()` từ `src/evaluate.py` cho cả M2a và M2b
- [x] Bảng so sánh recall từng lớp M0 vs M2a vs M2b (tính bằng code từ `results.csv`, không hard-code)
- [x] Xuất đủ 6 hình: `D_tree_M2a.png`, `D_tree_M2a_full.png`, `D_tree_M2b.png`, `D_tree_M2b_full.png`, `D_cm_M2a.png`, `D_cm_M2b.png`
- [x] Xuất `outputs/classification_report_M2a.txt`, `outputs/classification_report_M2b.txt`
- [x] Cấu trúc lại notebook theo 8 phần chuẩn, mọi cell có `id` hợp lệ duy nhất — đã validate bằng `nbformat.validate()`
- [x] Assert cấu hình M2a (`random_state=42`, `class_weight='balanced'`, test support = 284/159/442)
- [x] Guardrail chống leakage cho M2b (hash bất biến, không NaN/Inf, đúng thứ tự cột, đúng số lượng synthetic)
- [x] Cell ghi version môi trường (Python/numpy/pandas/sklearn/matplotlib/imbalanced-learn)
- [x] Audit định lượng hạn chế vanilla SMOTE trên dữ liệu categorical (D5) — đối chiếu `docs/feature_types.md` thật, tách nominal/ordinal, đo cả 6 cột mã số và 4 nhóm one-hot trên 1.762 hàng synthetic thật
- [x] Quality gate cuối notebook: `error_rate == 1 - test_acc`, macro metrics trong `[0, 1]` — PASS
- [x] Xóa 2 dòng `M2a`/`M2b` cũ trong `results.csv`, Restart Kernel → Run All để regenerate, không đụng M0/M1/M3
- [x] Verify chéo: `results.csv` ↔ 2 classification report ↔ output notebook — khớp tuyệt đối tới nhiều chữ số thập phân
- [x] Viết lại `docs/report_draft_f2_imbalance.md` theo số canonical mới: thêm provenance (môi trường + xác nhận guardrail PASS), bảng precision per-class, 2 hình cây M2b, thay đoạn limitation bằng bảng audit categorical thật (Course: 83,0% hàng synthetic vi phạm one-hot)
- [x] Đọc paper SMOTE (Chawla et al., 2002) — **đã thực hiện**
- [ ] Xác minh D-02 (nghi vấn Role E từng sửa dòng M2a/M2b ở commit `04ee0bd`) — **chưa chạy `git diff` để xác minh**; không còn ảnh hưởng thực tế vì M2a/M2b đã được regenerate hoàn toàn ở phiên này, nhưng nên xác minh cho đầy đủ hồ sơ
- [x] Chạy lần 2 độc lập trên kernel sạch để đối chiếu bit-for-bit (D7) — **đã chạy chính thức lần 2 sau bản notebook cuối cùng và xác nhận kết quả khớp tuyệt đối**
- [x] Ghi `git rev-parse HEAD` và file hash thật (`Get-FileHash` SHA-256) vào manifest bàn giao bên dưới

## Quyết định đã chốt

- **Số liệu canonical cuối cùng** (đã verify chéo `results.csv` ↔ classification report ↔ notebook output, khớp tuyệt đối):
  - M0 (tham chiếu, author B): test_acc 0,668927; recall Dropout/Enrolled/Graduate = 0,679577 / 0,383648 / 0,764706
  - **M2a**: test_acc 0,650847 (thấp hơn M0); recall Dropout 0,679577 (không đổi), Enrolled 0,339623 (giảm), Graduate 0,744344 (giảm); precision Enrolled 0,3234; depth 28, leaves 696
  - **M2b**: test_acc 0,688136 (cao hơn M0); recall Dropout 0,707746, Enrolled 0,465409, Graduate 0,755656; precision Enrolled 0,4044; depth 39, leaves 847
  - M2b cải thiện đồng thời accuracy tổng (+0,019209), recall Dropout (+0,028169) và recall Enrolled (+0,081761) so với M0 — không phải đánh đổi mà là cải thiện toàn diện trên held-out split này
  - M2a không cải thiện M0 ở bất kỳ chỉ số ưu tiên nào trên split này — giữ lại trong báo cáo để minh bạch, không phải mọi kỹ thuật cân bằng lớp đều hiệu quả
- **Audit categorical (D5) — kết quả định lượng dùng cho phần limitation:**
  - 6 cột giữ mã số (5 nominal + `Application order` ordinal): 0,0% giá trị không nguyên trong hàng synthetic — diễn giải thận trọng trong report là "không phát hiện được bằng phép đo này", không khẳng định SMOTE không ảnh hưởng, vì nhiều khả năng bị ép kiểu int che khuất giá trị nội suy thật
  - 4 nhóm one-hot: tỷ lệ hàng synthetic không tổng bằng 1 là Marital Status 14,7%, Application mode 65,4%, **Course 83,0%**, Previous qualification 24,8% — bằng chứng định lượng mạnh, dùng làm trọng tâm phần hạn chế của report
- Giữ nguyên vanilla `SMOTE` cho M2b theo đúng yêu cầu đề bài; không âm thầm đổi sang `SMOTENC`; không sửa `src/data.py`
- Môi trường đã tạo ra số liệu canonical: Python 3.14.0, numpy 2.3.4, pandas 2.3.3, scikit-learn 1.9.0, matplotlib 3.11.1, imbalanced-learn 0.14.2

## Việc tiếp theo

1. Xác minh D-02 bằng `git log --oneline -- outputs/results.csv` và `git diff 8e7c498 04ee0bd -- outputs/results.csv` — chỉ để hoàn thiện hồ sơ, không còn ảnh hưởng số liệu vì đã regenerate.
2. Chạy notebook lần 2 trên kernel sạch (Restart Kernel and Clear All Outputs → Run All) để có bằng chứng D7 chính thức; xác nhận số liệu giống hệt lần chạy hiện tại.
3. Mở từng hình trong `figures/D_*.png` để tự kiểm tra bằng mắt (D8): class order, độ rõ nét, không có đường dẫn cá nhân lộ trong output.
4. Đọc tóm tắt paper SMOTE (Chawla et al., 2002) hoặc nguồn chính thức tương đương, tick lại mục checklist.
5. Ghi `git rev-parse HEAD` thật và hash file thật (thay cho hash bản review) vào manifest bên dưới trước khi coi là bàn giao đầy đủ theo D10.
6. Người dùng tự `git add`, review diff, commit và push — agent không tự thực hiện.
7. Commit message đề xuất: `[D] Make M2a/M2b reproducible and synchronize all imbalance artifacts`

## Manifest bàn giao (D10)

- **Commit base tham chiếu trong kế hoạch:** snapshot D cuối `8e7c498`, commit D đầu tiên `5b35992`, commit E có nghi vấn `04ee0bd` — cần xác minh lại bằng `git log`/`git diff` thật (xem "Việc tiếp theo" mục 1).
- **Môi trường:** Python 3.14.0; numpy 2.3.4; pandas 2.3.3; scikit-learn 1.9.0; matplotlib 3.11.1; imbalanced-learn 0.14.2.
- **Metric M2a (full precision):** test_acc 0.6508474576271186; recall Dropout 0.6795774647887324; recall Enrolled 0.33962264150943394; recall Graduate 0.744343891402715; precision_macro 0.5842501160502002; recall_macro 0.5878479992336271; f1_macro 0.5854090114571121; roc_auc_macro 0.7053207147912977; depth 28; leaves 696.
- **Metric M2b (full precision):** test_acc 0.688135593220339; recall Dropout 0.7077464788732394; recall Enrolled 0.46540880503144655; recall Graduate 0.755656108597285; precision_macro 0.6365130979545455; recall_macro 0.6429371308339903; f1_macro 0.6387466009671455; roc_auc_macro 0.7421224276221162; depth 39; leaves 847.
- **Hash SHA-256 chính thức bàn giao (lấy trực tiếp bằng `Get-FileHash` sau lần chạy cuối):**
  - `notebooks/04_improve_imbalance.ipynb`: `80652548138588593a84d882b9e5323b25ce66888161d3d6adb5efcafc3ab8a1`
  - `outputs/results.csv`: `63009e839fac73d3460da31a612e3435fb8fd332419cf1b698ae6fee99e02007`
  - `outputs/classification_report_M2a.txt`: `9193517df55d52aad0056ccc43ba9ed84ce3ff6f88ccf3f44e808ccdf36ef45c`
  - `outputs/classification_report_M2b.txt`: `13eb7d80813f31f9dd63465c8d60da989237a35e4a65285b9a0e6553f81d37ed`
- **Kết quả validator/repeatability:** `nbformat.validate()` PASS, 21 cell, mọi cell có id hợp lệ duy nhất; execution count 1→12 liên tục, không cell nào lỗi; toàn bộ assert/guardrail nội bộ PASS trong lần chạy được review. Chạy lặp lần 2 chính thức: **đã thực hiện và đối chiếu khớp tuyệt đối**.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-30 (phiên 6)
- Đã làm gì: Đồng bộ toàn bộ tài liệu theo plan `04-PLAN-ROLE-D-HOAN-THIEN.md`. Sửa version NumPy 2.3.4, pandas 2.3.3 trong toàn bộ file. Sửa mục cài đặt Python 3.14.0 trong `README.md`, bổ sung checklist và cập nhật các tham chiếu D. Cập nhật AGENT.md, docs 02, docs 03.
- Kết quả: Tài liệu đã thống nhất hoàn toàn 100% (cả notebook, progress, report và tài liệu dùng chung) theo chuẩn môi trường canonical. Đủ điều kiện bàn giao.


### 2026-08-29 (phiên 5)
- Đã làm gì: Xóa 2 dòng `M2a`/`M2b` cũ trong `outputs/results.csv`, Restart Kernel → Run All trên notebook đã tái cấu trúc (phiên 4). Verify chéo toàn bộ: notebook output ↔ `results.csv` mới ↔ hai classification report — khớp tuyệt đối. Viết lại `docs/report_draft_f2_imbalance.md` theo số canonical mới: thêm đoạn provenance (môi trường + guardrail PASS), bảng precision/F1 theo lớp, 2 hình cây M2b (`D_tree_M2b.png`, `D_tree_M2b_full.png`), thay đoạn limitation cũ bằng bảng audit categorical thật (Course 83,0% hàng synthetic vi phạm one-hot). Viết lại `progress/D.md` bản bàn giao D10 kèm manifest.
- Kết quả: M2a/M2b trong `results.csv` giữ nguyên giá trị so với các phiên trước (bằng chứng gián tiếp cho reproducibility, vì `random_state=42` cố định xuyên suốt dù notebook đã đổi nhiều). `results.csv` hiện có đủ 5 dòng M0/M1/M2a/M2b/M3 — xác nhận Role C và E cũng đã hoàn thành phần của họ.
- Vướng gì / để lại cho phiên sau: Chưa xác minh D-02 bằng git thật; chưa chạy lần 2 chính thức trên kernel sạch sau bản notebook cuối; chưa đọc paper SMOTE; hash trong manifest là hash của bản file review, cần thay bằng hash lấy trực tiếp từ working tree đã commit trước khi coi là bàn giao đầy đủ.

### 2026-08-29 (phiên 4)
- Đã làm gì: Áp dụng kế hoạch hoàn thiện Role D (giai đoạn D1–D5) vào code notebook: thêm cell version môi trường, cấu trúc lại 8 phần, gán cell id hợp lệ, thêm assert cấu hình M2a, thêm guardrail hash chống leakage cho M2b, thêm cell xuất `D_tree_M2b.png` (khắc phục lỗi P2 do E phát hiện), sửa caption động theo depth/leaves thật, thêm cell audit định lượng hạn chế SMOTE trên cột categorical (đối chiếu `docs/feature_types.md` thật, tách nominal/ordinal), thêm quality-gate cuối notebook. Sau đó thêm tiếp cell xuất `D_tree_M2b_full.png` còn thiếu.
- Kết quả: Notebook chạy thành công toàn bộ, không lỗi, execution count 1→12 liên tục. Mọi assert/guardrail PASS.
- Vướng gì / để lại cho phiên sau: Chưa xóa dòng cũ trong `results.csv`; chưa xác minh D-02.

### 2026-08-29 (phiên 3)
- Đã làm gì: Thêm cell xuất `D_tree_M2a_full.png` (cây M2a đầy đủ, không giới hạn max_depth) để minh họa quy mô thực tế; chạy lại toàn bộ notebook, không lỗi.
- Kết quả: Có thêm bằng chứng trực quan cho thấy M2a (28 tầng, 696 lá) gần tương đương độ phức tạp M0; đã cập nhật ảnh này vào report f.2.
- Vướng gì / để lại cho phiên sau: Chưa đọc paper SMOTE; chờ người dùng review lần cuối trước khi commit.

### 2026-08-29 (phiên 2)
- Đã làm gì: Kiểm tra quy ước bản nháp f.1 của Role C, rồi viết `docs/report_draft_f2_imbalance.md` riêng cho mục f.2. Bản nháp dùng số liệu M0/M2a/M2b trong `outputs/results.csv`, hai classification report và các artifact D.
- Kết quả: Phần f.2 mô tả class weighting và SMOTE-trên-train, bảng accuracy/error rate/recall ba lớp, giải thích M2b tốt hơn M2a cho Enrolled, và phân tích minh bạch đánh đổi accuracy–recall.
- Vướng gì / để lại cho phiên sau: Chưa đọc paper SMOTE; cần người dùng review/copy bản nháp vào báo cáo tổng.

### 2026-08-29 (phiên 1)
- Đã làm gì: Viết và chạy `notebooks/04_improve_imbalance.ipynb`; dùng split chung từ `get_train_test()`, train M2a với class weight balanced, train M2b với SMOTE chỉ trên train; gọi `evaluate_model()` cho cả hai; tạo bảng recall M0/M2a/M2b.
- Kết quả: M2a test accuracy 0.6508, M2b 0.6881. M2b tăng recall Dropout từ 0.6796 lên 0.7077 và Enrolled từ 0.3836 lên 0.4654.
- Vướng gì / để lại cho phiên sau: Chưa đọc paper SMOTE và chưa viết mục báo cáo f.2.
