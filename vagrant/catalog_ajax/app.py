from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data["action"] == "testAjax":
            id = data["id"]
            return render_template('partials/catalog_items.html', id=id)

    return render_template('catalog.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
