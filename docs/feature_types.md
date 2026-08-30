# Phân loại kiểu feature thực tế

> Viết bởi Role A. Nguồn: chạy trực tiếp trên `data/raw/data.csv` (không copy từ UCI metadata) +
> đối chiếu `docs/02-DATASET-VA-CONG-VIEC.md` Phần A4/B1.

## Số liệu thực tế đã xác nhận

- `df.shape` = **(4424, 37)** → 36 feature + 1 cột `Target`
- `df.isnull().sum().sum()` = **0** — không có missing value
- Phân bố target: Graduate 2209 (49.9%), Dropout 1421 (32.1%), Enrolled 794 (17.9%) — khớp Phần A3
- Xác nhận chênh lệch 36 (UCI) vs 34 (bài báo, Phần A2): 2 cột dư ra là `Previous qualification (grade)` và `Admission grade`, đúng như cảnh báo trong `docs/02`

> Lưu ý tên cột: dataset thực tế dùng `Marital Status` (viết hoa S) và `Nacionality` (đúng chính tả gốc UCI, không phải "Nationality"). `src/data.py` dùng đúng tên cột thực tế này.

## Xử lý trong `src/data.py::load_and_preprocess()`

| Cột | Số giá trị | Xử lý | Lý do |
|---|---|---|---|
| `Marital Status` | 6 | **One-hot** | Ít giá trị, không có thứ tự |
| `Application mode` | 18 | **One-hot** | Ít giá trị, không có thứ tự |
| `Course` | 17 | **One-hot** | Ít giá trị, là feature quan trọng (⭐ Phần A5) — one-hot giúp split đọc được kiểu "có phải ngành X không" |
| `Previous qualification` | 17 | **One-hot** | Ít giá trị, không có thứ tự |
| `Mother's qualification` | 29 | Giữ nguyên mã số | Nhiều giá trị — one-hot sẽ tạo quá nhiều cột thưa |
| `Father's qualification` | 34 | Giữ nguyên mã số | Nhiều giá trị |
| `Mother's occupation` | 32 | Giữ nguyên mã số | Nhiều giá trị |
| `Father's occupation` | 46 | Giữ nguyên mã số | Nhiều giá trị nhất trong dataset |
| `Nacionality` | 21 | Giữ nguyên mã số | Nhiều giá trị; tương quan Pearson với `International` là 0.791. Correlation không tự nó quyết định feature importance |
| `Application order` | 8 | Giữ nguyên (ordinal) | Có thứ tự tự nhiên (nguyện vọng 1, 2, 3...) |

Sau one-hot: **90 cột feature** (từ 36 gốc, trừ `Target`, cộng thêm các cột dummy).

## Toàn bộ 36 feature theo 6 nhóm (tham chiếu, không lặp lại giải thích — xem `docs/02` Phần A4)

### Nhóm 1 — Nhân khẩu học
`Marital Status` (category, one-hot), `Nacionality` (category, giữ mã số), `Displaced` (binary), `Gender` (binary), `Age at enrollment` (numeric), `International` (binary)

### Nhóm 2 — Kinh tế xã hội
`Mother's qualification`, `Father's qualification`, `Mother's occupation`, `Father's occupation` (category, giữ mã số), `Educational special needs` (binary), `Debtor` (binary), `Tuition fees up to date` (binary, ⭐ quan trọng), `Scholarship holder` (binary)

### Nhóm 3 — Kinh tế vĩ mô
`Unemployment rate`, `Inflation rate`, `GDP` — đều numeric liên tục, phụ thuộc năm nhập học chứ không phải cá nhân sinh viên

### Nhóm 4 — Học vấn lúc nhập học
`Application mode` (category, one-hot), `Application order` (ordinal, giữ nguyên), `Course` (category, one-hot, ⭐ quan trọng), `Daytime/evening attendance` (binary), `Previous qualification` (category, one-hot), `Previous qualification (grade)` (numeric), `Admission grade` (numeric)

### Nhóm 5 — Kết quả học kỳ 1
6 cột `Curricular units 1st sem (...)` — tất cả numeric liên tục/đếm

### Nhóm 6 — Kết quả học kỳ 2
6 cột `Curricular units 2nd sem (...)` — tất cả numeric liên tục/đếm, `2nd sem (approved)` và `2nd sem (grade)` là 2 feature quan trọng nhất (⭐ Phần A5)

## Không chuẩn hóa (scale)

Theo `docs/02` Phần B2: decision tree không cần `StandardScaler`/`MinMaxScaler`. `load_and_preprocess()` không áp dụng bước này.

## Split

`get_train_test()` dùng `train_test_split(test_size=0.2, stratify=y, random_state=42)` — split duy nhất của cả nhóm, không notebook nào được tự split lại (Phần B3).
