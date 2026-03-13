import csv

data = "out/worldbank.csv"
sql = "out/worldbank.sql"
with open(data, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    rows = []
    for row in reader:
        country = row["Country Name"]
        code = row["Series Code"]
        val = row["LatestValue"]
        rows.append([country, code, val])

with open(sql, "w") as f:
    # discard old data and create table
    f.write("""DROP TABLE IF EXISTS worldbank;
PURGE RECYCLEBIN;
CREATE TABLE worldbank (
    country VARCHAR(100),
    series_code VARCHAR(100),
    latest_value FLOAT NOT NULL,
    FOREIGN KEY (country) REFERENCES netflix_prices ON DELETE CASCADE,
    PRIMARY KEY (country, series_code)
);
""")

    # convert data to insert statements ensuring blank values convert to null
    for country, code, val in rows:
        if (val != ""):
            f.write(f"INSERT INTO worldbank VALUES ('{country}', '{code}', '{val}');\n")
