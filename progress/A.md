# Tiến độ — Role A (Data Lead & Integrator)

> Chỉ [Tên thành viên A] và agent trong phiên làm việc của A được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role A (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-28)_
- Đang làm: —
- Bị chặn bởi: —

## Đã xong
- [x] Tải dataset qua `ucimlrepo` (id=697), lưu `data/raw/data.csv`
- [x] Chạy `df.shape`, `df.info()`, `df.isnull().sum()` — xác nhận số liệu thực tế
- [x] Xác định cột categorical mã hóa số, ghi `docs/feature_types.md`
- [x] Viết `src/data.py`: `load_and_preprocess()` + `get_train_test()`
- [x] EDA: phân bố target, thống kê mô tả, heatmap tương quan (5 hình, `notebooks/01_eda.ipynb`)
- [ ] Gộp `results.csv` cuối dự án, vẽ `figures/comparison.png` — chờ B/C/D/E train xong 4 model

## Quyết định đã chốt
_(Ghi các lựa chọn kỹ thuật đã quyết — để agent phiên sau không hỏi lại hoặc tự đổi ý)_
- Số feature đếm thực tế: `df.shape` = (4424, 37) → **36 feature + 1 cột `Target`**. Xác nhận chênh lệch 36 (UCI) vs 34 (bài báo): 2 cột dư là `Previous qualification (grade)` và `Admission grade`. `isnull().sum().sum()` = 0.
- Tên cột thực tế khác doc tóm tắt: `Marital Status` (không phải "Marital status"), `Nacionality` (không phải "Nationality") — `src/data.py` dùng đúng tên thật.
- One-hot: `Marital Status` (6), `Application mode` (18), `Course` (17), `Previous qualification` (17). Giữ nguyên mã số: `Mother's/Father's qualification` (29/34), `Mother's/Father's occupation` (32/46), `Nacionality` (21), `Application order` (ordinal). Chi tiết + lý do: `docs/feature_types.md`.
- Sau one-hot: **90 cột feature**. Split: `train_test_split(test_size=0.2, stratify=y, random_state=42)` → train (3539, 90), test (885, 90), tỉ lệ 3 lớp giữ nguyên ở cả 2 tập.
- Smoke test: `DecisionTreeClassifier(random_state=42)` trên output của `get_train_test()` cho test acc = 0.6689 — khớp khoảng kỳ vọng 0.65–0.72 ở `AGENT.md` §3, không có dấu hiệu rò rỉ dữ liệu.

## Việc tiếp theo
- Theo dõi B/C/D/E dùng `get_train_test()` — nếu có yêu cầu thêm hàm/tham số thì cập nhật `src/data.py`.
- Sau khi B/C/D/E có `results.csv`/hình: viết `notebooks/06_comparison.ipynb`, gộp bảng so sánh, vẽ `figures/comparison.png`.
- Viết mục **g. Comparison of Results** và **h. Conclusion** — vẫn phải đợi kết quả 4 model.
- Copy nội dung `docs/report_draft_b_c.md` vào Google Doc chung của nhóm (mục b, c đã viết xong, xem log bên dưới).

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-28 (phiên 2)
- Đã làm gì: Đọc lại toàn bộ `docs/00-DE-BAI-GOC.pdf` (đối chiếu bản gốc, xác nhận `docs/02` không lệch), đọc trực tiếp nội dung 5 hình EDA để lấy số liệu cụ thể, viết bản nháp báo cáo mục **b. Introduction** (lý thuyết decision tree + mục tiêu đồ án, có trích dẫn Quinlan 1986/Breiman 1984/Mitchell 1997/Pedregosa 2011) và **c. Dataset Description** (nguồn, số liệu thực tế, 6 nhóm feature, tiền xử lý, lý do phù hợp decision tree, lưu ý đạo đức) → lưu vào `docs/report_draft_b_c.md`.
- Kết quả: File nháp đầy đủ, có số liệu thật (không phải placeholder), có trích dẫn nguồn. Sẵn sàng để copy vào Google Doc chung.
- Vướng gì / để lại cho phiên sau: Chưa điền mục a (tên nhóm/MSSV/GroupID) — thuộc trách nhiệm Trưởng nhóm, không phải phạm vi A. File nháp viết bằng tiếng Việt theo yêu cầu người dùng phiên này.

### 2026-08-28 (phiên 1)
- Đã làm gì: Cài `ucimlrepo`/`imbalanced-learn`; tải dataset UCI id=697 → `data/raw/data.csv`; viết `src/data.py` (`load_and_preprocess()`, `get_train_test()`) với one-hot cho cột ít giá trị, giữ mã số cho cột nhiều giá trị, stratified split random_state=42; viết `docs/feature_types.md`; dựng và chạy (Restart & Run All qua `nbconvert --execute`) `notebooks/01_eda.ipynb` xuất 5 hình vào `figures/A_*.png`.
- Kết quả: `from src.data import get_train_test` chạy được, trả 4 giá trị đã stratify đúng schema (Definition of Done đạt). Smoke-test DecisionTreeClassifier cho acc trong khoảng kỳ vọng. 5 hình EDA đã xuất: target distribution, correlation heatmap, boxplot curricular units 2nd sem theo target, tuition/scholarship vs target, target theo course.
- Vướng gì / để lại cho phiên sau: Chưa có gì vướng. Notebook đang trỏ `FIG_DIR = Path.cwd().parent / "figures"` — giả định chạy notebook từ trong thư mục `notebooks/` (mặc định của Jupyter), cần lưu ý nếu ai chạy theo cách khác. Chưa viết phần báo cáo (b/c/g/h) vì cần chờ số liệu từ các model khác.
