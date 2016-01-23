class Parent():
    def __init__(self, last_name, eye_color):
        self.last_name = last_name
        self.eye_color = eye_color

    def show_info(self):
        print("Last Name - " + self.last_name)
        print("Eye Color - " + self.eye_color)


class Child(Parent):
    def __init__(self, last_name, eye_color, num_toys):
        Parent.__init__(self, last_name, eye_color)
        self.num_toys = num_toys

    def show_info(self):
        print("Last Name - " + self.last_name)
        print("Eye Color - " + self.eye_color)
        print("Number of Toys - " + str(self.num_toys))


billy_cyrus = Parent("cyrus", "blue")
miley_cyrus = Child("cyrus", "Blue", 5)


miley_cyrus.show_info()