class Matrix:
    rows, cols = 0, 0
    state = []

    def __init__(self, rows, cols: int):
        try:
            self.rows, self.cols = rows, cols
            self.state = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        except TypeError:
            self.rows, self.cols = 0, 0
            print("ERROR")

    def get_state_printable(self):
        matrix_printable = ""
        for row in self.state:
            for col in row:
                matrix_printable = matrix_printable + str(col) + " "
            matrix_printable += "\n"
        return matrix_printable

    def get_state_printable_round(self, digits):
        temp_matrix = Matrix(self.rows, self.cols)
        max_size = 1
        for row in range(self.rows):
            for col in range(self.cols):
                # delete -0.0 and so on
                if self.state[row][col] == 0:
                    self.state[row][col] = round(temp_matrix.state[row][col])
                # calculate max_size and turn values into strings
                temp_matrix.state[row][col] = str(round(self.state[row][col], digits))
                if len(temp_matrix.state[row][col]) > max_size:
                    max_size = len(temp_matrix.state[row][col])
        # increase all string values to the max_size
        for row in range(temp_matrix.rows):
            for col in range(temp_matrix.cols):
                diff = max_size - len(temp_matrix.state[row][col])
                temp_matrix.state[row][col] = " " * diff + temp_matrix.state[row][col]
        return temp_matrix.get_state_printable()

    def add_matrix(self, matrix):
        rows, cols = matrix.rows, matrix.cols
        if rows == self.rows and cols == self.cols:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.state[row][col] += matrix.state[row][col]
            return True
        else:
            return False

    def multiply_by_constant(self, constant):
        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.state[row][col] *= constant
            return True
        except TypeError:
            return False

    def multiply_by_matrix(self, matrix):
        rows, cols = matrix.rows, matrix.cols
        if self.cols == rows:
            temp_matrix = Matrix(self.rows, cols)
            for row in range(temp_matrix.rows):
                for col in range(temp_matrix.cols):
                    for _ in range(rows):
                        temp_matrix.state[row][col] += self.state[row][_] * matrix.state[_][col]
            self.rows, self.cols, self.state = temp_matrix.rows, temp_matrix.cols, temp_matrix.state
            return True
        else:
            return False

    def transpose(self, transpose_type):
        if transpose_type not in (1, 2, 3, 4):
            return False
        else:
            # main diagonal
            if transpose_type == 1:
                temp_matrix = Matrix(self.cols, self.rows)
                for row in range(temp_matrix.rows):
                    for col in range(temp_matrix.cols):
                        temp_matrix.state[row][col] = self.state[col][row]
            # side diagonal
            elif transpose_type == 2:
                temp_matrix = Matrix(self.cols, self.rows)
                for row in range(temp_matrix.rows):
                    for col in range(temp_matrix.cols):
                        temp_matrix.state[row][col] = self.state[self.cols - col - 1][self.rows - row - 1]
            # vertical line
            elif transpose_type == 3:
                temp_matrix = Matrix(self.rows, self.cols)
                for row in range(temp_matrix.rows):
                    for col in range(temp_matrix.cols):
                        temp_matrix.state[row][col] = self.state[row][self.cols - col - 1]
            # horizontal line
            else:  # transpose_type == 4:
                temp_matrix = Matrix(self.rows, self.cols)
                for row in range(temp_matrix.rows):
                    for col in range(temp_matrix.cols):
                        temp_matrix.state[row][col] = self.state[self.rows - row - 1][col]

            self.rows, self.cols, self.state = temp_matrix.rows, temp_matrix.cols, temp_matrix.state
            return True

    def get_minor(self, del_r: int, del_c: int):
        if type(del_r) != int or type(del_c) != int:
            return False
        if self.rows < 2 or self.cols < 2:
            return False
        if del_r > self.rows or del_c > self.cols:
            return False
        try:
            temp_matrix = Matrix(self.rows - 1, self.cols - 1)
            state = []
            for row in range(self.rows):
                if row != del_r:
                    state.append([])
                    for col in range(self.cols):
                        if col != del_c:
                            state[-1].extend([self.state[row][col]])

            temp_matrix.state = state
            return temp_matrix
        except IndexError:
            return False

    def get_cofactor(self, row: int, col: int):
        if type(row) != int or type(col) != int:
            return False
        if self.rows < 2 or self.cols < 2:
            return False
        if row > self.rows or col > self.cols:
            return False
        return (-1) ** (row + col + 2) * self.get_minor(row, col).get_determinant()

    def get_determinant(self):
        if self.rows != self.cols:
            return False
        if self.rows == 1:
            return self.state[0][0]
        else:
            det = 0
            for col in range(self.cols):
                det += self.state[0][col] * self.get_cofactor(0, col)
            return det

    def inverse(self):
        if not self.get_determinant():
            return False
        if self.get_determinant() == 0:
            return False
        temp_matrix = Matrix(self.rows, self.cols)
        for row in range(temp_matrix.rows):
            for col in range(temp_matrix.cols):
                temp_matrix.state[row][col] = self.get_cofactor(row, col)
        temp_matrix.transpose(1)
        temp_matrix.multiply_by_constant(1 / self.get_determinant())
        self.state = temp_matrix.state
        return True


