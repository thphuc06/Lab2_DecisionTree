# Tiến độ — Role A (Data Lead & Integrator)

> Chỉ [Tên thành viên A] và agent trong phiên làm việc của A được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role A (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: chưa có)_
- Đang làm: —
- Bị chặn bởi: —

## Đã xong
- [ ] Tải dataset qua `ucimlrepo` (id=697), lưu `data/raw/data.csv`
- [ ] Chạy `df.shape`, `df.info()`, `df.isnull().sum()` — xác nhận số liệu thực tế
- [ ] Xác định cột categorical mã hóa số, ghi `docs/feature_types.md`
- [ ] Viết `src/data.py`: `load_and_preprocess()` + `get_train_test()`
- [ ] EDA: phân bố target, thống kê mô tả, heatmap tương quan (4–5 hình)
- [ ] Gộp `results.csv` cuối dự án, vẽ `figures/comparison.png`

## Quyết định đã chốt
_(Ghi các lựa chọn kỹ thuật đã quyết — để agent phiên sau không hỏi lại hoặc tự đổi ý)_
- Số feature đếm thực tế: _(điền sau khi chạy `df.shape`)_
- Cột nào one-hot / cột nào giữ nguyên: _(xem gợi ý ở `docs/02-...` Phần B1, điền quyết định cuối cùng)_

## Việc tiếp theo
- —

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
