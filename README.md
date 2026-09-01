# Lab 2 - Decision Tree Modeling and Improvement

Đồ án xây dựng một cây quyết định baseline và ba hướng cải tiến trên bộ dữ
liệu UCI **Predict Students' Dropout and Academic Success**: pruning, xử lý
mất cân bằng lớp và loại các biến kết quả học kỳ cho thí nghiệm dự báo sớm.

## Trạng thái bản bàn giao — 2026-09-02

Vòng audit tích hợp ngày **2026-09-02** xác nhận:

- Sáu notebook `01`--`06` hợp lệ, execution count liên tục và không lưu error
  output, timing metadata hoặc đường dẫn máy cá nhân.
- `outputs/results.csv` có đúng năm cấu hình `M0`, `M1`, `M2a`, `M2b`, `M3`
  với schema 16 cột; metric đã được fit lại độc lập và đối chiếu với
  classification report/confusion matrix.
- Source report cuối nằm trong `docs/report/`; các bản nháp Markdown cũ đã bị
  loại bỏ để tránh tồn tại hai nguồn sự thật.
- Bản PDF canonical 41 trang là `docs/report/report.pdf`; bản đặt tên để nộp
  là `docs/report/2 - Report.pdf`. Hai bản có cùng SHA-256
  `dfeeb1f165824983d0c5d7750781bb9bab519176900e8ba4d45c9ee4af198a26`.
- Slide và video do nhóm quản lý ngoài workspace này. Trước khi nộp vẫn phải
  kiểm tra tên file/quyền truy cập và đóng gói ZIP theo đề gốc.

Các bước cuối cùng cho giai đoạn đóng gói và xác minh hồ sơ được thực hiện
ngoài workspace repo; không còn file checklist dạng Markdown nào được giữ lại
trong repository để tránh nhiều nguồn sự thật.

## Cấu trúc repository

```text
data/raw/       CSV gốc được version-control
src/            Pipeline dữ liệu, đánh giá và trực quan hóa dùng chung
notebooks/      EDA, baseline, ba cải tiến và notebook so sánh
figures/        22 hình thí nghiệm canonical + logo báo cáo
outputs/        Metrics, classification report, importance và luật cây
docs/           Đề gốc, đặc tả kỹ thuật, provenance và report LaTeX
progress/       Nhật ký kỹ thuật theo role
```

## Tài liệu liên quan

- [`AGENT.md`](AGENT.md): nguồn quy tắc canonical cho coding agent.
- [`docs/00-DE-BAI-GOC.pdf`](docs/00-DE-BAI-GOC.pdf): đề bài gốc, nguồn yêu
  cầu có thẩm quyền cao nhất.
- [`docs/02-DATASET-VA-CONG-VIEC.md`](docs/02-DATASET-VA-CONG-VIEC.md): đặc
  tả dataset, preprocessing, năm cấu hình model và metric contract.
- [`docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md`](docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md):
  ownership theo role và quy trình Git cho thành viên trong nhóm.
- [`docs/dataset_provenance.md`](docs/dataset_provenance.md): phân biệt claim
  kiểm chứng trực tiếp từ CSV với claim dựa trên nguồn xuất bản.
- [`docs/feature_types.md`](docs/feature_types.md): cách phân loại và mã hóa 36
  feature gốc.
- [`docs/report/README.md`](docs/report/README.md): cấu trúc, build và QA report
  LaTeX.
- Các checklist theo role và đóng gói đã được loại bỏ khỏi repo để tránh dư thừa
  nguồn thông tin; người phụ trách vẫn cần đối chiếu với report canonical và
  tài liệu tổ chức ngoài workspace trước khi nộp.

## Môi trường canonical

Artifact hiện tại được tạo với Python 3.14.0, `scikit-learn==1.9.0`,
`imbalanced-learn==0.14.2`, `pandas==2.3.3`, `numpy==2.3.4` và
`matplotlib==3.11.1`.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check

$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m ipykernel install `
    --prefix .venv `
    --name lab2-canonical `
    --display-name "Lab 2 canonical"
```

Trên macOS/Linux, thay `.venv\Scripts\python.exe` bằng
`.venv/bin/python`. `requirements.txt` liệt kê dependency trực tiếp;
`requirements-lock.txt` là lock đầy đủ để tái lập artifact canonical.

## Hợp đồng dữ liệu chung

Mọi model dùng cùng một split từ `src/data.py`:

```python
from src.data import get_train_test

X_train, X_test, y_train, y_test = get_train_test()
```

Split là 80/20, stratified và dùng `random_state=42`. Không notebook nào tự
split lại, không áp dụng scaling, và SMOTE chỉ được fit trên tập train.

