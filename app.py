import os
import requests
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY     = os.getenv("AIRTABLE_API_KEY")
BASE_ID     = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME  = os.getenv("AIRTABLE_TABLE_NAME")
ENDPOINT    = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS     = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

@app.route("/")
@app.route("/timeline")
def timeline():
	return render_template("timeline.html")

@app.route("/list")
def list_records():
	resp = requests.get(ENDPOINT, headers=HEADERS)
	records = resp.json().get("records", []) if resp.ok else []
	return render_template("list.html", records=records)

@app.route("/delete/<record_id>", methods=["POST"])
def delete_record(record_id):
	requests.delete(f"{ENDPOINT}/{record_id}", headers=HEADERS)
	return redirect(url_for("list_records"))

@app.route("/edit/<record_id>")
def edit(record_id):
	resp = requests.get(f"{ENDPOINT}/{record_id}", headers=HEADERS)
	record = resp.json() if resp.ok else {}
	return render_template("form.html", record=record)

@app.route("/save/<record_id>", methods=["POST"])
def save(record_id):
	data = {"fields": {"Name": request.form["name"], "Email": request.form["email"]}}
	requests.patch(f"{ENDPOINT}/{record_id}", headers=HEADERS, json=data)
	return redirect(url_for("list_records"))

if __name__ == "__main__":
	app.run(debug=True)
	
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
	
	

