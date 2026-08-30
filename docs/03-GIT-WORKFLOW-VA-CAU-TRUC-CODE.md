# CẤU TRÚC CODE & QUY TRÌNH GIT — 5 NGƯỜI LÀM SONG SONG

> Nguyên tắc cốt lõi: **mỗi file chỉ có đúng một người sửa.** Conflict git chỉ xảy ra khi hai người sửa cùng một file cùng lúc — nếu chia quyền sở hữu rõ, conflict gần như không xảy ra.

---

## 1. Cấu trúc thư mục cuối cùng

```
[GroupID]-decision-tree/
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
├── figures/                         ← 22 PNG canonical, tên file có prefix (xem mục 4)
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
| `figures/*.png` | Người tạo ra hình đó | File ảnh không conflict (binary, git tự ghi đè theo tên) |
| `README.md`, file kế hoạch | Trưởng nhóm tổng hợp | Người khác góp ý qua chat, không tự sửa trực tiếp |

> Quy tắc duy nhất cần nhớ: **thấy file không phải của mình → không mở app sửa, chỉ đọc.**

---

## 3. Chiến lược nhánh (branch)

> Bảng tên nhánh ban đầu bên dưới là **quy ước lập kế hoạch**, không phải danh sách ref hiện có. Tại vòng tích hợp 2026-08-30, các ref đã fetch là `main`, `feature/pruning` và `role-e-final-thuy`; nhánh đang làm là `role-e-final-thuy` và đang merge `origin/main` mới nhất.

Với nhóm 5 người mới dùng git, **branch theo người** là đơn giản và đủ an toàn — không cần quy trình PR phức tạp.

```bash
# Lần đầu — mỗi người tự tạo nhánh của mình từ main
git checkout main
git pull
git checkout -b feature/pruning        # ví dụ của C
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
git checkout feature/pruning
git pull origin main          # LUÔN kéo main mới nhất trước khi làm tiếp
# ... code, chạy notebook ...
git add notebooks/03_improve_pruning.ipynb outputs/results.csv
git commit -m "[C] Chạy pruning voi ccp_alpha, cap nhat results"
git push origin feature/pruning
```

**Merge vào `main`:** vì mỗi người chỉ động vào file của riêng mình (bảng mục 2), merge trực tiếp là an toàn — không bắt buộc phải làm Pull Request trên GitHub, nhưng **nên** tạo PR nếu muốn người khác review nhanh (đã có bảng "ai review ai" trong file kế hoạch tổng). Nhóm mới dùng git thì cứ merge thẳng:

```bash
git checkout main
git pull
git merge feature/pruning
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

Đây là file text ai cũng ghi vào. Nếu 2 người push gần nhau, git sẽ báo conflict — nhưng vì CSV chỉ là các dòng text, xử lý rất dễ, không đáng sợ như conflict trong code.

**Quy ước repo hiện tại:** dùng duy nhất `outputs/results.csv`; mỗi role chỉ được thêm hoặc đối soát model ID do mình sở hữu và không xóa/sửa row của role khác. Riêng Role E phải snapshot raw row M0/M1/M2a/M2b trước và sau `evaluate_model()` để chứng minh việc chạy M3 không thay đổi kết quả đã handoff.

**Khi file chung `results.csv` xảy ra conflict**, xử lý như sau:

```bash
git pull origin main
# Git báo conflict trong outputs/results.csv, file sẽ có dạng:

M0,Baseline,...,B
<<<<<<< HEAD
M1,Pruned,...,C
=======
M2,Balanced,...,D
>>>>>>> feature/imbalance
```
Chỉ cần **xóa 3 dòng đánh dấu** (`<<<<<<<`, `=======`, `>>>>>>>`) và giữ lại cả hai dòng dữ liệu:
```
M0,Baseline,...,B
M1,Pruned,...,C
M2,Balanced,...,D
```
Rồi `git add`, `git commit`, `git push` bình thường. Đây là conflict dễ nhất trong git — không có logic gì để "giải quyết sai", chỉ là ghép 2 dòng lại.

---

## 6. Quy ước commit message

Prefix bằng ký hiệu tên để dễ tra `git log` và dễ dùng cho bảng đóng góp (mục a báo cáo):

```
[A] Them ham get_train_test, EDA phan bo target
[B] Train M0 baseline, ve cay, xuat rules
[C] Chay cost_complexity_pruning_path, chon alpha bang CV
[D] Train M2 voi class_weight balanced
[E] Loc 12 cot HK1/HK2, train M3
```

---

## 7. Checklist trước khi merge vào `main`

- [ ] `git pull origin main` trước khi push lần cuối
- [ ] Notebook đã `Restart & Run All` — số thứ tự cell chạy liền mạch từ 1
- [ ] Đã xóa cell rác, cell lỗi, cell thử nghiệm
- [ ] Không sửa file không thuộc quyền của mình (đối chiếu bảng mục 2)
- [ ] `outputs/results.csv` đã có đúng dòng model thuộc role của mình, đúng schema chung và không thay đổi row của role khác

---

## 8. Việc không được làm

| Đừng | Vì sao |
|---|---|
| Mở sửa `src/data.py` khi không phải A | Phá pipeline chung, 4 người khác lệch kết quả ngay |
| Mở notebook của người khác để "sửa giùm" | JSON diff cực khó đọc, dễ hỏng file |
| Push thẳng vào `main` mà không `pull` trước | Đè mất commit của người khác |
| Để `.ipynb_checkpoints/` lên git | Rác, phình repo, dễ conflict vô nghĩa |
| Commit dataset đã encode/transform thành file mới tùy tiện | Người khác không biết bạn dùng bản nào, kết quả không tái lập được |
