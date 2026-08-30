# Bản nháp báo cáo — Mục b (Introduction) & c (Dataset Description)

> Viết bởi Role A, dựa trên: đề gốc `docs/00-DE-BAI-GOC.pdf`, số liệu thực tế chạy từ
> `notebooks/01_eda.ipynb` (không copy từ metadata UCI), và tài liệu tham khảo đã liệt kê
> ở `docs/02-DATASET-VA-CONG-VIEC.md` Phần H.
> Đây là **bản nháp** — copy vào Google Doc chung của nhóm, chỉnh sửa văn phong nếu cần.
> Chưa điền: tên nhóm, MSSV, GroupID (mục a — Trưởng nhóm phụ trách).

---

## b. Introduction

### Giới thiệu ngắn gọn về Decision Tree

Decision tree (cây quyết định) là một mô hình học có giám sát dùng cho cả bài toán phân
loại (classification) lẫn hồi quy (regression). Mô hình biểu diễn quá trình ra quyết định
dưới dạng một cây nhị phân (hoặc đa nhánh): mỗi **node trong** (internal node) là một phép
kiểm tra trên một feature (ví dụ: "Tuition fees up to date ≤ 0.5?"), mỗi **nhánh** ứng với
một kết quả của phép kiểm tra đó, và mỗi **node lá** (leaf) gán một nhãn lớp dự đoán.

Quá trình xây cây (training) đi theo chiến lược **chia để trị, tham lam, từ trên xuống**
(top-down, greedy, recursive partitioning): tại mỗi node, thuật toán thử mọi feature và mọi
ngưỡng chia có thể, chọn phép chia làm giảm "độ hỗn tạp" (impurity) của tập dữ liệu nhiều
nhất, rồi lặp lại đệ quy trên từng tập con. Hai độ đo impurity phổ biến nhất:

- **Entropy / Information Gain** — dùng trong thuật toán ID3 (Quinlan, 1986), đo lượng
  thông tin thu được sau mỗi lần chia.
- **Gini impurity** — dùng trong thuật toán CART (Breiman et al., 1984), đo xác suất phân
  loại sai nếu gán nhãn ngẫu nhiên theo phân bố lớp tại node đó.

Thư viện scikit-learn mà nhóm sử dụng cài đặt một phiên bản tối ưu hoá của CART
(Pedregosa et al., 2011), mặc định dùng Gini nhưng cho phép đổi sang Entropy qua tham số
`criterion`.

**Điểm mạnh lớn nhất** của decision tree so với các mô hình "hộp đen" (neural network,
ensemble phức tạp) là **khả năng diễn giải**: mỗi đường đi từ root đến leaf có thể đọc trực
tiếp thành một luật dạng `IF (điều kiện 1) AND (điều kiện 2) ... THEN (nhãn)`, không cần kỹ
thuật giải thích riêng (như SHAP, LIME) như các mô hình phức tạp hơn. Cây cũng xử lý tự
nhiên cả feature dạng số lẫn dạng phân loại, và không yêu cầu chuẩn hoá dữ liệu — hai điểm
này khai thác trực tiếp trong Phần c bên dưới.

**Điểm yếu chính** là xu hướng **overfitting**: nếu để cây phát triển không giới hạn, nó sẽ
tiếp tục chia cho tới khi mỗi leaf gần như thuần một mẫu, "học thuộc" luôn cả nhiễu của tập
train, dẫn tới độ chính xác rất cao trên train nhưng giảm mạnh trên test (Mitchell, 1997;
Breiman et al., 1984). Đây chính là hiện tượng nhóm quan sát được ở model baseline (mục d)
và là động lực cho cải tiến pruning (mục f.1).

### Mục tiêu đồ án

Đồ án áp dụng lý thuyết trên vào một bài toán thực tế có ý nghĩa xã hội: **dự đoán sinh
viên bỏ học, còn đang học kéo dài, hay tốt nghiệp đúng hạn**, dựa trên dữ liệu thật của
4.424 sinh viên đại học tại Bồ Đào Nha. Cụ thể, nhóm thực hiện:

1. Xây dựng và đánh giá một mô hình decision tree baseline không giới hạn, đo hiệu năng
   bằng đầy đủ các chỉ số phù hợp với bài toán phân loại 3 lớp (Accuracy, Precision, Recall,
   F1-score, ROC-AUC, Confusion Matrix).
2. Phân tích cấu trúc cây baseline: root split là gì và vì sao thuật toán chọn nó, cây có
   dấu hiệu overfitting hay không, trích xuất một số luật quyết định cụ thể.
