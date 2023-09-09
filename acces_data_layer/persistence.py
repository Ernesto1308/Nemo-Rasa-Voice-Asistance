# from models.models import *
from services import old_person_service

"""
resp_person1 = ResponsiblePerson(responsible_person_name="Nolan")
resp_person2 = ResponsiblePerson(responsible_person_name="Blake")

medicine1 = Medicine(medicine_name="Tylenol")
medicine2 = Medicine(medicine_name="Acetaminophen")

exercise1 = Exercise(exercise_name="Push up")
exercise2 = Exercise(exercise_name="Push down")

feeding1 = Feeding(feeding_name="Lunch")
feeding2 = Feeding(feeding_name="Brunch")

activity1 = Activity(activity_name="Shopping List")
activity2 = Activity(activity_name="Sweeping")

old_person = OldPerson(old_person_name="Felipe")

rel_old_resp1 = RelOldPersonResponsible(id_old_person=8, id_responsible_person=4)
rel_old_resp2 = RelOldPersonResponsible(id_old_person=8, id_responsible_person=6)

rel_old_act1 = RelOldPersonActivity(id_old_person=8, id_activity=2, activity_hour=datetime(2023, 8, 1, 9, 0))
rel_old_act2 = RelOldPersonActivity(id_old_person=8, id_activity=4, activity_hour=datetime(2023, 8, 1, 9, 10))

rel_old_med1 = RelOldPersonMedicine(id_old_person=8, id_medicine=2, medicine_hour=datetime(2023, 8, 1, 9, 0))
rel_old_med2 = RelOldPersonMedicine(id_old_person=8, id_medicine=3, medicine_hour=datetime(2023, 8, 1, 9, 10))

rel_old_ex1 = RelOldPersonExercise(id_old_person=8, id_exercise=4, exercise_hour=datetime(2023, 8, 1, 9, 0))
rel_old_ex2 = RelOldPersonExercise(id_old_person=8, id_exercise=5, exercise_hour=datetime(2023, 8, 1, 9, 10))

rel_old_feed1 = RelOldPersonFeeding(id_old_person=8, id_feeding=5, feeding_hour=datetime(2023, 8, 1, 9, 0))
rel_old_feed2 = RelOldPersonFeeding(id_old_person=8, id_feeding=7, feeding_hour=datetime(2023, 8, 1, 9, 10))
"""
# rel_old_resp_serv.insert(rel_old_resp1)
# rel_old_resp_serv.insert(rel_old_resp2)
# print(rel_old_resp_serv.select_by_id(8))
# print(rel_old_resp_serv.select_by_id(8, 5))
# rel_old_feed1.feeding_hour = datetime(2023, 8, 1, 9, 30)
# rel_old_resp_serv.update(rel_old_feed1)
# rel_old_resp_serv.delete(8, 6)
print(old_person_service.select())
