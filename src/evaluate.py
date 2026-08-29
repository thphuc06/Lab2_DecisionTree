"""Reusable evaluation utilities for the project's decision-tree models."""

from __future__ import annotations

import csv
import filecmp
import json
import os
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.utils.validation import check_is_fitted


REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_PATH = REPO_ROOT / "outputs" / "results.csv"
RESULT_COLUMNS = [
    "model_id",
    "model_name",
    "params",
    "train_acc",
    "test_acc",
    "error_rate",
    "precision_macro",
    "recall_macro",
    "f1_macro",
    "roc_auc_macro",
    "recall_dropout",
    "recall_enrolled",
    "recall_graduate",
    "tree_depth",
    "n_leaves",
    "author",
]


def _json_default(value: Any) -> Any:
    """Convert common non-JSON scalar values into stable representations."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (set, frozenset)):
        return sorted(value, key=str)
    return str(value)


def _serialize_params(params: Mapping[str, Any] | str) -> str:
    """Serialize parameters deterministically so they remain one valid CSV field."""
    if isinstance(params, str):
        try:
            parsed = json.loads(params)
        except json.JSONDecodeError:
            return params
        return json.dumps(
            parsed,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=_json_default,
        )
    return json.dumps(
        dict(params),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=_json_default,
    )


def _as_csv_row(result: Mapping[str, Any]) -> dict[str, str]:
    """Convert a result mapping to the exact string representation used by CSV."""
    return {column: str(result[column]) for column in RESULT_COLUMNS}


def _check_result_conflict(result: Mapping[str, Any], results_path: Path) -> bool:
    """Validate a result ID without writing; return whether a new row is needed."""
    new_row = _as_csv_row(result)
    if results_path.exists() and results_path.stat().st_size > 0:
        with results_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != RESULT_COLUMNS:
                raise ValueError(
                    f"Invalid results schema in {results_path}: "
                    f"expected {RESULT_COLUMNS}, got {reader.fieldnames}."
                )
            existing_rows = list(reader)

        same_id_rows = [row for row in existing_rows if row["model_id"] == new_row["model_id"]]
        if same_id_rows:
            if len(same_id_rows) == 1 and same_id_rows[0] == new_row:
                return False
            differences = {
                column: (same_id_rows[0].get(column), new_row[column])
                for column in RESULT_COLUMNS
                if same_id_rows[0].get(column) != new_row[column]
            }
            raise ValueError(
                f"model_id={new_row['model_id']!r} already exists with different "
                f"content in {results_path}. Differing fields: {differences}"
            )
    return True


def _append_result_once(result: Mapping[str, Any], results_path: Path) -> None:
    """Append a result once, rechecking conflicts immediately before writing."""
    results_path.parent.mkdir(parents=True, exist_ok=True)
    if not _check_result_conflict(result, results_path):
        return

    write_header = not results_path.exists() or results_path.stat().st_size == 0
    new_row = _as_csv_row(result)

    with results_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=RESULT_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(new_row)


def _temporary_output_path(destination: Path) -> Path:
    """Create and close a temporary file beside its final destination."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        dir=destination.parent,
        prefix=f".{destination.stem}.",
        suffix=destination.suffix,
        delete=False,
    ) as temporary_file:
        return Path(temporary_file.name)


def _replace_output(temporary_path: Path, destination: Path) -> None:
    """Replace an artifact atomically, tolerating an identical locked target.

    Windows can briefly deny replacement while an image previewer, antivirus
    scanner, or restricted notebook process has the existing target open. A few
    short retries cover transient locks. If the target already has byte-for-byte
    identical content, keeping it is equivalent to a successful idempotent write
    and avoids falling back to a non-atomic overwrite.
    """
    retry_delays = (0.0, 0.05, 0.10, 0.20, 0.40)
    last_error: PermissionError | None = None
    for delay in retry_delays:
        if delay:
            time.sleep(delay)
        try:
            os.replace(temporary_path, destination)
            return
        except PermissionError as error:
            last_error = error
            try:
                if destination.is_file() and filecmp.cmp(
                    temporary_path,
                    destination,
                    shallow=False,
                ):
                    return
            except OSError:
                # The same lock can temporarily block comparison; retry below.
                pass

    raise PermissionError(
        f"Could not atomically replace {destination}. Close any program previewing "
        "the file, then rerun from the repository root. The previous artifact "
        "was left unchanged."
    ) from last_error


def _save_classification_report(
    y_true: Any,
    y_pred: Any,
    classes: Sequence[Any],
    save_path: Path,
) -> None:
    """Atomically save a class-ordered text classification report."""
    report = classification_report(
        y_true,
        y_pred,
        labels=list(classes),
        target_names=[str(label) for label in classes],
        digits=4,
        zero_division=0,
    )
    temporary_path = _temporary_output_path(save_path)
    try:
        temporary_path.write_text(report, encoding="utf-8")
        _replace_output(temporary_path, save_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _save_confusion_matrix(
    y_true: Any,
    y_pred: Any,
    classes: Sequence[Any],
    model_id: str,
    model_name: str,
    save_path: Path,
) -> None:
    """Atomically save a labeled confusion matrix with counts and a colorbar."""
    matrix = confusion_matrix(y_true, y_pred, labels=list(classes))
    figure = Figure(figsize=(8, 6))
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    temporary_path = _temporary_output_path(save_path)
    try:
        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix,
            display_labels=[str(label) for label in classes],
        )
        display.plot(ax=axis, cmap="Blues", colorbar=True, values_format="d")
        axis.set_title(f"Confusion Matrix - {model_id}: {model_name}")
        axis.set_xlabel("Predicted label")
        axis.set_ylabel("True label")
        figure.tight_layout()
        figure.savefig(temporary_path, dpi=200, bbox_inches="tight")
        _replace_output(temporary_path, save_path)
    finally:
        figure.clear()
        temporary_path.unlink(missing_ok=True)


