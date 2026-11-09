"""Regenerate the article figures from the pipeline outputs.

Reads only the CSVs written by github-metrics-analyzer (one folder pair per
corpus) and writes only the article's vector PDFs to ../figures/.

    python Artigo_TCC/Real/scripts/make_figures.py

Corpus folders (see github-metrics-analyzer/scripts/run_all_corpus.py):
  NSA    -> data_nsa/,   reports_nsa/
  OSS    -> data/,       reports/        (Corpus 2, clean re-run)
  GOV.BR -> data_govbr/, reports_govbr/

Colour roles follow the presentation's categorical order (blue, ochre, magenta);
Stack position and hatching distinguish Java and non-Java findings in print.
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
    ("NSA", "data_nsa", "reports_nsa", "#4F7CB8", "o"),
    ("OSS", "data", "reports", "#B26B1F", "s"),
    ("GOV.BR", "data_govbr", "reports_govbr", "#A8467A", "^"),
]
MODELS = ["LogisticRegression", "DecisionTree", "RandomForest", "XGBoost", "LightGBM"]
MODEL_LABEL = {"LogisticRegression": "Logistic Regression", "DecisionTree": "Decision Tree",
               "RandomForest": "Random Forest", "XGBoost": "XGBoost", "LightGBM": "LightGBM"}

INK, INK2, MUTED = "#111820", "#3A4552", "#6C7886"
GRID, AXIS, SURFACE = "#E5EAF0", "#D3DAE2", "#ffffff"
GOV = "#A8467A"
FULL_W = 6.22   # \textwidth of the SciTePress template, inches

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
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
    from matplotlib.text import Text
    for label in fig.findobj(match=Text):
        label.set_fontfamily("Times New Roman")
        label.set_fontsize(9)
        label.set_fontweight("normal")
    fig.savefig(OUT / f"{name}.pdf")
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
    from matplotlib.patches import Patch
    from matplotlib.colors import to_rgb

    for label, dd, _, colour, _m in CORPORA:
        fig, ax = plt.subplots(figsize=(FULL_W, 2.8))
        fig.subplots_adjust(left=0.30, right=0.76, top=0.76, bottom=0.19)
        handles = [Patch(facecolor=INK2, label="Java files"),
                   Patch(facecolor="#EDF0F3", edgecolor=MUTED, hatch="////",
                         linewidth=0.3, label="Other files (web, configuration, etc.)")]
        fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0, 0.99),
                   ncol=2, frameon=False, handlelength=1.6, columnspacing=1.5)
        loc = pd.read_csv(GMA / dd / "loc.csv")
        sem = pd.read_csv(GMA / dd / "semgrep_findings.csv")
        is_java = sem.file.astype(str).str.lower().str.endswith(".java")
        rows = []
        for repo, kloc in zip(loc.repository, loc.java_code / 1000):
            s = sem.repository == repo
            rows.append((repo.split("/")[1], s.sum() / kloc, (s & is_java).sum() / kloc))
        d = pd.DataFrame(rows, columns=["repo", "all", "java"]).sort_values("all")
        y = np.arange(len(d))
        pale = tuple(0.85 + 0.15*c for c in to_rgb(colour))
        for yi in y[::2]:
            ax.axhspan(yi-0.48, yi+0.48, color="#F5F7F9", zorder=0)
        ax.barh(y, d.java, height=0.61, color=colour, zorder=3)
        ax.barh(y, d["all"]-d.java, left=d.java, height=0.61,
                color=pale, edgecolor=colour, hatch="////", linewidth=0.25, zorder=3)
        ax.set_yticks(y)
        ax.set_yticklabels(d.repo, fontsize=7)
        total_kloc = loc.java_code.sum() / 1000
        ax.set_title(f"{label}  |  {total_kloc:,.0f} Java KLOC", loc="left", color=colour, pad=8, fontsize=8.5, weight="normal")
        ax.set_xlim(0, 6.5)
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.tick_params(axis="x", labelbottom=True)
        ax.set_ylim(-0.65, len(d)-0.35)
        ax.text(1.12, 1.05, "Total", ha="center", transform=ax.transAxes, fontsize=7, color=INK2, weight="normal")
        ax.text(1.34, 1.05, "Java", ha="center", transform=ax.transAxes, fontsize=7, color=INK2, weight="normal")
        for yi, row in enumerate(d.itertuples()):
            ax.text(1.12, yi, f"{row.all:.2f}", transform=ax.get_yaxis_transform(), ha="center", va="center", fontsize=7, fontfamily="Times New Roman")
            ax.text(1.34, yi, f"{row.java:.2f}", transform=ax.get_yaxis_transform(), ha="center", va="center", fontsize=7, fontfamily="Times New Roman")
        style(ax)
        ax.set_xlabel("Findings per 1,000 lines of Java code", fontsize=8, labelpad=6)
        save(fig, "fig_density_" + label.lower().replace(".", ""))


# ------------------------------------------------------------------ #
# Figure 1 - the build-free pipeline (neutral fills: no corpus colours)
# ------------------------------------------------------------------ #
def fig_pipeline():
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=(FULL_W, 4.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 89)
    ax.axis("off")
    def card(x, y, w, h, title, body, fill="#F5F7F9"):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0,rounding_size=1.2",
                     facecolor=fill, edgecolor=AXIS, linewidth=0.7))
        ax.text(x+2, y+h-2.3, title, fontsize=8, weight="normal", va="top", color=INK)
        ax.text(x+2, y+h-7.5, body, fontsize=7.3, va="top", color=INK2, linespacing=1.25)

    def arrow(points, dashed=False):
        xs, ys = zip(*points)
        ax.plot(xs[:-1], ys[:-1], color=MUTED, lw=0.9,
                linestyle="--" if dashed else "-", zorder=0)
        ax.annotate("", xy=points[-1], xytext=points[-2],
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                    linestyle="--" if dashed else "-",
                                    shrinkA=0, shrinkB=0, mutation_scale=8), zorder=0)

    card(1, 75, 98, 12, "1  Collect source code and full Git history",
         "30 Java repositories: 10 NSA + 10 OSS + 10 GOV.BR", fill="#EDF0F3")
    ax.text(1, 70.5, "2  Extract three kinds of evidence", fontsize=8.5, weight="normal")
    card(1, 44, 31, 23, "Quality metrics",
         "SonarQube: 20 structural\nCK: 14 object-oriented\nPyDriller: 7 process\n41 features in total")
    card(35, 44, 30, 23, "Security label",
         "Semgrep + CodeQL\nPositive file = at least\none finding from\neither SAST tool")
    card(68, 44, 31, 23, "Additional context",
         "OSV: dependencies\nGitleaks + detect-secrets\ncloc: Java code size\nDescriptive evidence only")
    for x in (16.5, 50, 83.5):
        arrow([(x, 69), (x, 68), (x, 67)])

    card(1, 22, 64, 15, "3  Build the prediction dataset",
         "One row per file = 41 quality features + security label\nSAST finding counts are excluded from the features.", fill="#EDF0F3")
    card(68, 18, 31, 19, "Describe security posture",
         "Findings per Java KLOC\nCWE to ISO/IEC 25010\nDependencies and secrets")
    arrow([(16.5, 44), (16.5, 40), (16.5, 37)])
    arrow([(46, 44), (46, 40), (46, 37)])
    arrow([(56, 44), (56, 40), (75, 40), (75, 37)])
    arrow([(88, 44), (88, 40), (88, 37)])

    card(1, 1, 64, 16, "4  Train and evaluate five classifiers",
         "5 folds grouped by repository; SMOTE on training folds only\nLogistic regression, decision tree, random forest,\nXGBoost and LightGBM", fill="#EDF0F3")
    arrow([(33, 22), (33, 19.5), (33, 17)])
    ax.text(69, 10, "Context informs the report;\nit does not enter the models.",
            fontsize=7.2, color=INK2, va="top", linespacing=1.4)
    save(fig, "fig_pipeline")


if __name__ == "__main__":
    os.chdir(ROOT)
    fig_pipeline()
    fig_density()
