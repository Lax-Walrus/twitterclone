""" runs the app in dubug mode and is main script file """

from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
