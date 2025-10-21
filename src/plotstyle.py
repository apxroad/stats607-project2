def use_nice_style():
    """Apply a clean, consistent Matplotlib theme (visual only)."""
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "font.size": 12,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "axes.titleweight": "semibold",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "-",
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "lines.linewidth": 2.0,
        "lines.markersize": 6.5,
        "legend.frameon": False,
    })

# --- central plotting style helper ---
def apply_plot_style(rc_overrides: dict | None = None):
    import matplotlib as mpl
    import matplotlib.pyplot as plt  # noqa: F401
    rc = {
        "pdf.fonttype": 42,              # embed TrueType; text stays selectable
        "ps.fonttype": 42,
        "savefig.bbox": "tight",         # trim whitespace

        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.linewidth": 0.8,
        "grid.alpha": 0.25,
        "axes.titlesize": "large",
        "axes.labelsize": "medium",
        "legend.frameon": False,
        "xtick.labelsize": "small",
        "ytick.labelsize": "small",
    }
    if rc_overrides:
        rc.update(rc_overrides)
    mpl.rcParams.update(rc)
