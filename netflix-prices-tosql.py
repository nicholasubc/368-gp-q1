from pathlib import Path  # for getting array of json files
import json

data = Path("data/netflix-prices/data")
sql = "out/netflix_prices.sql"

rows = []

# load json files into rows array
for file in sorted(data.glob("*.json")):
    if (file.name != "latest.json"):
        date = file.stem
        with open(file) as f:
            data = json.load(f)
        for country in data:
            country_name = country["country"]
            country_code = country["country_code"]

            basic_price = None
            for plan in country["plans"]:
                if plan["name"] == "basic":
                    basic_price = plan["price_usd"]
                    break
            if basic_price is not None:
                rows.append((date, country_name, country_code, basic_price))

with open(sql, "w") as f:
    # discard old data and create table
    f.write("""DROP TABLE IF EXISTS netflix_prices;
PURGE RECYCLEBIN;
CREATE TABLE netflix_prices (
    date DATE PRIMARY KEY,
    country VARCHAR(100),
    country_code CHAR(2) PRIMARY KEY,
    basic_price FLOAT
);
""")

    # convert data to insert statements
    for date, country, code, price in rows:
        f.write(f"INSERT INTO netflix_prices VALUES ('{date}', '{country}', '{code}', {price});\n")
