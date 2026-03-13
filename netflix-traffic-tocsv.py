import pandas as pd  # for pivoting

df = pd.read_csv("data/multiTimeline.csv", skiprows=1)

out = df.melt(id_vars="Month", var_name="Country", value_name="Value")
out["Country"] = out["Country"].str.extract(r"\((.*?)\)")  # regex select only country name

out.to_csv("out/netflix_traffic.csv", index=False)
