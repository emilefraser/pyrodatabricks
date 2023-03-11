from test_data import rushikesh, aakash, biraj, hemanth, jadhesh, siddhant, sonaksh, vishal


class User:
    def __init__(self, username, name, email):
        self.username = username
        self.name = name
        self.email = email

    def introduce_yourself(self, guest_name):
        print(f"Hi {guest_name}, I am {self.name}! Contact me at {self.email}")

    def __repr__(self):
        return f"User(username= {self.username}, name= {self.name}, email= {self.email})"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    # print(rushikesh)
    rushikesh = User(rushikesh[0], rushikesh[1], rushikesh[2])
    aakash = User(aakash[0], aakash[1], aakash[2])
    biraj = User(biraj[0], biraj[1], biraj[2])
    hemanth = User(hemanth[0], hemanth[1], hemanth[2])
    jadhesh = User(jadhesh[0], jadhesh[1], jadhesh[2])
    siddhant = User(siddhant[0], siddhant[1], siddhant[2])
    sonaksh = User(sonaksh[0], sonaksh[1], sonaksh[2])
    vishal = User(vishal[0], vishal[1], vishal[2])
    print(f"User = {rushikesh}")
    # rushikesh.introduce_yourself('Rushi')
    all_users = [rushikesh, aakash, biraj, hemanth, jadhesh, siddhant, sonaksh, vishal]
    print(f"\nWe do print one of the user object value \n {biraj.username}, {biraj.name}, {biraj.email}\n")
    print(f"Prints user object directly here \n {rushikesh}")
    print(f"\nall users, \n {all_users}")


