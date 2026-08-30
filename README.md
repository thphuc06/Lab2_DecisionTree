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
& "C:\duong-dan-den-python-3.14.0\python.exe" -m venv .venv

# Dùng đúng lock canonical để regenerate artifact M0/D/E
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check

# Đăng ký kernel trỏ tuyệt đối vào .venv; PYTHONUTF8 tránh lỗi console khi đường dẫn có tiếng Việt
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name lab2-canonical --display-name "Lab 2 canonical"
```

Kiểm tra `.\.venv\Scripts\python.exe --version` phải trả về đúng `3.14.0` và `pip check` phải PASS trước khi tiếp tục. Trên macOS/Linux, thay `Scripts\python.exe` bằng `.venv/bin/python`.

Toàn bộ artifact M0/M1/M2a/M2b/M3 hiện tại được tái lập với môi trường canonical: Python 3.14.0, `scikit-learn==1.9.0`, `imbalanced-learn==0.14.2`, `pandas==2.3.3`, `numpy==2.3.4` và `matplotlib==3.11.1`. `requirements.txt` mô tả dependency trực tiếp ở mức mở; `requirements-lock.txt` khóa đầy đủ môi trường dùng để regenerate artifact.

## Pipeline dữ liệu dùng chung

Mọi model phải dùng đúng split stratified đã được cố định trong `src/data.py`:

```python
from src.data import get_train_test

X_train, X_test, y_train, y_test = get_train_test()
```

Không tự load/split lại trong notebook và không dùng `StandardScaler` hoặc `MinMaxScaler`; decision tree không cần scale. Quy ước toàn dự án là `random_state=42` ở mọi bước có ngẫu nhiên.

## Chạy toàn bộ pipeline canonical

Chạy từ repo root theo đúng thứ tự `01 → 06`. Lệnh dưới đây dùng kernel canonical, tắt timestamp timing trong notebook và dừng nếu bất kỳ notebook nào lỗi:

```powershell
$env:PYTHONUTF8 = "1"
$notebooks = @(
    "notebooks/01_eda.ipynb",
    "notebooks/02_baseline.ipynb",
    "notebooks/03_improve_pruning.ipynb",
    "notebooks/04_improve_imbalance.ipynb",
    "notebooks/05_improve_features.ipynb",
    "notebooks/06_comparison.ipynb"
)

foreach ($notebook in $notebooks) {
    .\.venv\Scripts\python.exe -m nbconvert `
        --to notebook --execute --inplace `
        --ExecutePreprocessor.timeout=900 `
        --ExecutePreprocessor.kernel_name=lab2-canonical `
        --ExecutePreprocessor.record_timing=False `
        --NotebookClient.record_timing=False `
        $notebook
    if ($LASTEXITCODE -ne 0) {
        throw "Notebook failed: $notebook"
    }
}
```

Sau khi chạy xong, `outputs/results.csv` phải có đúng năm model ID `M0`, `M1`, `M2a`, `M2b`, `M3`; `outputs/comparison_table.csv` và `figures/comparison.png` được notebook 06 tái tạo từ chính bảng kết quả này. Dữ liệu gốc `data/raw/data.csv` được version-control và không được sửa tay.

## Chạy baseline M0

Mở `notebooks/02_baseline.ipynb` và chọn **Restart & Run All**, hoặc chạy từ repo root:

```powershell
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 --ExecutePreprocessor.kernel_name=lab2-canonical --ExecutePreprocessor.record_timing=False --NotebookClient.record_timing=False notebooks/02_baseline.ipynb
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
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 --ExecutePreprocessor.kernel_name=lab2-canonical --ExecutePreprocessor.record_timing=False --NotebookClient.record_timing=False notebooks/04_improve_imbalance.ipynb
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

## Chạy Role E — M3 dự báo sớm

Mở `notebooks/05_improve_features.ipynb` và chọn **Restart & Run All**, hoặc chạy từ repo root trong môi trường canonical Python 3.14.0, NumPy 2.3.4, pandas 2.3.3, SciPy 1.17.1 và scikit-learn 1.9.0:

```powershell
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 --ExecutePreprocessor.kernel_name=lab2-canonical --ExecutePreprocessor.record_timing=False --NotebookClient.record_timing=False notebooks/05_improve_features.ipynb
```

Notebook tự dừng trước khi train nếu phiên bản môi trường không khớp. M3 loại đúng 12 feature kết quả HK1/HK2, giữ 24 feature gốc/78 cột encoded, gồm `International`, `Unemployment rate`, `Inflation rate` và `GDP`, rồi fit `DecisionTreeClassifier(random_state=42)` trên split chung.

Artifact Role E:

- `outputs/classification_report_M3.txt` và dòng `M3` trong `outputs/results.csv`
- `outputs/E_feature_importance_comparison.csv`
- `outputs/E_feature_importance_permutation.csv`
- `figures/E_cm_M3.png`
- `figures/E_tree_M3.png`
- `figures/E_feature_importance.png`
- `figures/E_feature_importance_permutation.png`
- `progress/E.md`

`E_feature_importance.png` là Gini/MDI của cây đã fit trên train và đã gộp dummy về feature gốc. `E_feature_importance_permutation.png` dùng grouped permutation trên đúng 885 test rows, 30 repeats, seed 42 và scorer accuracy; toàn bộ dummy của một feature categorical được hoán vị cùng nhau. Cả hai chỉ phản ánh association, không chứng minh quan hệ nhân quả.

Kết quả canonical M3: test accuracy `0.5412429378531074`, macro-F1 `0.49305009179124043`, depth 30 và 963 leaf. Accuracy thấp hơn M0 là đánh đổi có chủ đích để dự báo được ngay từ thời điểm nhập học.

Checklist bàn giao E cho phạm vi code hiện tại:

- Notebook assert đúng môi trường, feature contract, split/target fingerprint và `random_state=42`.
- Bốn row M0/M1/M2a/M2b cùng artifact D được snapshot/hash trước và sau evaluation, không bị E thay đổi.
- Hai lần Run All độc lập phải cho cùng metric, classification report, hai CSV importance và bốn PNG.
- Notebook phải validate, execution count liên tục và không có stored error hoặc path máy cá nhân.
- Report, slide và video không thuộc phạm vi sửa Role E lần này; nhóm sẽ thực hiện chung ở giai đoạn sau.

Đọc `AGENT.md` trước khi sửa repo để tuân thủ phạm vi file, workflow Git và trách nhiệm của từng role.
