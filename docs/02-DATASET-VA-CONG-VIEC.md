# DATASET & CÔNG VIỆC CHI TIẾT

> File kỹ thuật. Ai làm phần nào đọc kỹ mục của mình.
> Tổng quan xem `01-TOM-TAT-HUONG-DI.md`.

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

## A2. ⚠️ Cảnh báo về số feature — phải xử lý

Trang UCI ghi **36 features**. Nhưng Table 1 của bài báo gốc chỉ liệt kê **34 features**.

Chênh lệch nằm ở 2 cột có trong file CSV phát hành nhưng không có trong bảng bài báo:
- `Previous qualification (grade)`
- `Admission grade`

**→ Việc phải làm (A):** chạy `df.shape` và `df.columns.tolist()`, báo cáo **con số đếm thực tế**, kèm 1 câu ghi chú về chênh lệch này. Đây là điểm cộng — chứng minh nhóm đọc dữ liệu thật chứ không chép lại metadata.

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
| Marital status | **Category** (1–6) | 1=Độc thân, 2=Kết hôn, 3=Góa, 4=Ly hôn, 5=Sống chung, 6=Ly thân |
| Nationality | **Category** (1–21) | 1=Bồ Đào Nha (chiếm áp đảo) |
| Displaced | Binary | 1=sống xa nhà |
| Gender | Binary | 1=nam, 0=nữ |
| Age at enrollment | **Numeric** | 17–70, trung bình 23.1, median 20 |
| International | Binary | 1=sinh viên quốc tế |

### Nhóm 2 — Kinh tế xã hội (8 cột)
| Cột | Kiểu thực chất | Ghi chú |
|---|---|---|
| Mother's qualification | **Category** (1–34) | Trình độ học vấn mẹ |
| Father's qualification | **Category** (1–34) | Trình độ học vấn cha |
| Mother's occupation | **Category** (1–32) | Nghề nghiệp mẹ |
| Father's occupation | **Category** (1–46) | Nghề nghiệp cha |
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
| Application mode | **Category** (1–18) | Hình thức xét tuyển |
| Application order | Ordinal (1–9) | Nguyện vọng thứ mấy |
| **Course** | **Category** (1–17) | ⭐ **Feature quan trọng**. VD: 12=Điều dưỡng, 7=CNTT, 1=Công nghệ nhiên liệu sinh học |
| Daytime/evening attendance | Binary | 1=ban ngày (89.1%) |
| Previous qualification | **Category** (1–17) | Bằng cấp trước đó |
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

> ⚠️ **Đã rà soát lại 2026-08-30**: bảng bên dưới từng ghi sai 2 giá trị (`Nationality`↔`International` = 0.912 và `Mother's/Father's occupation` = 0.724, hạng 9). Tính lại trực tiếp trên `data/raw/data.csv` cho kết quả khác hẳn — bảng dưới đây đã là số đúng, sắp lại đúng thứ tự giảm dần theo số đã sửa.

| Cặp feature | r |
|---|---|
| 1st sem (credited) ↔ 2nd sem (credited) | **0.945** |
| 1st sem (enrolled) ↔ 2nd sem (enrolled) | **0.943** |
| Mother's occupation ↔ Father's occupation | **0.910** |
| 1st sem (approved) ↔ 2nd sem (approved) | **0.904** |
| 1st sem (grade) ↔ 2nd sem (grade) | 0.837 |
| Nationality ↔ International | 0.791 |
| 1st sem (evaluations) ↔ 2nd sem (evaluations) | 0.779 |
| 1st sem (credited) ↔ 1st sem (enrolled) | 0.774 |
| 2nd sem (approved) ↔ 2nd sem (grade) | 0.761 |
| 2nd sem (enrolled) ↔ 2nd sem (approved) | 0.703 |

> Cây quyết định không bị ảnh hưởng nặng bởi đa cộng tuyến như hồi quy tuyến tính, **nhưng** nó làm feature importance bị chia nhỏ và khiến cây kém ổn định. Đây là căn cứ để E loại bớt cột trùng lặp.
> Sau khi sửa số: `Mother's occupation ↔ Father's occupation` (r=0.91) mới là cặp cao thứ 3 toàn dataset — rõ ràng hơn cả `Nationality ↔ International` (r=0.79, vẫn cao nhưng không còn là cặp nổi bật nhất). Cân nhắc bỏ một trong hai cột nghề nghiệp cha/mẹ, hoặc một trong hai cột `Nationality`/`International`, tuỳ mục tiêu.

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
2. **Trộn cả categorical và numerical** (xem A4) → cây xử lý tự nhiên cả hai loại mà không cần chuẩn hóa (B2), khác với các mô hình như KNN hay hồi quy tuyến tính bắt buộc phải scale.
3. **Có mất cân bằng lớp thật** (50%/32%/18%, xem A3) → tạo tình huống thực tế để áp dụng và so sánh kỹ thuật xử lý imbalance — đúng một trong các hướng cải tiến đề gợi ý ở mục 3.2.d.
4. **Feature chia rõ theo thời điểm thu thập** (6 nhóm ở A4) → cho phép thí nghiệm feature selection có ý nghĩa ứng dụng thực (dự báo sớm), không chỉ chọn feature theo thống kê thuần túy.
5. **Không có missing value** (A1) → nhóm dồn thời gian cho phân tích và diễn giải thay vì làm sạch dữ liệu — đúng tinh thần đề nhấn mạnh ở mục 3.1: *"not only to run a ready-made model, but also to explain clearly how the tree is constructed, how it behaves on the dataset, and why certain improvements help."*

