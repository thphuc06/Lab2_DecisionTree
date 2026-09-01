# CẤU TRÚC CODE & QUY TRÌNH GIT — 5 NGƯỜI LÀM SONG SONG

> Nguyên tắc cốt lõi: **mỗi path chỉ có một owner chính.** Phần lớn conflict
> trong dự án này xuất hiện khi hai nhánh thay đổi cùng một path hoặc cùng một
> vùng nội dung. Ownership rõ giúp giảm mạnh, nhưng không loại bỏ hoàn toàn các
> trường hợp modify/delete, rename/modify hoặc binary conflict.

---

## 1. Cấu trúc thư mục cuối cùng

```
Lab2_DecisionTree/
├── AGENTS.md                        ← cổng tương thích cho tool tìm tên số nhiều
├── AGENT.md                         ← đọc trước tiên khi mở agent, đừng để lệch chỗ
├── README.md                       ← Trưởng nhóm
├── requirements.txt                ← dependency trực tiếp; role đề xuất lib mới cho A
├── requirements-lock.txt           ← lock canonical; CHỈ A/Integrator refresh sau full rerun
├── .gitignore                      ← A tạo lúc khởi tạo repo
│
├── data/
│   └── raw/
│       └── data.csv                ← A tải lên, KHÔNG ai sửa tay file này
│
├── src/                             ⭐ vùng dễ conflict nhất — xem mục 2
│   ├── __init__.py
│   ├── data.py                     ← CHỈ A sửa
│   ├── evaluate.py                 ← CHỈ B sửa
│   └── visualize.py                ← CHỈ B sửa
│
├── notebooks/                       ⭐ mỗi file 1 chủ, không ai đụng vào notebook người khác
│   ├── 01_eda.ipynb                ← A
│   ├── 02_baseline.ipynb           ← B
│   ├── 03_improve_pruning.ipynb    ← C
│   ├── 04_improve_imbalance.ipynb  ← D
│   ├── 05_improve_features.ipynb   ← E
│   └── 06_comparison.ipynb         ← A (chỉ tạo sau khi 4 người kia xong)
│
├── progress/                        ⭐ nhật ký tiến độ, mỗi file 1 chủ — agent đọc/ghi để nhớ giữa các phiên
│   ├── A.md                        ← CHỈ A (và agent của A) sửa
│   ├── B.md                        ← CHỈ B
│   ├── C.md                        ← CHỈ C
│   ├── D.md                        ← CHỈ D
│   └── E.md                        ← CHỈ E
│
├── figures/                         ← 22 PNG thí nghiệm + 1 logo, tên file có prefix (xem mục 4)
│
├── outputs/
│   ├── results.csv                 ⭐ 5 cấu hình, schema 16 cột
│   ├── comparison_table.csv
│   ├── classification_report_M*.txt
│   └── rules_M0.txt
│
└── docs/
    ├── 00-DE-BAI-GOC.pdf           ← đề gốc của thầy, nguồn xác thực cao nhất
    ├── 02-DATASET-VA-CONG-VIEC.md
    ├── 03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md   ← chính là file này
    ├── feature_types.md            ← A
    └── report/                     ← LaTeX source, sections, references và report.pdf
```

**`.gitignore` cần có:**
```
.ipynb_checkpoints/
__pycache__/
*.pyc
.venv/
.DS_Store
*.egg-info/
```

---

## 2. Ai sở hữu file nào — bảng quyền ghi

| File / thư mục | Người được sửa | Người khác muốn thay đổi thì làm gì |
|---|---|---|
| `src/data.py` | **Chỉ A** | Nhắn A yêu cầu thêm hàm, không tự sửa |
| `src/evaluate.py`, `src/visualize.py` | **Chỉ B** | Nhắn B yêu cầu thêm metric/hình, không tự sửa |
| `notebooks/0X_*.ipynb` | **Đúng 1 người ghi trong tên file** | Không mở sửa notebook người khác, kể cả "chỉ xem" — xem trên GitHub web |
| `progress/<X>.md` | **Đúng 1 chữ cái tương ứng** | Không đọc/sửa progress của role khác — mỗi người tự ghi nhật ký của mình |
| `outputs/results.csv` | **Ai cũng append được** | Chỉ được **thêm dòng**, không sửa/xóa dòng người khác (mục 5) |
| `figures/*.png` | Người tạo ra hình đó | Không sửa cùng một path. PNG là binary nên Git không merge nội dung; nếu hai nhánh cùng sửa một ảnh, owner phải chọn hoặc tái sinh bản canonical |
| `README.md`, file kế hoạch | Trưởng nhóm tổng hợp | Người khác góp ý qua chat, không tự sửa trực tiếp |

> Quy tắc cần nhớ: **thấy file không phải của mình → chỉ đọc; muốn sửa phải
> phối hợp với owner hoặc có task integration được giao rõ.**

