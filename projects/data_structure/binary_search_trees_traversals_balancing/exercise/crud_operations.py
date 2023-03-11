from binary_search_trees_traversals_balancing.exercise.user_registration import User
from test_data import rushikesh, aakash, biraj, siddhant
import timeit
import cProfile


class UserDatabase:
    def __init__(self):
        self.users = []

    def insert(self, user):
        i = 0
        while i < len(self.users):
            # Find the First username greater than the new user's username
            if self.users[i][0] < user[0]:
                break
            i += 1
        self.users.insert(i, user)

    def find(self, username):
        for user in self.users:
            if user[0] == username:
                return user

    def update(self, user):
        target = self.find(user.username)
        target[1], target[2] = user.name, user.email

    def list_all(self):
        return self.users


if __name__ == "__main__":
    database = UserDatabase()
    database.insert(list(rushikesh))
    database.insert(list(aakash))
    database.insert(list(biraj))
    user_obj = database.find('biraj')
    print(f"{user_obj}")
    database.update(User(username=biraj[0], name='Biraj N', email='birajn@example.com'))
    user_obj = database.find('biraj')
    print(f"After updating biraj record in database {user_obj}")
    print(f"All users list, \n{database.list_all()}")
    database.insert(list(siddhant))
    print(f"Lets Verify new record successfully inserted")
    print(f"After record insertion, \n{database.list_all()}")

    # Below code is for to test Thoroughly by using for loop iterations
    # cProfile.run("[i for i in range(10000000)]")
