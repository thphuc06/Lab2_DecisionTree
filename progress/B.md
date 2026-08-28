# Tiến độ — Role B (Baseline & Tree Analysis)

> Chỉ [Tên thành viên B] và agent trong phiên làm việc của B được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role B (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: chưa có)_
- Đang làm: —
- Bị chặn bởi: — _(thường là: chờ A push `src/data.py` — xem `progress/A.md`)_

## Đã xong
- [ ] Viết `src/evaluate.py` — `evaluate_model()` tính đủ 16 cột, tự append `results.csv`
- [ ] Viết `src/visualize.py` — `plot_tree_figure()`, `export_rules()`
- [ ] Train M0 baseline
- [ ] Xuất cây đầy đủ + cây rút gọn `max_depth=3` + confusion matrix + `rules_M0.txt`
- [ ] Viết phân tích 5 câu (root split, 3 tầng đầu, độ sâu/leaf, overfit, luật IF-THEN)
- [ ] Kiểm tra nhanh Gini vs Entropy (không tính vào 3 cải tiến chính — xem `docs/02-...` Phần C0)

## Quyết định đã chốt
- ccp_alpha / criterion baseline dùng: _(mặc định `gini`, ghi rõ nếu đổi)_
- Kết quả train/test accuracy thực tế: _(điền sau khi chạy)_

## Việc tiếp theo
- —

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
