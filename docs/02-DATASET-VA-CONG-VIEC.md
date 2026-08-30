# DATASET & CÔNG VIỆC CHI TIẾT

> Tài liệu kỹ thuật đã được đồng bộ với pipeline canonical ngày 2026-08-30.
> Xem cách cài đặt/chạy ở `README.md`; yêu cầu gốc ở `docs/00-DE-BAI-GOC.pdf`.

---

# PHẦN A — DATASET

## A1. Thông tin nguồn

| Mục | Giá trị |
|---|---|
| Tên | Predict Students' Dropout and Academic Success |
| Nguồn | UCI Machine Learning Repository, **ID = 697** |
| DOI | `10.24432/C5MC89` |
| Bản gốc | Zenodo `10.5281/zenodo.5777339` |
| License | **CC BY 4.0** — được dùng tự do, bắt buộc ghi nguồn |
| Bài báo mô tả | Realinho et al. (2022), *Data* 7(11):146, DOI `10.3390/data7110146` |
| Bối cảnh | 17 ngành đại học, Instituto Politécnico de Portalegre (Bồ Đào Nha), niên khóa 2008/09 – 2018/19 |
| Số mẫu | **4.424** sinh viên |
| Số feature | **36** (theo UCI) — xem cảnh báo A2 |
| Missing values | **Không có** (tác giả đã tiền xử lý) |
| Kích thước file | ~0.5 MB |

**Cách tải:**
```python
from ucimlrepo import fetch_ucirepo
ds = fetch_ucirepo(id=697)
X, y = ds.data.features, ds.data.targets
print(ds.metadata)
print(ds.variables)
```

## A2. Đối chiếu số feature — đã xác nhận

Trang UCI ghi **36 features**. Nhưng Table 1 của bài báo gốc chỉ liệt kê **34 features**.

Chênh lệch nằm ở 2 cột có trong file CSV phát hành nhưng không có trong bảng bài báo:
- `Previous qualification (grade)`
- `Admission grade`

Pipeline đã kiểm tra trực tiếp `df.shape == (4424, 37)`: **36 feature + 1 target**. Hai cột chênh lệch được giữ lại và được mô tả trong báo cáo.

## A3. Phân bố lớp (target)

| Lớp | Số mẫu | Tỉ lệ | Ý nghĩa |
|---|---|---|---|
| **Graduate** | 2.209 | 50% | Tốt nghiệp đúng hạn |
| **Dropout** | 1.421 | 32% | Bỏ học |
| **Enrolled** | 794 | **18%** | Vẫn đang học khi hết thời hạn chuẩn |

> Lớp **Enrolled** là lớp thiểu số và là lớp khó nhất — nó nằm "ở giữa" hai lớp kia về mặt đặc trưng. Đây là lý do tồn tại của cải tiến M2.
> Thời gian chuẩn: 3 năm (riêng ngành Điều dưỡng 4 năm).

## A4. Toàn bộ 36 feature — chia theo 6 nhóm

### Nhóm 1 — Nhân khẩu học (6 cột)
| Cột | Kiểu thực chất | Ghi chú |
|---|---|---|
| `Marital Status` | **Category** | 6 giá trị quan sát, mã 1–6; tên cột có chữ `S` viết hoa trong CSV |
| `Nacionality` | **Category** | 21 giá trị quan sát, mã 1–109; giữ nguyên chính tả từ bộ dữ liệu |
| Displaced | Binary | 1=sống xa nhà |
| Gender | Binary | 1=nam, 0=nữ |
| Age at enrollment | **Numeric** | 17–70, trung bình 23.1, median 20 |
| International | Binary | 1=sinh viên quốc tế |

### Nhóm 2 — Kinh tế xã hội (8 cột)
| Cột | Kiểu thực chất | Ghi chú |
|---|---|---|
| Mother's qualification | **Category** | 29 giá trị quan sát |
| Father's qualification | **Category** | 34 giá trị quan sát |
| Mother's occupation | **Category** | 32 giá trị quan sát |
| Father's occupation | **Category** | 46 giá trị quan sát |
| Educational special needs | Binary | Chỉ 1.2% = 1 |
| Debtor | Binary | 1=đang nợ, 11.4% |
| **Tuition fees up to date** | Binary | ⭐ **Feature quan trọng**, 88.1% = 1 |
| Scholarship holder | Binary | 1=có học bổng, 24.8% |

### Nhóm 3 — Kinh tế vĩ mô (3 cột)
| Cột | Kiểu | Khoảng giá trị |
|---|---|---|
| Unemployment rate | Numeric | 7.6 – 16.2 |
| Inflation rate | Numeric | −0.8 – 3.7 |
| GDP | Numeric | −4.1 – 3.5 |

