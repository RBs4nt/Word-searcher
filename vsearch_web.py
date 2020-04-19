from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__) # Creating a Web Flask application object


def log_request(req: 'flask_request', res: str) -> None:
    """Records specific attributes of the request and response made in the application in a file"""
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    """Information collection page for search, phrase and letters"""
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are you results:'
    results = str(search4letters(phrase, letters)) # Perform data processing using the vsearch4letters function of the vsearch module
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Home page"""
    return render_template('entry.html', 
                           the_title='Welcome to SeArCh4Latters on the Web!!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    """Returns template with elegant view in table format for logs"""
    contents = []
    with open('vsearch.log') as log:
        for line in log: 
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', 
                          the_titles='View Log',
                          the_row_titles=titles,
                          the_data=contents,) 

if __name__ == '__main__': # dunder call
    app.run()
