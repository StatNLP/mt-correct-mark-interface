from annotproj.models import User, Annotation, db, fb_type

splits = open('../data/assignments.txt')
modes = ["pe", "mark", "user"]
agreement_en = open('../data/agreement.en')
agreement_hyp = open('../data/agreement.hyp')

agreement_en_lines = agreement_en.readlines()
agreement_hyp_lines = agreement_hyp.readlines()

def add_agreement(user):
    for i in range(len(agreement_en_lines)):
        mode = None
        if i < 5:
            mode = fb_type.post_edit
        elif i >=5 and i < 10:
            mode = fb_type.marking
        else:
            mode = fb_type.user_decide
        newAnnotation = Annotation(user_id = user,
            src=agreement_en_lines[i].strip("\n"),
            target=agreement_hyp_lines[i].strip("\n"),
            feedback_type=mode,
            sentence_id="agreement." + str(i),
            agreement=True)
        db.session.add(newAnnotation)
        db.session.commit()

parts_added = {}
for i in range(0, 10, 1):
    newUser = User(id = i)
    db.session.add(newUser)
    db.session.commit()
    parts_added[i] = 0
assignments = splits.readlines()
assignments = assignments[1:]
assignments = [x.split(" ") for x in assignments]
assignments.sort(key=lambda x: (x[3], str(x[0] + x[2])))

file_names = {}
for user in range(0, 10, 1):
    for mode in modes:
        file_names[(user, mode)] = []

for x in assignments:
    file_names[(int(x[3]), x[2])].append((x[0], x[1]))


for user in range(0, 10, 1):
    for doc in range(0, 3, 1):
        for mode in modes:
            doc_part = file_names[(user,mode)][0]
            doc_num = str(doc_part[0])
            part_num = str(doc_part[1])
            en = open('../data/split_talks/' + doc_num + 'p' + part_num + '.en')
            hyp = open('../data/split_talks/' + doc_num + 'p' + part_num + '.hyp')
            user_id = user
            en_lines = en.readlines()
            hyp_lines = hyp.readlines()

            feedback_type = None
            if mode == 'pe':
                feedback_type = fb_type.post_edit
            elif mode == 'mark':
                feedback_type = fb_type.marking
            else:
                feedback_type = fb_type.user_decide

            for i, (en_line, hyp_line) in enumerate(zip(en_lines, hyp_lines)):
                en_line = en_line.strip("\n")
                hyp_line = hyp_line.strip("\n")
                line_num = str(i)
                newAnnotation = Annotation(user_id = user_id, \
                src=en_line, \
                target=hyp_line, \
                sentence_id=doc_num + 'p' + part_num + '.' + line_num, \
                feedback_type=feedback_type)
                db.session.add(newAnnotation)
                db.session.commit()
            del file_names[(user, mode)][0]
        add_agreement(user)

        
