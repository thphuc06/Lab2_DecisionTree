# Tiến độ — Role C (Improvement 1: Pruning)

> Chỉ [Tên thành viên C] và agent trong phiên làm việc của C được sửa file này.
> Agent: đọc file này ngay sau khi xác nhận mình đang phục vụ role C (bước 5, Mục 0 của `AGENT.md`), và **cập nhật lại trước khi bàn giao cuối mỗi phiên** (bước 8, Mục 0).

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-08-30 — đã áp dụng và kiểm chứng toàn bộ vòng hoàn thiện Role C)_
- Đang làm: không còn hạng mục kỹ thuật nào của Role C; chờ người dùng duyệt diff/PDF cuối và tự commit/push với tiền tố `[C]`.
- Bị chặn bởi: không.

## Đã xong
- [x] Đọc và đối chiếu tài liệu scikit-learn 1.9 về cost-complexity pruning, `GridSearchCV` và `StratifiedKFold`
- [x] Chạy `cost_complexity_pruning_path`, lấy 334 điểm path / 236 alpha duy nhất để CV (đã loại alpha cây một nút)
- [x] Chọn alpha bằng CV trên **train set** (không phải test)
- [x] Grid nhỏ `max_depth` ∈ {5,8,10,15}, `min_samples_leaf` ∈ {1,5,10,20} — đủ 16 cấu hình
- [x] Gọi `evaluate_model()` từ `src/evaluate.py` — không tự viết lại
- [x] Xuất `figures/C_ccp_alpha_curve.png`, `figures/C_tree_M1.png`, bảng grid search trong notebook
- [x] Xuất thêm artifact theo contract chung: `figures/C_cm_M1.png`, `outputs/classification_report_M1.txt`, một dòng M1 trong `outputs/results.csv`
- [x] Viết mục báo cáo `docs/report_draft_f1_pruning.md` bằng số liệu thực, gồm phương pháp, bảng grid, so sánh M0–M1, cơ chế, trade-off và giới hạn
- [x] Chuyển bản thảo đã kiểm chứng sang `docs/report/sections/f1_pruning.tex`: đủ 4 yêu cầu của đề, 4 bảng, 3 hình, citation và phân tích trade-off theo lớp; không còn TODO trong section Role C
- [x] Restart & Run All bằng kernel mới: 12 code cell chạy liền mạch `1→12`, không có error output; chạy lại idempotent vẫn chỉ có đúng một dòng M1
- [x] Kiểm chứng độc lập trong process mới: tái sinh alpha/grid và tính lại 12 trường số; tất cả khớp `results.csv` trong tolerance `1e-12`
- [x] Kiểm tra trực quan đủ 3 hình Role C; kiểm tra schema 16 cột, artifact không rỗng và phạm vi file đúng quyền sở hữu
- [x] Áp dụng vòng polish học thuật: làm mềm các kết luận nhân quả, giải thích rõ trade-off CV accuracy/macro-F1, định nghĩa generalization gap và diễn giải thận trọng giới hạn của một held-out split
- [x] Tái sinh biểu đồ pruning và cây M1; rút gọn nhãn chỉ để hiển thị, đặt cây trên trang landscape riêng và xác nhận không còn node/nhãn chồng lấn
- [x] Đồng bộ đánh số mục tự động `a`–`i`, tài liệu scikit-learn 1.9 và các đoạn Comparison/Conclusion liên quan trực tiếp đến kết quả M1
- [x] Đồng bộ `docs/report/README.md` với trạng thái thật: f.1 đã hoàn tất, PDF 27 trang và còn năm section skeleton thuộc các role khác
- [x] Compile report đầy đủ thành PDF A4 27 trang; kiểm tra trực quan toàn bộ 27 trang và ở độ phân giải cao các trang Role C/Comparison/Conclusion/References; log LaTeX, citation/reference, `qpdf`, text extraction và toàn bộ mốc số liệu đều pass

## Quyết định đã chốt
- Giao thức: 5-fold `StratifiedKFold(shuffle=True, random_state=42)`, chọn theo mean validation accuracy; tie-break ưu tiên mô hình đơn giản hơn.
- Dữ liệu test: không dùng trong pruning path/CV/grid; chỉ đánh giá đúng một lần sau khi khóa M1.
- alpha cuối cùng chọn: `0.0014874613584826332` (mean CV accuracy `0.747669`; hòa 2 alpha nên chọn alpha lớn hơn).
- max_depth / min_samples_leaf cuối cùng: `5 / 20` (mean CV accuracy của grid winner `0.748235`).
- M1 trên held-out test: accuracy `0.755932`, macro-F1 `0.672925`, ROC-AUC macro `0.847692`; depth `5`, leaves `17`.

## Việc tiếp theo
- Người dùng review `git diff` và `docs/report/report.pdf`, rồi tự `git add` / `git commit` / `git push` theo `AGENT.md`; commit giữ tiền tố `[C]`.
- Trước khi nộp báo cáo nhóm, các role sở hữu phần còn lại cần hoàn tất những TODO màu đỏ ngoài phạm vi Role C; không tự suy diễn hoặc điền thay số liệu chưa có của các role đó.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

