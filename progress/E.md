# Tiến độ — Role E (Improvement 3: Feature Selection & Media)

> Chỉ [Tên thành viên E] và agent trong phiên làm việc của E được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role E (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-29)_
- Đang làm: Phần code/notebook M3 đã hoàn thiện và chạy sạch trên commit D mới nhất; report, slide và video để giai đoạn sau
- Bị chặn bởi: —

## Đã xong
- [x] Loại đúng 12 cột HK1+HK2 (xem `AGENT.md` Mục 3), giữ 24 feature còn lại
- [x] Train M3, gọi `evaluate_model()` từ `src/evaluate.py`
- [x] So sánh feature importance M0 vs M3 theo feature gốc (gộp one-hot) — `figures/E_feature_importance.png`, `outputs/E_feature_importance_comparison.csv`
- [x] Xuất `figures/E_tree_M3.png`
- [ ] Hỗ trợ B viết mục Analysis of the Tree nếu cần
- [ ] Làm slide 12–15 trang
- [ ] Ghép video (kịch bản 12–15 phút, 5 người đều nói)
- [ ] Viết mục References

## Quyết định đã chốt
- Accuracy M3 so với M0: 0,5412 so với 0,6689; giảm 0,1277 (12,77 điểm phần trăm) do loại thông tin kết quả hai học kỳ.
- Có loại thêm `International` (đa cộng tuyến với `Nationality`) không: Không. M3 chính thức chỉ loại đúng 12 cột bắt buộc để giữ thí nghiệm dễ đối chiếu và còn đúng 24 feature gốc.

## Việc tiếp theo
- Viết mục f.3 và References của báo cáo khi nhóm bắt đầu giai đoạn report.
- Làm slide 12–15 trang và ghép video sau khi A hoàn tất notebook so sánh tổng.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

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
