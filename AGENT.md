# AGENT.md — Hướng dẫn cho AI Coding Agent

> File này là nguồn hướng dẫn canonical duy nhất dành cho AI agent (Claude Code,
> Cursor, Codex...) trước khi làm bất kỳ việc gì trong repo; không sao chép quy
> tắc sang nhiều nơi.

---

## 0. Việc đầu tiên agent phải làm khi bắt đầu phiên làm việc

1. Đọc hết file này.
2. Đọc `docs/00-DE-BAI-GOC.pdf` — **đề gốc của thầy, nguồn xác thực cao nhất.** Các file bên dưới (`02-...`, `03-...`) là bản diễn giải lại từ đề này để tiện dùng, **có thể còn sai sót**. Nếu phát hiện điều gì trong `02-...`/`03-...` mâu thuẫn hoặc không khớp với đề gốc, **đề gốc luôn thắng** — báo lại cho người dùng, không tự ý chọn theo bản tóm tắt.
3. Đọc hết `docs/02-DATASET-VA-CONG-VIEC.md` — đặc tả dataset, feature, 5 cấu hình mô hình, metrics.
4. Đọc hết `docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md` — cấu trúc repo, quyền sở hữu file, quy trình git.
5. Xác định **chế độ công việc** trước khi sửa:
   - Task thuộc một workstream A/B/C/D/E: hỏi người dùng role nếu họ chưa nói;
     không tự đoán.
   - Task được người dùng giao rõ là integration, final audit, đồng bộ tài liệu
     hoặc rà soát toàn repository: không ép người dùng chọn một role; được đọc
     các file progress liên quan và sửa chéo role trong đúng phạm vi task đó.
6. Ở chế độ role, đọc `progress/<role>.md`. Ở chế độ integration/final audit,
   đọc các progress liên quan để đối chiếu attribution và trạng thái; không coi
   một nhật ký lịch sử là nguồn chuẩn cao hơn artifact/report hiện hành.
7. Ở chế độ role, chỉ hoạt động trong phạm vi Mục 5. Muốn sửa file của role
   khác phải hỏi. Ngoại lệ chỉ áp dụng khi người dùng đã cấp phạm vi
   integration/final-audit rõ ràng; ngoại lệ này không mở rộng sang thay đổi
   code/model ngoài yêu cầu.
8. Trước mọi thay đổi, chạy `git status --short`, `git branch --show-current`
   và `git log --oneline -10`. Có thể chạy `git fetch origin` để cập nhật remote
   refs mà không merge vào branch hiện tại. **`git pull` là thao tác ghi/tích
   hợp**: chỉ dùng khi người dùng yêu cầu đồng bộ, working tree sạch, đang đúng
   branch và đã xác định cách tích hợp; trên `main` ưu tiên
   `git pull --ff-only origin main`. Không pull trên working tree đang dirty.
9. **Cập nhật progress ngay sau mỗi mốc hoàn thành đáng kể.** Ở chế độ role,
   cập nhật đúng `progress/<role>.md`; ở chế độ integration, chỉ cập nhật các
   progress thực sự bị ảnh hưởng và ghi rõ đây là audit tích hợp. Không đợi tới
   cuối phiên vì phiên có thể bị ngắt bất cứ lúc nào.
10. Khi hoàn thành task (hoặc người dùng báo dừng), **KHÔNG tự chạy
    `git add`/`git commit`/`git push`** — kể cả khi được yêu cầu trực tiếp (xem
    Mục 7). Xác nhận các progress bị ảnh hưởng đã phản ánh đúng trạng thái mới
    nhất, rồi tóm tắt file thay đổi và đề xuất commit message theo quy ước
    `[X] ...` (`docs/03`) để người dùng tự review/commit/push.

Nếu task rõ ràng thuộc một role nhưng người dùng không cung cấp và từ chối xác
nhận role, agent dừng lại để tránh sửa sai ownership. Quy tắc này không áp dụng
cho task integration/final-audit đã được giao rõ trên toàn repository.

---

## 1. Dự án này là gì

Đồ án môn AI, **Lab 2: Decision Tree Modeling and Improvement**. Nhóm 5 sinh viên xây dựng:
- 1 cấu hình **baseline** (`DecisionTreeClassifier` không giới hạn)
- 3 **phương pháp cải tiến**: pruning, xử lý mất cân bằng lớp, feature selection cho dự báo sớm. Phương pháp imbalance có hai biến thể M2a/M2b, nên tổng cộng là **5 cấu hình** M0/M1/M2a/M2b/M3

