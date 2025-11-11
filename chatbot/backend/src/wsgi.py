# -*- coding: utf-8 -*-
from src.api.api import app
from src.config.config_init import FLASK_PORT, FLASK_DEBUG


if __name__ == "__main__":
    
    app.run(port=FLASK_PORT, debug=FLASK_DEBUG)