---

# PHẦN B — QUYẾT ĐỊNH TIỀN XỬ LÝ

## B1. Vấn đề: category mã hóa bằng số

Scikit-learn **không hiểu categorical**. Nó sẽ tạo split kiểu `Course <= 8.5` — vô nghĩa vì mã ngành không có thứ tự.

**Hai lựa chọn, chọn cái nào cũng được nhưng PHẢI giải thích trong báo cáo:**

| Cách | Ưu | Nhược |
|---|---|---|
| **(a)** Giữ nguyên mã số | Đơn giản, cây gọn | Split không diễn giải được → phải ghi vào Limitations |
| **(b)** One-hot encode | Split thành `Course_Nursing <= 0.5` = *"có phải ngành Điều dưỡng không?"* → dễ hiểu | Cây rộng ra, nhiều cột hơn |

**Khuyến nghị:** làm hỗn hợp
- **One-hot** các cột ít giá trị: `Course` (17), `Application mode` (18), `Marital status` (6), `Previous qualification` (17)
- **Giữ nguyên** các cột nhiều giá trị: `Mother's/Father's occupation` (32/46), `Mother's/Father's qualification` (34), `Nationality` (21)
- Ghi rõ lý do trong báo cáo: one-hot 46 nghề nghiệp sẽ tạo 46 cột thưa, làm cây kém ổn định

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

# PHẦN C — CHI TIẾT 4 MODEL

## C0. Baseline (B làm)

```python
DecisionTreeClassifier(random_state=42)   # không giới hạn gì
```

**Cần xuất ra:**
- [ ] `results.csv` — 1 dòng đủ 8 metrics
- [ ] `figures/tree_M0_full.png` — cây đầy đủ (sẽ rất rối, đó là điều ta muốn cho thấy)
- [ ] `figures/tree_M0_top3.png` — `plot_tree(..., max_depth=3)` để đọc được
- [ ] `figures/cm_M0.png` — confusion matrix
- [ ] `outputs/rules_M0.txt` — `export_text()`

**Dự đoán kết quả:** train accuracy ≈ 1.00, test accuracy ≈ 0.65–0.72, độ sâu 25–35 tầng. Chênh lệch train/test khổng lồ này **chính là bằng chứng overfit** mà đề yêu cầu bình luận.

> 💡 **Kiểm tra nhanh — không tính vào 3 cải tiến chính thức:** đề liệt kê *"Changing the splitting criterion (e.g., Gini vs. Entropy)"* làm một ví dụ hướng cải tiến (mục 3.2.d). Nhóm không chọn hướng này làm 1 trong 3 cải tiến chính (đề chỉ yêu cầu 2–3, không bắt làm hết danh sách), nhưng B nên chạy thêm 1 dòng `DecisionTreeClassifier(criterion='entropy', random_state=42)` để so nhanh với baseline (`criterion='gini'` mặc định), rồi ghi 1–2 câu trong mục d: *"đã thử criterion='entropy', chênh lệch không đáng kể (X%), nên nhóm tập trung vào 3 hướng có tác động lớn hơn."* Chỉ tốn 1 dòng code, nhưng cho thấy nhóm đã cân nhắc cả không gian giải pháp trước khi chọn.

## C1. Pruning (C làm)

**Quy trình đúng:**
1. `path = clf.cost_complexity_pruning_path(X_train, y_train)` → lấy mảng `ccp_alphas`
2. Với mỗi alpha, train một cây, đánh giá bằng **cross-validation trên TRAIN set**
3. Chọn alpha cho CV score cao nhất
4. Train lại với alpha đó, đánh giá **một lần duy nhất** trên test
5. Thêm grid nhỏ cho `max_depth` ∈ {5,8,10,15} và `min_samples_leaf` ∈ {1,5,10,20}

> ⚠️ **Bẫy:** KHÔNG chọn alpha theo test accuracy. Đó là tuning trên test set — gian lận thống kê, thầy sẽ hỏi.

