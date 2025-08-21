from flask import Flask, render_template, request, session, jsonify, Response
from scraper import scrape_and_store
import csv, io

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/", methods=["GET", "POST"])
def index():
    results=None
    if request.method == "POST":
        url = request.form["url"]
        data_type = request.form["data_type"]
        selector = request.form.get("selector")
        scape_name = request.form["scrape_name"]

        results = scrape_and_store(url, data_type, selector, scape_name)

        session["results"] = results
    return render_template("index.html", results=results)

@app.route("/export/csv")
def export_csv():
    results = session.get("results", [])
    if not results:
        return "No Data To Export"

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Result"])
    for item in results:
        writer.writerow([item])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=results.csv"}
    )

@app.route("/export/json")
def export_json():
    results = session.get("results", [])
    if not results:
        return "No data to Export"
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)