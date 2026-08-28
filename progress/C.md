# Tiến độ — Role C (Improvement 1: Pruning)

> Chỉ [Tên thành viên C] và agent trong phiên làm việc của C được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role C (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: chưa có)_
- Đang làm: —
- Bị chặn bởi: — _(nếu `src/data.py` chưa có: đang dùng tạm `load_iris()` để viết logic — xem `AGENT.md` Mục 5 Role C)_

## Đã xong
- [ ] Đọc trang sklearn về cost-complexity pruning
- [ ] Chạy `cost_complexity_pruning_path`, lấy mảng `ccp_alphas`
- [ ] Chọn alpha bằng CV trên **train set** (không phải test)
- [ ] Grid nhỏ `max_depth` ∈ {5,8,10,15}, `min_samples_leaf` ∈ {1,5,10,20}
- [ ] Gọi `evaluate_model()` từ `src/evaluate.py` — không tự viết lại
- [ ] Xuất `ccp_alpha_curve.png`, `tree_M1.png`, bảng grid search

## Quyết định đã chốt
- alpha cuối cùng chọn: _(điền sau khi chạy CV)_
- max_depth / min_samples_leaf cuối cùng: _(điền)_

## Việc tiếp theo
- —

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