### 2026-08-30 — áp dụng vòng hoàn thiện cuối và kiểm chứng bản bàn giao
- Đã làm gì: chỉnh lại toàn bộ văn phong học thuật của f.1; bổ sung giải thích giao thức chọn mô hình, trade-off accuracy/macro-F1 và giới hạn suy luận; tái sinh hai hình từ notebook; đặt cây M1 trên trang landscape; đồng bộ đánh số mục report, bibliography scikit-learn 1.9, trạng thái trong `docs/report/README.md` và các kết luận tổng hợp liên quan trực tiếp đến M1.
- Kết quả: notebook Run All thành công với 12 code cell có execution count liên tiếp `1→12`, không có error output và giữ nguyên các kết quả đã khóa. Một process độc lập đã fit lại M1 và xác nhận toàn bộ metric khớp `results.csv` trong tolerance `1e-12`; confusion matrix `[[195,36,53],[29,55,75],[12,11,419]]` khớp hình canonical. PDF cuối có 27 trang; kiểm tra trực quan toàn bộ report và kiểm tra độ phân giải cao các trang 12–17, 23–27 cho thấy không có chồng lấn, tràn trang hoặc lỗi đánh số. `qpdf`, LaTeX log, citation/reference, text extraction, kiểm tra số liệu và diff whitespace đều pass.
- Vướng gì / để lại cho phiên sau: không có lỗi chặn trong Role C; chỉ còn người dùng duyệt và tự commit/push với tiền tố `[C]`. Các TODO màu đỏ của role khác vẫn cần đúng owner xử lý trước khi nộp bản report toàn nhóm.

### 2026-08-30 — audit lại tính chuẩn xác và văn phong học thuật của f.1
- Đã làm gì: đối chiếu từng yêu cầu mục f trong đề gốc với nguồn LaTeX; kiểm tra lại notebook, M0/M1 trong `results.csv`, tài liệu scikit-learn 1.9.0, citation, log LaTeX và toàn bộ trang PDF 12–16; so sánh cách diễn giải M1 với các mục Comparison/Conclusion của report chung.
- Kết quả: không phát hiện lỗi công thức, số liệu, quy trình CV, test leakage, citation thiếu hoặc lỗi bố cục LaTeX trong f.1. Nội dung đã đủ chuẩn để nộp về mặt kỹ thuật. Có một vòng polish nên cân nhắc trước bản cuối: giảm mức khẳng định nhân quả ở đoạn bias–variance, nói rõ final grid tăng CV accuracy nhưng giảm CV macro-F1 so với alpha-only model, định nghĩa generalization gap, bỏ cách nhấn mạnh train accuracy như một “kết quả tốt”, thay tiêu đề hình mang tính nội bộ “Role C”, và làm cây M1 dễ đọc hơn khi in A4. Phát hiện thêm mismatch tài liệu tham khảo scikit-learn 1.8 so với môi trường canonical 1.9.0 và hai kết luận quá mạnh trong file của Role A.
- Vướng gì / để lại cho phiên sau: không có lỗi chặn; chưa sửa report vì yêu cầu hiện tại là review, chờ người dùng xác nhận có muốn áp dụng vòng polish hay không.

### 2026-08-30 — chuyển bản thảo pruning sang report LaTeX
- Đã làm gì: đồng bộ `origin/main`; đọc lại đề gốc, quy tắc report và tài liệu kỹ thuật; đối chiếu số liệu M0/M1 với `results.csv`, classification report và output CV trong notebook; viết hoàn chỉnh mục f.1 bằng tiếng Anh học thuật.
- Kết quả: section f.1 đã có mô tả cost-complexity/pre-pruning, giao thức train-only CV, bảng đủ 16 cấu hình grid, bảng setting M1, bảng M0–M1, ba hình canonical, cơ chế bias–variance, trade-off recall Enrolled và giới hạn của held-out split; không nhắc đường dẫn/hàm nội bộ trong nội dung báo cáo. Đã chạy lại độc lập toàn bộ 236 alpha và 16 cấu hình grid, compile PDF 25 trang, kiểm tra trực quan trang 12–16, xác thực cấu trúc PDF và rà log; mọi số liệu khớp, không còn TODO/cảnh báo/lỗi thuộc f.1.
- Vướng gì / để lại cho phiên sau: không; chỉ còn người dùng review và tự commit/push.

### 2026-08-29 — rà soát cuối và sửa finding P3
- Đã làm gì: sửa đơn vị tăng accuracy trong notebook thành “điểm phần trăm”, thay cách gọi “tầng” bằng “độ sâu” trong báo cáo/nhật ký, rồi Restart & Run All toàn bộ notebook.
- Kết quả: output hiển thị đúng `+8.70 điểm phần trăm`; 12 code cell chạy liên tiếp `1→12`, không có error output; M1 và toàn bộ số liệu/artifact không đổi.
- Vướng gì / để lại cho phiên sau: không.

### 2026-08-29 — bắt đầu triển khai
- Đã làm gì: đồng bộ `main`, tạo nhánh `feature/pruning`, kiểm tra đầu vào của Role A/B, đọc tài liệu chính thức theo scikit-learn 1.8, xây dựng và Run All notebook, chọn alpha/grid chỉ bằng train CV, fit và đánh giá M1 một lần trên test.
- Kết quả: M1 khóa tại `ccp_alpha=0.0014874613584826332`, `max_depth=5`, `min_samples_leaf=20`; test accuracy `0.755932`; độ sâu cây giảm từ 27 xuống 5 và số lá giảm từ 634 xuống 17; báo cáo f.1 và mọi artifact bắt buộc đã sinh thành công; Run All/QA độc lập đều pass.
- Vướng gì / để lại cho phiên sau: không.