**Cần xuất ra:**
- [ ] `figures/ccp_alpha_curve.png` — đồ thị alpha vs train/test accuracy
- [ ] `figures/tree_M1.png` — cây sau pruning (sẽ đẹp, in được)
- [ ] Bảng grid search
- [ ] 1 dòng `results.csv`

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

**Cần xuất ra:**
- [ ] `figures/D_tree_M2a.png`, `figures/D_tree_M2a_full.png`, `figures/D_tree_M2b.png`, `figures/D_tree_M2b_full.png` — ⚠️ **đừng quên hình cây.** Đề yêu cầu ở mục 3.4.f: *"Modified tree **or** model setting"* cho MỖI cải tiến, không riêng M1/M3. `class_weight='balanced'` vẫn làm Gini bị tính lại theo trọng số → cấu trúc split có thể đổi so với M0, nên vẫn cần so hình cây, không chỉ nêu tham số
- [ ] `figures/D_cm_M2a.png` và `figures/D_cm_M2b.png`
- [ ] Bảng so sánh **recall từng lớp** M0 vs M2a vs M2b
- [ ] 2 dòng `results.csv`

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

**Mở rộng (nếu còn thời gian):** dựa vào bảng A6, bỏ thêm `International` (r=0.79 với `Nationality`) → còn 23 feature.

**Cần xuất ra:**
- [ ] `figures/tree_M3.png`
- [ ] `figures/feature_importance.png` — so sánh top-10 importance của M0 vs M3
- [ ] 1 dòng `results.csv`

**Dự đoán:** accuracy giảm đáng kể (có thể 0.70 → 0.62–0.66). **Đó là kết quả mong đợi và là điểm mấu chốt:**

> *"M0 chính xác hơn M3 khoảng X%, nhưng M0 cần biết kết quả 2 học kỳ — tức là chỉ cảnh báo được khi sinh viên đã trượt môn. M3 kém hơn nhưng là model duy nhất triển khai được như hệ thống can thiệp sớm. Model tốt nhất theo accuracy không phải model tốt nhất theo mục tiêu ứng dụng."*

---

# PHẦN D — METRICS BẮT BUỘC

> ⚠️ **Đã rà soát lại và bổ sung 2 cột bị thiếu (Precision, ROC-AUC).** Đề ghi rõ ở mục 3.2.b: *"Confusion Matrix, Accuracy, Precision, Recall, F1-score, ROC-AUC, ..."* — bản trước của file này chỉ có Accuracy/Recall/F1, thiếu Precision và ROC-AUC. Bảng dưới đã đủ.

Mỗi model ghi đủ **10 cột số liệu** vào `results.csv`:

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

# PHẦN E — DANH SÁCH VIỆC PHẢI LÀM

## E1. Việc chung (cả nhóm)

- [ ] Xác nhận **GroupID** và **deadline** với thầy (`vntan.work@gmail.com`)
- [ ] Tạo GitHub repo, ai cũng push được
- [ ] Tạo Google Doc chung cho báo cáo
- [ ] Thống nhất `random_state=42`

## E2. A — Data Lead

- [ ] Tải dataset, lưu `data/raw/data.csv`
- [ ] Chạy `df.shape`, `df.info()`, `df.isnull().sum()` → xác nhận số thực tế
- [ ] EDA: phân bố target, thống kê mô tả, heatmap tương quan (4–5 hình)
- [ ] Viết `docs/feature_types.md` — cột nào là category dù lưu số
- [ ] ⭐ Viết `src/data.py`: `load_and_preprocess()` + `get_train_test()` — **deliverable quan trọng nhất, phải xong sớm nhất**
- [ ] Gộp `results.csv` thành bảng so sánh cuối
- [ ] Vẽ `figures/comparison.png`
- [ ] Viết mục **b** Introduction, **c** Dataset Description, **g** Comparison, **h** Conclusion

## E3. B — Baseline & Tree Analysis

- [ ] Viết `src/evaluate.py` — hàm tính đủ 8 metrics, tự append `results.csv`
- [ ] Viết `src/visualize.py` — `plot_tree_figure()`, `export_rules()`
- [ ] Train M0, xuất đủ deliverable mục C0
- [ ] ⭐ Viết mục **e** Analysis of the Tree — mục ăn điểm nhất, phải trả lời 5 câu:
  1. Root split là feature nào? Tại sao thuật toán chọn nó?
  2. Ba tầng đầu chia theo logic gì? Diễn giải bằng tiếng Việt.
  3. Cây sâu bao nhiêu tầng, bao nhiêu leaf? Có leaf nào chỉ 1–2 mẫu?
  4. Train vs test chênh bao nhiêu → overfit?
  5. Viết 2–3 luật IF-THEN đầy đủ
- [ ] Viết mục **d** Baseline Model
- [ ] Dọn code, viết `README.md`

