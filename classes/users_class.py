class CreateUser:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


class UpdateUser:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class ResponseUser:
    def __init__(self, id: int, name: str, email: str, role: str):
        self.id = id
        self.name = name
        self.email = email
        self.role = role


class UserLogin(object):
    def __init__(self, id, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.id = id

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_city(self):
        return self.city

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def has_role(self, role):
        return role == self.role
