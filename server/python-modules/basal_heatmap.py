import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import base64
import io
import numpy as np


def normalize_row(row):
    row = pd.to_numeric(row, errors="coerce")

    std_val = row.std(skipna=True)
    mean_val = row.mean(skipna=True)

    if std_val == 0 or np.isnan(std_val):
        return row * 0

    return (row - mean_val) / std_val


def clean_metric_name(name):
    name = str(name)

    name = name.replace("non_basal_", "Non-Basal ")
    name = name.replace("basal_", "Basal ")
    name = name.replace("_", " ")

    replacements = {
        "mean nucleus size": "Mean Nucleus Size",
        "median nucleus size": "Median Nucleus Size",
        "total nucleus volume": "Total Nucleus Volume",
        "Nuclear Elongation": "Nuclear Elongation",
        "Nuclear Flatness": "Nuclear Flatness",
        "Nuclear Volume": "Nuclear Volume",
        "Colony Elongation": "Colony Elongation",
        "Colony Flatness": "Colony Flatness",
        "Colony Radius": "Colony Radius",
        "Colony Diameter": "Colony Diameter",
        "Volume of Colony Convex Hull": "Convex Hull Volume",
        "Lumen Volume": "Lumen Volume",
        "Mean Neighbourhood Distance": "Mean Neighbor Distance",
        "Max Neighbourhood Distance": "Max Neighbor Distance",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    name = name.replace("non Basal", "Non-Basal")
    name = name.replace("Non Basal", "Non-Basal")

    return name


def metric_order_key(name):
    order = [
        "Mean Nucleus Size",
        "Median Nucleus Size",
        "Total Nucleus Volume",
        "Nuclear Volume",
        "Nuclear Elongation",
        "Nuclear Flatness",
        "Colony Radius",
        "Colony Diameter",
        "Colony Elongation",
        "Colony Flatness",
        "Convex Hull Volume",
        "Lumen Volume",
        "Mean Neighbor Distance",
        "Max Neighbor Distance",
    ]

    if name.startswith("Basal "):
        group_rank = 0
        metric_part = name.replace("Basal ", "")
    elif name.startswith("Non-Basal "):
        group_rank = 1
        metric_part = name.replace("Non-Basal ", "")
    else:
        group_rank = 2
        metric_part = name

    try:
        metric_rank = order.index(metric_part)
    except ValueError:
        metric_rank = 999

    return group_rank, metric_rank, name


def generate_basal_nonbasal_heatmap(json_strings, labels):
    data_list = []
    valid_labels = []

    for i, j in enumerate(json_strings):
        try:
            parsed = json.loads(j) if isinstance(j, str) else j

            if isinstance(parsed, dict) and parsed.get("status") != "failed":
                data_list.append(parsed)
                valid_labels.append(
                    labels[i] if i < len(labels) else f"Sample {i + 1}"
                )

        except Exception:
            continue

    if len(data_list) == 0:
        raise ValueError("No valid basal/non-basal JSON data found.")

    df = pd.DataFrame(data_list)

    keep_cols = [
        c for c in df.columns
        if str(c).startswith("basal_") or str(c).startswith("non_basal_")
    ]

    remove_words = [
        "cells",
        "percent",
        "mean_z",
        "mean_y",
        "mean_x",
        "morph_cells",
        "total_nucleus_volume"
    ]

    keep_cols = [
        c for c in keep_cols
        if not any(w in str(c) for w in remove_words)
    ]

    if len(keep_cols) == 0:
        raise ValueError("No basal_/non_basal_ numeric columns found.")

    df = df[keep_cols]
    df = df.apply(pd.to_numeric, errors="coerce")

    df = df.T
    df.columns = valid_labels

    df.index = [clean_metric_name(idx) for idx in df.index]
    df = df.loc[sorted(df.index, key=metric_order_key)]

    # Missing cells = truly not applicable, e.g. no non-basal cells.
    plot_mask = df.isna()

    # Fill only for clustering/normalization.
    df_for_norm = df.apply(
        lambda row: row.fillna(row.mean(skipna=True)),
        axis=1
    ).fillna(0)

    df_norm = df_for_norm.apply(normalize_row, axis=1)
    df_norm = df_norm.replace([np.inf, -np.inf], 0).fillna(0)

    annot_df = df_norm.applymap(lambda x: f"{x:.2g}")

    row_colors = pd.Series(
        [
            "#4C78A8" if idx.startswith("Basal ") else "#F58518"
            for idx in df_norm.index
        ],
        index=df_norm.index
    )

    n_rows = df_norm.shape[0]
    n_cols = df_norm.shape[1]

    fig_width = max(16, min(24, 1.8 * n_cols + 8))
    fig_height = max(14, min(28, 0.45 * n_rows + 8))

    heatmap = sns.clustermap(
        df_norm,
        mask=plot_mask,
        annot=annot_df,
        fmt="",
        cmap="vlag",
        center=0,
        row_cluster=False,
        col_cluster=True,
        row_colors=row_colors,
        tree_kws=dict(linewidths=2.2, colors=(0.18, 0.18, 0.38)),
        annot_kws={"fontsize": 8, "fontweight": "bold"},
        linewidths=0.4,
        linecolor="white",
        figsize=(fig_width, fig_height),
        cbar_kws={"label": "Row Z-score"}
    )

    ax = heatmap.ax_heatmap

    reordered_rows = (
        [df_norm.index[i] for i in heatmap.dendrogram_row.reordered_ind]
        if heatmap.dendrogram_row is not None
        else list(df_norm.index)
    )

    reordered_cols = (
        [df_norm.columns[i] for i in heatmap.dendrogram_col.reordered_ind]
        if heatmap.dendrogram_col is not None
        else list(df_norm.columns)
    )

    for y, r in enumerate(reordered_rows):
        for x, c in enumerate(reordered_cols):
            if plot_mask.loc[r, c]:
                ax.text(
                    x + 0.5,
                    y + 0.5,
                    "N/A",
                    ha="center",
                    va="center",
                    fontsize=8,
                    fontweight="bold",
                    color="black"
                )

    heatmap.ax_heatmap.set_xlabel("")
    heatmap.ax_heatmap.set_ylabel("")

    heatmap.ax_heatmap.tick_params(axis="x", labelsize=13, rotation=90)
    heatmap.ax_heatmap.tick_params(axis="y", labelsize=12)

    for tick in heatmap.ax_heatmap.get_xticklabels():
        tick.set_fontweight("bold")
        tick.set_rotation(90)

    for tick in heatmap.ax_heatmap.get_yticklabels():
        tick.set_fontweight("bold")

    heatmap.cax.tick_params(labelsize=11)
    heatmap.cax.set_ylabel(
        "Row Z-score",
        fontsize=11,
        fontweight="bold"
    )

    basal_count = sum(
        idx.startswith("Basal ")
        for idx in df_norm.index
    )

    if 0 < basal_count < len(df_norm.index):
        heatmap.ax_heatmap.axhline(
            basal_count,
            color="black",
            linewidth=2.5
        )

    heatmap.fig.suptitle(
        "Basal and Non-Basal Morphometric Heatmap",
        fontsize=20,
        fontweight="bold",
        y=1.02
    )

    heatmap.ax_row_colors.set_yticks([])

    buffer = io.BytesIO()
    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=150
    )
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close("all")

    return img_base64
