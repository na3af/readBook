activate_this = '/project.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))