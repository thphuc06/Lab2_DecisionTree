# d. Baseline Model

## Cấu hình và quy trình thí nghiệm

Mô hình M0 được huấn luyện bằng `DecisionTreeClassifier(random_state=42)` với criterion mặc định `gini`. Đây là cây baseline không giới hạn: `max_depth=None`, `min_samples_split=2`, `min_samples_leaf=1`, `ccp_alpha=0.0`, không pruning và không đặt class weight. Dữ liệu không được chuẩn hóa vì split của cây chỉ phụ thuộc vào thứ tự và ngưỡng của từng feature.

Notebook chỉ gọi một lần `src.data.get_train_test()`. Pipeline chung one-hot bốn nhóm category (`Marital Status`, `Application mode`, `Course`, `Previous qualification`), giữ các category nhiều giá trị ở dạng mã số để tránh ma trận quá thưa, rồi stratified split 80/20 với `random_state=42`. Tập train có 3.539 mẫu, tập test có 885 mẫu và cả hai có 90 feature sau one-hot. Phân bố lớp được giữ gần như không đổi: train gồm 1.137 Dropout, 635 Enrolled, 1.767 Graduate; test gồm 284 Dropout, 159 Enrolled, 442 Graduate. Không có bước split lại hoặc scale trong notebook.

## Kết quả định lượng

| Metric | M0 |
|---|---:|
| Train accuracy | 1.000000 |
| Test accuracy | 0.668927 |
| Error rate | 0.331073 |
| Precision macro | 0.607642 |
| Recall macro | 0.609310 |
| F1 macro | 0.608271 |
| ROC-AUC macro (OvR) | 0.719456 |
| Recall Dropout | 0.679577 |
| Recall Enrolled | 0.383648 |
| Recall Graduate | 0.764706 |
| Tree depth | 27 |
| Leaves | 634 |

ROC-AUC được tính từ `predict_proba(X_test)` theo đúng thứ tự `model.classes_ = [Dropout, Enrolled, Graduate]`, với `multi_class="ovr"` và `average="macro"`. Giá trị 0,7195 cho thấy khả năng xếp hạng one-vs-rest ở mức vừa phải, tốt hơn ngẫu nhiên nhưng còn xa mức mạnh. Các metric macro quanh 0,61 thấp hơn accuracy vì mỗi lớp được tính trọng số ngang nhau, làm lộ rõ hiệu năng yếu trên lớp Enrolled thiểu số.

Classification report theo từng lớp:

| Lớp | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Dropout | 0.6820 | 0.6796 | 0.6808 | 284 |
| Enrolled | 0.3567 | 0.3836 | 0.3697 | 159 |
| Graduate | 0.7842 | 0.7647 | 0.7743 | 442 |

Confusion matrix, theo thứ tự nhãn `[Dropout, Enrolled, Graduate]`, là:

| True \ Predicted | Dropout | Enrolled | Graduate |
|---|---:|---:|---:|
| Dropout | 193 | 51 | 40 |
| Enrolled | 45 | 61 | 53 |
| Graduate | 45 | 59 | 338 |

M0 nhận đúng 338/442 Graduate và 193/284 Dropout, nhưng chỉ nhận đúng 61/159 Enrolled. Enrolled bị phân tán gần như đều sang Dropout (45 mẫu) và Graduate (53 mẫu), phù hợp với việc đây là trạng thái trung gian khó phân biệt. Hình confusion matrix được lưu tại `figures/B_cm_M0.png`; classification report đầy đủ nằm tại `outputs/classification_report_M0.txt`.

Hai hình cây phục vụ hai mục đích khác nhau. `figures/B_tree_M0_full.png` trình bày toàn bộ 1.267 node để cho thấy cấu trúc rất lớn và rối. `figures/B_tree_M0_top3.png` chỉ giới hạn phần hiển thị ở `max_depth=3`, nên đọc được impurity, số mẫu, phân bố lớp và lớp dự đoán ở các node đầu; giới hạn hiển thị này không thay đổi mô hình đã fit. Toàn bộ luật dạng chữ nằm tại `outputs/rules_M0.txt`.

## Kiểm tra phụ Gini và Entropy

