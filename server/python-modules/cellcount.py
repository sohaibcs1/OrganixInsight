import json
import os
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from scipy.stats import mannwhitneyu
import base64
from PIL import Image

# -----------------------------
# Load DB config from JSON file
# -----------------------------
CFG_PATH = "db_config.json"
if not os.path.exists(CFG_PATH):
    raise FileNotFoundError(
        f"Config file '{CFG_PATH}' not found. Create it with keys: "
        "{database, user, host, password, port}"
    )

with open(CFG_PATH, "r", encoding="utf-8") as f:
    DB_CFG = json.load(f)


# -----------------------------
# Helpers
# -----------------------------
def _meta_to_df(data):
    df = pd.DataFrame(data, columns=["experiment_id", "drug_info", "treatment_group"])
    df["experiment_id"] = pd.to_numeric(df["experiment_id"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["experiment_id"]).astype({"experiment_id": "int64"})
    df = df.drop_duplicates(subset=["experiment_id"]).reset_index(drop=True)
    return df


def _normalize_ids_int(df, col="experiment_id"):
    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df.dropna(subset=[col], inplace=True)
    df[col] = df[col].astype("int64")
    return df


def get_model2ds_by_experiment_ids(experiment_ids):
    if not experiment_ids:
        raise ValueError("experiment_ids list is empty!")

    with psycopg2.connect(**DB_CFG) as conn:
        query = """
            SELECT *
            FROM model_2ds
            WHERE CAST(experiment_id AS INTEGER) = ANY(%s);
        """
        df = pd.read_sql(query, conn, params=(experiment_ids,))

    df = _normalize_ids_int(df, "experiment_id")
    return df


def fetch_model2ds_with_meta(meta_rows):
    df_meta = _meta_to_df(meta_rows)
    exp_ids = df_meta["experiment_id"].tolist()
    df_db = get_model2ds_by_experiment_ids(exp_ids)
    df_merged = pd.merge(df_db, df_meta, on="experiment_id", how="inner")
    return df_db, df_meta, df_merged


# -----------------------------
# Protein helpers
# -----------------------------
def get_model2dprots_by_experiment_ids(experiment_ids):
    if not experiment_ids:
        raise ValueError("experiment_ids list is empty!")

    with psycopg2.connect(**DB_CFG) as conn:
        query = """
            SELECT *
            FROM model_2d_prots
            WHERE CAST(experiment_id AS INTEGER) = ANY(%s);
        """
        df = pd.read_sql(query, conn, params=(experiment_ids,))

    df = _normalize_ids_int(df, "experiment_id")
    return df


def fetch_model2dprots_with_meta_from_cell_df(cell_df):
    exp_ids = cell_df["experiment_id"].dropna().astype(int).unique().tolist()

    df_db = get_model2dprots_by_experiment_ids(exp_ids)
    df_db["mean_nucli"] = pd.to_numeric(df_db["mean_nucli"], errors="coerce")
    df_db = df_db.dropna(subset=["mean_nucli"])

    meta = (
        cell_df[["experiment_id", "condition_str", "treatment_group"]]
        .drop_duplicates(subset=["experiment_id"])
        .copy()
    )

    df_merged = pd.merge(df_db, meta, on="experiment_id", how="inner")
    return df_merged


COLORS = {"control": "black", "treated": "#1f77b4"}


def _clean_condition(val):
    if pd.isna(val):
        return np.nan

    s = str(val)
    parts = [p.strip() for p in s.split("|")]
    cleaned = []

    for p in parts:
        low = p.lower()
        if (not p) or ("null" in low) or (low in ("none", "nan", "na")):
            continue
        cleaned.append(p)

    if not cleaned:
        return np.nan

    return " | ".join(cleaned)


def _b64_to_rgb_image(img_b64):
    return Image.open(io.BytesIO(base64.b64decode(img_b64))).convert("RGB")


def concat_base64_images_vertical(img1_b64, img2_b64, gap=50):
    img1 = _b64_to_rgb_image(img1_b64)
    img2 = _b64_to_rgb_image(img2_b64)

    width = max(img1.width, img2.width)
    height = img1.height + img2.height + gap

    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(img1, ((width - img1.width) // 2, 0))
    canvas.paste(img2, ((width - img2.width) // 2, img1.height + gap))

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=92, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def plot_positive_protein_expression(df: pd.DataFrame, threshold=None):
    """
    Uses model_2d_prots.mean_nucli.
    Positive/negative cells are separated by 1D KMeans clustering.
    Higher mean_nucli cluster = positive cells.
    """

    need = {"mean_nucli", "treatment_group", "experiment_id", "condition_str"}
    miss = need - set(df.columns)
    if miss:
        raise ValueError(f"Missing columns for protein plot: {sorted(miss)}")

    d = df.copy()
    d["value"] = pd.to_numeric(d["mean_nucli"], errors="coerce")
    d = d.dropna(subset=["value", "condition_str"]).reset_index(drop=True)

    if d.empty:
        raise ValueError("No valid mean_nucli values found in model_2d_prots.")

    d["label_internal"] = d["condition_str"] + " | " + d["experiment_id"].astype(str)

    # -----------------------------
    # KMeans logic for positive/negative
    # -----------------------------
    values = d["value"].to_numpy(dtype=float)

    if threshold is None:
        if len(values) < 2 or np.nanstd(values) == 0:
            threshold = float(np.nanmean(values))
            d["positive"] = d["value"] >= threshold
        else:
            # simple 1D kmeans k=2
            c1, c2 = np.percentile(values, [25, 75])

            for _ in range(100):
                dist1 = np.abs(values - c1)
                dist2 = np.abs(values - c2)

                labels = (dist2 < dist1).astype(int)

                new_c1 = values[labels == 0].mean() if np.any(labels == 0) else c1
                new_c2 = values[labels == 1].mean() if np.any(labels == 1) else c2

                if np.allclose([c1, c2], [new_c1, new_c2]):
                    break

                c1, c2 = new_c1, new_c2

            centers = np.array([c1, c2])
            positive_cluster = np.argmax(centers)

            d["positive"] = labels == positive_cluster
            threshold = float(np.mean(centers))
    else:
        threshold = float(threshold)
        d["positive"] = d["value"] >= threshold

    # -----------------------------
    # Positive % per image
    # -----------------------------
    per_img = d.groupby(["label_internal", "file_name"], as_index=False).agg(
        positive_percent=("positive", lambda x: 100.0 * x.sum() / len(x)),
        total_cells=("positive", "size"),
        group=("treatment_group", "first"),
        condition=("condition_str", "first"),
    )

    # -----------------------------
    # Summary across images
    # -----------------------------
    g = per_img.groupby("label_internal", as_index=False).agg(
        mean=("positive_percent", "mean"),
        sem=("positive_percent", lambda x: x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0),
        N=("positive_percent", "size"),
        group=("group", "first"),
        condition=("condition", "first"),
    )

    g["not_control"] = g["group"].str.lower() != "control"
    g = g.sort_values(["not_control", "condition", "label_internal"]).reset_index(drop=True)

    labels_internal = g["label_internal"].tolist()
    labels_display = g["condition"].tolist()
    means = g["mean"].to_numpy()
    sems = g["sem"].to_numpy()
    Ns = g["N"].to_numpy()
    groups = g["group"].str.lower().to_numpy()

    colors = [COLORS["control"] if gr == "control" else COLORS["treated"] for gr in groups]

    fig_w = max(12, 0.7 * len(labels_internal) + 4)
    fig, ax = plt.subplots(figsize=(fig_w, 6))

    x = np.arange(len(labels_internal))
    ax.bar(x, means, yerr=sems, capsize=4, linewidth=1.2, color=colors, edgecolor="black")

    ymax = max(
        8,
        float(max(per_img["positive_percent"].max(), (means + sems).max())) * 1.20
    ) if len(means) else 8

    for xi, (m, s, n) in enumerate(zip(means, sems, Ns)):
        ax.text(
            xi,
            m + s + (0.03 * ymax),
            f"{m:.1f}%\n(n={int(n)})",
            ha="center",
            va="bottom",
            fontsize=9,
            color="black"
        )

    for xi, lab in enumerate(labels_internal):
        vals = per_img.loc[
            per_img["label_internal"] == lab,
            "positive_percent"
        ].to_numpy()

        if len(vals):
            x_jitter = np.random.uniform(xi - 0.10, xi + 0.10, size=len(vals))
            y_jitter = vals + np.random.normal(0, 0.05, size=len(vals))
            y_jitter = np.clip(y_jitter, 0, None)

            ax.scatter(
                x_jitter,
                y_jitter,
                s=35,
                facecolors="none",
                edgecolors="lightcoral",
                alpha=0.7,
                linewidths=1.5,
                zorder=10
            )

    ax.set_ylim(-0.3, ymax)
    ax.set_ylabel("Positive Cells per Image (%)", fontsize=13)
    ax.set_title(
        f"Percentage of Marker-Positive Cells\nThreshold = {threshold:.2f}",
        fontsize=18,
        pad=12
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels_display, rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="jpg", dpi=220, pil_kwargs={"quality": 90, "optimize": True})
    plt.close(fig)

    img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return img_b64, threshold

def plot_per_experiment_improved(df: pd.DataFrame):
    need = {"cell_count", "treatment_group", "experiment_id"}
    miss = need - set(df.columns)
    if miss:
        raise ValueError(f"Missing columns: {sorted(miss)}")

    d = df.copy()
    d["count"] = pd.to_numeric(d["cell_count"], errors="coerce")
    d = d.dropna(subset=["count"]).reset_index(drop=True)

    if "condition" in d.columns:
        d["condition_str"] = d["condition"].map(_clean_condition)
    else:
        if "drug_info" not in d.columns:
            raise ValueError("Provide 'condition' or 'drug_info'.")
        d["condition_str"] = d["drug_info"].map(_clean_condition)

    d = d.dropna(subset=["condition_str"]).reset_index(drop=True)
    d["label_internal"] = d["condition_str"] + " | " + d["experiment_id"].astype(str)

    grp = d["treatment_group"].astype(str).str.strip().str.lower()
    ctrl_mask = grp.eq("control")
    normalized = False

    if ctrl_mask.any():
        baseline = d.loc[ctrl_mask, "count"].mean()
        if np.isfinite(baseline) and baseline > 0:
            d["norm"] = d["count"] / baseline
            normalized = True
        else:
            d["norm"] = d["count"]
    else:
        d["norm"] = d["count"]

    g = d.groupby("label_internal", as_index=False).agg(
        mean=("norm", "mean"),
        sem=("norm", lambda x: x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0),
        N=("norm", "size"),
        group=("treatment_group", "first"),
        condition=("condition_str", "first"),
    )

    g["not_control"] = g["group"].str.lower() != "control"
    g = g.sort_values(["not_control", "condition", "label_internal"]).reset_index(drop=True)

    labels_internal = g["label_internal"].tolist()
    labels_display = g["condition"].tolist()
    means = g["mean"].to_numpy()
    sems = g["sem"].to_numpy()
    Ns = g["N"].to_numpy()
    groups = g["group"].str.lower().to_numpy()

    colors = [COLORS["control"] if gr == "control" else COLORS["treated"] for gr in groups]

    fig_w = max(12, 0.7 * len(labels_internal) + 4)
    fig, ax = plt.subplots(figsize=(fig_w, 6))

    x = np.arange(len(labels_internal))
    ax.bar(x, means, yerr=sems, capsize=4, linewidth=1.2, color=colors, edgecolor="black")

    ymax_data = float((means + sems).max()) if len(means) else 1.0

    for xi, (m, s, n) in enumerate(zip(means, sems, Ns)):
        ax.text(
            xi,
            m + s * 1.02,
            f"{m:.2f}\n(n={int(n)})",
            ha="center",
            va="bottom",
            fontsize=9,
            color="black"
        )

    color_by_internal = dict(zip(labels_internal, colors))
    for xi, lab in enumerate(labels_internal):
        vals = d.loc[
            d["label_internal"] == lab,
            "norm"
        ].to_numpy()

        if len(vals):

            x_jitter = np.random.uniform(
                xi - 0.10,
                xi + 0.10,
                size=len(vals)
            )

            y_jitter = vals + np.random.normal(
                0,
                0.01,
                size=len(vals)
            )

            ax.scatter(
                x_jitter,
                y_jitter,
                s=30,
                facecolors="none",
                edgecolors="lightcoral",
                alpha=0.7,
                linewidths=1.2,
                zorder=10
            )

    def _format_p(p):
        return f"p={p:.3g}"

    comparisons = []
    ctrl_indices = [i for i, gname in enumerate(groups) if gname == "control"]

    if ctrl_indices:
        ci = ctrl_indices[0]
        lab_c = labels_internal[ci]
        vals_c = d.loc[d["label_internal"] == lab_c, "norm"].to_numpy()

        for oi in range(len(labels_internal)):
            if oi == ci or groups[oi] == "control":
                continue

            lab_o = labels_internal[oi]
            vals_o = d.loc[d["label_internal"] == lab_o, "norm"].to_numpy()

            if len(vals_c) >= 2 and len(vals_o) >= 2:
                stat, p = mannwhitneyu(vals_c, vals_o, alternative="two-sided")
                if np.isfinite(p):
                    comparisons.append((ci, oi, p))

    n_comp = len(comparisons)
    if n_comp == 0:
        top_for_brackets = ymax_data * 1.2
    else:
        base = ymax_data * 1.05
        step = ymax_data * 0.10
        top_for_brackets = base + step * (n_comp + 1)

        h = base
        for (ci, oi, p) in comparisons:
            x1, x2 = x[ci], x[oi]
            y_line = h
            y_line_top = h + ymax_data * 0.03

            ax.plot(
                [x1, x1, x2, x2],
                [y_line, y_line_top, y_line_top, y_line],
                color="black",
                linewidth=1.1
            )

            ax.text(
                (x1 + x2) / 2.0,
                y_line_top + ymax_data * 0.01,
                _format_p(p),
                ha="center",
                va="bottom",
                fontsize=10
            )

            h += step

    ax.set_ylim(0, max(top_for_brackets, ymax_data * 1.2))

    if normalized:
        ax.axhline(1.0, color="#888", linestyle="--", linewidth=1, label="Control = 1.0")
        ax.set_ylabel("Normalized Cell Count", fontsize=13)
    else:
        ax.set_ylabel("Cell Count", fontsize=13)

    ax.set_title("Mean Cell Count", fontsize=18, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels_display, rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(frameon=False, loc="upper right")

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="jpg", dpi=220, pil_kwargs={"quality": 90, "optimize": True})
    plt.close(fig)

    img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    # Add second plot below without changing socket/front-end
    try:
        protein_df = fetch_model2dprots_with_meta_from_cell_df(d)
        protein_img_b64, _threshold = plot_positive_protein_expression(protein_df)
        img_b64 = concat_base64_images_vertical(img_b64, protein_img_b64)
    except Exception as ex:
        print(f"[Protein plot skipped] {ex}")

    return img_b64, normalized