> Ba cột này phụ thuộc **năm nhập học**, không phải cá nhân sinh viên.

### Nhóm 4 — Học vấn lúc nhập học (7 cột)
| Cột | Kiểu thực chất | Ghi chú |
|---|---|---|
| Application mode | **Category** | 18 giá trị quan sát, mã 1–57 |
| Application order | Ordinal | 8 giá trị quan sát trong khoảng 0–9 |
| **Course** | **Category** | 17 giá trị quan sát, mã 33–9991; ⭐ feature quan trọng |
| Daytime/evening attendance | Binary | 1=ban ngày (89.1%) |
| Previous qualification | **Category** | 17 giá trị quan sát, mã 1–43 |
| Previous qualification (grade) | Numeric | Điểm bằng cấp trước |
| Admission grade | Numeric | Điểm xét tuyển |

### Nhóm 5 — Kết quả học kỳ 1 (6 cột)
| Cột | Kiểu | Ghi chú |
|---|---|---|
| Curricular units 1st sem (credited) | Numeric | 0–20, mean 0.71 |
| Curricular units 1st sem (enrolled) | Numeric | 0–26, mean 6.27 |
| Curricular units 1st sem (evaluations) | Numeric | 0–45, mean 8.30 |
| **Curricular units 1st sem (approved)** | Numeric | ⭐ **Feature quan trọng**, 0–26, mean 4.71 |
| Curricular units 1st sem (grade) | Numeric | 0–18.9, mean 10.64 |
| Curricular units 1st sem (without evaluations) | Numeric | 0–12, mean 0.14 |

### Nhóm 6 — Kết quả học kỳ 2 (6 cột)
| Cột | Kiểu | Ghi chú |
|---|---|---|
| Curricular units 2nd sem (credited) | Numeric | 0–19 |
| Curricular units 2nd sem (enrolled) | Numeric | 0–23 |
| Curricular units 2nd sem (evaluations) | Numeric | 0–33 |
| **Curricular units 2nd sem (approved)** | Numeric | ⭐ **Feature quan trọng nhất**, 0–20, mean 4.44 |
| **Curricular units 2nd sem (grade)** | Numeric | ⭐ **Feature quan trọng**, 0–18.6, mean 10.23 |
| Curricular units 2nd sem (without evaluations) | Numeric | 0–12 |

**Tổng: 6 + 8 + 3 + 7 + 6 + 6 = 36 feature** ✓

## A5. ⭐ Năm feature quan trọng nhất

Bài báo gốc chạy **permutation feature importance** trên 4 thuật toán (Random Forest, XGBoost, LightGBM, CatBoost). Năm feature này quan trọng ở **cả 4** thuật toán:

| Hạng | Feature | Nhóm | Có sẵn lúc nhập học? |
|---|---|---|---|
| 1 | Curricular units **2nd sem (approved)** | HK2 | ❌ Không |
| 2 | Curricular units **1st sem (approved)** | HK1 | ❌ Không |
| 3 | Curricular units **2nd sem (grade)** | HK2 | ❌ Không |
| 4 | **Course** | Nhập học | ✅ Có |
| 5 | **Tuition fees up to date** | Kinh tế xã hội | ✅ Có |

Quan trọng ở 3/4 thuật toán: `1st sem (enrolled)`, `1st sem (evaluations)`, `2nd sem (enrolled)`, `2nd sem (evaluations)`.

> 🎯 **Đây là nền tảng lập luận cho M3.** Ba trong năm feature mạnh nhất **chỉ biết được sau khi học kỳ kết thúc**. Model chính xác nhất lại là model can thiệp muộn nhất. Trích dẫn được phát hiện này từ một bài báo peer-reviewed mạnh hơn nhiều so với "nhóm em thấy vậy".

## A6. Đa cộng tuyến (Pearson > 0.7) — dùng cho feature selection

| Cặp feature | r |
|---|---|
| 1st sem (credited) ↔ 2nd sem (credited) | **0.945** |
| 1st sem (enrolled) ↔ 2nd sem (enrolled) | **0.943** |
| `Nacionality` ↔ International | **0.791** |
| 1st sem (approved) ↔ 2nd sem (approved) | **0.904** |
| 1st sem (grade) ↔ 2nd sem (grade) | 0.837 |
| 1st sem (evaluations) ↔ 2nd sem (evaluations) | 0.779 |
| 1st sem (credited) ↔ 1st sem (enrolled) | 0.774 |
| 2nd sem (approved) ↔ 2nd sem (grade) | 0.761 |
| Mother's occupation ↔ Father's occupation | **0.910** |
| 2nd sem (enrolled) ↔ 2nd sem (approved) | 0.703 |

