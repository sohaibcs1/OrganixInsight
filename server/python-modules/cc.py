import os
import json
from datetime import datetime
from typing import List, Tuple
import numpy as np
import pandas as pd
import psycopg2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# -----------------------------
# DB config
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
# Small utilities
# -----------------------------
def _normalize_rid(raw: str) -> str:
    s = (raw or "").strip()
    if s.lower().startswith("randomid"):
        s = s[len("randomid"):]
    return s

def _db_query(query: str, params: tuple = ()) -> List[tuple]:
    conn = psycopg2.connect(**DB_CFG)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()

def _ensure_dir(d: str) -> None:
    os.makedirs(d, exist_ok=True)

def _density_curve(x: np.ndarray, bins: int = 128) -> Tuple[np.ndarray, np.ndarray]:
    """Histogram-based smooth density (KDE-like) without SciPy."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < 2:
        return np.array([0.0, 1.0]), np.array([1.0, 1.0])
    y, edges = np.histogram(
        x,
        bins=min(bins, max(8, int(np.sqrt(x.size)))),
        density=True
    )
    grid = (edges[:-1] + edges[1:]) * 0.5
    if y.size >= 5:
        y = np.convolve(y, np.ones(5) / 5.0, mode="same")
    return grid, y

# -----------------------------
# Pure NumPy 1-D KMeans (k=2) + silhouette
# -----------------------------
def kmeans_1d(values: np.ndarray, k: int = 2, n_init: int = 10,
              max_iter: int = 100, rng=None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simple 1-D kmeans. Returns (labels, centers).
    """
    x = np.asarray(values, float).reshape(-1)
    assert k >= 1
    n = x.size
    if n == 0:
        return np.array([], dtype=int), np.array([])
    rng = np.random.default_rng(None if rng is None else rng)

    best_inertia = np.inf
    best_labels = None
    best_centers = None

    # kmeans++ init (1-D)
    def _init_centers():
        centers = np.empty(k, dtype=float)
        centers[0] = rng.choice(x)
        for j in range(1, k):
            d2 = np.min((x[:, None] - centers[:j][None, :]) ** 2, axis=1)
            probs = d2 / (d2.sum() + 1e-12)
            centers[j] = rng.choice(x, p=probs)
        return centers

    for _ in range(n_init):
        centers = _init_centers()
        for _ in range(max_iter):
            # assign
            d = np.abs(x[:, None] - centers[None, :])
            labels = np.argmin(d, axis=1)
            # update
            new_centers = np.array(
                [x[labels == j].mean() if np.any(labels == j) else centers[j]
                 for j in range(k)]
            )
            if np.allclose(new_centers, centers):
                centers = new_centers
                break
            centers = new_centers

        inertia = np.sum((x - centers[labels]) ** 2)
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels.copy()
            best_centers = centers.copy()

    return best_labels, best_centers

