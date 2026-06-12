import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# load COVID dataset
df = pd.read_csv("covid_19_clean_complete.csv")
print(df.head())

 # Rename column for simplicity + Removes Latitude and Longitude + Fills missing values
df.rename(columns={"Country/Region":"Country"}, inplace=True)
print(df.columns.tolist())
df = df.drop(columns=["Lat","Long"], errors="ignore")
df = df.fillna(0)

# Aggregate data by Country + Date
df_grouped = df.groupby(["Date","Country"])[["Confirmed","Deaths","Recovered"]].sum().reset_index()
print(df_grouped.head())


## VISUALIZATION------

# -----------------------------
# Line Chart
# ----------------------------- 

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=df_grouped[
        df_grouped["Country"].isin(
            ["India", "US", "Brazil"]
        )
    ],
    x="Date",
    y="Confirmed",
    hue="Country"
)
plt.title("COVID-19 Confirmed Cases Over Time")
plt.show()

# -----------------------------
# Top 10 Countries by Deaths
# -----------------------------
latest = df_grouped[
    df_grouped["Date"] == df_grouped["Date"].max()
]

top10 = latest.sort_values(
    "Deaths", 
    ascending=False
).head(10)

plt.figure(figsize=(10,6))

sns.barplot(
    data=top10, 
    x="Deaths", 
    y="Country"
)

plt.title("Top 10 Countries by COVID-19 Deaths")
plt.tight_layout()
plt.show()

# -----------------------------
# Correlation Heatmap
# -----------------------------
plt.figure(figsize=(6, 4))

sns.heatmap(
    df_grouped[
        ["Confirmed", "Deaths", "Recovered"]
    ].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title(
    "Correlation Between Confirmed, Deaths and Recovered"
)

plt.tight_layout()
plt.show()

# -----------------------------
# Interactive Plotly Chart
# -----------------------------
fig = px.line(
    df_grouped[
        df_grouped["Country"].isin(
            ["India", "US", "Brazil"]
        )
    ],
    x="Date",
    y="Confirmed",
    color="Country",
    title="COVID-19 Confirmed Cases"
)

fig.show()