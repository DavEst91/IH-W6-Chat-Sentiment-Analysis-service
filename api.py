from src.config import PORT,IP
from src.app import app as app
import src.controllers.users
import src.controllers.chats
import src.controllers.message
import src.controllers.reccomender_system
import os
port = int(os.environ.get("PORT", 5000))

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=PORT)
