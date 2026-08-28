# Tiến độ — Role D (Improvement 2: Class Imbalance)

> Chỉ [Tên thành viên D] và agent trong phiên làm việc của D được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role D (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: chưa có)_
- Đang làm: —
- Bị chặn bởi: — _(nếu `src/data.py` chưa có: đang dùng tạm `load_iris()` để viết logic)_

## Đã xong
- [ ] Đọc paper SMOTE (Chawla et al., 2002)
- [ ] Train M2a: `class_weight='balanced'`
- [ ] Train M2b: SMOTE — **chỉ trên `X_train`**, kiểm tra lại không áp dụng trước khi split
- [ ] Gọi `evaluate_model()` từ `src/evaluate.py`
- [ ] Bảng so sánh recall từng lớp M0 vs M2a vs M2b
- [ ] Xuất `tree_M2a.png` (⚠️ đừng quên — đề yêu cầu hình cây cho mọi cải tiến), `cm_M2a.png`, `cm_M2b.png`

## Quyết định đã chốt
- Accuracy tổng M2a so với M0: _(điền — nếu giảm, đó là kết quả đúng, xem `AGENT.md` Mục 3)_
- Recall lớp Enrolled thay đổi thế nào: _(điền)_

## Việc tiếp theo
- —

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
