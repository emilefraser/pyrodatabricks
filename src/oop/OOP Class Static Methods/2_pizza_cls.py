class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __repr__(self):
        return f'Pizza({self.ingredients})'

    @classmethod
    def margherita(cls):
        return cls(['cheese','tomatoes'])

    @classmethod
    def prosciutto(cls):
        return cls(['cheese','tomatoes'])

p = Pizza.margherita()
p = Pizza.prosciutto()