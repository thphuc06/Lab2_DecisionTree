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
# Dùng đúng CPython 3.14.0; không thay bằng patch/version khác khi regenerate artifact canonical
& "C:\duong-dan-den-python-3.14.0\python.exe" -m venv .venv

# Dùng trực tiếp interpreter trong venv để tránh nhầm Python trên PATH
.\.venv\Scripts\python.exe -m pip install numpy==2.3.4 pandas==2.3.3 scipy==1.17.1 scikit-learn==1.9.0 matplotlib==3.11.1 seaborn==0.13.2 imbalanced-learn==0.14.2 ucimlrepo==0.0.7 joblib==1.5.3 threadpoolctl==3.6.0 nbformat==5.11.1 nbconvert==7.17.1 ipython==9.17.0 ipykernel==7.3.0 narwhals==2.25.0 sklearn-compat==0.1.6
.\.venv\Scripts\python.exe -m pip check
```

Kiểm tra `.\.venv\Scripts\python.exe --version` phải trả về đúng `3.14.0` và `pip check` phải PASS trước khi tiếp tục. Trên macOS/Linux, thay `Scripts\python.exe` bằng `.venv/bin/python`.

Artifact canonical D/E dùng Python 3.14.0 và scikit-learn 1.9.0. `requirements.txt` hiện vẫn là danh sách dependency mở, chưa phải lock file; cho đến khi integration owner commit lock chung, phải dùng đúng lệnh pin ở trên khi regenerate artifact D/E.

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
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 notebooks/05_improve_features.ipynb
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
