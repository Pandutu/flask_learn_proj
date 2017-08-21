from flask import Flask, render_template, url_for, redirect, abort, session, flash, current_app
from flask import request

from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message as Mail_Message

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired

from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import INLINE as BOKEH_INLINE

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
import os.path
from threading import Thread


base_sqlite_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'ink add this shit for wtf secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///' + os.path.join(base_sqlite_dir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# E-mail Send Params
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Ink <{}>'.format(app.config['MAIL_USERNAME'])

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Mail_Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                       sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thrd = Thread(target=send_async_email, args=[app, msg])
    thrd.start()
    return thrd


class NameForm(FlaskForm):
    name = StringField(r"What's your name?", validators=[DataRequired()])
    selected = SelectField('Select WTF you want', choices=[('a', 'a'), ('b', 'b'), ('c', 'c')])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)

    users = relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)

    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    selected = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        session['selected'] = form.selected.data
        session['name'] = form.name.data
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            flash('Add A New User:{username} To DB.'.format(username=form.name.data))
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            flash('I Know This User Already.')
            session['known'] = True

        return redirect(url_for('index'))

    try:
        html = render_template('index.html',
                               current_time=datetime.utcnow(),
                               # get for returning None while no key in session
                               form=form, name=session.get('name'), selected_item=session.get('selected'),
                               known=session.get('known', False))
    except Exception:
        html = None

    return html


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
