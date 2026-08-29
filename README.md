# Lab 2 - Decision Tree Modeling and Improvement

Đồ án môn Trí tuệ nhân tạo xây dựng một cây quyết định baseline và ba hướng cải tiến trên bộ dữ liệu UCI **Predict Students' Dropout and Academic Success**. Mục tiêu là đánh giá mô hình, giải thích cấu trúc cây và kiểm chứng các cách giảm overfitting, xử lý mất cân bằng lớp và hỗ trợ dự báo sớm.

## Cấu trúc chính

```text
data/raw/       Dữ liệu gốc
src/            Pipeline dữ liệu, đánh giá và trực quan hóa dùng chung
notebooks/      EDA, baseline, ba cải tiến và notebook so sánh
figures/        Hình cây, confusion matrix và biểu đồ
outputs/        Bảng metrics, classification report và luật cây
docs/           Đề bài, quy định kỹ thuật và bản thảo báo cáo
progress/       Nhật ký theo role
```

## Cài đặt

```powershell
# Cách 1: Python Launcher đã nhận CPython 3.14
py -3.14 -m venv .venv

# Cách 2: nếu `py -3.14 --version` báo không tìm thấy Python
& "C:\duong-dan-den-python314\python.exe" -m venv .venv

# Dùng trực tiếp interpreter trong venv để tránh nhầm Python trên PATH
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip install notebook nbconvert ipykernel
```

Kiểm tra `.\.venv\Scripts\python.exe --version` phải chạy được trước khi tiếp tục. Trên macOS/Linux, dùng `python3 -m venv .venv` và thay `Scripts\python.exe` bằng `.venv/bin/python`.

Artifact M0 hiện tại đã được tái lập với môi trường canonical: Python 3.14.0, `scikit-learn==1.9.0`, `imbalanced-learn==0.14.2`, `pandas==2.3.3`, `numpy==2.3.4`, và `matplotlib==3.11.1` (các direct pin đã có trong `requirements-lock.txt`). Hướng dẫn cài từ manifest/lock đã commit. Không dùng version mở. Thêm lệnh pip check để xác nhận tương thích. Trình tự tích hợp là environment -> D -> E.

## Pipeline dữ liệu dùng chung

Mọi model phải dùng đúng split stratified đã được cố định trong `src/data.py`:

```python
from src.data import get_train_test

X_train, X_test, y_train, y_test = get_train_test()
```

Không tự load/split lại trong notebook và không dùng `StandardScaler` hoặc `MinMaxScaler`; decision tree không cần scale. Quy ước toàn dự án là `random_state=42` ở mọi bước có ngẫu nhiên.

## Chạy baseline M0

Mở `notebooks/02_baseline.ipynb` và chọn **Restart & Run All**, hoặc chạy từ repo root:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 notebooks/02_baseline.ipynb
```

M0 dùng đúng `DecisionTreeClassifier(random_state=42)` với Gini mặc định, không giới hạn độ sâu/split/leaf và không pruning.

Artifact M0:

- `figures/B_tree_M0_full.png`
- `figures/B_tree_M0_top3.png`
- `figures/B_cm_M0.png`
- `outputs/rules_M0.txt`
- `outputs/classification_report_M0.txt`
- Dòng `M0` trong `outputs/results.csv`

## Chạy Role D — M2a/M2b (Class Imbalance)

Role D thực hiện cải tiến Class Imbalance bằng hai cấu hình. 
Mở `notebooks/04_improve_imbalance.ipynb` và chọn **Restart & Run All**, hoặc chạy:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 notebooks/04_improve_imbalance.ipynb
```

Cấu hình của Role D:
- **M2a**: `DecisionTreeClassifier(class_weight="balanced", random_state=42)`
- **M2b**: Dùng SMOTE với `sampling_strategy="auto", random_state=42, k_neighbors=5`, và chỉ resample trên tập train.

Artifact Role D:
- Báo cáo: [docs/report_draft_f2_imbalance.md](docs/report_draft_f2_imbalance.md)
- Progress: [progress/D.md](progress/D.md)
- `figures/D_cm_M2a.png`, `figures/D_cm_M2b.png`
- `figures/D_tree_M2a.png`, `figures/D_tree_M2a_full.png`
- `figures/D_tree_M2b.png`, `figures/D_tree_M2b_full.png`
- `outputs/classification_report_M2a.txt`, `outputs/classification_report_M2b.txt`
- Dòng `M2a` và `M2b` trong `outputs/results.csv`

