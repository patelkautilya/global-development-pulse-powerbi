"""Build a reproducible World Development Indicators country panel.

Run: python scripts/build_dataset.py
Source: World Bank API, accessed 2026-11-04. Country/territory economies only;
regional and income aggregates are excluded using country metadata.
"""
from __future__ import annotations

import csv
import json
import statistics
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "SP.DYN.LE00.IN": "life_expectancy_years",
    "IT.NET.USER.ZS": "internet_users_pct",
    "SL.UEM.TOTL.ZS": "unemployment_pct",
}
YEARS = range(2020, 2025)


def get(url: str):
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[1], list):
        raise ValueError(f"Unexpected World Bank response: {url}")
    if int(payload[0]["pages"]) != 1:
        raise ValueError(f"Paginated response was truncated: {url}")
    return payload[1]


def main():
    DATA.mkdir(exist_ok=True)
    ANALYSIS.mkdir(exist_ok=True)
    country_url = "https://api.worldbank.org/v2/country?format=json&per_page=500"
    countries = {
        item["id"]: item
        for item in get(country_url)
        if item["region"]["id"] != "NA"
    }
    rows = {
        (code, year): {
            "country_code": code,
            "country": item["name"],
            "region": item["region"]["value"].strip(),
            "income_group": item["incomeLevel"]["value"],
            "year": year,
            **{column: None for column in INDICATORS.values()},
        }
        for code, item in countries.items()
        for year in YEARS
    }
    sources = {"country_metadata": country_url, "indicators": {}}
    for indicator, column in INDICATORS.items():
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
            "?format=json&per_page=20000&date=2020:2024"
        )
        sources["indicators"][indicator] = url
        for item in get(url):
            key = (item["countryiso3code"], int(item["date"]))
            if key in rows and item["value"] is not None:
                rows[key][column] = float(item["value"])
    panel = [rows[key] for key in sorted(rows)]
    # Keep the reported value for audit while excluding a clear implausible
    # life-expectancy outlier from visuals and medians.
    for row in panel:
        row["life_expectancy_source_years"] = row["life_expectancy_years"]
        if row["life_expectancy_years"] is not None and row["life_expectancy_years"] < 40:
            row["life_expectancy_years"] = None
    assert len(panel) == len(countries) * len(YEARS)
    for row in panel:
        for col in ("internet_users_pct", "unemployment_pct"):
            value = row[col]
            assert value is None or 0 <= value <= 100, (row, col)
        assert row["life_expectancy_years"] is None or 0 < row["life_expectancy_years"] < 120, row
        assert row["gdp_per_capita_current_usd"] is None or row["gdp_per_capita_current_usd"] > 0
    fieldnames = list(panel[0])
    output = DATA / "world_development_2020_2024.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(panel)
    year2024 = [row for row in panel if row["year"] == 2024]
    complete = [row for row in year2024 if all(row[col] is not None for col in INDICATORS.values())]
    summary = {
        "source_accessed_utc": "2026-11-04",
        "sources": sources,
        "country_economies": len(countries),
        "panel_rows": len(panel),
        "year_2024_complete_cases": len(complete),
        "year_2024_non_missing": {
            col: sum(row[col] is not None for row in year2024)
            for col in INDICATORS.values()
        },
        "year_2024_complete_case_medians": {
            col: statistics.median(row[col] for row in complete)
            for col in INDICATORS.values()
        },
        "year_2024_region_complete_cases": {
            region: sum(row["region"] == region for row in complete)
            for region in sorted({row["region"] for row in complete})
        },
        "life_expectancy_below_40_review": [
            {"country": row["country"], "year": row["year"], "source_value": row["life_expectancy_source_years"]}
            for row in panel
            if row["life_expectancy_source_years"] is not None and row["life_expectancy_source_years"] < 40
        ],
    }
    (ANALYSIS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "sources"}, indent=2))


if __name__ == "__main__":
    main()

