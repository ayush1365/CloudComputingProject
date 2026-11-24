import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 6.2)); ax.set_xlim(0, 110); ax.set_ylim(0, 67); ax.axis("off")
def box(x, y, w, h, text, fc="#eef3fb", ec="#33507a", fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")
def arrow(x1, y1, x2, y2, label="", style="-|>", ls="-", c="#333"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle=style, lw=1.4, ls=ls, color=c))
    if label: ax.text((x1+x2)/2, (y1+y2)/2 + 1.2, label, ha="center", fontsize=8, color=c)

box(2, 26, 14, 10, "User /\nBrowser / curl", "#fff4d6", "#a67c00", bold=True)
box(24, 26, 20, 10, "Nginx Gateway\n(localhost:8080)\nprimary + backup", "#e8f5e9", "#2e7d32", bold=True)
arrow(16, 31, 24, 31)
for name, y, port, col, ec in [("PRIVATE cluster (kind)  :8081", 34, 8081, "#eef3fb", "#33507a"),
                               ("PUBLIC cluster (simulated cloud)  :8082", 2, 8082, "#fdecea", "#b23a2e")]:
    ax.add_patch(FancyBboxPatch((56, y), 52, 26, boxstyle="round,pad=0.3,rounding_size=1.5", fc="white", ec=ec, lw=2))
    ax.text(82, y + 24, name, ha="center", fontsize=10, fontweight="bold", color=ec)
    box(58, y + 13, 14, 7, "Service: web\nNodePort 30080", col, ec, 8)
    box(76, y + 14.5, 14, 4.5, "web Pod 1", col, ec, 8); box(76, y + 8.5, 14, 4.5, "web Pod 2..6", col, ec, 8)
    box(93, y + 8.5, 13, 8, "Redis Pod\n+ Service", "#fff", ec, 8)
    box(58, y + 1.5, 22, 5.5, "HPA (2-6, 50% CPU)\n+ metrics-server", "#f3e5f5", "#6a1b9a", 8)
    arrow(72, y + 16.5, 76, y + 16.5); arrow(72, y + 15, 76, y + 11)
    arrow(90, y + 14, 93, y + 13)
arrow(44, 33, 56, 46, "", c="#2e7d32")
arrow(44, 29, 56, 16, "", ls="--", c="#b23a2e")
ax.text(55, 64.5, "Visitor Counter - Hybrid Cloud Architecture", ha="center", fontsize=13, fontweight="bold")
ax.text(50, 49, "primary route", fontsize=8.5, color="#2e7d32", ha="center", rotation=0)
ax.text(46, 10, "failover (backup) route", fontsize=8.5, color="#b23a2e", ha="center")
ax.text(26, 20, "Private cluster stopped?\nNginx automatically routes\nto the public cluster", fontsize=8.5, color="#b23a2e", ha="center")
plt.savefig("docs/architecture.png", dpi=170, bbox_inches="tight"); print("saved")
