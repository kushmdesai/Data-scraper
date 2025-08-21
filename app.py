from flask import Flask, render_template, request
from scraper import scrape_and_store

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results=None
    if request.method == "POST":
        url = request.form["url"]
        data_type = request.form["data_type"]
        selector = request.form.get("selector")
        scape_name = request.form["scrape_name"]

        results = scrape_and_store(url, data_type, selector, scape_name)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

"""
Export Options → allow users to download results as .csv, .json, or .xlsx.

Search/Filter → add a search bar to filter the scraped results in the UI.

Live Preview → display scraped results in a table with sorting, instead of just a list.

Error Handling → show friendly error messages if scraping fails (invalid URL, selector not found, etc.).

Loading State → add a spinner or animated “Scraping…” message while waiting for results.

Data Visualization → if scraping numbers/tables, render graphs (using Chart.js or Recharts).
"""