trên dataset **UCI Predict Students' Dropout and Academic Success** (id=697): 4.424 sinh viên, 36 feature, 3 lớp (Dropout/Enrolled/Graduate).

**Ba sản phẩm nộp:** báo cáo PDF, source code, video thuyết trình — đóng gói `[GroupID].zip`.

**Trạng thái tích hợp ngày 2026-09-01:** code/thí nghiệm và report LaTeX đã
hoàn tất vòng audit cuối. Source report canonical nằm trong `docs/report/`;
các file `docs/report_draft_*.md` cũ đã bị xóa để tránh hai nguồn sự thật.
Slide/video được nhóm quản lý ngoài workspace. Những task final-audit được
trưởng nhóm giao rõ cho toàn repository được phép cập nhật tài liệu chéo role,
nhưng vẫn không được tự ghi lịch sử Git.

**Không có yêu cầu UI/web app/deploy nào cả.** "Resulting tree" trong đề nghĩa là **hình ảnh tĩnh** của cây (`plot_tree` → PNG dán vào báo cáo), không phải giao diện tương tác. Nếu người dùng yêu cầu xây dashboard, web app, hay bất kỳ giao diện nào cho dự án này, agent nên hỏi lại vì đề bài không yêu cầu — có thể họ nhầm với môn khác.

Toàn bộ đặc tả kỹ thuật chi tiết (36 feature là gì, 5 feature quan trọng nhất, cách xử lý categorical, 12 cột phải bỏ ở model dự báo sớm, schema metrics...) nằm trong `docs/02-DATASET-VA-CONG-VIEC.md`. **Agent không được tự suy đoán các chi tiết này — phải lấy từ file đó.**

---

## 2. Hợp đồng chung — áp dụng cho MỌI role, không thương lượng

Bất kể role nào, agent phải tuân thủ tuyệt đối:

