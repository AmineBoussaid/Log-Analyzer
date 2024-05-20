from flask import Flask, redirect, render_template, jsonify, request, session, url_for
from service import AccessService, UserService

app = Flask(__name__)
app.secret_key = 'admin'  # Nécessaire pour les sessions

@app.route('/')
def hello():
    if 'user' in session:
        return redirect(url_for('web'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserService.login(email, password)
        
        if user:
            session['user'] = user.email
            return redirect(url_for('web'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        UserService.register(email, password)
        return redirect('/login')

    return render_template('register.html')


@app.route('/web')
def web():
    if 'user' in session:
        return render_template('web.html', user=session['user'])
    return redirect(url_for('login'))


@app.route('/security')
def security():
    if 'user' in session:
        return render_template('security.html', user=session['user'])
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/overview-stats')
def api_overview_stats():
    stats = AccessService.get_overview_stats()
    return jsonify(stats)

@app.route('/api/stats')
def api_stats():
    stats = AccessService.get_stats_par_mois()
    return jsonify(stats)

@app.route('/api/uri_stats')
def api_uri_stats():
    stats = AccessService.get_uri_stats()
    return jsonify(stats)


@app.route('/api/browser_stats')
def api_browser_stats():
    stats = AccessService.get_browser_stats()
    return jsonify(stats)

@app.route('/api/not_found_urls')
def api_not_found_urls():
    urls = AccessService.get_not_found_urls()
    return jsonify(urls)

@app.route('/api/operating-systems')
def api_operating_systems():
    stats = AccessService.get_operating_systems()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
