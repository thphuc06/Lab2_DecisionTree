# f.2. Improvement Method 2 — Class Imbalance

## Vấn đề của M0 và mục tiêu cải tiến

Target của dataset có phân bố không đều: Graduate là lớp lớn nhất, tiếp theo là Dropout,
còn Enrolled là lớp thiểu số. Trên held-out test gồm 885 sinh viên, M0 nhận đúng 338/442
Graduate và 193/284 Dropout, nhưng chỉ nhận đúng **61/159 Enrolled**. Vì vậy, dù test
accuracy của M0 là **0,668927**, recall Enrolled chỉ **0,383648**. Đây là hạn chế quan
trọng nếu mục tiêu ứng dụng là nhận diện cả những sinh viên chưa tốt nghiệp đúng hạn, thay
vì chỉ tối đa hóa số dự đoán đúng trên lớp đa số.

M2 kiểm tra hai cách thay đổi mức độ chú ý của decision tree tới các lớp ít mẫu. Cả hai
thí nghiệm đều gọi cùng một `get_train_test()` từ `src.data`, dùng 3.539 mẫu train, 885
mẫu held-out test, 90 feature sau one-hot và `random_state=42`. Không có scale hoặc split
riêng trong notebook.

## Hai phương pháp cân bằng lớp

### M2a — `class_weight='balanced'`

M2a dùng:

```python
DecisionTreeClassifier(class_weight='balanced', random_state=42)
```

Scikit-learn tự tăng trọng số của các lớp có ít quan sát khi tính tiêu chí chia node. M2a
vẫn fit trên đúng tập train gốc; không tạo thêm mẫu dữ liệu nào.

### M2b — SMOTE chỉ trên tập train

M2b dùng `SMOTE(random_state=42)` sau khi đã có split chung:

```python
X_train_smote, y_train_smote = SMOTE(random_state=42).fit_resample(
    X_train, y_train
)
DecisionTreeClassifier(random_state=42).fit(X_train_smote, y_train_smote)
```

Trước SMOTE, train có 1.137 Dropout, 635 Enrolled và 1.767 Graduate. Sau resampling,
mỗi lớp có 1.767 mẫu, tức 5.301 mẫu train. **SMOTE không được áp dụng lên toàn bộ dataset
và không được áp dụng lên test set.** Tập test vẫn là 885 quan sát thật, không thay đổi;
vì vậy các metric bên dưới không bị rò rỉ từ dữ liệu tổng hợp.

## Kết quả held-out test

| Chỉ số | M0 baseline | M2a class weight | M2b SMOTE-train | M2a − M0 | M2b − M0 |
|---|---:|---:|---:|---:|---:|
| Test accuracy | 0,668927 | 0,650847 | **0,688136** | −0,018079 | **+0,019209** |
| Error rate | 0,331073 | 0,349153 | **0,311864** | +0,018079 | **−0,019209** |
| Recall Dropout | 0,679577 | 0,679577 | **0,707746** | +0,000000 | **+0,028169** |
| Recall Enrolled | 0,383648 | 0,339623 | **0,465409** | −0,044025 | **+0,081761** |
| Recall Graduate | **0,764706** | 0,744344 | 0,755656 | −0,020362 | −0,009050 |
| Precision macro | 0,607642 | 0,584250 | **0,636513** | −0,023392 | **+0,028871** |
| Recall macro | 0,609310 | 0,587848 | **0,642937** | −0,021462 | **+0,033627** |
| F1 macro | 0,608271 | 0,585409 | **0,638747** | −0,022862 | **+0,030475** |

![Confusion matrix của M2a](../figures/D_cm_M2a.png)

*Hình f.2a. Confusion matrix M2a trên 885 mẫu held-out test.*

![Confusion matrix của M2b](../figures/D_cm_M2b.png)

*Hình f.2b. Confusion matrix M2b trên cùng held-out test.*

![Cây M2a với class weight balanced](../figures/D_tree_M2a.png)

*Hình f.2c. Bốn tầng đầu của cây M2a. Thay đổi trọng số lớp có thể thay đổi Gini và cấu
trúc split, nên đây vẫn là một cấu hình cây quyết định cần được trình bày, không chỉ là một
tham số bổ sung.*