**Mẫu viết một luật:**
> *"IF `Tuition fees up to date` = 0 AND `Curricular units 2nd sem (approved)` ≤ 2 THEN Dropout (n=187, độ thuần khiết 91%). Luật khớp với quan sát EDA của bài báo gốc: sinh viên vừa khó khăn tài chính vừa không qua môn nào là nhóm nguy cơ cao nhất."*

## E4. C — Pruning

- [ ] Đọc kỹ trang sklearn về cost-complexity pruning **trước khi code**
- [ ] Chạy `cost_complexity_pruning_path`, vẽ đường cong alpha
- [ ] Chọn alpha bằng **CV trên train**, không phải test
- [ ] Grid nhỏ cho `max_depth`, `min_samples_leaf`
- [ ] Xuất deliverable mục C1
- [ ] Viết mục **f.1** Improvement Method 1
- [ ] Kiểm tra code cả nhóm chạy được trên máy sạch

## E5. D — Class Imbalance

- [ ] Đọc paper SMOTE (Chawla et al., 2002)
- [ ] Train M2a với `class_weight='balanced'`
- [ ] Train M2b với SMOTE **chỉ trên train**
- [ ] Bảng so sánh recall từng lớp M0 vs M2a vs M2b
- [ ] Xuất deliverable mục C2
- [ ] Viết mục **f.2** Improvement Method 2 — **nhớ phân tích đánh đổi accuracy vs recall**

## E6. E — Feature Selection & Media

- [ ] Lọc đúng 12 cột theo mục C3, train M3
- [ ] So sánh feature importance M0 vs M3
- [ ] Xuất deliverable mục C3
- [ ] Viết mục **f.3** Improvement Method 3
- [ ] Hỗ trợ B viết mục **e**
- [ ] Làm slide 12–15 trang
- [ ] Ghép video (kịch bản: mỗi người nói phần mình, 12–15 phút)
- [ ] Viết mục **i** References

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
├── requirements.txt
├── data/raw/data.csv
├── src/
│   ├── data.py                ⭐ A — load, preprocess, split
│   ├── evaluate.py            B — 8 metrics + confusion matrix
│   └── visualize.py           B — vẽ cây, export rules
├── notebooks/
│   ├── 01_eda.ipynb                A
│   ├── 02_baseline.ipynb           B
│   ├── 03_improve_pruning.ipynb    C
│   ├── 04_improve_imbalance.ipynb  D
│   ├── 05_improve_features.ipynb   E
│   └── 06_comparison.ipynb         A
├── figures/
├── outputs/
│   ├── results.csv            ⭐ file kết quả chung
│   └── rules_M0.txt
└── docs/feature_types.md      A
```

**requirements.txt:**
```
pandas==2.3.3
numpy==2.3.4
scipy==1.17.1
scikit-learn==1.9.0
matplotlib==3.11.1
seaborn==0.13.2
imbalanced-learn==0.14.2
ucimlrepo==0.0.7
```

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
| **c.** Dataset Description | Nguồn, số mẫu/feature/target, tiền xử lý, **vì sao phù hợp** | Phần A1–A8, Phần B1–B3 | Số liệu **đếm thực tế** từ code (xem cảnh báo A2) |
| **d.** Baseline Model | Mô tả, quy trình train/test, **hình cây**, accuracy + error rate | Phần B3, Phần C0, Phần D, Phần G | Số liệu thực chạy ra |
| **e.** Analysis of the Tree | Trình bày cây, cấu trúc, điểm mạnh/yếu | Phần C0 + 5 câu hỏi bắt buộc ở mục E3 | Phân tích cụ thể trên cây thật, không viết chung chung |
| **f.** Improvement Methods (2–3) | Mô tả, **modified tree/setting**, accuracy + error rate, giải thích vì sao | Phần C1/C2/C3 — cả 3 đều đã có yêu cầu hình cây | Số liệu thực chạy ra |
| **g.** Comparison of Results | So sánh, bảng/hình, chỉ ra tốt nhất | `results.csv` (Phần D, 16 cột) → A tổng hợp | Chờ cả 4 model chạy xong |
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
| [Tên E] | | Nghiên cứu và triển khai cải tiến feature selection cho dự báo sớm, làm slide, dựng video, tổng hợp References | 20% |

> Nếu đóng góp thực tế không đều thì ghi đúng thực tế. Trưởng nhóm đối chiếu bảng này với **ai thực sự nói phần nào trong video** trước khi nộp (checklist E7).

## J2. Sản phẩm phụ — tùy chọn, không bắt buộc

Đề cho phép nộp thêm `[GroupID - Materials].txt` (mục 1 của đề). Nếu nhóm có tài liệu phụ (link Colab, ghi chú mở rộng, log thử nghiệm) thì đính kèm — không ảnh hưởng điểm nếu bỏ qua.
