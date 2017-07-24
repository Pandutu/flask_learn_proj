from flask import Flask, render_template
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap

from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import INLINE as BOKEH_INLINE

app = Flask(__name__, template_folder='../templates')
bootstrap = Bootstrap(app)
print(__name__)
manager = Manager(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/test/bokeh')
def bokeh_test():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]


    p = figure(title='simple line example', x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend='Temp.', line_width=2)

    html = file_html(p, BOKEH_INLINE, 'my plot')


    return html or '<h1>Shit Happen.</h1>'


if __name__ == '__main__':
    manager.run()
