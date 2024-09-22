
class CreateProduct:
    def __init__(self, obj):
        self.name = obj['name']
        self.description = obj['description']
        self.slug = obj['slug']
        self.brand_id = obj['brand_id']


class UpdateProduct:
    def __init__(self, obj):
        self.name = obj['name']
        self.description = obj['description']
        self.slug = obj['slug']
        self.brand_id = obj['brand_id']
