import json
import base64
import io
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def clean_label(label):
    label = str(label)

    bad_parts = [
        " | null",
        "| null",
        " / null",
        "/ null",
        "null",
        "None",
        "undefined"
    ]

    for b in bad_parts:
        label = label.replace(b, "")

    label = label.replace("  ", " ").strip()
    label = label.strip(" |-/")

    return label


def wrap_label(label, width=18):
    label = clean_label(label)
    return "\n".join(textwrap.wrap(label, width=width))


def make_message_image(message):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis("off")

    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        wrap=True
    )

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", dpi=220)
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close("all")

    return img_base64


def kmeans_positive_negative(values):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.array([], dtype=bool), 0.0

    if len(values) < 2 or np.std(values) == 0:
        threshold = float(np.mean(values))
        positive = values >= threshold
        return positive, threshold

    c1, c2 = np.percentile(values, [25, 75])

    for _ in range(100):
        d1 = np.abs(values - c1)
        d2 = np.abs(values - c2)

        labels = (d2 < d1).astype(int)

        new_c1 = values[labels == 0].mean() if np.any(labels == 0) else c1
        new_c2 = values[labels == 1].mean() if np.any(labels == 1) else c2

        if np.allclose([c1, c2], [new_c1, new_c2]):
            break

        c1, c2 = new_c1, new_c2

    centers = np.array([c1, c2])
    positive_cluster = np.argmax(centers)

    positive = labels == positive_cluster
    threshold = float(np.mean(centers))

    return positive, threshold


def get_intensity_values(d):
    intensity_values = (
        d.get("mean_nucli_values")
        or d.get("cell_intensities")
        or d.get("values")
        or d.get("mean_values")
        or d.get("intensity_values")
    )

    if intensity_values is None:
        return None

    try:
        arr = np.asarray(intensity_values, dtype=float)
        arr = arr[np.isfinite(arr)]
        return arr
    except Exception:
        return None


def compute_positive_counts(d):
    intensity_values = get_intensity_values(d)

    if intensity_values is not None and len(intensity_values) > 0:
        positive_flags, threshold = kmeans_positive_negative(intensity_values)

        total_cells = int(len(positive_flags))
        positive_cells = int(np.sum(positive_flags))
        negative_cells = int(total_cells - positive_cells)

        positive_percent = (
            100.0 * positive_cells / total_cells
            if total_cells > 0
            else 0.0
        )

        return {
            "total_cells": total_cells,
            "positive_cells": positive_cells,
            "negative_cells": negative_cells,
            "positive_percent": positive_percent,
            "threshold": threshold,
            "method": "kmeans"
        }

    total_cells = int(float(d.get("total_cells", 0)))
    positive_cells = int(float(d.get("positive_cells", 0)))
    negative_cells = int(float(d.get("negative_cells", 0)))

    if total_cells <= 0:
        total_cells = positive_cells + negative_cells

    if total_cells > 0:
        positive_percent = float(
            d.get(
                "positive_percent",
                100.0 * positive_cells / total_cells
            )
        )
    else:
        positive_percent = 0.0

    return {
        "total_cells": total_cells,
        "positive_cells": positive_cells,
        "negative_cells": negative_cells,
        "positive_percent": positive_percent,
        "threshold": None,
        "method": "precomputed"
    }


def get_marker_display_name(ch):
    marker = ch.get("marker")
    display_name = ch.get("display_name")
    channel_name = ch.get("channel_name")

    if marker is not None and str(marker).strip():
        return str(marker).strip()

    if display_name is not None and str(display_name).strip():
        return str(display_name).strip()

    if channel_name is not None and str(channel_name).strip():
        return str(channel_name).strip()

    channel_index = ch.get("channel_index", 0)
    return f"Channel {channel_index}"


def get_fluor_name(ch):
    channel_index = int(ch.get("channel_index", 0))

    fluor_name = ch.get(
        "channel_name",
        f"Channel {channel_index}"
    )

    return str(fluor_name)


def parse_positive_rows(json_strings, labels):
    rows = []

    for j, label in zip(json_strings, labels):
        try:
            data = json.loads(j) if isinstance(j, str) else j

            if not isinstance(data, dict):
                continue

            if data.get("status") == "failed":
                continue

            label = clean_label(label)

            if isinstance(data.get("channels"), list):

                for ch in data["channels"]:
                    if not isinstance(ch, dict):
                        continue

                    if ch.get("status") == "failed":
                        continue

                    counts = compute_positive_counts(ch)

                    total_cells = counts["total_cells"]
                    positive_cells = counts["positive_cells"]
                    negative_cells = counts["negative_cells"]
                    positive_percent = counts["positive_percent"]

                    if total_cells <= 0:
                        continue

                    channel_index = int(ch.get("channel_index", 0))
                    marker_name = get_marker_display_name(ch)
                    fluor_name = get_fluor_name(ch)

                    rows.append({
                        "label": label,
                        "channel_index": channel_index,
                        "channel_name": marker_name,
                        "marker_name": marker_name,
                        "fluor_name": fluor_name,
                        "positive_percent": positive_percent,
                        "positive_cells": positive_cells,
                        "negative_cells": negative_cells,
                        "total_cells": total_cells,
                        "threshold": counts["threshold"],
                        "method": counts["method"],
                    })

            else:
                counts = compute_positive_counts(data)

                total_cells = counts["total_cells"]
                positive_cells = counts["positive_cells"]
                negative_cells = counts["negative_cells"]
                positive_percent = counts["positive_percent"]

                if total_cells <= 0:
                    continue

                channel_index = int(data.get("channel_index", 0))

                marker_name = (
                    data.get("marker")
                    or data.get("display_name")
                    or data.get("channel_name")
                    or f"Channel {channel_index}"
                )

                fluor_name = (
                    data.get("channel_name")
                    or f"Channel {channel_index}"
                )

                marker_name = str(marker_name)
                fluor_name = str(fluor_name)

                rows.append({
                    "label": label,
                    "channel_index": channel_index,
                    "channel_name": marker_name,
                    "marker_name": marker_name,
                    "fluor_name": fluor_name,
                    "positive_percent": positive_percent,
                    "positive_cells": positive_cells,
                    "negative_cells": negative_cells,
                    "total_cells": total_cells,
                    "threshold": counts["threshold"],
                    "method": counts["method"],
                })

        except Exception:
            continue

    return rows


