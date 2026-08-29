# Tiến độ — Role E (Improvement 3: Feature Selection & Media)

> Chỉ [Tên thành viên E] và agent trong phiên làm việc của E được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role E (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-29)_
- Đang làm: Đã xong phần code/notebook M3; chờ thực hiện report, slide và video ở giai đoạn sau
- Bị chặn bởi: — _(nếu `src/data.py` chưa có: đang dùng tạm `load_iris()` để viết logic)_

## Đã xong
- [x] Loại đúng 12 cột HK1+HK2 (xem `AGENT.md` Mục 3), giữ 24 feature còn lại
- [x] Train M3, gọi `evaluate_model()` từ `src/evaluate.py`
- [x] So sánh feature importance M0 vs M3 — `figures/E_feature_importance.png`
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

### 2026-08-29
- Đã làm gì: Đọc đề gốc, đặc tả kỹ thuật, quy ước repo; kiểm tra pipeline A–D; hoàn thiện và chạy toàn bộ `05_improve_features.ipynb`.
- Kết quả: M3 dùng 24 feature gốc/78 cột sau one-hot, test accuracy 0,5412, error rate 0,4588, macro-F1 0,4931; đã sinh cây, confusion matrix, classification report, biểu đồ importance và dòng M3 trong `results.csv`. Tất cả quality gates của notebook đều PASS. A–C tái lập được; D có sai khác nhẹ theo phiên bản scikit-learn nên cần Role D khóa phiên bản trước khi bàn giao cuối.
- Vướng gì / để lại cho phiên sau: Phần code/notebook không còn vướng; report, slide và video để sau theo yêu cầu hiện tại.

### _(ngày)_
- Đã làm gì:
- Kết quả:
- Vướng gì / để lại cho phiên sau:
