"""
Data extraction from the database after human annotation.
"""
import argparse
import os 
import re
import sys

from annotproj import db, bcrypt
from annotproj.models import User, Annotation, Eval, Ranking, fb_type

annotations = Annotation.query.filter_by(annotated=True,agreement=False).all()


def extract_data(paras):
    '''
    src: source sentence
    target: mt output
    annot: mt output if marking else post-editing
    feedback: 0 for marked words else 1 for both post-edited and unmarked
    mode: 1: marking 0: post-editing
    '''
    
    mout_src = os.path.join(paras.output_file_path, "marking.src")
    mout_target = os.path.join(paras.output_file_path, "marking.target")
    mout_annot = os.path.join(paras.output_file_path, "marking.annot")

    pout_src = os.path.join(paras.output_file_path, "postedit.src")
    pout_target = os.path.join(paras.output_file_path, "postedit.target")
    pout_annot = os.path.join(paras.output_file_path, "postedit.annot")

    uout_src = os.path.join(paras.output_file_path, "user.src")
    uout_target = os.path.join(paras.output_file_path, "user.target")
    uout_annot = os.path.join(paras.output_file_path, "user.annot")
    uout_mode = os.path.join(paras.output_file_path, "user.mode")

    print('inactive:', paras.inactive_user)

    file_dict = {}

    file_dict["marking"] = {
        "src": open(mout_src, 'w'),
        "target": open(mout_target, 'w'),
        "annot": open(mout_annot, 'w')
    }

    file_dict["postedit"] = {
        "src": open(pout_src, 'w'),
        "target": open(pout_target, 'w'),
        "annot": open(pout_annot, 'w')
    }

    file_dict["user"] = {
        "src": open(uout_src, 'w'),
        "target": open(uout_target, 'w'),
        "annot": open(uout_annot, 'w'),
        "mode": open(uout_mode, 'w')
    }

    for a in annotations:
    
        mode = a.feedback_type
        if mode == fb_type.marking:
            mode_str = "marking"
        elif mode == fb_type.post_edit:
            mode_str = "postedit"
        else:
            mode_str = "user"
        # Check the current sample is marked or post-edited.
        target_split = a.target.split()

        # Output 
        file_dict[mode_str]["src"].write(a.src + "\n")
        file_dict[mode_str]["target"].write(a.target + "\n")
        if mode == fb_type.marking:
            ## "true" <=> marked <=> bad
            ## convert the "true", "false" into 1 and 0 
            annotation = a.annotation
            annotation = annotation.split(',')
            feedback = [0 if mark == "true" else 1 for mark in annotation]
            feedback = [str(x) for x in feedback]
            feedback = " ".join(feedback)                
            file_dict[mode_str]["annot"].write(feedback + "\n")
        elif mode == fb_type.post_edit:
            post_edit = a.annotation

            # Filter html tags due to improper submission of text format
            post_edit = re.sub('<[^>]*>', '', post_edit)
            post_edit = post_edit.replace("&nbsp;", "")

            ## The spacing of ? and 's are not of the same format
            post_edit = post_edit.replace("?", " ?")
            post_edit = post_edit.replace("'s", " 's")

            post_edit = " ".join(post_edit.split())

            file_dict[mode_str]["annot"].write(post_edit + "\n")
        else:
            uc = a.user_choice
            if uc == fb_type.marking:
                annotation = a.annotation
                annotation = annotation.split(',')
                feedback = [0 if mark == "true" else 1 for mark in annotation]
                feedback = [str(x) for x in feedback]
                feedback = " ".join(feedback)                
                file_dict[mode_str]["annot"].write(feedback + "\n")
                file_dict[mode_str]["mode"].write("1\n")
            else:
                post_edit = a.annotation

                # Filter html tags due to improper submission of text format
                post_edit = re.sub('<[^>]*>', '', post_edit)
                post_edit = post_edit.replace("&nbsp;", "")

                ## The spacing of ? and 's are not of the same format
                post_edit = post_edit.replace("?", " ?")
                post_edit = post_edit.replace("'s", " 's")

                post_edit = " ".join(post_edit.split())

                file_dict[mode_str]["annot"].write(post_edit + "\n")
                file_dict[mode_str]["mode"].write("0\n")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get source, target, annotation & reward from database')
    parser.add_argument('output_file_path', type=str)
    parser.add_argument('--inactive_user', nargs='+', type=int, default=None,
        help='A list of indexes telling which user ids are inactive')
    paras = parser.parse_args()

    extract_data(paras)

