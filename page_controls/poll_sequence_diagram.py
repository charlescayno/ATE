"""Render Steady-State Poll 2 Port sequence timing diagram for Add Test flow dialog."""
from __future__ import annotations

import io
import textwrap
from typing import Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# Fixed relative widths (not wall-clock seconds) — generic teaching diagram.
_W_T_INT = 4.2
_W_READ = 0.95
_W_SCOPE = 1.25
_W_WAIT = 1.15
_MAX_SAMPLES_DRAWN = 5
_ROW_H = 0.38
_ROW_GAP = 0.55


def _short_dual_load_mode(text: str) -> str:
    s = (text or "").strip()
    if not s:
        return ""
    if "Option A" in s:
        return "Option A: Proportional sync"
    if "Option B" in s:
        return "Option B: Cross-reg matrix"
    if "Option C" in s:
        return "Option C: Fixed aux / swept main (P2 fixed load)"
    return s if len(s) <= 56 else s[:53] + "…"


def _short_prompts(text: str) -> str:
    s = (text or "").strip()
    if not s:
        return ""
    if "Fully Automated" in s:
        return "Prompts: fully automated"
    if len(s) > 40:
        return "Prompts: " + s[:37] + "…"
    return f"Prompts: {s}"


def render_poll_sequence_diagram_png(
    *,
    n_samples: int,
    poll_wait_s: float = 0.0,
    integration_s: float = 0.0,
    dual_load_mode: str = "",
    user_prompts: str = "",
    scope_capture_s: float = 12.0,
    read_overhead_s: float = 2.0,
) -> bytes:
    """Return PNG bytes for one load point (generic timing, N from form)."""
    del poll_wait_s, integration_s, scope_capture_s, read_overhead_s

    n_total = max(1, int(n_samples))
    n_draw = min(n_total, _MAX_SAMPLES_DRAWN)

    sample_span = _W_T_INT + _W_READ + _W_SCOPE
    t_end = n_draw * sample_span + max(0, n_draw - 1) * _W_WAIT
    t_right = t_end + (2.8 if n_total > n_draw else 1.2)

    y_dc = 3 * _ROW_GAP + 2 * _ROW_H
    y_sc = 2 * _ROW_GAP + 1.5 * _ROW_H
    y_sw = 1 * _ROW_GAP + _ROW_H
    y_xl = 0.15
    label_x = -0.15

    fig_w = max(10.0, min(15.0, 3.0 + n_draw * 3.0))
    fig_h = 5.6
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=130)
    rect = [0.11, 0.20, 0.86, 0.52]
    ax = fig.add_axes(rect)
    ax.set_xlim(label_x, t_right)
    ax.set_ylim(-0.35, y_dc + _ROW_H + 0.45)
    ax.set_yticks([])
    ax.set_xlabel(
        "Time →  (not to scale; t = 0 at start of sample 1 T_int, after load soak)",
        fontsize=9,
        color="#444",
        labelpad=6,
    )

    row_labels = [
        (y_dc, "DC + eLoad"),
        (y_sc, "Scope"),
        (y_sw, "Pin / wait"),
        (y_xl, "Excel"),
    ]
    for yy, title in row_labels:
        ax.text(
            label_x,
            yy + _ROW_H / 2,
            title,
            ha="right",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="#222",
        )

    ax.barh(
        y_dc + (_ROW_H - 0.08) / 2,
        t_end,
        left=0,
        height=_ROW_H - 0.08,
        color="#C8E6C9",
        edgecolor="#2E7D32",
        linewidth=0.8,
    )
    ax.text(
        t_end / 2,
        y_dc + _ROW_H / 2,
        "Held at load point",
        ha="center",
        va="center",
        fontsize=9,
        color="#1B5E20",
        fontweight="bold",
        clip_on=True,
    )

    tcur = 0.0
    for sample in range(1, n_draw + 1):
        cy_sw = y_sw + _ROW_H / 2
        cy_sc = y_sc + _ROW_H / 2

        ax.barh(y_sw, _W_T_INT, height=_ROW_H, left=tcur, color="#4C78A8", edgecolor="white", linewidth=0.6)
        if sample == 1:
            ax.plot(
                [tcur, tcur],
                [y_sw, y_sw + _ROW_H],
                color="#E3F2FD",
                linewidth=2.0,
                linestyle=(0, (3, 2)),
                zorder=3,
            )
            ax.text(
                tcur + _W_T_INT / 2,
                cy_sw,
                "t = 0\nS1 · T_int",
                ha="center",
                va="center",
                fontsize=8,
                color="white",
                fontweight="bold",
                linespacing=1.05,
            )
        else:
            ax.text(
                tcur + _W_T_INT / 2,
                cy_sw,
                f"S{sample}\nT_int",
                ha="center",
                va="center",
                fontsize=8,
                color="white",
                fontweight="bold",
                linespacing=1.05,
            )
        tcur += _W_T_INT

        ax.barh(y_sw, _W_READ, height=_ROW_H, left=tcur, color="#7986CB", edgecolor="white", linewidth=0.6)
        ax.text(
            tcur + _W_READ / 2,
            cy_sw,
            "PM",
            ha="center",
            va="center",
            fontsize=8,
            color="white",
            fontweight="bold",
        )
        tcur += _W_READ

        ax.barh(y_sc, _W_SCOPE, height=_ROW_H, left=tcur, color="#F58518", edgecolor="#E65100", linewidth=0.8)
        ax.text(
            tcur + _W_SCOPE / 2,
            cy_sc,
            f"S{sample}\nPNG",
            ha="center",
            va="center",
            fontsize=8,
            color="white",
            fontweight="bold",
            linespacing=1.05,
        )
        tcur += _W_SCOPE

        xl_cy = y_xl + _ROW_H / 2
        ax.scatter(
            [tcur],
            [xl_cy],
            s=520,
            marker="s",
            c="#00695C",
            edgecolors="white",
            linewidths=0.8,
            zorder=5,
        )
        ax.text(
            tcur,
            xl_cy,
            f"Row\n{sample}",
            ha="center",
            va="center",
            fontsize=7.5,
            color="white",
            fontweight="bold",
            linespacing=1.0,
            zorder=6,
        )

        if sample < n_draw:
            ax.barh(y_sw, _W_WAIT, height=_ROW_H, left=tcur, color="#EECA3B", edgecolor="#F9A825", linewidth=0.6)
            ax.text(
                tcur + _W_WAIT / 2,
                cy_sw,
                "T_wait",
                ha="center",
                va="center",
                fontsize=8,
                color="#333",
                fontweight="bold",
            )
            tcur += _W_WAIT

    if n_total > n_draw:
        ax.text(
            t_end + 0.55,
            cy_sw,
            f"… repeat to N = {n_total}",
            ha="left",
            va="center",
            fontsize=9,
            color="#555",
            style="italic",
        )

    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="x", labelbottom=False)

    leg = [
        mpatches.Patch(fc="#4C78A8", label="T_int (soak integration)"),
        mpatches.Patch(fc="#7986CB", label="Meter read (PM)"),
        mpatches.Patch(fc="#F58518", label="Scope capture"),
        mpatches.Patch(fc="#EECA3B", label="T_wait (poll wait)"),
        mpatches.Patch(fc="#00695C", label="Excel row"),
    ]
    fig.legend(
        handles=leg,
        loc="lower center",
        ncol=3,
        fontsize=8.5,
        frameon=True,
        framealpha=0.95,
        edgecolor="#ccc",
        bbox_to_anchor=(0.5, 0.02),
        columnspacing=1.2,
        handlelength=1.4,
    )

    fig.suptitle(
        "Each sample: integrate Pin → meters → scope RUN SINGLE → Excel row",
        fontsize=11.5,
        fontweight="bold",
        y=0.96,
    )

    meta_lines = [
        "T_int = soak integration time   ·   T_wait = poll wait between samples   ·   "
        "N = samples per load point (Add Test)",
    ]
    mode = _short_dual_load_mode(dual_load_mode)
    if mode:
        meta_lines.insert(0, mode)
    prompts = _short_prompts(user_prompts)
    if prompts:
        meta_lines.append(prompts)

    wrapped = []
    for line in meta_lines:
        wrapped.append(textwrap.fill(line, width=88) if len(line) > 88 else line)
    meta = "\n".join(wrapped)
    fig.text(
        0.5,
        0.875,
        meta,
        ha="center",
        va="top",
        fontsize=8.5,
        color="#333",
        linespacing=1.35,
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white", pad_inches=0.35)
    plt.close(fig)
    return buf.getvalue()


def poll_sequence_diagram_pixmap(
    parent,
    *,
    n_samples: int,
    poll_wait_s: float = 0.0,
    integration_s: float = 0.0,
    dual_load_mode: str = "",
    user_prompts: str = "",
) -> Optional["QPixmap"]:
    from PySide2.QtGui import QPixmap

    png = render_poll_sequence_diagram_png(
        n_samples=n_samples,
        poll_wait_s=poll_wait_s,
        integration_s=integration_s,
        dual_load_mode=dual_load_mode,
        user_prompts=user_prompts,
    )
    pix = QPixmap()
    if not pix.loadFromData(png, "PNG"):
        return None
    return pix
