from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, login, password):
        self.id = login
        self.password = password       

    def __repr__(self):
        return "%s/%s" % (self.login, self.password)