> Cây quyết định không bị ảnh hưởng nặng bởi đa cộng tuyến như hồi quy tuyến tính, **nhưng** các feature tương quan có thể chia nhỏ importance và làm cấu trúc cây kém ổn định. M3 canonical không loại cột chỉ dựa trên correlation: nó loại **đúng 12 cột kết quả học kỳ** theo mục tiêu dự báo sớm và giữ cả `Nacionality` lẫn `International`.

## A7. Quan sát từ EDA của bài báo (dùng cho phần diễn giải)

- Ngành thành công nhất: **Điều dưỡng (72% tốt nghiệp)**, **Công tác xã hội (70%)**
- Ngành kém nhất: **Công nghệ nhiên liệu sinh học** và **Kỹ thuật CNTT** — chỉ **8%** tốt nghiệp đúng hạn, tỉ lệ bỏ học 67% và 54%
- **Nữ** tốt nghiệp nhiều hơn nam
- Sinh viên **có học bổng** và **đóng học phí đúng hạn** thành công hơn rõ rệt
- Sinh viên **học ban ngày** tốt nghiệp sớm hơn học buổi tối

> Những quan sát này rất hợp để đối chiếu với các split mà cây tự tìm ra. Nếu cây chọn `Course` hoặc `Tuition fees up to date` ở tầng trên → khớp với EDA → viết được đoạn phân tích thuyết phục.

## A8. ⚠️ Vì sao dataset phù hợp cho decision tree modeling (bắt buộc — mục 3.2.a)

Đề yêu cầu nguyên văn: *"Explain why the dataset is appropriate for decision tree modeling."* Đây là câu trả lời trực tiếp, dùng được ngay cho mục Dataset Description:

1. **Feature có ngữ nghĩa rõ ràng** → mọi split đều diễn giải được thành câu bình thường (VD: `Tuition fees up to date = 0` → "chưa đóng học phí"). Decision tree là mô hình *diễn giải được* (interpretable), và dataset này tận dụng đúng thế mạnh đó — khác với dữ liệu ảnh hay văn bản, nơi cây quyết định không phát huy được lợi thế diễn giải.
2. **Trộn cả categorical và numerical** (xem A4) → sau khi các biến nominal được mã hóa phù hợp, cây xử lý các cột số mà không cần scale (B2). `DecisionTreeClassifier` của scikit-learn không nhận chuỗi category trực tiếp.
3. **Có mất cân bằng lớp thật** (50%/32%/18%, xem A3) → tạo tình huống thực tế để áp dụng và so sánh kỹ thuật xử lý imbalance — đúng một trong các hướng cải tiến đề gợi ý ở mục 3.2.d.
4. **Feature chia rõ theo thời điểm thu thập** (6 nhóm ở A4) → cho phép thí nghiệm feature selection có ý nghĩa ứng dụng thực (dự báo sớm), không chỉ chọn feature theo thống kê thuần túy.
5. **Không có missing value** (A1) → nhóm dồn thời gian cho phân tích và diễn giải thay vì làm sạch dữ liệu — đúng tinh thần đề nhấn mạnh ở mục 3.1: *"not only to run a ready-made model, but also to explain clearly how the tree is constructed, how it behaves on the dataset, and why certain improvements help."*

---

# PHẦN B — QUYẾT ĐỊNH TIỀN XỬ LÝ

## B1. Vấn đề: category mã hóa bằng số

Scikit-learn **không hiểu categorical**. Nó sẽ tạo split kiểu `Course <= 8.5` — vô nghĩa vì mã ngành không có thứ tự.

**Pipeline canonical đã chốt cách xử lý sau:**

| Cách | Ưu | Nhược |
|---|---|---|
| **One-hot encode** | `Marital Status`, `Application mode`, `Course`, `Previous qualification` | Ít cardinality hơn; split theo dummy dễ diễn giải |
| **Giữ mã số** | `Nacionality`, qualification/occupation của cha mẹ | Tránh tạo quá nhiều cột thưa; phải nêu hạn chế thứ tự giả trong báo cáo |
| **Giữ ordinal** | `Application order` | Có thứ tự tự nhiên |

Kết quả sau tiền xử lý là **90 cột encoded**. Hợp đồng cột và split được cố định trong `src/data.py` và được tất cả notebook dùng chung.

## B2. Không cần scale

Cây quyết định **không cần chuẩn hóa dữ liệu**. Nếu nhóm thấy tutorial nào dùng `StandardScaler` với decision tree thì đó là thừa. Nêu điểm này trong báo cáo cũng là một điểm cộng nhỏ.

