class CreateTag:
    def __init__(self, obj):
        self.name = obj['name']
        self.description = obj['description']


class UpdateTag:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