def get_choice():
    return input("Your choice: > ")


def get_result(user_choice: str):
    if user_choice == "1":
        matr1 = read_matrix("first ")
        if not matr1:
            return False
        matr2 = read_matrix("second ")
        if not matr2:
            return False
        success = matr1.add_matrix(matr2)
        return matr1.get_state_printable() if success else False

    elif user_choice == "2":
        matr = read_matrix("")
        if not matr:
            return False
        const = read_constant()
        if not const:
            return False
        success = matr.multiply_by_constant(const)
        return matr.get_state_printable() if success else False

    if user_choice == "3":
        matr1 = read_matrix("first ")
        if not matr1:
            return False
        matr2 = read_matrix("second ")
        if not matr2:
            return False
        success = matr1.multiply_by_matrix(matr2)
        return matr1.get_state_printable() if success else False

    if user_choice == "4":
        print("\n1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line")
        transpose_type = get_choice()
        if transpose_type not in ("1", "2", "3", "4"):
            return False
        matr = read_matrix("")
        if not matr:
            return False
        success = matr.transpose(int(transpose_type))
        return matr.get_state_printable() if success else False

    if user_choice == "5":
        matr = read_matrix("")
        if not matr:
            return False
        success = matr.get_determinant()
        return str(success) + "\n" if success else False

    if user_choice == "6":
        matr = read_matrix("")
        if not matr:
            return False
        success = matr.inverse()
        return matr.get_state_printable() if success else False


def read_matrix(matr_type=""):
    try:
        rows, cols = map(int, input(f"Enter size of {matr_type}matrix: > ").split())
        matrix = Matrix(rows, cols)
    except ValueError:
        return False

    print(f"Enter {matr_type}matrix:")
    for row in range(rows):
        try:
            curr_row = list(map(float, input("> ").split()))
        except ValueError:
            return False
        if len(curr_row) != cols:
            return False
        for col in range(cols):
            if curr_row[col] == int(curr_row[col]):
                curr_row[col] = int(curr_row[col])
            matrix.state[row][col] += curr_row[col]
    return matrix


def read_constant():
    try:
        constant = float(input("Enter constant: > "))
    except ValueError:
        return False
    if constant == int(constant):
        constant = int(constant)
    return constant


if __name__ == "__main__":
    choice = ""

    while choice != "0":
        print("1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n"
              "4. Transpose matrix\n5. Calculate a determinant\n6. Inverse matrix\n0. Exit")
        choice = get_choice()
        if choice in ("1", "2", "3", "4", "5", "6"):
            result = get_result(choice)
            print("The result is:", result, sep="\n") if result else print("The operation cannot be performed.\n")
        elif choice == "0":
            pass
        else:
            print("No such option\n")