Pipeline one-hot encode bốn nhóm nominal có cardinality thấp, tạo 90 cột đầu
vào cho M0/M1/M2a/M2b. Các cột nominal cardinality cao vẫn được giữ dưới dạng
mã số nguyên; đây là một giới hạn biểu diễn được công khai trong report. M3
loại đúng 12 biến kết quả học kỳ, giữ 24 feature gốc/78 cột encoded. Việc xem
các feature còn lại là có sẵn lúc nhập học là giả định của thí nghiệm, không
phải điều CSV tự chứng minh.

## Chạy toàn bộ pipeline

Chạy từ repo root theo thứ tự `01` đến `06`:

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

Sau khi chạy, `outputs/results.csv` phải có đúng một dòng cho mỗi model. Notebook
06 tái tạo `outputs/comparison_table.csv` và `figures/comparison.png` từ bảng
kết quả này. Không sửa tay `data/raw/data.csv` hoặc các hàng metric.

## Kết quả canonical

| Model | Cấu hình | Test accuracy | Error rate | Macro-F1 | ROC-AUC | Depth | Leaves |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| M0 | Baseline Gini không giới hạn | 0.668927 | 0.331073 | 0.608271 | 0.719456 | 27 | 634 |
| M1 | Cost-complexity + depth/leaf constraints | 0.755932 | 0.244068 | 0.672925 | 0.847692 | 5 | 17 |
| M2a | `class_weight="balanced"` | 0.650847 | 0.349153 | 0.585409 | 0.705321 | 28 | 696 |
| M2b | Vanilla SMOTE trên train | 0.688136 | 0.311864 | 0.638747 | 0.742122 | 39 | 847 |
| M3 | Loại 12 biến kết quả học kỳ | 0.541243 | 0.458757 | 0.493050 | 0.625355 | 30 | 963 |

M1 tốt nhất theo các metric tổng hợp và độ gọn. M2b có recall Dropout/Enrolled
cao nhất nhưng phải đọc cùng giới hạn vanilla SMOTE trên feature categorical.
M3 đo đánh đổi giữa độ chính xác và thời điểm dự báo dưới giả định availability
được công bố trong report.

## Giới hạn đã biết

- Một số nominal feature cardinality cao vẫn được giữ dưới dạng mã số để tránh
  tăng mạnh số chiều; split theo ngưỡng trên các mã này có thể áp đặt thứ tự
  nhân tạo.
- Vanilla SMOTE trên representation chứa one-hot/categorical không bảo toàn
  mọi ràng buộc category; kết quả M2b phải được đọc cùng audit limitation trong
  report.
- So sánh model dựa trên một held-out split cố định. Kết quả đủ để so sánh nội
  bộ trong thí nghiệm này nhưng không chứng minh hiệu năng trên quần thể khác.
- M3 xem các feature còn lại là có sẵn lúc nhập học theo giả định nghiên cứu;
  triển khai thật cần data dictionary và row-level snapshot timestamps.

## Artifact chính

- `figures/A_*.png`: năm hình EDA.
- `figures/B_*.png`, `outputs/rules_M0.txt`: cây, confusion matrix và luật M0.
- `figures/C_*.png`: pruning path, toàn bộ cây M1 và confusion matrix.
- `figures/D_*.png`: cây và confusion matrix M2a/M2b.
- `figures/E_*.png`, `outputs/E_*.csv`: cây M3 và hai phép đo importance.
- `outputs/classification_report_M*.txt`: precision/recall/F1 theo lớp.
- `outputs/results.csv`: nguồn metric canonical dùng chung.

## Dataset attribution và license

Dataset **Predict Students' Dropout and Academic Success** được phát hành theo
CC BY 4.0. URL, DOI, ngày truy cập và phạm vi từng claim nằm trong
[`docs/dataset_provenance.md`](docs/dataset_provenance.md).

Repository hiện không có file `LICENSE` riêng cho source code. Không suy diễn
rằng code được phát hành theo CC BY 4.0 chỉ vì dataset dùng license đó; nếu
nhóm công bố repository ngoài phạm vi nộp môn học, chủ sở hữu cần chọn và thêm
code license một cách rõ ràng.

## Build report

XeLaTeX là engine đã kiểm chứng và không cần cài `vntex`:

```powershell
Push-Location docs/report
xelatex -interaction=nonstopmode -halt-on-error report.tex
bibtex report
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
Pop-Location
```

Nhánh pdfLaTeX dùng T5 và chỉ phù hợp khi máy đã có `vntex`. Chi tiết build và
QA nằm trong [`docs/report/README.md`](docs/report/README.md).

## Quy ước Git

Đọc `AGENT.md` và `docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md` trước khi sửa.
Coding agent không được tự `git add`, `git commit`, `git push` hoặc rewrite
lịch sử. Người dùng phải review diff và tự thực hiện các thao tác Git.
