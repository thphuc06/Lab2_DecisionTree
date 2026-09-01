# LaTeX report

Thư mục này chứa source và hai bản PDF của written-report deliverable theo
Mục 3.3--3.4 trong `docs/00-DE-BAI-GOC.pdf`. LaTeX là nguồn canonical duy
nhất; năm bản nháp `docs/report_draft_*.md` đã được loại bỏ trong vòng audit
cuối vì chúng đã bị thay thế và có thể chứa cách diễn giải cũ.

## Cấu trúc

```text
docs/report/
├── report.tex
├── references.bib
├── report.pdf
├── 2 - Report.pdf
├── README.md
└── sections/
    ├── a_group_intro.tex
    ├── b_introduction.tex
    ├── c_dataset.tex
    ├── d_baseline.tex
    ├── e_analysis.tex
    ├── f1_pruning.tex
    ├── f2_imbalance.tex
    ├── f3_features.tex
    ├── g_comparison.tex
    └── h_conclusion.tex
```

Mục i (References) được BibTeX sinh từ `references.bib`; không có section
LaTeX riêng. `report.pdf` là bản canonical trong repository. `2 - Report.pdf`
tuân theo mẫu `[GroupID - Report].pdf` cho Group 2 và phải được tái tạo sau
bất kỳ thay đổi nào của `.tex`, `.bib` hoặc figure.

## Trạng thái cuối

Vòng audit tích hợp ngày **2026-09-02** đã xác nhận:

- Có đủ mục a--i theo đề gốc.
- Group ID, năm họ tên, năm MSSV và contribution 20% mỗi người đã được điền.
- Không còn lời gọi TODO, placeholder, `??`, undefined reference/citation hoặc
  cross-reference trỏ nhầm.
- Metric M0/M1/M2a/M2b/M3 khớp artifact canonical và classification report.
- Claim từ CSV được tách khỏi claim metadata bên ngoài; nguồn ngoài có DOI/URL
  và ngày truy cập trong `references.bib`/`docs/dataset_provenance.md`.
- M2b luôn đi cùng giới hạn vanilla SMOTE trên representation categorical;
  M3 luôn đi cùng giả định về thời điểm availability của feature.
- PDF cuối có 41 trang A4; Figure 10 là toàn bộ cây M1 ở trang mang số in 22
  (trang vật lý 23 của file PDF), không crop và prose tiếp tục bên dưới hình.
- Các trang bị ảnh hưởng bởi lần chỉnh layout cuối — bảng phân bố lớp, hai bảng
  cây M0, Figure 10, bảng chọn model và References — đã được render và kiểm tra
  trực quan sau build.
- `report.pdf` và `2 - Report.pdf` có cùng SHA-256
  `dfeeb1f165824983d0c5d7750781bb9bab519176900e8ba4d45c9ee4af198a26`.
- XeLaTeX/BibTeX build sạch 41 trang A4, không còn `Underfull \hbox`,
  `Overfull \hbox`, undefined reference/citation hoặc yêu cầu rerun.

Các bước chỉ con người mới xác nhận được — media, tên chính thức, ZIP nộp bài
và Git history — được đối chiếu trực tiếp với đề gốc và hệ thống nộp bài.

## Quy tắc caption

Caption chỉ mô tả hình/bảng; số liệu so sánh, diễn giải và kết luận phải đặt
trong body text ngay trước hoặc sau float.

Giữ behavior mặc định của package `caption`:

- Caption vừa một dòng: căn giữa.
- Caption tự xuống từ hai dòng trở lên: trình bày như một khối text bình
  thường, không ép căn giữa toàn bộ.

## Build bằng XeLaTeX

XeLaTeX là đường build canonical vì đọc trực tiếp tên tiếng Việt UTF-8 và
không cần `vntex`:

```powershell
Push-Location docs/report
xelatex -interaction=nonstopmode -halt-on-error report.tex
bibtex report
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
Copy-Item -LiteralPath report.pdf -Destination '2 - Report.pdf' -Force
Pop-Location
```

Nhánh pdfLaTeX trong preamble dùng encoding T5 và vì vậy cần `vntex`. Không cần
cài package này nếu tiếp tục dùng XeLaTeX. MiKTeX `latexmk` cần Perl trên
`PATH`; chuỗi lệnh tường minh ở trên không cần Perl.

## Cổng kiểm tra sau mỗi lần build

```powershell
rg -n "Overfull|Undefined|undefined|Rerun|Label\(s\) may have changed|Fatal error|^!" docs/report/report.log
pdftotext -layout docs/report/report.pdf - | rg -n "\?\?|TODO|Undefined"
qpdf --check docs/report/report.pdf
pdfinfo docs/report/report.pdf
Get-FileHash -Algorithm SHA256 -LiteralPath `
    docs/report/report.pdf, 'docs/report/2 - Report.pdf'
```

Kỳ vọng:

- Lệnh `rg` trên log/text không trả finding nghiêm trọng.
- `qpdf` không báo syntax/stream error.
- Hai PDF có cùng SHA-256.
- Render lại toàn bộ trang sau mọi thay đổi ảnh hoặc dàn trang; exit code build
  không thay thế visual QA.

## Trước khi nộp

- Đối chiếu trực tiếp Group 2, tên, MSSV, instructor và ngày trên title page
  với thông tin chính thức của lớp.
- Không đưa file build trung gian (`.aux`, `.bbl`, `.blg`, `.log`, `.out`,
  `.toc`) vào gói nộp nếu đề không yêu cầu.
- Giữ đúng tên `2 - Report.pdf`; kiểm tra mở được từ bản sao nằm trong ZIP.
- Đối chiếu số trong video với bảng `outputs/results.csv` và report PDF.
