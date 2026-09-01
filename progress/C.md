# Tiến độ — Role C (Improvement 1: Pruning)

> Owner: Thái Quang Huy (Role C). Ngoài owner, chỉ agent đang làm task Role C
> hoặc task integration/final-audit được người dùng giao rõ mới sửa file này.
> Agent: đọc file này sau khi xác định phạm vi theo `AGENT.md` Mục 0 và cập
> nhật ngay sau mỗi mốc đáng kể, đồng thời kiểm tra lại trước khi bàn giao.

## Trạng thái hiện tại
_(cập nhật lần cuối: 2026-09-02 — đồng bộ PDF và audit cảnh báo LaTeX)_
- Trạng thái: hoàn tất; report được build lại bằng XeLaTeX/BibTeX thành 41 trang A4, Figure 10 nằm trên trang mang số in 22 (trang vật lý 23), và log không còn Underfull/Overfull box hay reference/citation cần xử lý.
- Hash hiện hành: `notebooks/03_improve_pruning.ipynb` = `edfbb84cf1f155f34a98f12fe14c79f591a64e74bf73ae99b1ff01d7b0d8c619`; hai PDF report = `dfeeb1f165824983d0c5d7750781bb9bab519176900e8ba4d45c9ee4af198a26`.
- Bị chặn bởi: không.

## Đã xong
- [x] Đọc và đối chiếu tài liệu scikit-learn 1.9 về cost-complexity pruning, `GridSearchCV` và `StratifiedKFold`
- [x] Chạy `cost_complexity_pruning_path`, lấy 334 điểm path / 236 alpha duy nhất để CV (đã loại alpha cây một nút)
- [x] Chọn alpha bằng CV trên **train set** (không phải test)
- [x] Grid nhỏ `max_depth` ∈ {5,8,10,15}, `min_samples_leaf` ∈ {1,5,10,20} — đủ 16 cấu hình
- [x] Gọi `evaluate_model()` từ `src/evaluate.py` — không tự viết lại
- [x] Xuất `figures/C_ccp_alpha_curve.png`, `figures/C_tree_M1.png`, bảng grid search trong notebook
- [x] Xuất thêm artifact theo contract chung: `figures/C_cm_M1.png`, `outputs/classification_report_M1.txt`, một dòng M1 trong `outputs/results.csv`
- [x] Viết và tích hợp nội dung f.1 bằng số liệu thực; bản nháp trung gian đã được xóa sau audit cuối
- [x] Chuyển bản thảo đã kiểm chứng sang `docs/report/sections/f1_pruning.tex`: đủ 4 yêu cầu của đề, 4 bảng, 3 hình, citation và phân tích trade-off theo lớp; không còn TODO trong section Role C
- [x] Restart & Run All bằng kernel mới: 12 code cell chạy liền mạch `1→12`, không có error output; chạy lại idempotent vẫn chỉ có đúng một dòng M1
- [x] Kiểm chứng độc lập trong process mới: tái sinh alpha/grid và tính lại 12 trường số; tất cả khớp `results.csv` trong tolerance `1e-12`
- [x] Kiểm tra trực quan đủ 3 hình Role C; kiểm tra schema 16 cột, artifact không rỗng và phạm vi file đúng quyền sở hữu
- [x] Chuẩn bị kịch bản và tài liệu hỗ trợ quay video trong giai đoạn media; nhóm xác nhận slide/video hiện đã hoàn thành và được quản lý ngoài workspace này
- [x] Rà lại đủ 3 ảnh canonical của Role C (`C_ccp_alpha_curve.png`, `C_tree_M1.png`, `C_cm_M1.png`); bổ sung confusion matrix vào danh sách tab, ACTION cuối và PDF, dùng hàng Enrolled `29 / 55 / 75` để giải thích trade-off
- [x] Sửa luồng quay: bỏ checklist khỏi đoạn `0:00–0:14` và khỏi danh sách tab trình chiếu; bắt đầu trực tiếp tại cell tiêu đề của `notebooks/03_improve_pruning.ipynb`
- [x] Bỏ `\clearpage` ngay sau Figure 10 trong `f1_pruning.tex` để tận dụng phần trắng bên dưới cho prose, không thay đổi ảnh/caption/kích thước cây M1
- [x] Bỏ `\clearpage` ngay trước Figure 10 để đặt hình vào phần trống của trang mang số in 22; build lại PDF 41 trang và kiểm tra trực quan toàn bộ tài liệu
- [x] Áp dụng vòng polish học thuật: làm mềm các kết luận nhân quả, giải thích rõ trade-off CV accuracy/macro-F1, định nghĩa generalization gap và diễn giải thận trọng giới hạn của một held-out split
- [x] Tái sinh biểu đồ pruning và cây M1; rút gọn nhãn chỉ để hiển thị, đặt toàn bộ cây trên trang A4 dọc và xác nhận không crop/chồng lấn
- [x] Đồng bộ đánh số mục tự động `a`–`i`, tài liệu scikit-learn 1.9 và các đoạn Comparison/Conclusion liên quan trực tiếp đến kết quả M1
- [x] Đồng bộ `docs/report/README.md` với trạng thái cuối: mọi section hoàn tất, không còn skeleton/TODO
- [x] Compile report đầy đủ và kiểm tra toàn bộ trang, log LaTeX, citation/reference, `qpdf`, text extraction và các mốc số liệu

