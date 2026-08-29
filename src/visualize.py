"""Reusable decision-tree visualization and rule-export helpers."""

from __future__ import annotations

import filecmp
import os
import time
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from sklearn.tree import export_text, plot_tree
from sklearn.utils.validation import check_is_fitted


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
    """Replace an artifact atomically, tolerating an identical locked target."""
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


def _validate_tree_metadata(
    model: Any,
    feature_names: Sequence[str],
    class_names: Sequence[str],
) -> tuple[list[str], list[str]]:
    """Validate feature/class metadata against the fitted estimator."""
    check_is_fitted(model)
    features = [str(name) for name in feature_names]
    classes = [str(name) for name in class_names]

    expected_feature_count = int(model.n_features_in_)
    if len(features) != expected_feature_count:
        raise ValueError(
            f"Expected {expected_feature_count} feature names, got {len(features)}."
        )

    fitted_classes = [str(label) for label in model.classes_]
    if classes != fitted_classes:
        raise ValueError(
            "class_names must follow model.classes_ exactly: "
            f"expected {fitted_classes}, got {classes}."
        )
    return features, classes


def plot_tree_figure(
    model: Any,
    feature_names: Sequence[str],
    class_names: Sequence[str],
    save_path: str | Path,
    max_depth: int | None = None,
    *,
    figsize: tuple[float, float] | None = None,
    dpi: int = 200,
    fontsize: float | None = None,
    title: str | None = None,
) -> Path:
    """Render a fitted sklearn decision tree to a report-ready PNG.

    Nodes include their split, impurity, sample count, class distribution, and
    predicted class. ``class_names`` is deliberately validated against
    ``model.classes_`` so labels cannot silently be attached in the wrong order.

    Args:
        model: Fitted sklearn decision-tree estimator.
        feature_names: Names in the same order as the fitted feature matrix.
        class_names: Class labels in the exact order of ``model.classes_``.
        save_path: Destination image path.
        max_depth: Optional display-only depth limit; the model is not modified.
        figsize: Figure dimensions in inches. A larger default is used for a full
            tree than for a depth-limited tree.
        dpi: Output resolution.
        fontsize: Optional node-label font size passed to ``plot_tree``.
        title: Optional figure title.

    Returns:
        The resolved destination ``Path``.
    """
    features, classes = _validate_tree_metadata(model, feature_names, class_names)
    destination = Path(save_path)
    temporary_path = _temporary_output_path(destination)

    if figsize is None:
        figsize = (40, 24) if max_depth is None else (24, 14)

    figure = Figure(figsize=figsize)
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    try:
        plot_tree(
            model,
            feature_names=features,
            class_names=classes,
            max_depth=max_depth,
            filled=True,
            rounded=True,
            impurity=True,
            proportion=False,
            precision=3,
            fontsize=fontsize,
            ax=axis,
        )
        axis.set_title(
            title
            or (
                "Decision Tree (full model)"
                if max_depth is None
                else f"Decision Tree (first {max_depth} levels)"
            ),
            pad=18,
        )
        figure.tight_layout()
        figure.savefig(temporary_path, dpi=dpi, bbox_inches="tight", facecolor="white")
        _replace_output(temporary_path, destination)
    finally:
        figure.clear()
        temporary_path.unlink(missing_ok=True)
    return destination.resolve()


def export_rules(
    model: Any,
    feature_names: Sequence[str],
    save_path: str | Path,
    *,
    max_depth: int | None = None,
    decimals: int = 3,
    spacing: int = 3,
) -> Path:
    """Export readable IF-THEN-style rules from a fitted sklearn tree.

    When ``max_depth`` is omitted, the estimator's actual depth is used so
    ``sklearn.tree.export_text`` does not truncate its default at depth 10.

    Args:
        model: Fitted sklearn decision-tree estimator.
        feature_names: Names in fitted-column order.
        save_path: Destination UTF-8 text file.
        max_depth: Optional export depth; defaults to the complete tree.
        decimals: Decimal places used for thresholds and values.
        spacing: Number of spaces per indentation level.

    Returns:
        The resolved destination ``Path``.
    """
    check_is_fitted(model)
    features = [str(name) for name in feature_names]
    if len(features) != int(model.n_features_in_):
        raise ValueError(
            f"Expected {model.n_features_in_} feature names, got {len(features)}."
        )

    export_depth = int(model.get_depth()) if max_depth is None else int(max_depth)
    rules = export_text(
        model,
        feature_names=features,
        max_depth=export_depth,
        decimals=decimals,
        spacing=spacing,
        show_weights=True,
    )
    destination = Path(save_path)
    temporary_path = _temporary_output_path(destination)
    try:
        temporary_path.write_text(rules, encoding="utf-8")
        _replace_output(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination.resolve()
