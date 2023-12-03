from flask import Flask
from flask_cors import CORS

from acces_data_layer import db_session
from api.controllers import (older_person_controller, responsible_person_controller,
                             medicine_controller, r_older_person_medicine_controller,
                             r_old_person_responsible_controller, audio_controller)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(older_person_controller.bp)
    app.register_blueprint(responsible_person_controller.bp)
    app.register_blueprint(medicine_controller.bp)
    app.register_blueprint(r_older_person_medicine_controller.bp)
    app.register_blueprint(r_old_person_responsible_controller.bp)
    app.register_blueprint(audio_controller.bp)
    CORS(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
