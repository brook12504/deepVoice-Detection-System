from flask import Flask, request, redirect, render_template

app = Flask(__name__, static_url_path='/templates/assets', static_folder='templates/assets')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input-page')
def input_page():
    return render_template('input-page.html')

@app.route('/output-page')
def output_page():
    return render_template('output-page.html')



if __name__ == '__main__':
    app.run(debug=True)