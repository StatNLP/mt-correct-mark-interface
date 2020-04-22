from annotproj import db, bcrypt
from annotproj.models import User, Annotation, Eval, Ranking, fb_type
import os
import random

de = open('TARGET_DATA', 'r')
en = open('SOURCE_DATA', 'r')

de_data = de.read()
en_data = en.read()

de_lines = de_data.split('\n')
en_lines = en_data.split('\n')
users = User.query.all()

for i in range(200):
    index = random.randint(0, len(de_lines) - 2)
    src = de_lines[index]
    target = en_lines[index]
    feed_back_type = random.choice(list(fb_type))
    user_id = users[random.randint(0,len(users) - 1)].id
    newAnnotation = Annotation(src=src, target=target, feedback_type = feed_back_type, user_id=user_id)
    db.session.add(newAnnotation)
    db.session.commit()

for i in range(200):
    index = random.randint(0, len(de_lines) - 2)
    src = de_lines[index]
    target1 = en_lines[index]
    target2 = en_lines[index]
    user_id = users[random.randint(0, len(users) - 1)].id
    newEval = Eval(src=src, target1=target1, target2=target2, model1="baseline", model2="postedit", user_id=user_id)
    db.session.add(newEval)
    db.session.commit()

for i in range(200):
    index = random.randint(0, len(de_lines) - 1)
    src = de_lines[index]
    target1 = en_lines[index]
    target2 = en_lines[index]
    target3 = en_lines[index]
    target4 = en_lines[index]
    target5 = en_lines[index]
    user_id = users[random.randint(0, len(users) - 1 )].id
    newRanking = Ranking(src=src, target1=target1, target2=target2, target3=target3, target4=target4, target5=target5, 
        model1="baseline", model2="postedit", model3="marking", model4="userdecide", model5="systemdecide", user_id=user_id)
    db.session.add(newRanking)
    db.session.commit()