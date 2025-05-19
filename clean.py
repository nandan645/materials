# import json
# import re
# from pathlib import Path

# # File paths
# JSON_PATH = Path("nature_articles.json")
# ARIA2C_LIST_PATH = Path("pdf_list.txt")

# def safe_filename(title):
#     """Sanitize article title into a safe filename."""
#     return re.sub(r'[\\/*?:"<>|]', "_", title)[:150] + ".pdf"

# def main():
#     try:
#         with open(JSON_PATH, "r", encoding="utf-8") as f:
#             articles = json.load(f)
#     except Exception as e:
#         print(f"[ERROR] Failed to load JSON: {e}")
#         return

#     open_access_articles = [a for a in articles if a.get("Open Access") == "Yes"]

#     if not open_access_articles:
#         print("[INFO] No Open Access articles found.")
#         return

#     with open(ARIA2C_LIST_PATH, "w", encoding="utf-8") as f:
#         for article in open_access_articles:
#             pdf_url = article["URL"] + ".pdf"
#             filename = safe_filename(article["Title"])
#             f.write(f"{pdf_url}\n  out={filename}\n")

#     print(f"[DONE] {len(open_access_articles)} entries written to {ARIA2C_LIST_PATH}")

# if __name__ == "__main__":
#     main()


import json
from pathlib import Path

# File paths
JSON_PATH = Path("nature_articles.json")
URL_LIST_PATH = Path("pdf_urls.txt")  # Changed output file name for clarity

def main():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return

    open_access_articles = [a for a in articles if a.get("Open Access") == "Yes"]

    if not open_access_articles:
        print("[INFO] No Open Access articles found.")
        return

    with open(URL_LIST_PATH, "w", encoding="utf-8") as f:
        for article in open_access_articles:
            pdf_url = article["URL"] + ".pdf"
            f.write(f"{pdf_url}\n")

    print(f"[DONE] {len(open_access_articles)} PDF URLs written to {URL_LIST_PATH}")

if __name__ == "__main__":
    main()
