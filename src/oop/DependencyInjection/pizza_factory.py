class DoughFactory(object):
    def get_dough(self):
        return "insectide treated wheat dough"


class Pizza(DoughFactory):

    def order(self, *toppings):
        print("Getting dough")
        dough = super().get_dough()
        print("Making pizza with %s" % dough)
        for topping in toppings:
            print("Adding: %s" % topping)


if __name__ == "__main__":
    Pizza().order("Pepperoni", "Bell Pepper")