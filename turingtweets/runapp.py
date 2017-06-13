import os

from paste.deploy import loadapp
from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to='.')

<<<<<<< HEAD
    serve(app, host='0.0.0.0', port=port)
=======
    serve(app, host='0.0.0.0', port=port)
>>>>>>> 8cdccfb57e4fddb9de2265d7d2d17cba45f1609c