| Luật | Chi tiết |
|---|---|
| `random_state=42` | Ở mọi nơi có tham số ngẫu nhiên: split, model, SMOTE |
| Một lần split duy nhất | Chỉ qua `src/data.py::get_train_test()`, không notebook nào tự split lại |
| Stratified split | `stratify=y` bắt buộc — dataset mất cân bằng (50/32/18) |
| Không chuẩn hóa dữ liệu | Decision tree không cần `StandardScaler`/`MinMaxScaler` — nếu agent thấy code có bước này, đó là thừa, nên bỏ |
| Thư viện | `scikit-learn` là chính. `imbalanced-learn` chỉ cho SMOTE (role D). Không dùng framework nào khác (TensorFlow, PyTorch, Weka...) trừ khi người dùng yêu cầu rõ ràng |
| SMOTE (nếu dùng) | **Chỉ áp dụng trên tập train**, tuyệt đối không trước khi split — đây là lỗi rò rỉ dữ liệu nghiêm trọng nhất có thể mắc |
| Chọn `ccp_alpha` | Bằng cross-validation trên **train set**, không bao giờ theo test accuracy — đó là tuning trên test set |
| Mọi model phải xuất | (1) đủ metrics theo schema `results.csv` ở Mục 3, (2) ít nhất 1 hình cây PNG, (3) confusion matrix, (4) `classification_report` |
| `error_rate` | Bắt buộc tính = `1 - test_accuracy`, đề yêu cầu rõ ràng, đừng bỏ sót |
| Comment code | Đề yêu cầu "clearly organized and commented" — mọi hàm phải có docstring ngắn |
| File sở hữu | Ở task role-scoped, xem Mục 5 và `docs/03-GIT-WORKFLOW...`, không sửa file ngoài role nếu chưa hỏi. Task integration/final-audit được giao rõ có thể sửa chéo role trong đúng phạm vi audit, không tự mở rộng sang code/model |
| Nhánh làm việc | Nắm rõ agent đang ở nhánh nào (`feature/<tên-role>` theo `docs/03`, VD `feature/pruning` cho role C) — nhưng **không tự tạo/checkout/merge nhánh** nếu người dùng chưa yêu cầu rõ |
| Đồng bộ Git | Kiểm tra `status`/branch trước, dùng `git fetch origin` để cập nhật remote refs. `git pull` là thao tác thay đổi trạng thái vì cập nhật branch/working tree; chỉ chạy trên tree sạch với ý định tích hợp rõ, ưu tiên `--ff-only` trên `main` |
| **Commit & Push** | ⛔ **Agent KHÔNG BAO GIỜ tự chạy `git add`/`git commit`/`git push`, kể cả khi được yêu cầu trực tiếp** ("commit giúp tôi", "push lên đi"). Chỉ người dùng tự thao tác. Agent dừng lại, tóm tắt thay đổi + đề xuất commit message, để người dùng tự review diff và tự commit/push — xem Mục 7 |
| `outputs/results.csv` | File **duy nhất nhiều role cùng ghi vào**. Mỗi role chỉ được upsert/đối soát model ID mình sở hữu, phải giữ nguyên row role khác và kết thúc với đúng một header + một row cho mỗi M0/M1/M2a/M2b/M3. Khi có conflict, không chỉ ghép máy móc: bỏ marker, kiểm tra schema 16 cột, model ID trùng và đối chiếu row canonical trước khi bàn giao cho người dùng commit (chi tiết: `docs/03` Mục 5) |
| Chữ trong hình (matplotlib) | Toàn bộ `title`/`xlabel`/`ylabel`/`suptitle`/legend phải là **tiếng Anh** — báo cáo nộp là tiếng Anh, hình ảnh xuất ra (PNG) không tự dịch lại được nếu code để tiếng Việt. Markdown giải thích trong notebook có thể vẫn tiếng Việt (không phải deliverable chấm điểm trực tiếp), nhưng chữ **bên trong hình** thì không |
| Viết văn bản báo cáo (`docs/report/sections/*.tex`) | **Không được nhắc tên file, đường dẫn, tên hàm hay commit nội bộ của repo** trong văn bản báo cáo thật (VD: không viết `src/data.py`, `get_train_test()`, `outputs/results.csv`, `docs/02-...md`) — báo cáo cho thầy đọc như một bài luận học thuật, không phải nhật ký kỹ thuật. Trích dẫn nguồn ngoài (bài báo, thư viện như `scikit-learn`, `DecisionTreeClassifier`, `SMOTE`) vẫn được. Comment `%` trong source có thể ghi provenance nội bộ nhưng không hiển thị trong PDF. Bản nộp không được còn TODO/placeholder. Xem `docs/report/README.md` để biết quy tắc caption/nhận xét (caption ngắn mô tả hình, phân tích viết thành đoạn văn riêng, không nhét vào caption) |
| **Mọi số liệu trong báo cáo phải truy được nguồn** | Mỗi con số trong văn bản báo cáo (accuracy, error rate, feature importance, hệ số tương quan, rank, purity, n mẫu...) phải **verify được trực tiếp** từ (a) output code thật (`outputs/results.csv`, `classification_report_*.txt`, hoặc tự chạy lại để đối chiếu), hoặc (b) một bảng/hình/diagram artifact **đã có mặt trong chính báo cáo** mà người đọc tra được ngay tại chỗ (không phải hình sẽ xuất hiện ở mục sau, không phải "tự tin là đúng"). **Tuyệt đối không suy diễn số liệu "nghe có vẻ hợp lý"** (VD: bịa điều kiện luật quyết định vì nghe giống mẫu hình thường gặp) và **không copy số từ tài liệu kế hoạch** (`docs/02-...md`) mà không re-verify trên dữ liệu/artifact thật — tài liệu kế hoạch có thể sai (đã từng xảy ra 2 lần: bảng đa cộng tuyến A6 và bảng feature importance A5 khác thuật toán). Nếu một đoạn phân tích trích số nhưng không hình/bảng nào trong báo cáo thể hiện được số đó, phải **thêm bảng nhỏ ngay tại chỗ** (kèm `\ref{}` trỏ tới), không được để số liệu "không biết từ đâu ra". Trước khi coi văn bản báo cáo là xong, đọc lại và tự hỏi: mỗi con số này có bảng/hình nào ngay trong báo cáo chứng minh được không? |

---

## 3. Tham chiếu nhanh — dùng ngay không cần mở file khác

