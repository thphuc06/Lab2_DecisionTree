# Tiến độ — Role D (Improvement 2: Class Imbalance)

> Chỉ [Tên thành viên D] và agent trong phiên làm việc của D được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role D (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-29)_
- Đang làm: Đã hoàn thành triển khai M2a/M2b và bản nháp báo cáo f.2; chờ người dùng review.
- Bị chặn bởi: —

## Đã xong
- [ ] Đọc paper SMOTE (Chawla et al., 2002) — chưa thực hiện trong phiên này
- [x] Train M2a: `class_weight='balanced'`
- [x] Train M2b: SMOTE — **chỉ trên `X_train`**, kiểm tra lại không áp dụng trước khi split
- [x] Gọi `evaluate_model()` từ `src/evaluate.py`
- [x] Bảng so sánh recall từng lớp M0 vs M2a vs M2b
- [x] Xuất `D_tree_M2a.png`, `D_cm_M2a.png`, `D_cm_M2b.png`
- [x] Viết bản nháp mục báo cáo f.2 trong `docs/report_draft_f2_imbalance.md`

## Quyết định đã chốt
- M2a: test accuracy 0.6508, thấp hơn M0 0.6689; recall Dropout giữ nguyên 0.6796, Enrolled giảm từ 0.3836 xuống 0.3396, Graduate giảm từ 0.7647 xuống 0.7443.
- M2b: train SMOTE với `SMOTE(random_state=42)` chỉ trên `X_train, y_train`; đánh giá trên split gốc. Test accuracy 0.6881; recall Dropout 0.7077, Enrolled 0.4654, Graduate 0.7557.
- M2b cải thiện recall Dropout +0.0282 và Enrolled +0.0818 so với M0; đây là model ưu tiên cho phần phân tích M2.

## Việc tiếp theo
- Đọc paper SMOTE để hoàn tất checklist tài liệu.
- Copy/review mục báo cáo f.2, phân tích M2a không hiệu quả trên split này và M2b cải thiện recall lớp thiểu số.
- Người dùng review diff rồi tự commit/push nếu muốn.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-29 (phiên 2)
- Đã làm gì: Kiểm tra quy ước bản nháp f.1 của Role C, rồi viết `docs/report_draft_f2_imbalance.md` riêng cho mục f.2. Bản nháp dùng số liệu M0/M2a/M2b trong `outputs/results.csv`, hai classification report và các artifact D.
- Kết quả: Phần f.2 mô tả class weighting và SMOTE-trên-train, bảng accuracy/error rate/recall ba lớp, giải thích M2b tốt hơn M2a cho Enrolled, và phân tích minh bạch đánh đổi accuracy–recall.
- Vướng gì / để lại cho phiên sau: Chưa đọc paper SMOTE; cần người dùng review/copy bản nháp vào báo cáo tổng.

### 2026-08-29 (phiên 1)
- Đã làm gì: Viết và chạy `notebooks/04_improve_imbalance.ipynb`; dùng split chung từ `get_train_test()`, train M2a với class weight balanced, train M2b với SMOTE chỉ trên train; gọi `evaluate_model()` cho cả hai; tạo bảng recall M0/M2a/M2b.
- Kết quả: M2a test accuracy 0.6508, M2b 0.6881. M2b tăng recall Dropout từ 0.6796 lên 0.7077 và Enrolled từ 0.3836 lên 0.4654.
- Vướng gì / để lại cho phiên sau: Chưa đọc paper SMOTE và chưa viết mục báo cáo f.2.
