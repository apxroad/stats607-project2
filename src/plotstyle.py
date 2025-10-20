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