## B3. Split dữ liệu — quy ước chung

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,          # BẮT BUỘC — dữ liệu mất cân bằng
    random_state=42      # BẮT BUỘC — thống nhất toàn nhóm
)
```

---

# PHẦN C — CHI TIẾT 5 CẤU HÌNH MÔ HÌNH

## C0. Baseline (B làm)

```python
DecisionTreeClassifier(random_state=42)   # không giới hạn gì
```

**Artifact đã có:**
- [x] Dòng `M0` đủ schema 16 cột trong `outputs/results.csv`
- [x] `figures/B_tree_M0_full.png`
- [x] `figures/B_tree_M0_top3.png` (`max_depth=3`, hiển thị từ depth 0 đến 3)
- [x] `figures/B_cm_M0.png`
- [x] `outputs/rules_M0.txt` và `outputs/classification_report_M0.txt`

**Dự đoán kết quả:** train accuracy ≈ 1.00, test accuracy ≈ 0.65–0.72, độ sâu 25–35 tầng. Chênh lệch train/test khổng lồ này **chính là bằng chứng overfit** mà đề yêu cầu bình luận.

> 💡 **Kiểm tra phụ đã chạy, không tính là cải tiến chính:** Entropy đạt test accuracy `0.6531`, thấp hơn Gini `0.6689` **1.58 điểm phần trăm** trên cùng split. Vì vậy nhóm giữ Gini cho baseline và tập trung vào ba hướng cải tiến chính.

## C1. Pruning (C làm)

**Quy trình đúng:**
1. `path = clf.cost_complexity_pruning_path(X_train, y_train)` → lấy mảng `ccp_alphas`
2. Với mỗi alpha, train một cây, đánh giá bằng **cross-validation trên TRAIN set**
3. Chọn alpha cho CV score cao nhất
4. Train lại với alpha đó, đánh giá **một lần duy nhất** trên test
5. Thêm grid nhỏ cho `max_depth` ∈ {5,8,10,15} và `min_samples_leaf` ∈ {1,5,10,20}

> ⚠️ **Bẫy:** KHÔNG chọn alpha theo test accuracy. Đó là tuning trên test set — gian lận thống kê, thầy sẽ hỏi.

**Artifact đã có:**
- [x] `figures/C_ccp_alpha_curve.png` — cost-complexity path và CV score **chỉ trên train**, không vẽ test curve trong giai đoạn tuning
- [x] `figures/C_tree_M1.png`, `figures/C_cm_M1.png`
- [x] Bảng 16 cấu hình grid search trong notebook
- [x] `outputs/classification_report_M1.txt` và đúng một dòng `M1`

**Dự đoán:** test accuracy tăng nhẹ hoặc giữ nguyên, nhưng **độ sâu giảm từ ~30 xuống ~5–8 tầng, số leaf giảm hàng chục lần**. Đây mới là kết quả đáng nói: *"giữ nguyên hiệu năng mà cây dễ đọc hơn 10 lần"*.

## C2. Class imbalance (D làm)

**Hai thí nghiệm:**
```python
# M2a
DecisionTreeClassifier(class_weight='balanced', random_state=42)

