"""Regenerate the article figures from the pipeline outputs.

Reads only the CSVs written by github-metrics-analyzer (one folder pair per
corpus) and writes vector PDFs (plus 300-dpi PNG previews) to ../figures/.

    python Artigo_TCC/Real/scripts/make_figures.py

Corpus folders (see github-metrics-analyzer/scripts/run_all_corpus.py):
  NSA    -> data_nsa/,   reports_nsa/
  OSS    -> data/,       reports/        (Corpus 2, clean re-run)
  GOV.BR -> data_govbr/, reports_govbr/

Colour roles follow the validated categorical order (blue, orange, aqua);
marker shape is a second identity channel for grayscale printing.
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                       # E:/AP2-Projeto-ES
GMA = ROOT / "github-metrics-analyzer"
OUT = HERE.parent / "figures"
OUT.mkdir(exist_ok=True)

CORPORA = [  # label, data dir, reports dir, colour, marker
    ("NSA", "data_nsa", "reports_nsa", "#2a78d6", "o"),
    ("OSS", "data", "reports", "#eb6834", "s"),
    ("GOV.BR", "data_govbr", "reports_govbr", "#1baf7a", "^"),
]
MODELS = ["LogisticRegression", "DecisionTree", "RandomForest", "XGBoost", "LightGBM"]
MODEL_LABEL = {"LogisticRegression": "Logistic Regression", "DecisionTree": "Decision Tree",
               "RandomForest": "Random Forest", "XGBoost": "XGBoost", "LightGBM": "LightGBM"}

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#ffffff"
GOV = "#1baf7a"
FULL_W = 6.22   # \textwidth of the SciTePress template, inches

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.6, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.major.width": 0.6,
    "ytick.major.width": 0, "xtick.major.size": 2.5, "text.color": INK,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300,
})


def style(ax, xgrid=True, ygrid=False):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(False)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, linewidth=0.5)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", pad_inches=0.02, dpi=300)
    plt.close(fig)
    print("wrote", OUT / f"{name}.pdf")


SHORT = {"datawave-authorization-service": "datawave-authz",
         "datawave-audit-service": "datawave-audit",
         "datawave-query-service": "datawave-query",
         "httpcomponents-client": "httpcomponents",
         "eta-backend-services": "eta-backend"}


# ------------------------------------------------------------------ #
# Figure 2 - Semgrep findings per Java KLOC, all files vs .java only
# ------------------------------------------------------------------ #
def fig_density():
    fig, axes = plt.subplots(1, 3, figsize=(FULL_W, 2.05), sharex=True)
    for ax, (label, dd, _, colour, _m) in zip(axes, CORPORA):
        loc = pd.read_csv(GMA / dd / "loc.csv")
        sem = pd.read_csv(GMA / dd / "semgrep_findings.csv")
        is_java = sem.file.astype(str).str.lower().str.endswith(".java")
        rows = []
        for repo, kloc in zip(loc.repository, loc.java_code / 1000):
            s = sem.repository == repo
            rows.append((repo.split("/")[1], s.sum() / kloc, (s & is_java).sum() / kloc))
        d = pd.DataFrame(rows, columns=["repo", "all", "java"]).sort_values("all")
        y = np.arange(len(d))
        ax.hlines(y, d.java, d["all"], color=AXIS, linewidth=1.2, zorder=1)
        ax.scatter(d.java, y, s=16, facecolor=SURFACE, edgecolor=colour, linewidth=1.0, zorder=3)
        ax.scatter(d["all"], y, s=18, color=colour, edgecolor=SURFACE, linewidth=0.6, zorder=4)
        ax.set_yticks(y)
        ax.set_yticklabels([SHORT.get(r, r) for r in d.repo])
        total_kloc = loc.java_code.sum() / 1000
        ax.set_title(f"{label}  ({total_kloc:,.0f} Java KLOC)", loc="left", color=INK, pad=3)
        ax.set_xlim(-0.15, 6.6)
        ax.set_xticks([0, 2, 4, 6])
        style(ax)
        top = d.iloc[-1]
        if top["all"] > 4:   # the vendored-code outlier (siga): note it in the empty area
            ax.text(6.5, 1.5, f"{top.repo}: {top['all']:.2f} for all files,\n"
                                f"{top['java']:.2f} for .java files only",
                    ha="right", va="center", fontsize=6.3, color=INK2, linespacing=1.25)
    axes[1].set_xlabel("Semgrep findings per Java KLOC")
    handles = [Line2D([], [], marker="o", linestyle="none", markersize=4.6, markerfacecolor=INK2,
                      markeredgecolor=SURFACE, label="all scanned files"),
               Line2D([], [], marker="o", linestyle="none", markersize=4.2, markerfacecolor=SURFACE,
                      markeredgecolor=INK2, markeredgewidth=1.0, label=".java files only")]
    axes[0].legend(handles=handles, loc="lower right", frameon=False, handletextpad=0.3,
                   borderaxespad=0.2)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig_density")


# ------------------------------------------------------------------ #
# Figure 3 - performance across corpora + GOV.BR fold-level view
# ------------------------------------------------------------------ #
def gov_folds():
    conf = pd.read_csv(GMA / "reports_govbr" / "ml_confusions.csv")
    conf["fold"] = conf.groupby("model").cumcount() + 1
    return conf


def fig_performance():
    res = {lab: pd.read_csv(GMA / rd / "ml_results.csv").set_index("model")
           for lab, _, rd, _, _ in CORPORA}
    conf = gov_folds()
    dspace = conf.fold.isin([1, 3])          # evidencia / deposita tested alone
    excl = conf[~dspace].groupby("model").roc_auc.mean()

    fig = plt.figure(figsize=(FULL_W, 2.15))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.55, 1, 1], wspace=0.38)

    # (a) ROC-AUC by model and corpus
    ax = fig.add_subplot(gs[0])
    y = np.arange(len(MODELS))[::-1]
    for yi, m in zip(y, MODELS):
        vals = [res[lab].loc[m, "roc_auc"] for lab, *_ in CORPORA] + [excl[m]]
        ax.hlines(yi, min(vals), max(vals), color=AXIS, linewidth=1.2, zorder=1)
        for (lab, _, _, colour, mk), v in zip(CORPORA, vals[:3]):
            ax.scatter(v, yi, marker=mk, s=22, color=colour, edgecolor=SURFACE, linewidth=0.6, zorder=3)
        ax.scatter(excl[m], yi, marker="^", s=20, facecolor=SURFACE, edgecolor=GOV,
                   linewidth=1.1, zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels([MODEL_LABEL[m] for m in MODELS])
    ax.set_xlim(0.70, 1.0)
    ax.set_xticks([0.70, 0.80, 0.90, 1.00])
    ax.set_xlabel("ROC-AUC (axis starts at 0.70)")
    ax.set_title("(a) Mean ROC-AUC per corpus", loc="left", color=INK, pad=3)
    style(ax)
    handles = [Line2D([], [], marker=mk, linestyle="none", markersize=4.6, markerfacecolor=c,
                      markeredgecolor=SURFACE, label=lab) for lab, _, _, c, mk in CORPORA]
    handles.append(Line2D([], [], marker="^", linestyle="none", markersize=4.4,
                          markerfacecolor=SURFACE, markeredgecolor=GOV, markeredgewidth=1.1,
                          label="GOV.BR without folds 1, 3"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.55, -0.27), ncol=4,
              frameon=False, handletextpad=0.2, columnspacing=0.7)

    # (b), (c) GOV.BR per fold, one dot per classifier (folds defined in the caption)
    fold_lab = ["1", "2", "3", "4", "5"]
    offsets = np.linspace(-0.22, 0.22, len(MODELS))
    for k, (metric, title, ylim) in enumerate([("roc_auc", "(b) ROC-AUC per fold", (0.55, 1.02)),
                                               ("precision", "(c) Precision per fold", (0, 1.0))]):
        ax = fig.add_subplot(gs[k + 1])
        for f in range(1, 6):
            leak = f in (1, 3)
            if leak:
                ax.axvspan(f - 0.42, f + 0.42, color=GOV, alpha=0.10, linewidth=0, zorder=0)
            for off, m in zip(offsets, MODELS):
                v = conf[(conf.model == m) & (conf.fold == f)][metric].iloc[0]
                ax.scatter(f + off, v, s=14, color=GOV if leak else MUTED,
                           edgecolor=SURFACE, linewidth=0.5, zorder=3)
        ax.set_xticks(range(1, 6))
        ax.set_xticklabels(fold_lab)
        ax.set_xlabel("GOV.BR test fold")
        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(*ylim)
        ax.tick_params(axis="y", length=0)
        ax.set_title(title, loc="left", color=INK, pad=3)
        style(ax, xgrid=False, ygrid=True)
    handles = [Line2D([], [], marker="o", linestyle="none", markersize=4.2, markerfacecolor=GOV,
                      markeredgecolor=SURFACE, label="DSpace twin in training (folds 1, 3)"),
               Line2D([], [], marker="o", linestyle="none", markersize=4.2, markerfacecolor=MUTED,
                      markeredgecolor=SURFACE, label="other folds")]
    ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(1.02, -0.27), ncol=2,
              frameon=False, handletextpad=0.2, columnspacing=0.7)
    save(fig, "fig_performance")


# ------------------------------------------------------------------ #
# Figure 1 - the build-free pipeline (neutral fills: no corpus colours)
# ------------------------------------------------------------------ #
def fig_pipeline():
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=(FULL_W, 2.3))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 37.8)
    ax.axis("off")

    def box(x, y, w, h, text, size=6.2):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                    facecolor=SURFACE, edgecolor=AXIS, linewidth=0.7))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
                color=INK, linespacing=1.3)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.7,
                                    shrinkA=0, shrinkB=0, mutation_scale=7))

    # collector groups: header 1.6 + boxes of 3.0 with 0.4 gaps + 0.8 padding
    gx, gw, bh = 29.0, 31.0, 3.0
    groups = [  # (bottom y, height, title, fill, tool texts)
        (24.5, 13.0, "features (ISO/IEC 25010: maintainability)", "#f3f3f1",
         ["SonarQube 26.6: 20 structural", "CK 0.7.0: 14 object-oriented", "PyDriller 2.9: 7 process"]),
        (14.1, 9.6, "label (ISO/IEC 25010: security)", "#e9e8e3",
         ["Semgrep 1.165 (auto rules)", "CodeQL 2.25.6 (security-extended)"]),
        (0.3, 13.0, "descriptive only", "#f3f3f1",
         ["OSV API: vulnerable dependencies", "secrets: Gitleaks + detect-secrets", "cloc: Java KLOC"]),
    ]
    mids = []
    for gy, gh, title, fill, texts in groups:
        ax.add_patch(FancyBboxPatch((gx, gy), gw, gh, boxstyle="round,pad=0,rounding_size=1.0",
                                    facecolor=fill, edgecolor="none"))
        top = gy + gh
        ax.text(gx + 1.0, top - 0.7, title, ha="left", va="top", fontsize=6.0,
                color=INK2, style="italic")
        for i, txt in enumerate(texts):
            box(gx + 1.5, top - 2.4 - bh - i * (bh + 0.4), gw - 3.0, bh, txt, size=6.1)
        mids.append(gy + gh / 2)

    # inputs, centred on the label group
    yc = mids[1]
    box(0.5, yc - 5.5, 11.5, 11.0, "30 Java\nrepositories\n3 corpora × 10\nNSA, OSS,\nGOV.BR")
    box(15.0, yc - 5.5, 10.5, 11.0, "git clone\nfull history\nno build,\nno execution")
    arrow(12.0, yc, 15.0, yc)
    for ym in mids:
        arrow(25.5, yc, gx, ym)

    # dataset builder, posture report, ML
    box(64.0, 19.0, 16.0, 14.0, "dataset builder\none row per file\nlabel: any Semgrep\n"
                                "or CodeQL finding\n41 features; tool\ncounts excluded")
    box(64.0, 2.0, 16.0, 13.0, "posture report\nfindings per KLOC\nCWE to ISO/IEC\n25010 mapping\nSCA and secrets")
    box(84.0, 18.5, 15.5, 15.0, "machine learning\nGroupKFold (5)\nby repository\nSMOTE on training\n"
                                "folds only\nLR, DT, RF,\nXGBoost, LightGBM")
    arrow(gx + gw, mids[0], 64.0, 29.5)    # features -> dataset
    arrow(gx + gw, 20.0, 64.0, 22.5)       # label -> dataset
    arrow(gx + gw, 16.5, 64.0, 12.0)       # label -> report (CWE profile)
    arrow(gx + gw, mids[2], 64.0, 7.5)     # descriptive -> report
    arrow(80.0, 26.0, 84.0, 26.0)          # dataset -> ML
    save(fig, "fig_pipeline")


if __name__ == "__main__":
    os.chdir(ROOT)
    fig_pipeline()
    fig_density()
    fig_performance()
    # numbers quoted in the text / Table 5
    conf = gov_folds()
    conf["group"] = np.where(conf.fold.isin([1, 3]), "dspace", "others")
    print(conf.groupby(["model", "group"])[["roc_auc", "precision"]].mean().round(3).unstack())