| Criterion | Train accuracy | Test accuracy | Error rate | Depth | Leaves |
|---|---:|---:|---:|---:|---:|
| Gini - M0 chính thức | 1.000000 | 0.668927 | 0.331073 | 27 | 634 |
| Entropy - kiểm tra phụ | 1.000000 | 0.653107 | 0.346893 | 27 | 584 |

Entropy giảm test accuracy 0,015819 (khoảng 1,58 điểm phần trăm) so với Gini. Dù có ít hơn 50 leaf, cây Entropy vẫn sâu 27 và fit train hoàn hảo, nên thay criterion đơn thuần không giải quyết overfitting. Vì vậy nhóm giữ Gini mặc định làm M0; Entropy không được ghi vào `results.csv` và không được xem là một trong ba cải tiến chính thức.

# e. Analysis of the Tree

## 1. Root split

Root dùng feature `Curricular units 2nd sem (approved)` với threshold 4,5. Trước split, root chứa 3.539 mẫu với phân bố `[Dropout=1.137, Enrolled=635, Graduate=1.767]` và Gini 0,615292.

- Nhánh trái (`<= 4,5`) có 1.500 mẫu, phân bố `[936, 357, 207]`, Gini 0,534936 và dự đoán Dropout.
- Nhánh phải (`> 4,5`) có 2.039 mẫu, phân bố `[201, 278, 1.560]`, Gini 0,386345 và dự đoán Graduate.

Gini sau split có trọng số là:

`(1500/3539) * 0.534936 + (2039/3539) * 0.386345 = 0.449325`.

Mức giảm impurity thực tế là `0.615292 - 0.449325 = 0.165967`. CART duyệt các feature/threshold ứng viên tại node và chọn split làm giảm impurity có trọng số nhiều nhất; vì vậy lý do trực tiếp không phải chỉ là feature này “quan trọng”, mà là ngưỡng 4,5 tạo ra hai nhóm có phân bố lớp khác biệt rõ nhất trong số các split đang xét. Về bối cảnh, số học phần HK2 đã đạt là tín hiệu trực tiếp về tiến độ học tập: phía ít học phần đạt tập trung Dropout, còn phía vượt ngưỡng tập trung Graduate. Đây là tương quan quan sát, không phải quan hệ nhân quả.

## 2. Root và ba tầng tiếp theo

| Depth/node | Điều kiện đến node | Split tại node | n; phân bố `[D,E,G]` | Dự đoán | Diễn giải |
|---|---|---|---|---|---|
| 0 / 0 | Root | `Curricular units 2nd sem (approved) <= 4.5` | 3539; `[1137,635,1767]` | Graduate | Tách tiến độ HK2 thấp/cao. |
| 1 / 1 | HK2 approved `<= 4.5` | HK2 approved `<= 1.5` | 1500; `[936,357,207]` | Dropout | Trong nhóm tiến độ thấp, mức gần như không qua học phần nào tạo nhóm rủi ro hơn. |
| 1 / 552 | HK2 approved `> 4.5` | `Tuition fees up to date <= 0.5` | 2039; `[201,278,1560]` | Graduate | Sau khi có tiến độ tốt, trạng thái học phí tiếp tục tách một nhóm nhỏ có kết quả kém hơn. |
| 2 / 2 | HK2 approved `<= 1.5` | `Curricular units 2nd sem (enrolled) <= 0.5` | 792; `[654,74,64]` | Dropout | Số học phần đăng ký giúp phân biệt trường hợp không có hoạt động HK2 với nhóm có đăng ký nhưng gần như không đạt. |
| 2 / 213 | `1.5 <` HK2 approved `<= 4.5` | `Tuition fees up to date <= 0.5` | 708; `[282,283,143]` | Enrolled | Vùng tiến độ trung gian có Dropout và Enrolled gần cân bằng; học phí là split kế tiếp. |
| 2 / 553 | HK2 approved `> 4.5`, học phí chưa cập nhật | `GDP <= 1.905` | 84; `[49,17,18]` | Dropout | Đây là node nhỏ; GDP phản ánh năm nhập học chứ không phải thuộc tính cá nhân và không nên suy diễn nhân quả. |
| 2 / 588 | HK2 approved `> 4.5`, học phí cập nhật | `Curricular units 1st sem (evaluations) <= 8.5` | 1955; `[152,261,1542]` | Graduate | Đây là vùng Graduate áp đảo; số lượt đánh giá HK1 tiếp tục tinh chỉnh dự đoán. |
| 3 / 98 | HK2 approved `<= 1.5`, HK2 enrolled `> 0.5` | `Mother's occupation <= 116.5` | 644; `[591,53,0]` | Dropout | Nhánh rất đậm Dropout; split nghề nghiệp mẹ là biến nhạy cảm và chỉ có giá trị mô tả tương quan. |
| 3 / 214 | Tiến độ trung gian, học phí chưa cập nhật | `GDP <= 1.765` | 111; `[98,12,1]` | Dropout | Chưa cập nhật học phí trong vùng tiến độ trung gian gắn với tỷ trọng Dropout cao. |
| 3 / 235 | Tiến độ trung gian, học phí cập nhật | HK2 approved `<= 3.5` | 597; `[184,271,142]` | Enrolled | Khi học phí cập nhật, trạng thái Enrolled trở thành lớp lớn nhất nhưng node vẫn pha trộn mạnh. |
| 3 / 589 | Tiến độ cao, học phí cập nhật, HK1 evaluations `<= 8.5` | HK2 approved `<= 5.5` | 1285; `[77,100,1108]` | Graduate | Graduate chiếm ưu thế rõ; cây tiếp tục chia rất chi tiết theo mức đạt HK2. |
| 3 / 996 | Tiến độ cao, học phí cập nhật, HK1 evaluations `> 8.5` | HK1 approved `<= 5.5` | 670; `[75,161,434]` | Graduate | Nhiều lượt đánh giá nhưng số học phần đạt HK1 giúp tách Graduate khỏi Enrolled. |

