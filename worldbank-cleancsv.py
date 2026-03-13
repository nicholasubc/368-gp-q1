import csv

data = "data/11e258b4-4a6a-456f-bca5-52cea556de9a_Data.csv"
csvout = "out/worldbank.csv"
with open(data, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    rows = []
    for row in reader:
        name = row["Country Name"]
        code = row["Series Code"]
        val = row["2024 [YR2024]"]
        if val == "..":  # .. means null
            val = ""
        rows.append([name, code, val])

# the last 5 rows are not relavent data
rows = rows[:-5]

# write out csv
with open(csvout, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Country Name", "Series Code", "LatestValue"])
    writer.writerows(rows)
