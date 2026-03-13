import csv

data = "out/netflix_traffic.csv"
sql = "out/netflix_traffic.sql"
with open(data, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    rows = []
    for row in reader:
        month = row["Month"]
        country = row["Country"]
        value = row["Value"]
        rows.append([month, country, value])

with open(sql, "w", encoding="utf-8") as f:
    # discard old data and create table
    f.write("""DROP TABLE IF EXISTS netflix_traffic;
PURGE RECYCLEBIN;
CREATE TABLE netflix_traffic (
    month DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    value INT NOT NULL,
    PRIMARY KEY (month, country),
    FOREIGN KEY (country) REFERENCES countries_relation ON DELETE CASCADE
);
""")

    # blank values become 0
    for month, country, value in rows:
        if (value != ""):
            f.write(f"INSERT INTO netflix_traffic VALUES ('{month}', '{country}', {value});\n")
        else:
            f.write(f"INSERT INTO netflix_traffic VALUES ('{month}', '{country}', 0);\n")
