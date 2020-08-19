import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

from BatchConversions import get_path


df = pd.read_csv(get_path())
fig, ax = plt.subplots()
my_scatter_plot = ax.scatter(
    df["CumDistance (m)"],
    df["Ho"]
)

ax.set_xlabel("Distance over Polyline (m)")
ax.set_ylabel("Orthometric Elevation (m)")
ax.set_title("Elevation on Polyline")

plt.show()