## Quyết định đã chốt
- Giao thức: 5-fold `StratifiedKFold(shuffle=True, random_state=42)`, chọn theo mean validation accuracy; tie-break ưu tiên mô hình đơn giản hơn.
- Dữ liệu test: không dùng trong pruning path/CV/grid; chỉ đánh giá đúng một lần sau khi khóa M1.
- alpha cuối cùng chọn: `0.0014874613584826332` (mean CV accuracy `0.747669`; hòa 2 alpha nên chọn alpha lớn hơn).
- max_depth / min_samples_leaf cuối cùng: `5 / 20` (mean CV accuracy của grid winner `0.748235`).
- M1 trên held-out test: accuracy `0.755932`, macro-F1 `0.672925`, ROC-AUC macro `0.847692`; depth `5`, leaves `17`.

## Việc tiếp theo
- Không còn việc Role C trong workspace. Nhóm đối chiếu file/link video, số liệu report và đóng gói trực tiếp theo đề gốc.
- Người dùng review diff/PDF rồi tự `git add` / `git commit` / `git push` theo `AGENT.md`.

## Nhật ký phiên làm việc
<!-- Mỗi phiên thêm 1 mục mới lên TRÊN CÙNG, không xóa mục cũ -->

> Các entry dưới đây là snapshot lịch sử tại thời điểm được ghi. Khi số trang,
> phiên bản, TODO hoặc trạng thái cũ khác phần đầu file, phần **Trạng thái hiện
> tại** và artifact canonical mới nhất được ưu tiên.

### 2026-09-02 — đồng bộ bản report nộp bài và trạng thái hiện hành
- Đã làm gì: build lại report bằng XeLaTeX/BibTeX sau khi chuyển các cột mô tả hẹp sang ragged-right; đồng bộ bản PDF mang tên nộp bài và cập nhật hash hiện hành của notebook C/report.
- Kết quả: report giữ 41 trang A4; Figure 10 giữ đúng vị trí; log cuối không còn Underfull/Overfull box, undefined reference/citation hoặc yêu cầu rerun; hai PDF có cùng SHA-256 được ghi ở phần trạng thái hiện tại.
- Vướng gì / để lại cho phiên sau: không có việc kỹ thuật Role C; chỉ còn các cổng media/đóng gói do con người xác nhận.

### 2026-09-01 — đưa Figure 10 lên trang mang số in 22
- Đã làm gì: xác định `\clearpage` ngay trước Figure 10 là nguyên nhân tạo khoảng trắng lớn; bỏ đúng lệnh ngắt trang này, giữ nguyên ảnh, kích thước, caption và prose; build lại bằng XeLaTeX/BibTeX rồi render kiểm tra toàn bộ 41 trang.
- Kết quả: Figure 10 nằm trọn trên trang mang số in 22 (trang vật lý 23), caption hai dòng vẫn căn theo khối, prose tiếp tục ngay dưới hình; hai PDF tại snapshot này qua `qpdf`. Hash hiện hành được ghi ở phần trạng thái hiện tại.
- Vướng gì / để lại cho phiên sau: không.