**Schema `results.csv` (16 cột — khớp `docs/02` Phần D):**
```
model_id,model_name,params,train_acc,test_acc,error_rate,precision_macro,recall_macro,f1_macro,roc_auc_macro,recall_dropout,recall_enrolled,recall_graduate,tree_depth,n_leaves,author
```
> `precision_macro`/`roc_auc_macro` là 2 cột đề yêu cầu (mục 3.2.b: Precision, ROC-AUC) — đừng bỏ sót khi viết `evaluate_model()`. ROC-AUC dùng `predict_proba` + `roc_auc_score(..., multi_class='ovr', average='macro')`.

**12 cột phải loại bỏ cho model dự báo sớm (M3 — role E):**
```
Curricular units 1st sem (credited/enrolled/evaluations/approved/grade/without evaluations)
Curricular units 2nd sem (credited/enrolled/evaluations/approved/grade/without evaluations)
```
Giữ lại 3 biến vĩ mô (`Unemployment rate`, `Inflation rate`, `GDP`) vì đã biết tại thời điểm nhập học.

**Cấu hình 5 model:**
| Model | Owner | Cấu hình |
|---|---|---|
| M0 Baseline | B | `DecisionTreeClassifier(random_state=42)` |
| M1 Pruning | C | `cost_complexity_pruning_path` + CV để chọn `ccp_alpha`, thêm grid `max_depth`/`min_samples_leaf` |
| M2a Class balance | D | `class_weight='balanced'` |
| M2b SMOTE | D | SMOTE chỉ trên train, sau đó fit `DecisionTreeClassifier(random_state=42)` |
| M3 Dự báo sớm | E | Loại 12 cột trên, giữ 24 feature còn lại |

**Kỳ vọng kết quả (để agent nhận biết nếu ra số bất thường, khả năng có bug):**
- M0: train acc ≈ 1.00, test acc ≈ 0.65–0.72, độ sâu 25–35 tầng → nếu test acc > 0.90, nghi ngờ rò rỉ dữ liệu
- M2: accuracy tổng **có thể giảm** so với M0 trong khi recall lớp Enrolled/Dropout tăng — **đây là kết quả bình thường, không phải bug**, đừng "sửa" cho đến khi accuracy tăng lại
- M3: accuracy giảm rõ rệt so với M0 — **đây là kết quả mong đợi và là luận điểm chính của model này**, không phải thất bại cần khắc phục

---

## 4. Cách xác định phạm vi — role hoặc integration

Nếu task chỉ thuộc một workstream và người dùng chưa nói rõ, agent hỏi:

> "Bạn đang làm role nào trong nhóm — A (Data Lead), B (Baseline & Tree Analysis), C (Pruning), D (Class Imbalance), hay E (Early-warning Feature Selection)?"

Sau khi có câu trả lời, đọc đúng mục tương ứng ở Mục 5 và chỉ làm việc trong
phạm vi đó.

Nếu người dùng yêu cầu rõ audit/đồng bộ toàn repository, agent không cần gán
task vào một role giả. Agent được đọc toàn bộ tài liệu cần thiết và sửa các file
chéo role trong phạm vi audit, nhưng phải bảo toàn code/artifact ngoài yêu cầu,
không tự mở rộng thành thay đổi model hoặc lịch sử Git.

Nếu người dùng yêu cầu việc nằm ngoài phạm vi role của họ (ví dụ role C yêu cầu sửa `src/data.py`), agent nhắc: *"Việc này thuộc quyền sở hữu của role A theo quy ước repo. Bạn có muốn tôi (a) đề xuất thay đổi để bạn gửi cho A, hay (b) vẫn muốn tôi sửa trực tiếp?"* — không tự ý sửa mà không hỏi trước, vì sửa file dùng chung có thể làm lệch kết quả của cả nhóm.

---

## 5. Định nghĩa từng role

### Role A — Data Lead & Integrator

**File được sửa:** `src/data.py`, `docs/feature_types.md`, `notebooks/01_eda.ipynb`, `notebooks/06_comparison.ipynb`, `progress/A.md`, `requirements.txt`, `requirements-lock.txt`, mục Introduction/Dataset Description/Comparison/Conclusion trong báo cáo.

**Mục tiêu:** Đây là nút thắt của cả nhóm — 4 người còn lại phụ thuộc vào `src/data.py`. Ưu tiên tuyệt đối: có `get_train_test()` chạy được **càng sớm càng tốt**, kể cả trước khi EDA xong.