Tên feature được giữ nguyên theo dữ liệu thật; đặc biệt dataset dùng `Nacionality`, không phải `Nationality`. Ở các feature one-hot, điều kiện `<= 0.5` nghĩa là không thuộc category mang mã ở hậu tố, còn `> 0.5` nghĩa là thuộc category đó.

## 3. Độ phức tạp

| Chỉ báo | Giá trị |
|---|---:|
| Độ sâu tối đa | 27 |
| Tổng node | 1.267 |
| Tổng leaf | 634 |
| Leaf đúng 1 mẫu | 279 (44,01%) |
| Leaf không quá 2 mẫu | 399 (62,93%) |
| Leaf thuần | 634/634 (100%) |
| Độ sâu trung bình của leaf | 13,323 |

Không giới hạn độ sâu cho phép cây tách đến khi mọi leaf train đều thuần. Việc 44% leaf chỉ nhớ đúng một mẫu và gần 63% leaf chứa tối đa hai mẫu là bằng chứng mạnh rằng cây đã học các ngoại lệ rất chi tiết thay vì chỉ giữ quy luật ổn định. Hình cây đầy đủ với 1.267 node vì thế có giá trị như minh họa overfitting, còn bản top-3 mới phù hợp để diễn giải.

## 4. Overfitting

Train accuracy đạt 1,000000 nhưng test accuracy chỉ 0,668927; generalization gap là `1.000000 - 0.668927 = 0.331073`, tức 33,11 điểm phần trăm. Test accuracy nằm trong vùng kiểm tra hợp lý 0,65–0,72 và không vượt 0,90, nên không có dấu hiệu leakage từ kết quả này. Tuy nhiên, kết hợp gap lớn với depth 27, 634 leaf thuần và 399 leaf chỉ chứa 1–2 mẫu cho thấy M0 có variance cao và overfit rõ rệt. Điểm mạnh của M0 là các split đầu dễ đọc, xử lý được quan hệ phi tuyến và không cần scale; điểm yếu là cây tổng thể khó trình bày, dự đoán kém ổn định, đặc biệt yếu ở Enrolled, và dùng feature kết quả học kỳ nên không phù hợp cho cảnh báo sớm.

## 5. Các luật IF-THEN tiêu biểu

Các luật dưới đây được chọn có chủ đích: với mỗi lớp, chọn leaf có purity ít nhất 90% và số mẫu train lớn nhất. Toàn bộ điều kiện từ root đến leaf được giữ lại. Chính độ dài của các luật cũng là dấu hiệu cây phân mảnh quá sâu.

### Luật Dropout

IF:

