from src.app import app
from src.helpers.errorHandler import errorHandler, APIError
import random
from flask import request

@app.route("/hola")
def basicResponse():
    return {
        "hola":"que tal"
    }


app.route("/ta")(lambda: random.choice(["Clara","Felipe","Marc"]))

@app.route("/ta/favorito")
def personajeFavorito():
    return """
     <img src="https://upload.wikimedia.org/wikipedia/ca/thumb/0/02/Homer_Simpson_2006.png/224px-Homer_Simpson_2006.png" />
    """

# Query params
@app.route("/pepe")
@errorHandler
def pepe():
    saludo = request.args.get("saludo")
    if saludo:
        return {
            "saludo": f"Hola {saludo}"
        }
    raise APIError("Tienes que mandar un query parameter ?saludo=<tunombre>")