**Việc cụ thể:**
1. Tải dataset qua `ucimlrepo` (id=697), lưu `data/raw/data.csv`
2. Chạy `df.shape`, `df.info()`, `df.isnull().sum()` — xác nhận số liệu thực tế, không copy số từ tài liệu
3. Xác định cột nào là categorical dù lưu dạng số (xem bảng đầy đủ trong `docs/02-...`), ghi vào `docs/feature_types.md`
4. Viết `src/data.py` với tối thiểu 2 hàm public: `load_and_preprocess()` và `get_train_test()` — có docstring, có type hint
5. EDA: phân bố target, thống kê mô tả, heatmap tương quan (4–5 hình, lưu `figures/A_*.png`)
6. Cuối dự án: kiểm tra file chung `outputs/results.csv` có đúng các model ID và vẽ biểu đồ so sánh
7. Quản lý dependency: `requirements.txt` liệt kê dependency trực tiếp; chỉ A/Integrator cập nhật `requirements-lock.txt` sau khi cài sạch, chạy `pip check` và tái lập thành công toàn bộ artifact liên quan

**Không được làm:** sửa `src/evaluate.py`, `src/visualize.py`, hay bất kỳ notebook nào có tên khác `01_` hoặc `06_`.

**Definition of Done:** `from src.data import get_train_test` chạy được từ bất kỳ notebook nào khác, trả về đúng 4 giá trị đã stratify + `random_state=42`.

---

### Role B — Baseline & Tree Analysis

**File được sửa:** `src/evaluate.py`, `src/visualize.py`, `notebooks/02_baseline.ipynb`, `progress/B.md`, mục Baseline Model + Analysis of the Tree trong báo cáo, `README.md`.

**Mục tiêu:** Train model M0, và viết mục phân tích cây — **mục ăn điểm nhất của toàn báo cáo**.

**Việc cụ thể:**
1. Viết `src/evaluate.py`: hàm `evaluate_model(model, X_train, y_train, X_test, y_test, model_id, model_name, params, author) -> dict`, tính đủ metrics theo schema Mục 3 (16 cột, gồm cả `precision_macro` và `roc_auc_macro`), upsert idempotent đúng row `model_id` do caller sở hữu và giữ nguyên row khác trong `results.csv`
2. Viết `src/visualize.py`: `plot_tree_figure(model, feature_names, class_names, max_depth=None, save_path)` và `export_rules(model, feature_names, save_path)`
3. Train M0: `DecisionTreeClassifier(random_state=42)`
4. Xuất: cây đầy đủ (`figures/B_tree_M0_full.png`), cây rút gọn `max_depth=3` để đọc (`figures/B_tree_M0_top3.png`), confusion matrix, `outputs/rules_M0.txt`
5. Viết phân tích trả lời đủ 5 câu: root split là gì và tại sao, 3 tầng đầu nghĩa là gì, độ sâu/số leaf, train vs test → bằng chứng overfit, 2–3 luật IF-THEN cụ thể kèm số liệu (n, độ thuần khiết)

**Không được làm:** sửa `src/data.py`. Chỉ gọi hàm từ đó, không tự viết logic load/split riêng trong notebook.

**Definition of Done:** `results.csv` có dòng M0 đủ 16 cột theo schema Mục 3;
có cây đầy đủ, cây top-3 và confusion matrix; mục Analysis of the Tree trả lời
đủ 5 câu ở trên với số liệu cụ thể, không chỉ mô tả chung chung.

---

### Role C — Improvement 1: Pruning

**File được sửa:** `notebooks/03_improve_pruning.ipynb`, `progress/C.md`, mục Improvement Method 1 trong báo cáo.

**Mục tiêu:** Trả lời câu hỏi "cây nhỏ hơn nhiều lần có mất hiệu năng không?"

**Việc cụ thể:**
1. `path = clf.cost_complexity_pruning_path(X_train, y_train)` lấy mảng `ccp_alphas`
2. Với mỗi alpha, đánh giá bằng cross-validation **trên train set** — không được nhìn test set ở bước chọn alpha
3. Chọn alpha tối ưu theo CV, train lại, đánh giá **một lần duy nhất** trên test
4. Thêm grid nhỏ `max_depth` ∈ {5,8,10,15}, `min_samples_leaf` ∈ {1,5,10,20}
5. Gọi `evaluate_model()` từ `src/evaluate.py` (của B), không tự viết hàm tính metric riêng
6. Xuất: `figures/C_ccp_alpha_curve.png`, `figures/C_tree_M1.png`, bảng grid search

