# %% load data
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_excel("processed responses with rejected.xlsx")
# use the second panel
df_sel = pd.read_excel("Final sample_After correction_MS.xlsx", sheet_name="60 osób")

# %%
groups = df_sel["grupa dotychczasowa"]
emails = df_sel["mail"]

# %%
# for each email in df_sel (emails), for the same email in df, set the group into df["post_selection_group"]

# Create a mapping from email to group
email_to_group = dict(zip(emails, groups))

# Assign groups using the mapping
df["post_selection_group"] = df["Email Address"].map(email_to_group)

# %%
# should be 20 20 20
counts = df["post_selection_group"].value_counts()
assert counts["control"] == 20 and counts["worry"] == 20 and counts["phobia"] == 21
assert len(email_to_group) == int(df["post_selection_group"].notna().sum())
assert not set(emails) - set(df[df["post_selection_group"].notna()]["Email Address"])
assert not set(df[df["post_selection_group"].notna()]["Email Address"]) - set(emails)

# note: needed to edit manually two emails to match formatting from the original df
# also added JU68 to phobia

# %% plots
# NaN is grey
color_map = {"control": "green", "worry": "yellow", "phobia": "red"}
colors = df["post_selection_group"].apply(
    lambda x: color_map[x] if pd.notna(x) else "gray"
)
ax = df.plot.scatter(x="PSWQ rank", y="SPQ+SNAQ rank", c=colors)
ax.set_aspect("equal")

# pad = 0.05
# ax.set_xlim(0 - pad, 1 + pad)
# ax.set_ylim(0 - pad, 1 + pad)
