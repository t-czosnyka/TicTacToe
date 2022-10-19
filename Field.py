class Field:

    def __init__(self):
        self.value = " "

    def set(self, player):
        if self.value == " ":
            if player == 1:
                self.value = "X"
                return True
            elif player == 2:
                self.value = "O"
                return True
            else:
                print("Wrong player number.")
                return False
        else:
            print("Field already set.")
            return False

    def get(self):
        return self.value