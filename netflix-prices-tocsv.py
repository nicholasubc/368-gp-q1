from pathlib import Path  # for getting array of json files
import json

data = Path("data/netflix-prices/data")
csv = "out/netflix_prices.csv"
countries_csv = "out/countries_relation.csv"

rows = []
countries = set()

# load json files into rows arrays
for file in sorted(data.glob("*.json")):
    if (file.name != "latest.json"):
        date = file.stem
        with open(file) as f:
            data = json.load(f)
        for country in data:
            countries.add(country["country"])
            country_name = country["country"]
            country_code = country["country_code"]

            basic_price = None
            for plan in country["plans"]:
                if plan["name"] == "basic":
                    basic_price = plan["price_usd"]
                    break
            if basic_price is not None:
                rows.append((date, country_name, country_code, basic_price))

# write out csvs
with open(csv, "w") as f:
    f.write("date,country,country_code,basic_price\n")

    for date, country, code, price in rows:
        f.write(f"{date},{country},{code},{price}\n")

with open(countries_csv, "w") as f:
    f.write("country\n")

    for country in countries:
        f.write(f"{country}\n")
