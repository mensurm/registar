__author__ = 'mensur'

from admin import app

app.debug = True



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)