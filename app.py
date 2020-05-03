from src.config import PORT,IP
from src.app import app as application
import src.controllers.users
import src.controllers.chats
import src.controllers.message
import src.controllers.reccomender_system

application.run(debug=True)
