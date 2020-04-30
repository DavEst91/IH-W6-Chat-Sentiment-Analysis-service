from src.config import PORT
from src.app import app
import src.controllers.users
app.run("127.0.0.1", PORT, debug=True)