## So sánh M2a và M2b, đặc biệt với lớp Enrolled

M2a không đạt mục tiêu của thí nghiệm trên split này. Test accuracy giảm **1,81 điểm phần
trăm** so với M0; đồng thời recall Dropout không đổi, recall Enrolled giảm **4,40 điểm** và
recall Graduate giảm **2,04 điểm**. Vì cả accuracy lẫn recall của các lớp cần ưu tiên đều
giảm hoặc không đổi, không có bằng chứng từ held-out test rằng `class_weight='balanced'`
một mình cải thiện mô hình M0 trong cấu hình này.

M2b hiệu quả hơn rõ rệt. Recall Enrolled tăng từ **0,383648** lên **0,465409**, tương ứng
nhận đúng khoảng 74/159 thay vì 61/159 sinh viên Enrolled trên test. Đồng thời, recall
Dropout tăng từ **0,679577** lên **0,707746** (khoảng 201/284 thay vì 193/284). Recall
Graduate chỉ giảm nhẹ từ 0,764706 xuống 0,755656. Các macro metric cũng tăng: macro-F1
từ 0,608271 lên 0,638747 và macro recall từ 0,609310 lên 0,642937.

Kết quả này phù hợp với mục đích của SMOTE: lớp Enrolled có ít quan sát gốc nhất trong
train; resampling tạo thêm điểm tổng hợp trong vùng đặc trưng của lớp này để cây có nhiều
cơ hội tìm split phân biệt Enrolled với hai lớp còn lại. Đây là diễn giải về cơ chế của
thí nghiệm, không phải kết luận nhân quả rằng mọi dataset hoặc mọi split đều sẽ có cùng
mức tăng. M2b có cây sâu 39 và 847 lá, nên cải thiện recall không đồng nghĩa cây đơn giản
hơn; mục tiêu của M2 là cân bằng hiệu năng theo lớp, không phải pruning.

## Đánh đổi accuracy và recall

Trong bài toán mất cân bằng lớp, accuracy tổng không thể là tiêu chí duy nhất. Một mô hình
có thể giảm accuracy vì bớt thiên vị Graduate để dự đoán đúng hơn các lớp ít mẫu; khi đó
phải xem recall từng lớp thay vì tiếp tục tối ưu chỉ để đưa accuracy quay về bằng M0.

M2a là ví dụ rằng đánh đổi này không tự động có lợi: accuracy giảm và recall Enrolled cũng
giảm, nên kết quả cần được báo cáo thẳng thay vì chọn lọc chỉ các con số thuận lợi. Ngược
lại, M2b không phải đánh đổi accuracy lấy recall trong held-out split hiện tại: nó tăng
đồng thời test accuracy, recall Dropout và recall Enrolled; chi phí là recall Graduate
giảm nhẹ 0,91 điểm phần trăm. Vì vậy, nếu ưu tiên phát hiện sinh viên Dropout/Enrolled,
M2b là lựa chọn tốt hơn M0 và M2a trong thí nghiệm này.

Các kết quả chỉ được đo trên một held-out split cố định. Trước khi triển khai thực tế, cần
đánh giá thêm trên các split hoặc cohort khác và xem xét fairness đối với các nhóm nhạy
cảm trong dataset. Tuy nhiên, với split chung của dự án, M2b trả lời tích cực câu hỏi của
cải tiến: lớp thiểu số Enrolled và lớp Dropout được nhận diện tốt hơn khi SMOTE chỉ được
thực hiện trên tập train.

## Kết luận Improvement Method 2

`class_weight='balanced'` (M2a) không cải thiện M0 trên held-out test này. SMOTE trên tập
train (M2b) tăng recall Enrolled **8,18 điểm phần trăm**, recall Dropout **2,82 điểm phần
trăm**, và đồng thời giảm error rate từ 0,331073 xuống 0,311864. Do đó nhóm chọn M2b là
cấu hình cân bằng lớp thành công hơn; phần báo cáo vẫn giữ M2a để minh bạch rằng không phải
mọi kỹ thuật cân bằng lớp đều tạo ra cải thiện với cùng dữ liệu và cùng mô hình.