### Checklist bàn giao cho Role D
- Chỉ gọi `get_train_test()` một lần; không tự split/scale lại dữ liệu.
- SMOTE chỉ resample tập train sau khi split, chứng minh không leakage.
- Các row D đúng author="D" và đúng params.
- Run A/Run B độc lập cho kết quả khớp tuyệt đối.
- Validator pass (đủ 6 hình, 2 báo cáo, audit).
- Đồng nhất cross-file.
- Không thay đổi M0/M1/M3 và dữ liệu chung.

## Tái sử dụng helper cho M1/M2/M3

Các role C/D/E truyền một model **đã fit** vào `evaluate_model()`. Nếu notebook được mở với working directory là `notebooks/`, chạy cell khởi tạo dưới đây trước để import luôn ổn định; không hard-code đường dẫn máy cá nhân:

```python
import sys
from pathlib import Path

def find_repo_root(start: Path | None = None) -> Path:
    """Find the nearest ancestor containing the shared data pipeline."""
    start = (start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "src" / "data.py").is_file():
            return candidate
    raise FileNotFoundError("Không tìm thấy repo root chứa src/data.py")

REPO_ROOT = find_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
```

Chỉ ghi những tham số định nghĩa thí nghiệm vào `params` thay vì toàn bộ `model.get_params()`, để CSV ổn định giữa các phiên bản scikit-learn. Ví dụ cho M1:

```python
from src.evaluate import evaluate_model
from src.visualize import plot_tree_figure

OUTPUTS_DIR = REPO_ROOT / "outputs"
FIGURES_DIR = REPO_ROOT / "figures"

m1_result = evaluate_model(
    m1,
    X_train, y_train,
    X_test, y_test,
    model_id="M1",
    model_name="Cost-complexity pruned tree",
    params={
        "ccp_alpha": float(best_alpha),
        "max_depth": m1.get_params()["max_depth"],
        "min_samples_leaf": m1.get_params()["min_samples_leaf"],
        "random_state": 42,
    },
    author="C",
    classification_report_path=OUTPUTS_DIR / "classification_report_M1.txt",
    confusion_matrix_path=FIGURES_DIR / "C_cm_M1.png",
)

plot_tree_figure(
    m1,
    X_train.columns,
    m1.classes_,
    FIGURES_DIR / "C_tree_M1.png",
)
```

Nếu `model_id` đã tồn tại với nội dung khác, helper dừng trước khi ghi đè artifact. Một lần chạy lại có nội dung giống hệt là idempotent, không thêm dòng trùng và giữ nguyên artifact byte-for-byte khi Windows không cho thay thế file đang được xem. Helper không hạ xuống kiểu ghi đè trực tiếp; nếu file đích thực sự khác và đang bị khóa, nó giữ nguyên file cũ rồi báo cách khắc phục.

### Checklist bàn giao cho Role C

- Chỉ gọi `get_train_test()` một lần; không tự split/scale lại dữ liệu.
- Tạo `ccp_alphas` từ train, chọn hyperparameter bằng cross-validation chỉ trên train; tuyệt đối không dùng test accuracy để chọn mô hình.
- Mọi bước CV có xáo trộn dùng `random_state=42`; grid bắt buộc bao gồm `max_depth ∈ {5, 8, 10, 15}` và `min_samples_leaf ∈ {1, 5, 10, 20}`.
- Sau khi chốt cấu hình, fit lại M1 trên toàn bộ train rồi chỉ đánh giá test qua `evaluate_model()` với `model_id="M1"`, `author="C"`.
- Xuất tối thiểu `figures/C_ccp_alpha_curve.png`, `figures/C_tree_M1.png`, `figures/C_cm_M1.png` và `outputs/classification_report_M1.txt`; lưu bảng grid search trong notebook.
- Trước khi bàn giao, **Restart & Run All**, xác nhận `outputs/results.csv` chỉ có đúng một dòng M1 và không có cell lỗi.

Đọc `AGENT.md` trước khi sửa repo để tuân thủ phạm vi file, workflow Git và trách nhiệm của từng role.
