from flask import Flask

from api.controllers import (old_person_controller, responsible_person_controller, activity_controller,
                             exercise_controller, feeding_controller, medicine_controller, r_old_person_act_controller,
                             r_old_person_exercise_controller, r_old_person_feeding_controller,
                             r_old_person_medicine_controller, r_old_person_responsible_controller)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(old_person_controller.bp)
    app.register_blueprint(responsible_person_controller.bp)
    app.register_blueprint(activity_controller.bp)
    app.register_blueprint(exercise_controller.bp)
    app.register_blueprint(feeding_controller.bp)
    app.register_blueprint(medicine_controller.bp)
    app.register_blueprint(r_old_person_act_controller.bp)
    app.register_blueprint(r_old_person_exercise_controller.bp)
    app.register_blueprint(r_old_person_feeding_controller.bp)
    app.register_blueprint(r_old_person_medicine_controller.bp)
    app.register_blueprint(r_old_person_responsible_controller.bp)

    return app