# M2b — SMOTE
from imblearn.over_sampling import SMOTE
X_res, y_res = SMOTE(sampling_strategy="auto", random_state=42, k_neighbors=5).fit_resample(X_train, y_train)  # CHỈ train!
```

> ⚠️ **Bẫy chí mạng:** SMOTE **chỉ áp dụng trên tập train**, tuyệt đối không trước khi split. Sai chỗ này = rò rỉ dữ liệu, accuracy ảo, và là câu hỏi đầu tiên thầy sẽ hỏi.

**Artifact đã có:**
- [x] `figures/D_tree_M2a.png`, `figures/D_tree_M2a_full.png`, `figures/D_tree_M2b.png`, `figures/D_tree_M2b_full.png`
- [x] `figures/D_cm_M2a.png` và `figures/D_cm_M2b.png`
- [x] Bảng so sánh recall từng lớp trong notebook/bản thảo f.2
- [x] Hai classification report và đúng một dòng cho mỗi `M2a`, `M2b`

**Dự đoán quan trọng:** accuracy tổng **có thể giảm**, trong khi recall lớp Enrolled và Dropout **tăng**. Đây không phải lỗi. Đề cho phép rõ: *"explain why the method improves **or does not improve**"*. Phân tích đánh đổi này là phần hay nhất của M2.

## C3. Dự báo sớm / Feature selection (E làm)

**Bỏ chính xác 12 cột sau:**
```
Curricular units 1st sem (credited)
Curricular units 1st sem (enrolled)
Curricular units 1st sem (evaluations)
Curricular units 1st sem (approved)
Curricular units 1st sem (grade)
Curricular units 1st sem (without evaluations)
Curricular units 2nd sem (credited)
Curricular units 2nd sem (enrolled)
Curricular units 2nd sem (evaluations)
Curricular units 2nd sem (approved)
Curricular units 2nd sem (grade)
Curricular units 2nd sem (without evaluations)
```

**Còn lại 24 feature.**

> ✅ **Giữ lại 3 biến vĩ mô** (`Unemployment rate`, `Inflation rate`, `GDP`) — chúng phụ thuộc năm nhập học, đã biết tại thời điểm dự báo, không phải thông tin tương lai.
> M3 canonical cũng giữ `International`: thí nghiệm chỉ thay đổi đúng 12 feature học kỳ để còn 24 feature gốc và dễ đối chiếu trực tiếp với M0.

**Artifact đã có:**
- [x] `figures/E_tree_M3.png` và `figures/E_cm_M3.png`
- [x] `outputs/classification_report_M3.txt` và đúng một dòng M3 trong `outputs/results.csv`
- [x] `figures/E_feature_importance.png` + `outputs/E_feature_importance_comparison.csv`
- [x] `figures/E_feature_importance_permutation.png` + `outputs/E_feature_importance_permutation.csv`
- [x] Quality gate bảo vệ M0/M1/M2a/M2b và artifact D

**Kết quả canonical hiện tại:** accuracy giảm từ M0 `0.6689` xuống M3 `0.5412`. **Đó là kết quả mong đợi và là điểm mấu chốt:**

> *"M0 cao hơn M3 **12.77 điểm phần trăm accuracy**, nhưng M0 cần biết kết quả hai học kỳ. M3 kém chính xác hơn nhưng là cấu hình duy nhất trong năm cấu hình có thể chạy ngay lúc nhập học. Model tốt nhất theo accuracy không nhất thiết là model phù hợp nhất với mục tiêu can thiệp sớm."*

---

# PHẦN D — METRICS BẮT BUỘC

> ⚠️ **Đã rà soát lại và bổ sung 2 cột bị thiếu (Precision, ROC-AUC).** Đề ghi rõ ở mục 3.2.b: *"Confusion Matrix, Accuracy, Precision, Recall, F1-score, ROC-AUC, ..."* — bản trước của file này chỉ có Accuracy/Recall/F1, thiếu Precision và ROC-AUC. Bảng dưới đã đủ.

Mỗi model ghi đủ **12 cột số liệu** vào `results.csv` (tổng schema 16 cột khi tính cả 4 cột định danh/mô tả):

| Cột | Công thức / Ghi chú |
|---|---|
| `train_acc` | Để so với test → bằng chứng overfit |
| `test_acc` | Đề yêu cầu |
| `error_rate` | **`1 - test_acc`** — đề yêu cầu rõ, lặp 3 lần, đừng quên |
| `precision_macro` | `precision_score(..., average='macro')` — đề yêu cầu rõ, dễ bị bỏ sót nhất |
| `recall_macro` | `recall_score(..., average='macro')` |
| `f1_macro` | `f1_score(..., average='macro')` — công bằng 3 lớp |
| `roc_auc_macro` | Xem công thức riêng bên dưới — đề nêu đích danh, hay bị quên vì phức tạp hơn với bài toán 3 lớp |
| `recall_dropout` | Lớp quan trọng nhất về ứng dụng |
| `recall_enrolled` | Lớp thiểu số, chỗ khó nhất |
| `recall_graduate` | Lớp đa số |
| `tree_depth` | `model.get_depth()` |
| `n_leaves` | `model.get_n_leaves()` |

**Schema `results.csv`:**
```
model_id,model_name,params,train_acc,test_acc,error_rate,precision_macro,recall_macro,f1_macro,roc_auc_macro,recall_dropout,recall_enrolled,recall_graduate,tree_depth,n_leaves,author
```

**ROC-AUC với bài toán 3 lớp — cần `predict_proba`, không phải `predict`:**
```python
from sklearn.metrics import roc_auc_score

