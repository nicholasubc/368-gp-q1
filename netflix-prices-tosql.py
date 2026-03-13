from pathlib import Path
import json

data = Path("data/netflix-prices/data")
csv = "out/netflix_prices.csv"
sql = "out/netflix_prices.sql"

rows = []

for file in sorted(data.glob("*.json")):
    date = file.stem
    with open(file) as f:
        data = json.load(f)
    for country in data:
        country_code = country["country_code"]

        basic_price = None
        for plan in country["plans"]:
            if plan["name"] == "basic":
                basic_price = plan["price_usd"]
                break
        if basic_price is not None:
            rows.append((date, country_code, basic_price))

with open(csv, "w") as f:
    f.write("date,country_code,basic_price\n")

    for date, code, price in rows:
        f.write(f"{date},{code},{price}\n")

with open(sql, "w") as f:
    f.write("""DROP TABLE IF EXISTS netflix_prices;
CREATE TABLE netflix_prices (
    date DATE,
    country_code CHAR(2),
    basic_price FLOAT
);
""")

    for date, code, price in rows:
        f.write(f"INSERT INTO netflix_prices VALUES ('{date}', '{code}', {price});\n")
