# Tiến độ — Role C (Improvement 1: Pruning)

> Chỉ [Tên thành viên C] và agent trong phiên làm việc của C được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role C (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-29 — hoàn tất toàn bộ Role C)_
- Đang làm: đã hoàn tất, chờ người dùng review diff và tự commit/push theo quy ước repo.
- Bị chặn bởi: không.

## Đã xong
- [x] Đọc trang sklearn 1.8 về cost-complexity pruning, `GridSearchCV` và `StratifiedKFold`
- [x] Chạy `cost_complexity_pruning_path`, lấy 334 điểm path / 236 alpha duy nhất để CV (đã loại alpha cây một nút)
- [x] Chọn alpha bằng CV trên **train set** (không phải test)
- [x] Grid nhỏ `max_depth` ∈ {5,8,10,15}, `min_samples_leaf` ∈ {1,5,10,20} — đủ 16 cấu hình
- [x] Gọi `evaluate_model()` từ `src/evaluate.py` — không tự viết lại
- [x] Xuất `figures/C_ccp_alpha_curve.png`, `figures/C_tree_M1.png`, bảng grid search trong notebook
- [x] Xuất thêm artifact theo contract chung: `figures/C_cm_M1.png`, `outputs/classification_report_M1.txt`, một dòng M1 trong `outputs/results.csv`
- [x] Viết mục báo cáo `docs/report_draft_f1_pruning.md` bằng số liệu thực, gồm phương pháp, bảng grid, so sánh M0–M1, cơ chế, trade-off và giới hạn
- [x] Restart & Run All bằng kernel mới: 12 code cell chạy liền mạch `1→12`, không có error output; chạy lại idempotent vẫn chỉ có đúng một dòng M1
- [x] Kiểm chứng độc lập trong process mới: tái sinh alpha/grid và tính lại 12 trường số; tất cả khớp `results.csv` trong tolerance `1e-12`
- [x] Kiểm tra trực quan đủ 3 hình Role C; kiểm tra schema 16 cột, artifact không rỗng và phạm vi file đúng quyền sở hữu

## Quyết định đã chốt
- Giao thức: 5-fold `StratifiedKFold(shuffle=True, random_state=42)`, chọn theo mean validation accuracy; tie-break ưu tiên mô hình đơn giản hơn.
- Dữ liệu test: không dùng trong pruning path/CV/grid; chỉ đánh giá đúng một lần sau khi khóa M1.
- alpha cuối cùng chọn: `0.0014874613584826332` (mean CV accuracy `0.747669`; hòa 2 alpha nên chọn alpha lớn hơn).
- max_depth / min_samples_leaf cuối cùng: `5 / 20` (mean CV accuracy của grid winner `0.748235`).
- M1 trên held-out test: accuracy `0.755932`, macro-F1 `0.672925`, ROC-AUC macro `0.847692`; depth `5`, leaves `17`.

## Việc tiếp theo
- Người dùng review `git diff`, sau đó tự `git add` / `git commit` / `git push` theo `AGENT.md`.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-29 — rà soát cuối và sửa finding P3
- Đã làm gì: sửa đơn vị tăng accuracy trong notebook thành “điểm phần trăm”, thay cách gọi “tầng” bằng “độ sâu” trong báo cáo/nhật ký, rồi Restart & Run All toàn bộ notebook.
- Kết quả: output hiển thị đúng `+8.70 điểm phần trăm`; 12 code cell chạy liên tiếp `1→12`, không có error output; M1 và toàn bộ số liệu/artifact không đổi.
- Vướng gì / để lại cho phiên sau: không.

### 2026-08-29 — bắt đầu triển khai
- Đã làm gì: đồng bộ `main`, tạo nhánh `feature/pruning`, kiểm tra đầu vào của Role A/B, đọc tài liệu chính thức theo scikit-learn 1.8, xây dựng và Run All notebook, chọn alpha/grid chỉ bằng train CV, fit và đánh giá M1 một lần trên test.
- Kết quả: M1 khóa tại `ccp_alpha=0.0014874613584826332`, `max_depth=5`, `min_samples_leaf=20`; test accuracy `0.755932`; độ sâu cây giảm từ 27 xuống 5 và số lá giảm từ 634 xuống 17; báo cáo f.1 và mọi artifact bắt buộc đã sinh thành công; Run All/QA độc lập đều pass.
- Vướng gì / để lại cho phiên sau: không.
