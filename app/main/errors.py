from flask import render_template, redirect, url_for
from . import main



@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main.app_errorhandler(403)
def permission_not_allowed(e):
    return redirect(url_for('main.index'))