def silhouette_1d(values: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Silhouette for 1-D clustering.
    """
    x = np.asarray(values, float).reshape(-1)
    lab = np.asarray(labels, int).reshape(-1)
    n = x.size
    s = np.zeros(n, float)

    unique = np.unique(lab)
    if unique.size <= 1:
        return s

    xd = np.abs(x[:, None] - x[None, :])
    for i in range(n):
        ci = lab[i]
        same = (lab == ci)
        if np.sum(same) > 1:
            a = xd[i, same].sum() / (np.sum(same) - 1)
        else:
            a = 0.0
        b = np.inf
        for c in unique:
            if c == ci:
                continue
            mask = (lab == c)
            if np.any(mask):
                b = min(b, xd[i, mask].mean())
        if not np.isfinite(b):
            b = 0.0
        denom = max(a, b)
        s[i] = 0.0 if denom == 0 else (b - a) / denom
    return s

# -----------------------------
# Consensus helpers (no SciPy)
# -----------------------------
def consensus_matrix(label_runs: np.ndarray) -> np.ndarray:
    R, N = label_runs.shape
    M = np.zeros((N, N), float)
    for r in range(R):
        lr = label_runs[r]
        for c in np.unique(lr):
            idx = np.where(lr == c)[0]
            if idx.size > 1:
                M[np.ix_(idx, idx)] += 1.0
    M /= float(R)
    M = np.minimum(M, M.T)
    np.fill_diagonal(M, 1.0)
    return M

def order_by_cluster_and_value(values: np.ndarray, labels: np.ndarray) -> np.ndarray:
    x = np.asarray(values, float)
    lab = np.asarray(labels, int)
    groups = np.unique(lab)
    means = [(g, x[lab == g].mean()) for g in groups]
    groups_order = [g for g, _ in sorted(means, key=lambda t: t[1])]
    out = []
    for g in groups_order:
        idx = np.where(lab == g)[0]
        out.append(idx[np.argsort(x[idx])])
    return np.concatenate(out) if out else np.arange(x.size)

# -----------------------------
# Main API
# -----------------------------
def save_consensus_panel_from_db(
    *,
    rid: str,
    results_dir: str = "static/results",
    table: str = "model_2d_prots",
    reps: int = 3,
    sample_size: int = 1000,
    iterations: int = 100,
    k_clusters: int = 2,
) -> str:
    """
    Generate a visually improved consensus clustering panel from database values.

    Auto-selects the feature:
      1) Try mean_nucli
      2) If not enough numeric values, fall back to mean_dapi
    """
    rid_raw = (rid or "").strip()
    rid_norm = _normalize_rid(rid_raw)

    # fetch both columns so we can auto-select
    sql = f"SELECT mean_nucli, mean_dapi FROM {table} WHERE random_id IN (%s, %s)"
    rows = _db_query(sql, (rid_raw, rid_norm))

    _ensure_dir(results_dir)
    rid_safe = rid_norm.replace("/", "_").replace("\\", "_")
    out_name = f"consensus_{rid_safe}.jpg"
    out_path = os.path.abspath(os.path.join(results_dir, out_name))

    # ---- Handle missing rows ----
    if not rows:
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.text(
            0.5, 0.5,
            "No data found for this random_id",
            ha="center", va="center",
            fontsize=18, weight="bold"
        )
        ax.axis("off")
        fig.savefig(out_path, dpi=250, bbox_inches="tight", format="jpg")
        plt.close(fig)
        return os.path.basename(out_path)

    # ---- Separate nucli vs dapi ----
    df = pd.DataFrame(rows, columns=["mean_nucli", "mean_dapi"])
    vals_nucli = pd.to_numeric(df["mean_nucli"], errors="coerce").dropna().to_numpy()
    vals_dapi  = pd.to_numeric(df["mean_dapi"],  errors="coerce").dropna().to_numpy()

    min_points = 10

    if vals_nucli.size >= min_points:
        vals_all = vals_nucli
        feature_label = "mean_nucli (marker intensity)"
    elif vals_dapi.size >= min_points:
        vals_all = vals_dapi
        feature_label = "mean_dapi (DAPI intensity)"
    else:
        # neither has enough points → explain clearly
        msg = (
            "Not enough data for clustering\n"
            f"(need ≥ {min_points} cells with numeric mean_nucli or mean_dapi,\n"
            f" got {vals_nucli.size} nucli values and {vals_dapi.size} dapi values)"
        )
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.text(0.5, 0.5, msg, ha="center", va="center",
                fontsize=16, weight="bold", wrap=True)
        ax.axis("off")
        fig.savefig(out_path, dpi=250, bbox_inches="tight", format="jpg")
        plt.close(fig)
        return os.path.basename(out_path)

    # ---- Visual enhancements ----
    row_h, fig_w = 5.0, 20.0
    fig_h = max(1, reps) * row_h

    with plt.rc_context({
        "font.size": 14,
        "axes.titlesize": 18,
        "axes.labelsize": 16,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 13,
        "figure.titlesize": 22,
    }):
        fig, axes = plt.subplots(reps, 4, figsize=(fig_w, fig_h), constrained_layout=True)
        if reps == 1:
            axes = np.array([axes])
        rng_master = np.random.default_rng(12345)

        for r in range(reps):
            N = min(sample_size, vals_all.size)
            idx = rng_master.choice(vals_all.size, size=N, replace=False)
            sample = vals_all[idx]

            # bootstrap label runs
            label_runs = []
            for it in range(iterations):
                sub_idx = rng_master.choice(N, size=max(5, int(0.8 * N)), replace=False)
                xsub = sample[sub_idx]
                lab_sub, _ = kmeans_1d(xsub, k=k_clusters, n_init=5, rng=10_000 * r + it)
                full = np.full(N, -1, int)
                full[sub_idx] = lab_sub
                miss = full < 0
                if miss.any():
                    base = (full[~miss].max() + 1) if (~miss).any() else 0
                    full[miss] = base + np.arange(miss.sum())
                label_runs.append(full)
            label_runs = np.stack(label_runs, axis=0)
            M = consensus_matrix(label_runs)

            # final labels/order
            final_labels, _ = kmeans_1d(sample, k=k_clusters, n_init=10, rng=42 + r)
            order = order_by_cluster_and_value(sample, final_labels)
            M_ord = M[np.ix_(order, order)]
            x_ord = sample[order]
            lab_ord = final_labels[order]

            # silhouette
            sil = silhouette_1d(x_ord, lab_ord)

            # ---- Panels ----
            # 1) Density
            ax1 = axes[r, 0]
            gx, gy = _density_curve(vals_all)
            sx, sy = _density_curve(sample)
            ax1.plot(gx, gy, label="Population", lw=2.4)
            ax1.plot(sx, sy, label="Sample", lw=2.4)
            ax1.set_xlabel(feature_label)
            ax1.set_ylabel("Density")
            ax1.legend(frameon=False, loc="upper right")
            ax1.grid(True, alpha=0.25)

            # 2) Silhouette
            ax2 = axes[r, 1]
            y_base = 10
            for c in np.unique(lab_ord):
                vals = sil[lab_ord == c]
                vals.sort()
                y_upper = y_base + len(vals)
                ax2.fill_betweenx(np.arange(y_base, y_upper), 0, vals, alpha=0.8)
                y_base = y_upper + 10
            ax2.set_xlim(-1, 1)
            ax2.set_yticks([])
            ax2.set_title("Silhouette")
            ax2.grid(True, axis="x", alpha=0.25)

            # 3) Consensus CDF
            ax3 = axes[r, 2]
            sims = M.flatten()
            sims.sort()
            if sims.size:
                cdf = np.linspace(0, 1, sims.size)
                ax3.plot(sims, cdf, lw=2.6)
            ax3.set_xlim(0, 1)
            ax3.set_ylim(0, 1)
            ax3.set_title("Consensus CDF")
            ax3.set_xlabel("Similarity")
            ax3.set_ylabel("CDF")
            ax3.grid(True, alpha=0.25)

            # 4) Similarity matrix
            ax4 = axes[r, 3]
            th_lo = np.quantile(M_ord, 0.25)
            th_hi = np.quantile(M_ord, 0.75)
            show = np.zeros_like(M_ord)
            show[(M_ord > th_lo) & (M_ord < th_hi)] = 1
            show[M_ord >= th_hi] = 2
            cmap = ListedColormap(["#ff6b6b", "white", "#1dd1a1"])  # red-white-greenish
            ax4.imshow(show, cmap=cmap, aspect="auto")
            ax4.set_title("Similarity")
            ax4.set_xticks([])
            ax4.set_yticks([])

        fig.savefig(out_path, dpi=300, bbox_inches="tight", format="jpg")
        plt.close(fig)

    return os.path.basename(out_path)



# -----------------------------
# if __name__ == "__main__":
#     p = save_consensus_panel_from_db(
#         rid="OUdSMgSN",
#         results_dir="static/results",
#         reps=3,
#         sample_size=1000,
#         iterations=100,
#     )
#     print("Saved:", p)