1. `Curricular units 2nd sem (approved) <= 4.500`;
2. `Curricular units 2nd sem (approved) <= 1.500`;
3. `Curricular units 2nd sem (enrolled) > 0.500`;
4. `Mother's occupation <= 116.500`;
5. `Curricular units 2nd sem (grade) <= 13.585`;
6. `Curricular units 2nd sem (evaluations) <= 7.500`;
7. `Marital Status_3 <= 0.500`;
8. `Previous qualification (grade) > 99.500`;
9. `Curricular units 2nd sem (evaluations) <= 4.500`;

THEN dự đoán **Dropout**. Leaf có `n=189`, phân bố `[189,0,0]`, purity 100%. Luật mô tả một nhóm có rất ít học phần HK2 được thông qua và ít lượt đánh giá, phù hợp với tín hiệu tiến độ học tập thấp. Tuy nhiên, điều kiện về nghề nghiệp mẹ và hôn nhân là biến nhạy cảm; chúng không được hiểu là nguyên nhân bỏ học.

### Luật Graduate

IF:

1. `Curricular units 2nd sem (approved) > 4.500`;
2. `Tuition fees up to date > 0.500`;
3. `Curricular units 1st sem (evaluations) <= 8.500`;
4. `Curricular units 2nd sem (approved) > 5.500`;
5. `Curricular units 2nd sem (without evaluations) <= 0.500`;
6. `Course_9119 <= 0.500`;
7. `Curricular units 1st sem (credited) <= 4.500`;
8. `Scholarship holder > 0.500`;
9. `Admission grade > 98.500`;
10. `Course_9773 <= 0.500`;
11. `Curricular units 1st sem (without evaluations) <= 0.500`;
12. `Course_9070 <= 0.500`;
13. `Application mode_43 <= 0.500`;
14. `Curricular units 2nd sem (evaluations) <= 10.500`;
15. `Father's occupation <= 8.500`;
16. `Curricular units 2nd sem (grade) > 12.264`;

THEN dự đoán **Graduate**. Leaf có `n=176`, phân bố `[0,0,176]`, purity 100%. Tín hiệu thực tế dễ hiểu nhất là đã qua trên 5,5 học phần HK2, không có học phần HK2 thiếu đánh giá, học phí cập nhật và điểm HK2 trên 12,264. Các điều kiện mã ngành, học bổng và nghề nghiệp cha chỉ là các tương quan bổ sung trên tập train.

### Luật Enrolled

IF:

1. `Curricular units 2nd sem (approved) <= 4.500`;
2. `Curricular units 2nd sem (approved) > 1.500`;
3. `Tuition fees up to date > 0.500`;
4. `Curricular units 2nd sem (approved) <= 3.500`;
5. `Age at enrollment <= 26.500`;
6. `Curricular units 1st sem (approved) <= 5.500`;
7. `Course_9853 <= 0.500`;
8. `Mother's occupation > 0.500`;
9. `Inflation rate > 1.000`;
10. `Curricular units 1st sem (evaluations) <= 19.000`;
11. `Curricular units 1st sem (grade) > 10.100`;
12. `Admission grade <= 123.050`;
13. `Application order <= 5.500`;
14. `Course_9254 <= 0.500`;
15. `Curricular units 2nd sem (without evaluations) <= 2.500`;
16. `Admission grade > 113.500`;

THEN dự đoán **Enrolled**. Leaf có `n=29`, phân bố `[0,29,0]`, purity 100%. Luật mô tả trạng thái trung gian: đã qua một số nhưng chưa nhiều học phần, điểm HK1 trên 10,1 và học phí cập nhật. Số mẫu nhỏ và chuỗi 16 điều kiện khiến luật kém ổn định hơn hai luật còn lại; nó nên được xem như mô tả một phân khúc train chứ không phải quy tắc can thiệp phổ quát.

## Giới hạn đạo đức

Dataset chứa các feature nhạy cảm như giới tính, `Nacionality`, tình trạng hôn nhân, trình độ/nghề nghiệp cha mẹ và hoàn cảnh tài chính. Split trên các feature này chỉ phản ánh tương quan trong mẫu sinh viên tại một cơ sở giáo dục Bồ Đào Nha trong giai đoạn quan sát. Không được suy diễn quan hệ nhân quả, gán lỗi cho cá nhân hoặc dùng các luật của cây làm căn cứ cho chính sách phân biệt đối xử. Nếu triển khai hỗ trợ sinh viên, mô hình cần audit fairness, giám sát sai số theo nhóm và luôn có con người xem xét.
