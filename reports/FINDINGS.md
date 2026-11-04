# Findings and quality notes

## Comparable 2024 sample

The World Bank API lists 217 country economies after excluding aggregates. In 2024, 200 have GDP per capita, 217 have life expectancy, 182 have Internet-use estimates, and 182 have modeled unemployment estimates. **165** have all four and form the comparable KPI sample. Every number below is a median across these 165 country economies, unweighted by population.

The Power BI report deliberately shows metric-specific non-missing coverage, rather than applying the complete-case restriction to every visual. Its unfiltered 2024 Internet KPI is **82.10%** across 182 economies, and the Sub-Saharan Africa bar is **36.80%** across 45 economies. These match independent calculations from the curated CSV. The complete-case medians below answer a different, common-sample question.

| 2024 KPI | Median |
| --- | ---: |
| GDP per capita, current US$ | $7,649.82 |
| Life expectancy at birth | 74.576 years |
| Internet users | 81.957% of population |
| Modeled unemployment | 5.051% of labor force |

The high-income group (57 complete economies) has median Internet use of **93.78%** and median life expectancy of **81.97 years**. The low-income group (19 complete economies) has corresponding medians of **20.53%** and **63.80 years**. These are group descriptions, not evidence of causation or of population-level gaps.

Among regions, the 44 complete Sub-Saharan Africa economies have median Internet use of **35.89%**. Europe & Central Asia's 46 complete economies have **91.03%**. North America's two complete economies are a very small group and should not be treated as a stable regional benchmark.

## Data cautions

- GDP per capita is in **current US dollars**. The 2020–2024 panel is useful for selected indicator exploration, but nominal GDP movements conflate price, exchange-rate, and real changes. The dashboard should center cross-sectional 2024 comparisons.
- Country medians treat each economy equally. They are not World Bank published regional aggregates, and the complete-case subset is not a random sample.
- Missing values remain blank. Selecting a single metric can show more economies than the four-metric complete-case view. The report must label its sample basis.
- The API returns an anomalous 2022 Central African Republic life expectancy of **18.818 years**, between 40.279 in 2021 and 57.408 in 2023. The curated analysis field blanks that point while retaining the raw source value for audit. This is a quality rule, not a corrected estimate.
- World Bank indicator definitions and country classifications can be revised. Re-running the script may yield updated values.

Sources: [World Bank API](https://api.worldbank.org/v2/), [GDP per capita](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD), [life expectancy](https://data.worldbank.org/indicator/SP.DYN.LE00.IN), [Internet use](https://data.worldbank.org/indicator/IT.NET.USER.ZS), [modeled unemployment](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS). Accessed 2026-11-04.