**Nếu `src/data.py` chưa có khi bắt đầu:** dùng tạm `sklearn.datasets.load_iris()` để viết trước toàn bộ logic, ghi rõ `# TODO: thay bằng src.data.get_train_test() khi A push xong`, không tự viết hàm load data thay A.

**Không được làm:** sửa `src/data.py`, `src/evaluate.py`, `src/visualize.py`.

**Definition of Done:** `results.csv` có dòng M1; có đồ thị alpha; cây sau pruning đọc được (không còn hàng trăm node); mục báo cáo giải thích được **vì sao** pruning giúp (hoặc không giúp) — không chỉ nêu số.

---

### Role D — Improvement 2: Class Imbalance

**File được sửa:** `notebooks/04_improve_imbalance.ipynb`, `progress/D.md`, `docs/report/sections/f2_imbalance.tex`, `outputs/classification_report_M2a.txt`, `outputs/classification_report_M2b.txt`. Ngoại lệ: được cập nhật thông tin cài đặt/M2a/M2b trong `README.md`, `docs/02-DATASET-VA-CONG-VIEC.md`, `docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md` và `AGENT.md`.

**Mục tiêu:** Trả lời câu hỏi "lớp thiểu số (Enrolled 18%, Dropout 32%) có được phát hiện tốt hơn không?"

**Việc cụ thể:**
1. M2a: `DecisionTreeClassifier(class_weight='balanced', random_state=42)`
2. M2b: SMOTE — **`from imblearn.over_sampling import SMOTE`, chỉ `fit_resample` trên `X_train, y_train`**, không bao giờ trên toàn bộ dataset trước khi split
3. Gọi `evaluate_model()` từ `src/evaluate.py`, không tự viết lại
4. So sánh **recall từng lớp** (Dropout, Enrolled, Graduate) giữa M0/M2a/M2b — đây là điểm chính của phân tích, không phải accuracy tổng
5. Xuất: `figures/D_cm_M2a.png`, `figures/D_cm_M2b.png`, `figures/D_tree_M2a.png`, `figures/D_tree_M2a_full.png`, `figures/D_tree_M2b.png`, `figures/D_tree_M2b_full.png` và 2 bảng classification report.

**Nếu accuracy tổng giảm sau khi cân bằng lớp:** đây là kết quả **đúng và mong đợi** (xem Mục 3). Không cần "tối ưu lại" cho tới khi accuracy quay lại bằng M0 — mục tiêu của cải tiến này là recall lớp thiểu số, không phải accuracy tổng.

**Không được làm:** sửa `src/data.py`, `src/evaluate.py`, `src/visualize.py`. Không áp dụng SMOTE trước khi gọi `get_train_test()`.

**Definition of Done:** `results.csv` có 2 dòng (M2a, M2b); section f.2 có bảng recall 3 lớp × 3 model, giải thích representation categorical và hình cây; đủ 6 hình D; file dùng chung (`README.md`, docs) đã cập nhật xong theo ngoại lệ; validator PASS; manifest `progress/D.md` phản ánh đúng trạng thái cuối.

---

### Role E — Improvement 3: Early-warning Feature Selection

**File được sửa trong giai đoạn code hiện tại:** `notebooks/05_improve_features.ipynb`, `progress/E.md`, artifact `E_*`, chỉ row M3 trong `outputs/results.csv`, và các đoạn Role E được cấp quyền hẹp trong `README.md`/tài liệu kỹ thuật.

**Mục tiêu:** Trả lời câu hỏi "có cảnh báo sớm được không, trước khi có kết quả học kỳ?"

**Việc cụ thể:**
1. Loại đúng 12 cột liệt kê ở Mục 3 (nhóm HK1 + HK2), giữ 24 feature còn lại kể cả 3 biến vĩ mô
2. Train `DecisionTreeClassifier(random_state=42)` trên tập feature đã lọc
3. Gọi `evaluate_model()` từ `src/evaluate.py`
4. So sánh Gini/MDI importance của M0 vs M3 theo feature gốc — `figures/E_feature_importance.png`, `outputs/E_feature_importance_comparison.csv`
5. Tính grouped permutation importance trên test: 30 repeats, `random_state=42`, scorer accuracy; permute toàn bộ dummy của cùng feature bằng chung một hoán vị — `figures/E_feature_importance_permutation.png`, `outputs/E_feature_importance_permutation.csv`
6. Snapshot bốn row M0/M1/M2a/M2b và artifact D trước/sau evaluation; phải chứng minh byte-for-byte bất biến
7. Hỗ trợ B hoàn thiện mục Analysis of the Tree nếu B cần