3. Đề xuất và thử nghiệm 3 hướng cải tiến, mỗi hướng nhắm vào một điểm yếu khác nhau của
   baseline:
   - **Pruning** (cost-complexity pruning) — giải quyết overfitting, đánh đổi giữa độ phức
     tạp của cây và khả năng tổng quát hoá.
   - **Xử lý mất cân bằng lớp** (`class_weight='balanced'`, SMOTE) — giải quyết việc mô hình
     mặc định thiên vị lớp đa số (Graduate), bỏ sót lớp thiểu số quan trọng về mặt ứng dụng
     (Enrolled, Dropout).
   - **Feature selection cho dự báo sớm** — giải quyết một giới hạn thực tế: các feature
     mạnh nhất của baseline chỉ có được *sau khi* học kỳ kết thúc, nên mô hình chính xác
     nhất chưa chắc là mô hình dùng được để can thiệp sớm.
4. So sánh định lượng cả 4 mô hình và rút ra kết luận không chỉ về con số, mà về **việc mô
   hình nào phù hợp với mục tiêu ứng dụng nào** — đúng tinh thần đề bài nhấn mạnh: không chỉ
   chạy mô hình có sẵn, mà phải giải thích được cây được xây dựng ra sao, hành xử thế nào
   trên dữ liệu, và vì sao mỗi cải tiến giúp ích (hoặc không).

---

## c. Dataset Description

### Nguồn dữ liệu

Nhóm sử dụng bộ dữ liệu **"Predict Students' Dropout and Academic Success"** từ UCI Machine
Learning Repository (ID = 697), công bố bởi Realinho, Vieira Martins, Machado và Baptista
(2021), DOI `10.24432/C5MC89`, giấy phép **CC BY 4.0**. Dữ liệu mô tả chi tiết trong bài báo
đi kèm của Realinho et al. (2022), đăng trên tạp chí *Data*, 7(11):146.

Dữ liệu được thu thập tại **Instituto Politécnico de Portalegre**, Bồ Đào Nha, trải trên
**17 ngành đại học** khác nhau (Nông nghiệp, Thiết kế truyền thông, Điều dưỡng, Báo chí và
Truyền thông, Quản trị, Công tác xã hội, Công nghệ nhiên liệu sinh học, Kỹ thuật CNTT, v.v.),
niên khoá **2008/09 đến 2018/19**. Dữ liệu tổng hợp thông tin từ nhiều nguồn hành chính khác
nhau tại thời điểm nhập học (hồ sơ tuyển sinh, dữ liệu kinh tế xã hội) và kết quả học tập
cuối mỗi học kỳ đầu tiên, nên phản ánh khá đầy đủ hành trình học tập ban đầu của sinh viên.

### Mô tả dữ liệu — số liệu xác nhận thực tế

Nhóm không lấy số liệu trực tiếp từ trang mô tả UCI mà **tự chạy code kiểm tra** trên file
`data/raw/data.csv` để xác nhận:

- `df.shape` = **(4424, 37)** → 4.424 mẫu (sinh viên), 36 feature + 1 cột nhãn `Target`.
- `df.isnull().sum().sum()` = **0** — không có giá trị thiếu (tác giả đã tiền xử lý sẵn).
- **Phát hiện đáng chú ý:** trang UCI ghi nhận 36 feature, nhưng Bảng 1 trong bài báo gốc
  (Realinho et al., 2022) chỉ liệt kê 34. Đối chiếu trực tiếp `df.columns.tolist()` với bảng
  đó, nhóm xác định chênh lệch nằm ở 2 cột `Previous qualification (grade)` và
  `Admission grade` — có trong file CSV phát hành nhưng không xuất hiện trong bảng của bài
  báo. Đây là bằng chứng nhóm đọc dữ liệu thật thay vì chép lại metadata.

36 feature chia thành 6 nhóm theo bản chất: nhân khẩu học (6 cột, VD Gender, Age at
enrollment), kinh tế xã hội (8 cột, VD Tuition fees up to date, Scholarship holder), kinh
tế vĩ mô (3 cột: Unemployment rate, Inflation rate, GDP), học vấn lúc nhập học (7 cột, VD
Course, Admission grade), kết quả học kỳ 1 (6 cột) và kết quả học kỳ 2 (6 cột) — hai nhóm
sau ghi nhận số môn đăng ký/qua môn/điểm trung bình mỗi học kỳ.

**Biến mục tiêu (Target)** có 3 lớp, phân bố mất cân bằng vừa phải:

