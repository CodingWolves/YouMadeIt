from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, _id):
        self.id = _id
        self.name = "user" + str(_id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
