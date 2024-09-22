class CreateBrand:
    def __init__(self, obj):
        self.name = obj['name']
        self.slug = obj['slug']
        self.country = obj['country']


class UpdateBrand:
    def __init__(self, obj):
        self.name = obj['name']
        self.slug = obj['slug']
        self.country = obj['country']