| Lớp | Số mẫu | Tỉ lệ | Ý nghĩa |
|---|---|---|---|
| Graduate | 2.209 | 49,9% | Tốt nghiệp đúng thời hạn chuẩn (3 năm, riêng Điều dưỡng 4 năm) |
| Dropout | 1.421 | 32,1% | Bỏ học |
| Enrolled | 794 | 17,9% | Vẫn đang học khi hết thời hạn chuẩn |

Lớp **Enrolled** là lớp thiểu số và khó phân loại nhất vì nằm "ở giữa" hai lớp còn lại về
đặc trưng — đây là lý do tồn tại của cải tiến xử lý mất cân bằng lớp (mục f.2).

![Phân bố 3 lớp Target trên 4.424 sinh viên](../figures/A_target_distribution.png)

*Hình c.1. Phân bố lớp Target: Graduate 49,9%, Dropout 32,1%, Enrolled 17,9%. Enrolled là
lớp thiểu số rõ rệt, tạo tình huống mất cân bằng lớp thật để thử nghiệm ở mục f.2.*

Một số quan sát thống kê mô tả từ EDA (`notebooks/01_eda.ipynb`) minh hoạ rõ mức độ liên
quan của một số feature tới Target: trong nhóm sinh viên **chưa đóng học phí đúng hạn**, tới
86% thuộc lớp Dropout, trong khi nhóm đã đóng đúng hạn chỉ có 25% Dropout và tới 56%
Graduate. Tương tự, sinh viên **có học bổng** chỉ 12% Dropout so với 39% ở nhóm không có học
bổng.

![Tỉ lệ Target theo Tuition fees up to date và Scholarship holder](../figures/A_tuition_scholarship_vs_target.png)

*Hình c.2. Trái: sinh viên chưa đóng học phí đúng hạn có tỉ lệ Dropout áp đảo (86%).
`Tuition fees up to date` nằm trong 5 feature quan trọng nhất theo permutation importance
của bài báo gốc (Phần A5), và cũng là hạng 3 theo Gini importance thực tế của M0 (0,045) —
khác biệt tỉ lệ Dropout rất lớn giữa hai nhóm khớp với việc feature này quan trọng ở cả hai
cách đo. Phải: sinh viên có học bổng có tỉ lệ Dropout thấp hơn ba lần so với nhóm không có
học bổng (12% vs 39%) — tương quan quan sát được rõ, nhưng `Scholarship holder` **không**
nằm trong top-5 của bài báo gốc lẫn của M0 (hạng 24, importance chỉ 0,0097): tỉ lệ chênh lệch
lớn trong biểu đồ phần trăm không đồng nghĩa cây coi đây là feature phân tách quan trọng khi
đặt cạnh các feature khác — có thể vì thông tin của nó phần lớn trùng lặp với các feature
mạnh hơn như `Tuition fees up to date`.*

Xét theo ngành học, hai ngành có tỉ lệ tốt nghiệp thấp nhất là Công nghệ nhiên liệu sinh học
(mã 33) và Kỹ thuật CNTT (mã 9119) — phần lớn sinh viên bỏ học, trong khi Điều dưỡng (mã
9500) và Công tác xã hội (mã 9238) có tỉ lệ tốt nghiệp cao nhất — khớp với quan sát đã công
bố trong bài báo gốc.

![Tỉ lệ Target theo mã ngành (Course), sắp xếp theo %Graduate](../figures/A_target_by_course.png)

*Hình c.3. 17 ngành sắp xếp theo tỉ lệ tốt nghiệp tăng dần. Hai ngành thấp nhất — mã 9119
(54,1% Dropout) và mã 33 (66,7% Dropout) — chỉ có **8,2% và 8,3%** sinh viên Graduate, thấp
hơn nhiều so với trung bình 49,9% của toàn dataset. Hai ngành cao nhất — mã 9238 (69,9%
Graduate) và mã 9500 (71,5% Graduate) — có Dropout thấp nhất, lần lượt 18,3% và 15,4%.
`Course` được bài báo gốc xếp trong 5 feature quan trọng nhất theo permutation importance
(Phần A5); theo Gini importance thực tế của cây M0 nhóm tự train, `Course` xếp hạng **6**
(importance 0,044, xem `outputs/E_feature_importance_comparison.csv`) — vẫn rất gần top-5,
và quan trọng hơn cả: có sẵn ngay lúc nhập học, nên là nền tảng cho model dự báo sớm M3 (mục
f.3), bất kể xếp hạng chính xác là 4 hay 6 tùy thuật toán đo importance.*

