
class CreateBussiness:
    def __init__(self, obj):
        self.name = obj['name']
        self.email = obj['email']
        self.address = obj['address']
        self.phone = obj['phone']
        self.description = obj['description']
        self.slug = obj['slug']
        self.rif = obj['rif']
        self.lat = obj['lat']
        self.lon = obj['lon']
        self.city = obj['city']
        self.user_id = obj['user_id']


class UpdateBussiness:
    def __init__(self, obj):
        self.name = obj['name']
        self.email = obj['email']
        self.address = obj['address']
        self.phone = obj['phone']
        self.description = obj['description']
        self.slug = obj['slug']
        self.rif = obj['rif']
        self.lat = obj['lat']
        self.lon = obj['lon']
        self.city = obj['city']