---

## 3. Chiến lược nhánh (branch)

> Bảng tên nhánh bên dưới là **quy ước lịch sử khi phát triển**, không phải danh sách ref hiện có. Ở lần đồng bộ cuối ngày 2026-09-01, working branch là `main`, tại commit `9393993`, và `main` khớp `origin/main` trước khi bắt đầu các chỉnh sửa audit chưa commit. Không suy ra trạng thái hiện tại chỉ từ tên nhánh cũ trong nhật ký.

Với nhóm 5 người mới dùng git, **branch theo người** là đơn giản và đủ an toàn — không cần quy trình PR phức tạp.

```bash
# Lần đầu — mỗi người tự tạo nhánh của mình từ main
git switch main
git status --short                     # phải sạch trước khi đồng bộ
git fetch origin
git pull --ff-only origin main
git switch -c feature/pruning          # ví dụ của C
```

| Role | Tên nhánh khuyến nghị cho công việc mới |
|---|---|
| A | `feature/data-pipeline` |
| B | `feature/baseline` |
| C | `feature/pruning` |
| D | `feature/imbalance` |
| E | `feature/early-warning` |

**Quy trình làm việc mỗi ngày:**

> Các lệnh `git add`/`commit`/`push` trong ví dụ này chỉ dành cho **thành viên thao tác Git**. Theo `AGENT.md`, coding agent phải dừng trước ba lệnh này và bàn giao thay đổi để con người duyệt.
```bash
git switch feature/pruning
git status --short            # dừng nếu còn work chưa commit/stash
git fetch origin
git merge origin/main         # thành viên chủ động tích hợp main mới
# ... code, chạy notebook ...
git add notebooks/03_improve_pruning.ipynb outputs/results.csv
git commit -m "[C] Chạy pruning voi ccp_alpha, cap nhat results"
git push origin feature/pruning
```

`git fetch` chỉ cập nhật remote refs; `git merge`/`git pull` thay đổi branch và
working tree. Không chạy merge/pull trên tree dirty. Nếu nhóm chọn rebase thay
merge, phải thống nhất trước; không tự rebase một branch đã chia sẻ công khai.

**Merge vào `main`:** ownership làm giảm conflict nhưng không thay thế review.
Ưu tiên Pull Request nếu repository hỗ trợ. Nếu nhóm thống nhất merge trực tiếp,
thành viên thực hiện phải kiểm tra tree sạch, cập nhật `main` bằng fast-forward
và chạy checklist Mục 7 trước khi push:

```bash
git switch main
git status --short
git fetch origin
git pull --ff-only origin main
git merge --no-ff feature/pruning
git push origin main
```

---

## 4. Trình tự thời gian — ai chờ ai

**A là nút thắt.** Không ai code được phần đánh giá thật sự cho tới khi có `src/data.py`. Xử lý bằng 2 cách song song:

**Lưu ý cho D và E:** Vì Role D được phép cập nhật tài liệu chung (`README.md`), Role E bắt buộc phải pull code (hoặc làm) **sau** khi Role D đã hoàn thành để tránh conflict file `README.md`.

**Cách 1 — A chạy đua xong sớm:** A dồn toàn lực trong 1–2 ngày đầu để push `src/data.py` với hàm `get_train_test()` chạy được, dù EDA chưa xong.

**Cách 2 — 4 người kia không ngồi chờ:** trong lúc chờ A, C/D/E viết sẵn khung notebook của mình dùng **dữ liệu giả** (`sklearn.datasets.load_iris()` hoặc tự tạo `X, y` ngẫu nhiên), code toàn bộ logic train/tune/evaluate. Khi A push `src/data.py` xong, chỉ cần đổi 1 dòng:

```python
# Trước (lúc chờ A) — dùng iris để test logic
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)

# Sau (khi A đã push) — đổi 1 dòng
from src.data import get_train_test
X_train, X_test, y_train, y_test = get_train_test()
```

Cách này giúp cả nhóm không có ai rảnh tay quá lâu.

**Đặt tên hình theo prefix** để tránh trùng tên khi 5 người cùng lưu vào `figures/`:
```
figures/A_target_distribution.png
figures/B_tree_M0_full.png
figures/C_ccp_alpha_curve.png
figures/D_cm_M2b.png
figures/E_feature_importance.png
figures/E_feature_importance_permutation.png
```

---

## 5. Điểm conflict thật sự duy nhất: `results.csv`

Đây là file text nhiều role cùng ghi. Conflict có thể giải quyết có hệ thống,
nhưng vẫn phải kiểm tra schema, model ID và provenance; ghép được text không có
nghĩa là kết quả khoa học đã đúng.

