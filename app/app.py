from flask import Flask, redirect, url_for, render_template
from app import create_app

# create the app object
app = create_app()

if  __name__ == "__main__":
    app.run(debug=True)