
class CreateRating:
    def __init__(self, obj):
        self.score = obj['score']
        self.comment = obj.get('comment', None)
        self.user_id = obj['user_id']
        self.bussiness_id = obj.get('bussiness_id', None)
        self.product_id = obj.get('product_id', None)


class UpdateRating:
    def __init__(self, obj):
        self.score = obj['score']
        self.comment = obj['comment']
        self.user_id = obj['user_id']