y_proba = model.predict_proba(X_test)          # trả về xác suất cho cả 3 lớp
roc_auc = roc_auc_score(
    y_test, y_proba,
    multi_class='ovr',      # one-vs-rest — cách chuẩn cho multi-class
    average='macro'
)
```
> Decision tree hỗ trợ `predict_proba` sẵn, không cần thêm gì. Thứ tự cột của `y_proba` khớp với `model.classes_`, sklearn tự xử lý — không cần tự binarize nhãn.

**Ngoài `results.csv`, mỗi model còn cần xuất riêng (dùng cho mục d/e/f của báo cáo, không nhét hết vào 1 dòng CSV):**
- **Confusion matrix** (hình) — đề yêu cầu trực tiếp
- **`classification_report`** đầy đủ (lưu `outputs/classification_report_M{n}.txt`) — đây là nơi có **precision/recall/f1 theo từng lớp** (Dropout/Enrolled/Graduate riêng biệt), chi tiết hơn 3 cột macro trong `results.csv`. Dùng bảng này khi viết mục d/f cho từng model; dùng `results.csv` khi viết bảng so sánh tổng ở mục g.

---

# PHẦN E — TRẠNG THÁI BÀN GIAO VÀ VIỆC CÒN LẠI

> Trạng thái được đồng bộ ngày 2026-08-30. Pha code/thí nghiệm đã hoàn tất; các ô chưa đánh dấu là đầu vào của pha report/slide/video hoặc thông tin nhóm mà repository không thể tự suy đoán.

## E1. Việc chung (cả nhóm)

- [ ] Xác nhận **GroupID**, danh sách thành viên và **deadline** với giảng viên
- [x] Git repository và quy trình branch đã hoạt động
- [x] Dự án báo cáo LaTeX trong `docs/report/` đã thay cho kế hoạch Google Doc
- [x] Toàn bộ bước có ngẫu nhiên dùng `random_state=42`

## E2. A — Data Lead

- [x] Dataset gốc có tại `data/raw/data.csv`; notebook 01 có thể tải lại khi bootstrap
- [x] Xác nhận shape, schema, missing value, duplicate và phân bố target
- [x] EDA và 5 hình prefix `A_`
- [x] `docs/feature_types.md`
- [x] `src/data.py`: `load_and_preprocess()` + `get_train_test()`
- [x] `outputs/comparison_table.csv` và `figures/comparison.png`
- [x] Bản LaTeX nền cho mục **b**, **c**, **g**, **h**; cần biên tập cuối trong pha viết report

## E3. B — Baseline & Tree Analysis

- [x] `src/evaluate.py` — helper ghi 12 số liệu/schema 16 cột, classification report và confusion matrix
- [x] `src/visualize.py` — `plot_tree_figure()`, `export_rules()`
- [x] Train M0 và xuất đủ artifact mục C0
- [ ] Hoàn thiện mục **e** Analysis of the Tree trong report, trả lời 5 câu:
  1. Root split là feature nào? Tại sao thuật toán chọn nó?
  2. Ba tầng đầu chia theo logic gì? Diễn giải bằng tiếng Việt.
  3. Cây sâu bao nhiêu tầng, bao nhiêu leaf? Có leaf nào chỉ 1–2 mẫu?
  4. Train vs test chênh bao nhiêu → overfit?
  5. Viết 2–3 luật IF-THEN đầy đủ
- [ ] Chuyển bản thảo đã kiểm chứng sang mục **d** Baseline Model
- [x] Dọn code và viết `README.md`

**Quy tắc viết luật:** chỉ chép IF–THEN từ `outputs/rules_M0.txt` và đối chiếu số mẫu/impurity trên cây đã fit; không dùng số minh họa chưa được xác minh.

## E4. C — Pruning

- [x] Cost-complexity path và tài liệu API đã được đối chiếu
- [x] Chọn alpha bằng CV chỉ trên train
- [x] Grid 16 cấu hình cho `max_depth`, `min_samples_leaf`
- [x] Xuất đủ artifact mục C1
- [ ] Chuyển bản thảo đã kiểm chứng sang mục **f.1**
- [x] Full pipeline đã được kiểm tra trong môi trường canonical

## E5. D — Class Imbalance

- [x] Nền tảng SMOTE đã có trong references
- [x] Train M2a với `class_weight='balanced'`
- [x] Train M2b với SMOTE **chỉ trên train**
- [x] Bảng so sánh recall từng lớp M0/M2a/M2b
- [x] Xuất đủ artifact mục C2
- [ ] Chuyển bản thảo đã kiểm chứng sang mục **f.2**, giữ phân tích trade-off accuracy/recall

## E6. E — Early-warning Feature Selection

- [x] Loại đúng 12 cột học kỳ và train M3 trên 24 feature gốc/78 cột encoded
- [x] So sánh Gini/MDI và held-out grouped permutation importance M0/M3
- [x] Xuất đủ artifact mục C3
- [x] Kiểm tra tái lập và bảo vệ artifact D
- [ ] Viết nội dung cuối cho mục **f.3** trong pha report

## E7. Trưởng nhóm — đóng gói

- [ ] Điền bảng đóng góp cụ thể từng thành viên (mục **a**)
- [ ] Kiểm tra tên file: `[GroupID].zip`, `[GroupID - Report].pdf`, `[GroupID - Code].zip`, `[GroupID - Video].mp4`
- [ ] Nếu nộp link video: đặt quyền công khai, tự mở thử ở chế độ ẩn danh
- [ ] Đối chiếu: số liệu báo cáo = số liệu video = `results.csv`
- [ ] Đối chiếu: bảng đóng góp khớp với người thực sự nói trong video

---

# PHẦN F — CẤU TRÚC REPO

```
[GroupID]-decision-tree/
├── README.md
├── AGENT.md
├── requirements.txt
├── requirements-lock.txt       ⭐ lock canonical — chỉ A/Integrator cập nhật
├── data/raw/data.csv
├── src/
│   ├── data.py                ⭐ A — load, preprocess, split
│   ├── evaluate.py            B — schema 16 cột + report/confusion matrix
│   └── visualize.py           B — vẽ cây, export rules
├── notebooks/
│   ├── 01_eda.ipynb                A
│   ├── 02_baseline.ipynb           B
│   ├── 03_improve_pruning.ipynb    C
│   ├── 04_improve_imbalance.ipynb  D
│   ├── 05_improve_features.ipynb   E
│   └── 06_comparison.ipynb         A
├── figures/                      22 PNG canonical, prefix A/B/C/D/E + comparison
├── outputs/
│   ├── results.csv            ⭐ 5 cấu hình, schema 16 cột
│   ├── comparison_table.csv
│   ├── classification_report_M*.txt
│   └── rules_M0.txt
└── docs/
    ├── 00-DE-BAI-GOC.pdf
    ├── feature_types.md
    └── report/                    LaTeX source + report.pdf