def get_marker_color(marker_name, fluor_name, index):
    text = f"{marker_name} {fluor_name}".upper()

    if "DAPI" in text or "HOECHST" in text:
        return "#1f77b4"

    if "488" in text or "FITC" in text or "GFP" in text:
        return "#2ca02c"

    if "594" in text or "TRITC" in text:
        return "#ff7f0e"

    if "647" in text or "CY5" in text:
        return "#d62728"

    default_colors = [
        "#1f77b4",
        "#2ca02c",
        "#ff7f0e",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#7f7f7f",
    ]

    return default_colors[index % len(default_colors)]


def generate_positive_barplot(json_strings, labels):
    rows = parse_positive_rows(json_strings, labels)

    if len(rows) == 0:
        return make_message_image("No valid positive-cell data found.")

    df = pd.DataFrame(rows)

    label_order = []

    for label in labels:
        label = clean_label(label)

        if label and label in df["label"].values and label not in label_order:
            label_order.append(label)

    if len(label_order) == 0:
        label_order = list(df["label"].drop_duplicates())

    marker_table = (
        df[["channel_index", "channel_name", "fluor_name"]]
        .drop_duplicates()
        .sort_values(["channel_index", "channel_name"])
        .reset_index(drop=True)
    )

    marker_names = marker_table["channel_name"].tolist()

    marker_colors = {}

    for i, row in marker_table.iterrows():
        marker = row["channel_name"]
        fluor = row["fluor_name"]

        marker_colors[marker] = get_marker_color(
            marker,
            fluor,
            i
        )

    n_labels = len(label_order)

    fig_width = max(12, n_labels * 2.4)
    fig_height = 8.5

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    x = np.arange(n_labels)

    for li, label in enumerate(label_order):

        sub_label = (
            df[df["label"] == label]
            .sort_values(["channel_index", "channel_name"])
            .reset_index(drop=True)
        )

        n_present = len(sub_label)

        if n_present == 0:
            continue

        local_group_width = 0.72

        if n_present == 1:
            local_bar_width = 0.36
        else:
            local_bar_width = min(
                0.22,
                local_group_width / max(n_present, 1)
            )

        for ci, (_, r) in enumerate(sub_label.iterrows()):

            if n_present == 1:
                offset = 0
            else:
                offset = (
                    -local_bar_width * (n_present - 1) / 2
                    + ci * local_bar_width
                )

            marker_name = str(r["channel_name"])
            value = float(r["positive_percent"])

            ax.bar(
                x[li] + offset,
                value,
                width=local_bar_width * 0.92,
                color=marker_colors.get(marker_name, "#7f7f7f"),
                edgecolor="black",
                linewidth=1.0
            )

            ax.text(
                x[li] + offset,
                value + 1.6,
                f"{value:.1f}%\n"
                f"({int(r['positive_cells'])}/{int(r['total_cells'])})",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold"
            )

    ax.set_ylabel(
        "Positive cells (%)",
        fontsize=17,
        fontweight="bold"
    )

    ax.set_xlabel("")

    if len(marker_names) == 1:
        plot_title = f"{marker_names[0]} Positive Cell Fraction"
    else:
        plot_title = "Marker-wise Positive Cell Fraction"

    ax.set_title(
        plot_title,
        fontsize=22,
        fontweight="bold",
        pad=24
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        [wrap_label(label, width=18) for label in label_order],
        rotation=25,
        ha="right",
        fontsize=12,
        fontweight="bold"
    )

    ymax = float(df["positive_percent"].max())

    if ymax <= 20:
        ytop = 30
    elif ymax <= 40:
        ytop = 50
    elif ymax <= 60:
        ytop = 75
    else:
        ytop = min(100, ymax + 18)

    ax.set_ylim(0, ytop)

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.8,
        alpha=0.30
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)

    ax.tick_params(
        axis="y",
        labelsize=12,
        width=1.2
    )

    if len(marker_names) > 1:
        legend_handles = [
            Patch(
                facecolor=marker_colors[marker],
                edgecolor="black",
                label=marker
            )
            for marker in marker_names
        ]

        ax.legend(
            handles=legend_handles,
            title="Marker",
            fontsize=11,
            title_fontsize=12,
            loc="upper right",
            frameon=True
        )

    plt.tight_layout()

    buffer = io.BytesIO()

    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=300,
        pad_inches=0.35
    )

    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close("all")

    return img_base64
