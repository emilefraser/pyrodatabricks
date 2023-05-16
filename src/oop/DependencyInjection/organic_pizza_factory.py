from pizza_factory import Pizza, DoughFactory

class OrganicDoughFactory(DoughFactory):

    def get_dough(self):
        return "Pure untreated wheat dough"

class OrganicPizza(Pizza, OrganicDoughFactory):
    pass

if __name__ == "__main__":
    OrganicPizza().order("Pepperoni", "Bell Pepper")