```

**Dependency trực tiếp trong `requirements.txt`:**
```
pandas
numpy
scikit-learn>=1.0
matplotlib
seaborn
imbalanced-learn
ucimlrepo
```

`requirements-lock.txt` khóa cả dependency trực tiếp lẫn bắc cầu của môi trường canonical dùng để tái lập artifact. Chỉ A/Integrator refresh file này sau khi cài sạch, chạy `pip check` và chạy lại đầy đủ notebook/artifact bị ảnh hưởng.

---

# PHẦN G — MẸO VẼ CÂY

Cây baseline có hàng trăm node — in vào A4 sẽ thành vệt mờ. Xuất **3 hình**:

1. **Cây đầy đủ, thu nhỏ** — chỉ để minh họa "cây rất lớn và rối", chính là bằng chứng overfit
2. **`plot_tree(model, max_depth=3, filled=True, feature_names=..., class_names=...)`** — đọc được, dùng để phân tích luật
3. **Cây sau pruning (M1)** — thường vài tầng, in đẹp

Thông số: `figsize=(20,12)`, `dpi=150`, lưu PNG.
Thêm `export_text()` vào phụ lục để có bản luật dạng chữ.

---

# PHẦN H — TÀI LIỆU THAM KHẢO

**Dataset**
1. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
2. Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student Dropout and Academic Success. *Data*, 7(11), 146. https://doi.org/10.3390/data7110146 ← **bảng feature, đa cộng tuyến, feature importance đều lấy từ đây**
3. Martins, M. V. et al. (2021). Early Prediction of Student's Performance in Higher Education: A Case Study. *AISC*, 1365, 166–175. ← chống lưng cho M3

**Kỹ thuật**
4. Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830.
5. Scikit-learn. *DecisionTreeClassifier*. https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
6. Scikit-learn. *Post pruning decision trees with cost complexity pruning*. https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html ← **C đọc trước khi code**
7. Chawla, N. V. et al. (2002). SMOTE. *JAIR*, 16, 321–357. ← **D trích dẫn**

**Lý thuyết**
8. Quinlan, J. R. (1986). Induction of Decision Trees. *Machine Learning*, 1(1), 81–106.
9. Breiman, L. et al. (1984). *Classification and Regression Trees*. Wadsworth. ← gốc của CART & cost-complexity pruning
10. Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill. Ch.3.

---

# PHẦN I — LƯU Ý ĐẠO ĐỨC (nên có 3–4 câu trong báo cáo)

Dataset chứa biến nhạy cảm: giới tính, quốc tịch, tình trạng hôn nhân, trình độ và nghề nghiệp của cha mẹ.

Báo cáo nên ghi rõ: các split trên những biến này chỉ phản ánh **tương quan trong mẫu khảo sát tại một trường đại học Bồ Đào Nha giai đoạn 2008–2019**, không phải quan hệ nhân quả, và không nên dùng làm cơ sở cho chính sách phân biệt đối xử với sinh viên.

Một đoạn ngắn thôi, nhưng nó thể hiện độ chín của nhóm và thường được đánh giá cao.

---

# PHẦN J — RÀ SOÁT ĐỐI CHIẾU TOÀN BỘ MỤC BÁO CÁO (đúng theo 3.4.a → i của đề)

> Đối chiếu từng dòng đề gốc với file này. Dùng bảng này để tự kiểm trước khi nộp — nếu cột cuối còn trống, chưa xong.

| Mục đề (3.4) | Yêu cầu nguyên văn (rút gọn) | Đã chuẩn bị ở đâu trong file này | Việc còn lại (tự điền số liệu thật) |
|---|---|---|---|
| **a.** Group Introduction | Tên nhóm, MSSV, **đóng góp cụ thể từng người** | Bảng J1 ngay dưới đây | Điền tên thật, MSSV, GroupID |
| **b.** Introduction | Giới thiệu decision tree, mục tiêu đồ án | Tham khảo Phần H mục 8–9 (Quinlan, Breiman) | Viết ~1 trang dựa lý thuyết chuẩn |
| **c.** Dataset Description | Nguồn, số mẫu/feature/target, tiền xử lý, **vì sao phù hợp** | Phần A1–A8, Phần B1–B3 | Số liệu đã xác minh; biên tập văn phong cuối |
| **d.** Baseline Model | Mô tả, quy trình train/test, **hình cây**, accuracy + error rate | Phần B3, Phần C0, Phần D, Phần G | Chuyển bản thảo đã kiểm chứng sang LaTeX |
| **e.** Analysis of the Tree | Trình bày cây, cấu trúc, điểm mạnh/yếu | Phần C0 + 5 câu hỏi bắt buộc ở mục E3 | Phân tích cụ thể trên cây thật, không viết chung chung |
| **f.** Improvement Methods (2–3) | Mô tả, **modified tree/setting**, accuracy + error rate, giải thích vì sao | Phần C1/C2/C3 — cả 3 đã có artifact | Chuyển ba bản thảo sang LaTeX |
| **g.** Comparison of Results | So sánh, bảng/hình, chỉ ra tốt nhất | `results.csv` (16 cột), `comparison_table.csv`, `comparison.png` | Năm cấu hình đã hoàn tất; biên tập cuối |
| **h.** Conclusion | Tóm tắt, phát hiện chính, đánh giá hiệu quả decision tree | — viết mới dựa trên kết quả thật | Viết ~1 trang |
| **i.** References | Nguồn dataset, tài liệu, thư viện | Phần H — 10 mục đã soạn sẵn | Bổ sung nếu trích thêm nguồn khác |

**Ba metric đề nêu tên mà bản trước của file này còn thiếu — đã bổ sung ở Phần D:** Precision (macro), ROC-AUC (macro, one-vs-rest). Confusion Matrix, Accuracy, Recall, F1-score đã có sẵn từ đầu.

## J1. Bảng đóng góp thành viên — copy trực tiếp vào mục a báo cáo

| Thành viên | MSSV | Đóng góp cụ thể | % |
|---|---|---|---|
| [Tên A] | | Thu thập & mô tả dữ liệu, EDA, pipeline tiền xử lý, tổng hợp bảng so sánh, viết mục Introduction/Dataset Description/Comparison/Conclusion | 20% |
| [Tên B] | | Xây dựng và đánh giá baseline, trực quan hóa cây, trích luật quyết định, viết mục Baseline Model & Analysis of the Tree | 20% |
| [Tên C] | | Nghiên cứu và triển khai cải tiến pruning (cost-complexity + giới hạn depth/leaf), viết mục Improvement Method 1 | 20% |
| [Tên D] | | Nghiên cứu và triển khai cải tiến xử lý mất cân bằng lớp (class weighting, SMOTE), viết mục Improvement Method 2 | 20% |
| [Tên E] | | Nghiên cứu và triển khai feature selection cho dự báo sớm, kiểm chứng Gini/MDI và grouped permutation importance, bảo đảm tái lập và tích hợp an toàn với kết quả D | 20% |

> Nếu đóng góp thực tế không đều thì ghi đúng thực tế. Trưởng nhóm đối chiếu bảng này với **ai thực sự nói phần nào trong video** trước khi nộp (checklist E7).

## J2. Sản phẩm phụ — tùy chọn, không bắt buộc

Đề cho phép nộp thêm `[GroupID - Materials].txt` (mục 1 của đề). Nếu nhóm có tài liệu phụ (link Colab, ghi chú mở rộng, log thử nghiệm) thì đính kèm — không ảnh hưởng điểm nếu bỏ qua.