**Quy ước repo hiện tại:** dùng duy nhất `outputs/results.csv`; mỗi role chỉ
được upsert hoặc đối soát model ID do mình sở hữu và không xóa/sửa row của role
khác. Riêng Role E phải snapshot raw row M0/M1/M2a/M2b trước và sau
`evaluate_model()` để chứng minh việc chạy M3 không thay đổi kết quả đã handoff.

**Khi file chung `results.csv` xảy ra conflict**, xử lý như sau:

```bash
git status --short     # phải sạch trước khi tích hợp
git fetch origin
git merge origin/main
# Git báo conflict trong outputs/results.csv, file sẽ có dạng:

M0,Baseline,...,B
<<<<<<< HEAD
M1,Pruned,...,C
=======
M2a,Class Weight,...,D
M2b,SMOTE,...,D
>>>>>>> feature/imbalance
```
Xóa ba loại conflict marker (`<<<<<<<`, `=======`, `>>>>>>>`), giữ các row
canonical không trùng model ID và kiểm tra lại toàn bộ file:
```
M0,Baseline,...,B
M1,Pruned,...,C
M2a,Class Weight,...,D
M2b,SMOTE,...,D
```

Không ghép máy móc hai phiên bản: một phía có thể chứa row cũ, header lặp hoặc
model ID trùng. Chạy tối thiểu kiểm tra sau trước khi người dùng commit:

```powershell
$rows = Import-Csv -LiteralPath outputs/results.csv
$expected = @('M0', 'M1', 'M2a', 'M2b', 'M3')
$actual = @($rows.model_id | Sort-Object)

if ((Get-Content -LiteralPath outputs/results.csv -First 1).Split(',').Count -ne 16) {
    throw 'results.csv must have 16 columns'
}
if (@($rows | Group-Object model_id | Where-Object Count -ne 1).Count -ne 0) {
    throw 'Duplicate model_id in results.csv'
}
if (@(Compare-Object $expected $actual).Count -ne 0) {
    throw 'Expected exactly M0, M1, M2a, M2b, M3'
}
```

Sau đó đối chiếu row bị conflict với notebook/classification report canonical.
Agent được sửa nội dung và báo kết quả kiểm tra, nhưng theo `AGENT.md` chỉ người
dùng mới chạy `git add`/`commit`/`push`.

---

## 6. Quy ước commit message

Prefix bằng ký hiệu tên để dễ tra `git log` và dễ dùng cho bảng đóng góp (mục a báo cáo):

```
[A] Them ham get_train_test, EDA phan bo target
[B] Train M0 baseline, ve cay, xuat rules
[C] Chay cost_complexity_pruning_path, chon alpha bang CV
[D] Train M2a/M2b voi class_weight va SMOTE
[E] Loc 12 cot HK1/HK2, train M3
```

Ngoại lệ lịch sử đã biết: commit `0969118` có prefix `[C]` nhưng nội dung thuộc
Role E. Không dùng prefix sai này để tính contribution và không rewrite 23
commit hậu duệ đã công bố chỉ để sửa nhãn; xem quy trình human-only trong
[`Cac_Cong_Viec_Can_Phai_Lam.md`](../Cac_Cong_Viec_Can_Phai_Lam.md).

---

## 7. Checklist mẫu trước khi merge vào `main`

Đây là mẫu tái sử dụng cho một lần tích hợp mới, **không phải danh sách việc còn tồn đọng của bản nộp hiện tại**:

- `git status --short` sạch và đang ở đúng branch trước khi tích hợp.
- `git fetch origin`, sau đó tích hợp `origin/main` bằng quy trình nhóm đã chọn;
  trên `main`, dùng `git pull --ff-only origin main`.
- Notebook đã `Restart & Run All`; execution count của code cell liên tục từ 1.
- Đã xóa cell rác, cell lỗi và cell thử nghiệm.
- Không sửa file ngoài phạm vi đã thống nhất nếu chưa được yêu cầu.
- `outputs/results.csv` có đúng một dòng cho model thuộc role, đúng schema chung và không thay đổi row của role khác.
- Không có conflict marker; source/dependency/Markdown gate liên quan đều pass.

---

## 8. Việc không được làm

| Đừng | Vì sao |
|---|---|
| Mở sửa `src/data.py` khi không phải A | Phá pipeline chung, 4 người khác lệch kết quả ngay |
| Mở notebook của người khác để "sửa giùm" | JSON diff cực khó đọc, dễ hỏng file |
| Push vào `main` mà chưa fetch, cập nhật và kiểm tra branch | Có thể bị reject, tích hợp base cũ hoặc bỏ sót thay đổi của người khác |
| Để `.ipynb_checkpoints/` lên git | Rác, phình repo, dễ conflict vô nghĩa |
| Commit dataset đã encode/transform thành file mới tùy tiện | Người khác không biết bạn dùng bản nào, kết quả không tái lập được |
