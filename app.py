from website import create_app
from flask_login import login_required
from flask import request, render_template
import os

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)