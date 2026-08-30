# Tiến độ — Role B (Baseline & Tree Analysis)

> Chỉ [Tên thành viên B] và agent trong phiên làm việc của B được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role B (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-30)_
- Đang làm: Đã hoàn tất và QA hai section LaTeX d/e; chờ người dùng review để commit/push.
- Bị chặn bởi: —

## Đã xong
- [x] Viết `src/evaluate.py` — `evaluate_model()` tính đủ 16 cột, tự append `results.csv`
- [x] Viết `src/visualize.py` — `plot_tree_figure()`, `export_rules()`
- [x] Train M0 baseline
- [x] Xuất cây đầy đủ + cây rút gọn `max_depth=3` + confusion matrix + `rules_M0.txt`
- [x] Viết phân tích 5 câu (root split, 3 tầng đầu, độ sâu/leaf, overfit, luật IF-THEN)
- [x] Kiểm tra nhanh Gini vs Entropy (không tính vào 3 cải tiến chính — xem `docs/02-...` Phần C0)
- [x] Viết `docs/report_draft_d_e.md` và cập nhật `README.md`
- [x] Hoàn thành kiểm thử cuối và QA trực quan artifact
- [x] Hoàn thiện bản tiếng Anh `docs/report/sections/d_baseline.tex` (6 TODO)
- [x] Hoàn thiện và QA `docs/report/sections/e_analysis.tex` (7 TODO)

## Quyết định đã chốt
- ccp_alpha / criterion baseline dùng: `ccp_alpha=0.0`, criterion mặc định `gini`; không giới hạn depth/split/leaf.
- Kết quả train/test accuracy thực tế: `1.000000` / `0.668927`; error rate `0.331073`; depth `27`; leaves `634`.
- Root split: `Curricular units 2nd sem (approved) <= 4.5`; Gini `0.615292 -> 0.449325`, giảm có trọng số `0.165967`.
- Generalization gap: `0.331073`; 1.267 node, 279 leaf một mẫu, 399 leaf không quá hai mẫu, 100% leaf thuần.
- An toàn tái sử dụng: kiểm tra conflict CSV trước khi chạm artifact; ghi report/PNG/rules qua file tạm rồi thay thế nguyên tử; retry khóa file Windows và coi artifact giống hệt là lần ghi idempotent (không ghi đè trực tiếp); renderer PNG dùng backend Agg nên chạy được cả notebook/script/headless; M0 chỉ serialize tập key tham số ổn định giữa các phiên bản sklearn.

## Việc tiếp theo
- Người dùng review diff và tự commit/push; Role C/D/E có thể tái sử dụng helper của B.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-30 — giai đoạn báo cáo
- Đã làm gì: Đồng bộ `main`, đọc lại đề gốc/quy tắc LaTeX và chuyển toàn bộ 13 TODO của hai mục d--e sang tiếng Anh học thuật. Mục d bổ sung bảng split, metrics đầy đủ, classification report và so sánh Gini--Entropy. Mục e bổ sung phép tính root split, toàn bộ node từ depth 0 đến 3, thống kê độ phức tạp/overfitting, ba luật IF--THEN đầy đủ, cùng phân tích ưu/nhược điểm và giới hạn đạo đức.
- Kết quả: `d_baseline.tex` và `e_analysis.tex` đều không còn TODO. Toàn báo cáo compile thành công bằng `pdflatex`--`bibtex`--`pdflatex`--`pdflatex` (thêm một lượt `pdflatex` để ổn định nhãn); log cuối không có LaTeX error, undefined citation/reference hoặc overfull box. Đã render và kiểm tra trực quan toàn bộ phần Role B trên các trang 9--19: không cắt bảng/hình, không tràn lề, caption ngắn, hình top-3/confusion matrix và các luật đều đọc được.
- Vướng gì / để lại cho phiên sau: Không có lỗi thuộc phạm vi Role B; các TODO còn lại nằm ở section của role khác. Người dùng review diff và tự commit/push.

### 2026-08-29
- Đã làm gì: Đồng bộ `main`; đọc đề gốc và toàn bộ quy định Role B; triển khai `evaluate_model()` với schema 16 cột, ROC-AUC từ `predict_proba`, recall theo tên lớp, artifact báo cáo/CM và ghi CSV idempotent; triển khai `plot_tree_figure()` và `export_rules()` có kiểm tra metadata, tạo thư mục cha và đóng figure. Sau audit trước push, bổ sung preflight conflict trước artifact, ghi artifact nguyên tử, retry/so sánh byte khi Windows khóa file, backend Agg không phụ thuộc GUI/Tk, bộ params M0 ổn định và hướng dẫn + checklist tái sử dụng cho M1 trong README.
- Kết quả: `src/evaluate.py` và `src/visualize.py` đã qua kiểm thử tích hợp. Notebook chạy lại bằng `nbconvert` đủ 13 code cell, execution count 1–13 và không có error; M0 train/test accuracy `1.000000/0.668927`, error `0.331073`, depth `27`, leaves `634`; đã sinh đủ 3 PNG, rules và classification report. Hoàn thành phân tích root/ba tầng đầu/độ phức tạp/overfit/ba luật, viết `docs/report_draft_d_e.md` và cập nhật README. Entropy giảm test accuracy khoảng `0.0158` so với Gini và không được append vào CSV. Đã kiểm tra idempotency/conflict CSV, xác nhận conflict không còn ghi đè artifact, mô phỏng thành công luồng M1 của Role C, chạy kernel từ cả repo root và thư mục `notebooks`, recompute metric độc lập, import/compile, QA trực quan ba PNG, `git diff --check` và phạm vi file Role B.
- Vướng gì / để lại cho phiên sau: Không có; chỉ còn người dùng review và tự commit/push.
