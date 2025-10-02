# Technical Overview

Each team scraper is a function in src/scrapper.py.

Each function accepts either raw HTML or JSON (as string) and returns:

- headers: List[str]
- rows: List[List[str]]

src/main.py orchestrates HTTP requests to each career portal, calls the appropriate scraper, builds pandas DataFrames, and writes them into output/F1_Jobs.xlsx as one sheet per team.

**Notes:**
- The scrapers are custom for each site because each site structures job listings differently (table, list, JSON API, etc.)
- The project currently writes directly to output/F1_Jobs.xlsx
- Sample output generated for 3rd October 2025 to data/sample_output.xlsx