from rankedRetrieval import processQuery
from flask import Flask, render_template, redirect, url_for, request

app = Flask('app', template_folder='templates')
app.debug = True


# Search Page
@app.route('/')
@app.route('/search')
def search():
    return render_template('search.html')


# Results Page
@app.route('/results')
def results():
    query = request.args.get("query")
    if query.strip():
        results, time = processQuery(query)
        return render_template('results.html', 
            query = query, 
            results = results, 
            time = time)
    return redirect(url_for('search'))

# Runs Function
if __name__ == '__main__':
    app.run(debug=False) 