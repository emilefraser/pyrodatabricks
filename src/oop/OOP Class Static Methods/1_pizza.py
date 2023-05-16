class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __repr__(self):
        return f'Pizza({self.ingredients})'

p = Pizza(['cheese','tomatoes'])
p = Pizza(['cheese','tomatoes','ham'])
p = Pizza(['cheese','tomatoes','ham','mushrooms'])
