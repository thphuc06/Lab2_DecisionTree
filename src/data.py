"""
Role A: data loading, preprocessing, and train/test split.

Nguồn dữ liệu: UCI ML Repository id=697 (Predict Students' Dropout and
Academic Success), 4424 mẫu, 36 feature + 1 target 3 lớp
(Dropout / Enrolled / Graduate). Chi tiết: docs/02-DATASET-VA-CONG-VIEC.md.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "data.csv"
TARGET_COL = "Target"
RANDOM_STATE = 42

# Cột ít giá trị -> one-hot (split thành câu hỏi có/không đọc được).
# Cột nhiều giá trị -> giữ nguyên mã số (one-hot sẽ tạo quá nhiều cột thưa).
# Quyết định theo docs/02-DATASET-VA-CONG-VIEC.md Phần B1.
ONE_HOT_COLS = [
    "Marital Status",
    "Application mode",
    "Course",
    "Previous qualification",
]


def load_and_preprocess(csv_path: str | Path = RAW_DATA_PATH) -> tuple[pd.DataFrame, pd.Series]:
    """Đọc data.csv, one-hot các cột category ít giá trị, trả về (X, y).

    Không chuẩn hóa/scale (decision tree không cần).
    Args:
        csv_path: đường dẫn tới data/raw/data.csv.
    Returns:
        X: DataFrame feature đã tiền xử lý (numeric, sẵn sàng cho DecisionTreeClassifier).
        y: Series nhãn gốc dạng chuỗi (Dropout / Enrolled / Graduate).
    """
    df = pd.read_csv(csv_path)

    y = df[TARGET_COL]
    X = df.drop(columns=[TARGET_COL])

    X = pd.get_dummies(X, columns=ONE_HOT_COLS, prefix=ONE_HOT_COLS, dtype=int)

    return X, y


def get_train_test(
    csv_path: str | Path = RAW_DATA_PATH,
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load, tiền xử lý, rồi stratified split train/test.

    Đây là điểm split DUY NHẤT của cả nhóm — mọi notebook phải gọi hàm này,
    không tự split lại (docs/02 Phần B3, AGENT.md mục 2).
    Returns:
        X_train, X_test, y_train, y_test
    """
    X, y = load_and_preprocess(csv_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    return X_train, X_test, y_train, y_test
