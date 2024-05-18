from flask import Flask, render_template, jsonify
from service import get_stats_par_mois, get_uri_stats, get_browser_stats, get_not_found_urls,get_operating_systems,get_overview_stats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/overview-stats')
def api_overview_stats():
    stats = get_overview_stats()
    return jsonify(stats)

@app.route('/api/stats')
def api_stats():
    stats = get_stats_par_mois()
    return jsonify(stats)

@app.route('/api/uri_stats')
def api_uri_stats():
    stats = get_uri_stats()
    return jsonify(stats)


@app.route('/api/browser_stats')
def api_browser_stats():
    stats = get_browser_stats()
    return jsonify(stats)

@app.route('/api/not_found_urls')
def api_not_found_urls():
    urls = get_not_found_urls()
    return jsonify(urls)

@app.route('/api/operating-systems')
def api_operating_systems():
    stats = get_operating_systems()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