![Số môn qua học kỳ 2 theo từng lớp Target](../figures/A_curricular_units_2nd_sem_by_target.png)

*Hình c.4. Boxplot `Curricular units 2nd sem (approved)` theo Target: median Dropout = 0,
Enrolled = 4, Graduate = 6. Đây là feature quan trọng nhất theo permutation importance của
bài báo gốc (Phần A5), nhưng chỉ có giá trị sau khi học kỳ 2 kết thúc — không dùng được cho
model dự báo sớm M3.*

### Tiền xử lý dữ liệu đã thực hiện

Toàn bộ logic tiền xử lý nằm trong `src/data.py` (`load_and_preprocess()` và
`get_train_test()`), được cả nhóm dùng chung để đảm bảo mọi model đánh giá trên cùng một
tập train/test.

1. **Không cần xử lý giá trị thiếu** — dataset đã sạch từ nguồn (0 giá trị thiếu).

2. **Mã hoá lại các cột categorical lưu dưới dạng số.** Nhiều cột trong dataset gốc là mã
   số đại diện cho phạm trù không có thứ tự (VD `Course` mã 33 = Công nghệ nhiên liệu sinh
   học, mã 9500 = Điều dưỡng — các mã này không mang quan hệ lớn/nhỏ). Nếu giữ nguyên,
   scikit-learn sẽ coi chúng là biến số liên tục và tạo ra các phép chia vô nghĩa kiểu
   `Course ≤ 8.5`. Nhóm xử lý theo hướng kết hợp:
   - **One-hot encode** 4 cột có ít giá trị: `Marital Status` (6), `Application mode` (18),
     `Course` (17), `Previous qualification` (17) — giúp mỗi phép chia đọc được thành câu
     hỏi có/không rõ ràng (VD "có phải ngành Điều dưỡng hay không?").
   - **Giữ nguyên mã số** cho các cột có quá nhiều giá trị: `Mother's/Father's occupation`
     (32/46 giá trị), `Mother's/Father's qualification` (29/34), `Nationality` (21) — vì
     one-hot các cột này sẽ tạo ra hàng chục cột thưa (sparse), làm cây kém ổn định và khó
     diễn giải hơn là có lợi. Đây là một đánh đổi được ghi nhận rõ trong giới hạn của báo
     cáo (Limitations).
   - Sau bước này, số cột feature tăng từ 36 lên **90** (do one-hot).

3. **Không chuẩn hoá (scale) dữ liệu.** Decision tree chọn điểm chia dựa trên ngưỡng của
   từng feature riêng lẻ, không dựa trên khoảng cách giữa các điểm dữ liệu như KNN hay hồi
   quy tuyến tính, nên hoàn toàn bất biến với các phép biến đổi đơn điệu (như chuẩn hoá) áp
   dụng riêng từng cột. Việc thêm `StandardScaler`/`MinMaxScaler` ở đây là dư thừa, không
   ảnh hưởng tới cấu trúc cây học được.

4. **Chia tập train/test bằng stratified split**: 80% train / 20% test, `stratify=y` để
   giữ đúng tỉ lệ 3 lớp (≈50/32/18) ở cả hai tập — bắt buộc vì dữ liệu mất cân bằng, tránh
   trường hợp tập test ngẫu nhiên thiếu hẳn một lớp thiểu số. `random_state=42` cố định để
   toàn bộ 5 model của nhóm đánh giá trên cùng một lần chia, đảm bảo so sánh công bằng.

Sau tiền xử lý: **3.539 mẫu train / 885 mẫu test**, mỗi mẫu có 90 feature numeric, sẵn sàng
đưa thẳng vào `sklearn.tree.DecisionTreeClassifier`.

### Đa cộng tuyến giữa các feature

![Ma trận tương quan Pearson giữa các feature numeric](../figures/A_correlation_heatmap.png)

*Hình c.5. Heatmap tương quan Pearson, **tự tính lại trực tiếp trên `data/raw/data.csv`**
(không copy số từ tài liệu kế hoạch). Ba cặp tương quan cao nhất toàn dataset: `1st sem
credited` ↔ `2nd sem credited` (r=0,945), `1st sem enrolled` ↔ `2nd sem enrolled` (r=0,943),
và **`Mother's occupation` ↔ `Father's occupation` (r=0,911)** — cặp này cao hơn cả nhóm
feature học kỳ 1 quan hệ với học kỳ 2 (`1st/2nd sem approved`, r=0,904). Cặp `Nacionality` ↔
`International` có r=0,791 — vẫn là tương quan cao (sinh viên quốc tế gần như luôn có
`Nacionality` khác Bồ Đào Nha) nhưng thấp hơn 3 cặp trên.*

