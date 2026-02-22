from flask import Flask
from api.api import Api
from routers.router import router



app = Flask(__name__)

app.register_blueprint(Api , url_prefix='/api/problems' )
app.register_blueprint(router)


if __name__ == "__main__":
    app.run(debug=True)