def evaluate_model(
    model: Any,
    X_train: Any,
    y_train: Any,
    X_test: Any,
    y_test: Any,
    model_id: str,
    model_name: str,
    params: Mapping[str, Any] | str,
    author: str,
    *,
    results_path: str | Path = RESULTS_PATH,
    classification_report_path: str | Path | None = None,
    confusion_matrix_path: str | Path | None = None,
) -> dict[str, Any]:
    """Evaluate a fitted decision-tree classifier and persist its result safely.

    The function computes the project's fixed 16-column result schema. Multiclass
    ROC-AUC uses ``predict_proba`` in the exact order of ``model.classes_``.
    Per-class recall is mapped by class name rather than by a positional shortcut.
    A result is appended only when ``model_id`` is absent; an identical rerun is a
    no-op, while a conflicting row raises ``ValueError``.

    Args:
        model: A fitted classifier exposing ``predict``, ``predict_proba``,
            ``classes_``, ``get_depth``, and ``get_n_leaves``.
        X_train: Training features used to compute training accuracy.
        y_train: Training labels.
        X_test: Held-out test features.
        y_test: Held-out test labels.
        model_id: Stable identifier such as ``"M0"``.
        model_name: Human-readable model name.
        params: Model parameters to serialize deterministically as JSON.
        author: Role or contributor responsible for the result.
        results_path: Destination CSV; defaults relative to this source file.
        classification_report_path: Optional text-report destination.
        confusion_matrix_path: Optional confusion-matrix PNG destination.

    Returns:
        A dictionary ordered according to ``RESULT_COLUMNS``.

    Raises:
        ValueError: If expected classes are missing, probability columns do not
            match ``model.classes_``, or ``model_id`` conflicts in the CSV.
    """
    check_is_fitted(model)
    required_methods = ("predict", "predict_proba", "get_depth", "get_n_leaves")
    missing_methods = [name for name in required_methods if not callable(getattr(model, name, None))]
    if missing_methods:
        raise TypeError(f"Model is missing required methods: {missing_methods}")

    classes = np.asarray(model.classes_)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_proba = np.asarray(model.predict_proba(X_test))
    if y_test_proba.ndim != 2 or y_test_proba.shape[1] != len(classes):
        raise ValueError(
            "predict_proba columns must match model.classes_: "
            f"shape={y_test_proba.shape}, classes={classes.tolist()}"
        )

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    per_class_recall = recall_score(
        y_test,
        y_test_pred,
        labels=classes,
        average=None,
        zero_division=0,
    )
    recall_by_name = {
        str(label).casefold(): float(value)
        for label, value in zip(classes, per_class_recall, strict=True)
    }
    expected_classes = ("dropout", "enrolled", "graduate")
    missing_classes = [name for name in expected_classes if name not in recall_by_name]
    if missing_classes:
        raise ValueError(
            f"Expected target classes are missing from model.classes_: {missing_classes}; "
            f"got {classes.tolist()}"
        )

    if len(classes) == 2:
        roc_auc_macro = roc_auc_score(y_test, y_test_proba[:, 1], labels=classes)
    else:
        roc_auc_macro = roc_auc_score(
            y_test,
            y_test_proba,
            labels=classes,
            multi_class="ovr",
            average="macro",
        )

    result: dict[str, Any] = {
        "model_id": str(model_id),
        "model_name": str(model_name),
        "params": _serialize_params(params),
        "train_acc": float(train_acc),
        "test_acc": float(test_acc),
        "error_rate": float(1.0 - test_acc),
        "precision_macro": float(
            precision_score(y_test, y_test_pred, average="macro", zero_division=0)
        ),
        "recall_macro": float(
            recall_score(y_test, y_test_pred, average="macro", zero_division=0)
        ),
        "f1_macro": float(f1_score(y_test, y_test_pred, average="macro", zero_division=0)),
        "roc_auc_macro": float(roc_auc_macro),
        "recall_dropout": recall_by_name["dropout"],
        "recall_enrolled": recall_by_name["enrolled"],
        "recall_graduate": recall_by_name["graduate"],
        "tree_depth": int(model.get_depth()),
        "n_leaves": int(model.get_n_leaves()),
        "author": str(author),
    }

    destination_results_path = Path(results_path)
    # Fail before touching reports/figures when the model ID conflicts. This
    # prevents a stale CSV row from being paired with newly overwritten artifacts.
    _check_result_conflict(result, destination_results_path)

    if classification_report_path is not None:
        _save_classification_report(
            y_test,
            y_test_pred,
            classes,
            Path(classification_report_path),
        )
    if confusion_matrix_path is not None:
        _save_confusion_matrix(
            y_test,
            y_test_pred,
            classes,
            str(model_id),
            str(model_name),
            Path(confusion_matrix_path),
        )

    _append_result_once(result, destination_results_path)
    return result