**Trạng thái deliverable liên quan:** section f.3 và References đã hoàn tất trong
`docs/report/`. Slide/video đã được nhóm thực hiện ngoài workspace; không tự sửa
media nếu người dùng không cung cấp file hoặc yêu cầu rõ.

**Không được làm:** sửa `src/data.py`, `src/evaluate.py`, `src/visualize.py`.

**Definition of Done cho phạm vi code:** `results.csv` có đúng một dòng M3; loại đúng 12/giữ 24 feature; có tree, confusion matrix, classification report, Gini/MDI và held-out grouped permutation CSV/PNG; hai Run All độc lập tái lập cùng kết quả; non-M3 rows và artifact D bất biến; notebook không có stored error/path máy cá nhân.

---

## 6. Khi nào agent phải dừng lại và hỏi người dùng thay vì tự quyết

- Task role-scoped nhưng chưa biết role → hỏi trước khi viết code; task
  integration/final-audit đã được giao rõ thì không cần ép chọn role
- Task role-scoped yêu cầu sửa file thuộc quyền role khác → hỏi trước khi sửa;
  task integration/final-audit đã cấp phạm vi chéo role thì tuân theo phạm vi đó
- `src/data.py` chưa tồn tại và role hiện tại không phải A → dùng dữ liệu giả tạm thời, không tự viết loader thay A
- Metric hoặc kết quả ra số bất thường so với Mục 3 (VD: SMOTE mà accuracy tăng vọt lên 0.99) → nghi ngờ rò rỉ dữ liệu, báo người dùng thay vì tự "sửa" bằng cách nới lỏng ràng buộc
- Người dùng yêu cầu thứ không có trong đề (UI, deploy, thêm thuật toán ngoài decision tree, dataset khác) → hỏi lại xem có chắc không, vì có thể lệch khỏi yêu cầu thầy
- Conflict trong `results.csv` khi người dùng pull/push → agent có thể sửa nội dung file để gỡ conflict marker theo hướng dẫn trong `docs/03-GIT-WORKFLOW...`, nhưng không tự commit — báo người dùng review rồi tự commit
- Được yêu cầu "commit giúp tôi" / "push lên đi" / bất kỳ hình thức nào yêu cầu tự thao tác git ghi lịch sử → **không thực hiện**. Trả lời rằng theo quy ước dự án (Mục 7) chỉ người dùng tự `git add`/`commit`/`push`, rồi tóm tắt các file đã đổi kèm đề xuất commit message để người dùng tự chạy

---

## 7. Việc tuyệt đối không được làm, bất kể role

- ⛔ **Không bao giờ tự chạy `git commit`, `git push`, hay `git add` để commit thay — kể cả khi người dùng yêu cầu trực tiếp.** Agent chỉ được sửa file trong working directory; người dùng luôn là người xem diff và tự thực hiện commit/push. `git status`/`git log`/`git diff` và `git fetch` không merge vào working tree; `git pull` có thể thay branch/working tree nên chỉ được dùng theo điều kiện an toàn ở Mục 0/Mục 2
- Không tạo UI, web app, dashboard, hay bất kỳ giao diện tương tác nào — đề không yêu cầu
- Không dùng framework ngoài scikit-learn (+ imbalanced-learn) trừ khi được yêu cầu rõ ràng
- Không scale/chuẩn hóa dữ liệu cho decision tree
- Không split dữ liệu ở đâu ngoài `src/data.py`
- Không SMOTE/oversample trước khi split
- Không chọn hyperparameter (đặc biệt `ccp_alpha`) dựa theo kết quả test set
- Không sửa file thuộc role khác trong task role-scoped nếu chưa được cho phép;
  ngoại lệ integration/final-audit chỉ có hiệu lực trong phạm vi người dùng giao
- Không để notebook có cell lỗi, cell rác, hoặc thứ tự chạy không liền mạch khi commit lần cuối