### 2026-09-01 — chuẩn hóa metadata và trạng thái Figure 10
- Đã làm gì: điền owner thật, đồng bộ hướng dẫn progress với `AGENT.md` mới và sửa checklist hiện hành để phản ánh đúng Figure 10 ở trang A4 dọc thay vì trạng thái landscape trung gian.
- Kết quả: current state, README, checklist và PDF đều thống nhất Figure 10 ở trang vật lý 24, không crop, có prose bên dưới; metric/artifact M1 không đổi.
- Vướng gì / để lại cho phiên sau: không.

### 2026-09-01 — đồng bộ trạng thái media và report cuối
- Đã làm gì: loại tham chiếu hiện hành tới hai file kịch bản/PDF không còn trong workspace; giữ các mục lịch sử như bằng chứng công việc tại thời điểm chúng tồn tại; đồng bộ trạng thái theo xác nhận của nhóm rằng slide/video đã hoàn thành. Loại riêng `metadata.execution` khỏi 12 code cell của notebook C, không thay cell order/ID/source/output/execution count hoặc metadata khác.
- Kết quả: f.1 không còn finding mở; bản tại snapshot này có 42 trang và Figure 10 ở trang vật lý 24. Caption hai dòng căn theo khối, cây không crop và prose/bảng kết quả tiếp tục ngay dưới hình. Notebook C giữ execution count 1→12, 0 error/timing metadata, qua validator; hash hiện hành được ghi ở phần trạng thái hiện tại.
- Vướng gì / để lại cho phiên sau: chỉ còn cổng kiểm tra file/link media và đóng gói do con người thực hiện.

### 2026-09-01 — tận dụng khoảng trắng dưới Figure 10
- Đã làm gì: đối chiếu PDF cũ và source f.1, xác định `\clearpage` ngay sau Figure 10 là nguyên nhân đẩy toàn bộ đoạn giải thích sang trang sau; bỏ lệnh này nhưng giữ `\clearpage` trước figure. Đồng thời đối chiếu checklist audit tại thời điểm đó và đánh dấu các mục đã có bằng chứng đạt.
- Kết quả: preamble hỗ trợ XeLaTeX/LuaLaTeX nên không cần cài `vntex`; XeLaTeX/BibTeX build thành công PDF A4 dọc 44 trang. Render trang 25 xác nhận Figure 10 đầy đủ, caption hai dòng giữ căn theo khối mặc định, prose/tiêu đề f.1.3/bảng kết quả được đặt ngay trong phần trắng còn lại. Log không còn undefined reference/citation, rerun hay overfull warning; checklist có 58 mục đã đánh dấu và 21 mục còn lại.
- Vướng gì / để lại cho phiên sau: không có vướng mắc Role C; các owner còn lại tiếp tục 21 mục chưa đạt trong final-fix checklist.

### 2026-08-31 — soạn kịch bản video Role C
- Đã làm gì: đối chiếu yêu cầu video trong đề gốc, checklist Role C, notebook pruning và các artifact M0/M1; tạo kịch bản tiếng Việt theo từng mốc thời gian với hai cột ACTION + SCRIPT.
- Kết quả: `docs/report/ROLE_C_VIDEO_SCRIPT.md` có thời lượng mục tiêu 2:15–2:21; video bắt đầu trực tiếp tại cell tiêu đề của `notebooks/03_improve_pruning.ipynb`, không chiếu checklist, Markdown hoặc PDF kịch bản. Nội dung vẫn có đồ thị alpha, log grid/configuration, toàn bộ cây M1 không crop, accuracy/error rate, generalization gap, cơ chế giảm overfitting và trade-off recall Enrolled. Đã bổ sung thứ tự tab cần mở trên thanh VS Code, rà đủ ba ảnh canonical của Role C và đưa `C_cm_M1.png` vào đoạn kết để giải thích hàng Enrolled `29 / 55 / 75`. `output/pdf/ROLE_C_VIDEO_SCRIPT.pdf` đã được tái xuất thành 5 trang A4. Kiểm tra `pdfinfo`, `pypdf`, text extraction và render PNG đều đạt; không có trang rỗng, lỗi ký tự, crop, tràn lề hoặc chồng chữ.
- Vướng gì / để lại cho phiên sau: không có lỗi chặn; người dùng cần điền họ tên, quay thử bằng đồng hồ và không ứng biến thêm nếu muốn giữ chắc giới hạn 2:30.

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
