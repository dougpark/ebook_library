
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash
from flask import request
from flask import jsonify
from LibraryScanner import LibraryScanner
from FolderRenamer import FolderRenamer
from CodeGenerator import CodeGenerator
from MetadataDB import MetadataDB
import os

VERSION = "1.0"
app = Flask(__name__)
app.secret_key = "supersecretkey"  # 🔑 required for flash messages

# EBOOK_FOLDER = os.path.join(os.getcwd(), "ebooks")
EBOOK_FOLDER= os.path.join(os.path.dirname(__file__), "ebooks")
print(f"Scanning folder: {EBOOK_FOLDER}")

# Shared singletons
gen = CodeGenerator()
folder_renamer = FolderRenamer(gen)
scanner = LibraryScanner()
metadata = MetadataDB()

@app.route("/")
def index():
    ebooks = scanner.scan_folder(EBOOK_FOLDER)
    categories = metadata.get_all_categories_with_counts()
    # Calculate total count for "All"
    total_count = sum(cat["count"] for cat in categories)
    return render_template("index.html", ebooks=ebooks, categories=categories, total_count=total_count, version=VERSION)

@app.route("/edit/<code>", methods=["GET", "POST"])
def edit(code):
    entry = metadata.get_entry(code)
    if not entry:
        flash(f"No metadata found for code {code} ❌")
        return redirect(url_for("index"))

    if request.method == "POST":
        # Get edited values from form
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        date_published = request.form.get("date_published", "").strip()
        
        metadata.update_entry(code, title, author, date_published)
        flash(f"Metadata for {code} updated successfully ✅")
        return redirect(url_for("index"))

    # GET request → show edit form
    return render_template("edit.html", entry=entry)

@app.route("/update_metadata", methods=["POST"])
def update_metadata():
    data = request.json
    code = data.get("code")
    title = data.get("title", "").strip()
    author = data.get("author", "").strip()
    date_published = data.get("date", "").strip()
    category = data.get("category", "").strip()
    notes = data.get("notes", "").strip()

    if not code:
        return jsonify({"success": False, "message": "Missing code"}), 400

    metadata.update_entry(code, title, author, date_published, category, notes)
    return jsonify({"success": True, "message": f"Metadata for {code} updated ✅", "category":"success"})

@app.route("/download/<path:rel_path>")
def download(rel_path):
    """Serve a file from EBOOK_FOLDER and its subfolders."""
    dir_name = os.path.dirname(rel_path)
    file_name = os.path.basename(rel_path)
    return send_from_directory(os.path.join(EBOOK_FOLDER, dir_name), file_name, as_attachment=True)

@app.route("/reindex")
def reindex():
    """Run FolderRenamer to assign codes to new files, then update DB."""
    renamed_files = folder_renamer.rename_folder(EBOOK_FOLDER)

    for file in renamed_files:
        filename = os.path.basename(file)
        title = filename.rsplit("_", 1)[0]
        # Infer category from immediate parent folder name
        newcategory = os.path.basename(os.path.dirname(file))
        code = filename.split("_")[-1].split(".")[0]
        metadata.add_entry(code, title=title, author="Author", date_published="Date", category=newcategory, notes="")

    if renamed_files:
        flash(f"{len(renamed_files)} new ebooks indexed successfully ✅")
    else:
        flash("No new ebooks found to index")

    return redirect(url_for("index"))

@app.route("/categories")
def categories():
    categories = metadata.get_all_categories_with_counts()
    return jsonify(categories)

@app.route("/categories_list")
def categories_list():
    categories = metadata.get_all_categories_with_counts()
    total_count = sum(cat["count"] for cat in categories)
    return jsonify({"categories": categories, "total_count": total_count})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5100)