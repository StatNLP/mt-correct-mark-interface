from faker import Faker
from faker.providers import profile, lorem
from annotproj import db, bcrypt
from annotproj.models import User, Annotation, Eval, Ranking, fb_type
import os
import random

fake = Faker()

fake.add_provider(profile)
fake.add_provider(lorem)

for i in range(10):
    data = fake.simple_profile()
    newUser = User(username=data['username'], 
        email=data['mail'], 
        password=bcrypt.generate_password_hash("password"),
        native_language = "en",
        german_level = "c2",
        english_level = "c2")
    db.session.add(newUser)
    db.session.commit()

berger = User(username="User",
    email="User@email.com",
    password=bcrypt.generate_password_hash("password"),
    native_language = "en",
    german_level = "c2",
    english_level = "c2")
db.session.add(berger)
db.session.commit()

users = User.query.all()

for i in range(200):
    src = fake.sentence(nb_words=50)
    target = fake.sentence(nb_words=50)
    feed_back_type = random.choice(list(fb_type))
    user_id = users[random.randint(0,len(users) - 1)].id
    newAnnotation = Annotation(src=src, target=target, feedback_type = feed_back_type, user_id=user_id)
    db.session.add(newAnnotation)
    db.session.commit()

for i in range(100):
    src = fake.sentence(nb_words = 50)
    target1 = fake.sentence(nb_words=10)
    target2 = fake.sentence(nb_words=10)
    user_id = users[random.randint(0, len(users) - 1)].id
    newEval = Eval(src=src, target1=target1, target2=target2, model1="baseline", model2="postedit", user_id=user_id)
    db.session.add(newEval)
    db.session.commit()

