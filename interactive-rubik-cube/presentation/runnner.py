from .app.app import App
from kink import di

def bootstrap():
    di

def run():
    bootstrap()
    app = App()
    app.run()
