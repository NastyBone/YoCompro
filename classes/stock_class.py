

class CreateStock:
    def __init__(self, obj):
        self.quantity = obj['quantity']
        self.price = obj['price']
        self.discount = obj['discount']
        self.product_id = obj['product_id']
        self.bussiness_id = ['bussiness_id']


class UpdateStock:
    def __init__(self, obj):
        self.quantity = obj['quantity']
        self.price = obj['price']
        self.discount = obj['discount']