> ⚠️ Bảng đa cộng tuyến ở `docs/02-DATASET-VA-CONG-VIEC.md` Phần A6 có 2 số liệu không khớp
> khi đối chiếu lại với `data/raw/data.csv` thật: cặp `Nacionality`↔`International` bảng đó
> ghi r=0,912 (thực tế r=0,791), và cặp `Mother's/Father's occupation` bảng đó ghi r=0,724
> (thực tế r=0,911 — **cao hơn nhiều** so với số đã ghi, đây là cặp tương quan cao thứ 3 toàn
> dataset chứ không phải hạng 9 như bảng cũ xếp). Số liệu trong báo cáo dùng giá trị tự tính
> lại ở trên; nên cập nhật lại bảng A6 để tránh lệch khi role E dùng bảng đó làm căn cứ chọn
> cột trong mục f.3.

Decision tree không bị ảnh hưởng nặng bởi đa cộng tuyến như hồi quy tuyến tính (không cần
loại bỏ feature trùng lặp để mô hình hội tụ), nhưng đa cộng tuyến vẫn làm feature importance
bị chia sẻ giữa các cột tương quan cao và có thể khiến cấu trúc cây kém ổn định giữa các lần
chạy khác nhau của cùng thuật toán. Đây là căn cứ định lượng cho việc E cân nhắc loại bớt cột
trùng lặp (VD `International`, hoặc một trong hai cột nghề nghiệp cha/mẹ) khi mở rộng thí
nghiệm feature selection ở mục f.3.

### Vì sao dataset này phù hợp cho decision tree modeling

1. **Feature có ngữ nghĩa rõ ràng, gần gũi đời thực** (học phí, học bổng, kết quả học kỳ,
   ngành học...) nên mọi phép chia của cây đều diễn giải được thành câu bình thường — khai
   thác đúng thế mạnh diễn giải của decision tree, khác với dữ liệu ảnh/văn bản nơi cây
   quyết định ít phát huy được lợi thế này.
2. **Trộn cả feature categorical và numerical** — cây xử lý tự nhiên cả hai loại mà không
   cần chuẩn hoá, khác các mô hình như KNN hay hồi quy tuyến tính buộc phải scale.
3. **Có mất cân bằng lớp thật** (50%/32%/18%) — tạo tình huống thực tế để áp dụng và so
   sánh kỹ thuật xử lý imbalance, đúng một hướng cải tiến đề bài gợi ý (mục 3.2.d — Handling
   class imbalance).
4. **Feature chia rõ theo thời điểm thu thập** (thông tin lúc nhập học vs. kết quả cuối học
   kỳ) — cho phép thí nghiệm feature selection có ý nghĩa ứng dụng thực (dự báo sớm), không
   chỉ chọn feature theo thống kê thuần tuý.
5. **Không có missing value** — nhóm dồn được thời gian cho phân tích và diễn giải thay vì
   làm sạch dữ liệu, đúng tinh thần đề nhấn mạnh: không chỉ chạy mô hình có sẵn mà còn phải
   giải thích rõ cây được xây dựng thế nào và vì sao các cải tiến giúp ích.

### Lưu ý đạo đức

Dataset chứa các biến nhạy cảm: giới tính, quốc tịch, tình trạng hôn nhân, trình độ học vấn
và nghề nghiệp của cha mẹ. Các phép chia của cây trên những biến này chỉ phản ánh **tương
quan quan sát được trong mẫu khảo sát tại một trường đại học Bồ Đào Nha giai đoạn
2008–2019**, không phải quan hệ nhân quả, và không nên được dùng làm cơ sở cho bất kỳ chính
sách phân biệt đối xử nào với sinh viên trong thực tế.

---

## Tài liệu tham khảo dùng trong 2 mục trên

1. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students'
   Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository.
   https://doi.org/10.24432/C5MC89
2. Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student
   Dropout and Academic Success. *Data*, 7(11), 146. https://doi.org/10.3390/data7110146
3. Quinlan, J. R. (1986). Induction of Decision Trees. *Machine Learning*, 1(1), 81–106.
4. Breiman, L., Friedman, J. H., Olshen, R. A., & Stone, C. J. (1984). *Classification and
   Regression Trees*. Wadsworth.
5. Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill, Chương 3.
6. Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12,
   2825–2830.
