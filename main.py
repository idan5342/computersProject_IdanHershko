from matplotlib import pyplot


def fit_linear(input_file):
    def is_rows(input_file):  # returns true if the input file has table of rows,otherwise false
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        line = data[0]
        line = line.lower()
        if 'x' in line and 'y' in line:
            return False
        return True

    def length_rows(input_file):  # rows table,  true if the length of each row is the same, else return false
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        line = data[0]
        list_line = line.split()
        length = len(list_line)
        for i in range(0, 4):
            line = data[i]
            list_line = line.split()
            if len(list_line) != length:
                return False
        return True

    def length_columns(input_file):  # columns table,  true if the length of each row is the same, else return false
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        for line in data:
            list_line = line.split()
            if list_line == []:
                break
            if 'axis' in line:
                break
            if len(list_line) != 4:
                return False
        return True

    def positive_rows(input_file):  # rows table, returns true if the values of the dx,dy are + else false
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        for i in range(0, 4):
            line = data[i]
            list_line = line.split()
            if len(list_line[0]) == 2:
                for item in list_line:
                    try:
                        num = float(item)
                    except:
                        continue
                    else:
                        if num <= 0:
                            return False
        return True

    def positive_columns(input_file):  # columns table, returns true if the values of the dx,dy are + else false
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        first_line = data[0]
        first_line = first_line.lower()
        first_list = first_line.split()
        dx = -1
        dy = -1
        for word in first_list:
            if 'dx' == word:
                dx = first_list.index(word)
            if 'dy' == word:
                dy = first_list.index(word)
        if dx == -1 or dy == -1:
            return False
        for line in data:
            list_line = line.split()
            if line != data[0]:
                if list_line == []:
                    break
                if float(list_line[dx]) <= 0 or float(list_line[dy]) <= 0:
                    return False
        return True

    def check(input_file):
        if is_rows(input_file):
            if length_rows(input_file):
                if positive_rows(input_file):
                    return True
                else:
                    print("Input file error: Not all uncertainties are positive")
            else:
                print("Input file error: Data lists are not the same length")
        else:
            if length_columns(input_file):
                if positive_columns(input_file):
                    return True
                else:
                    print("Input file error: Not all uncertainties are positive")
            else:
                print("Input file error: Data lists are not the same length")
        return False

    def find_chi2(input_file):
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        chi2 = 0
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        a = find_a(input_file)
        b = find_b(input_file)
        x = table[0]
        y = table[2]
        dy = table[3]
        for column in range(1, len(table[0])):
            part_of_sum = (y[column] - (a * x[column] + b)) / dy[column]
            chi2 = chi2 + (part_of_sum ** 2)
        return chi2

    def create_table(input_file, data):
        if is_rows(input_file) == True:
            table = []
            for i in range(0,4):
                data[i] = data[i].lower()
            titles = ['x', 'dx', 'y', 'dy']
            for j in range(0, 4):  # the for loop builts a 2dim list that represents the table(x,dx,y,dy)
                for i in range(0, 4):
                    if j == 0 or j == 2:
                        if data[i][0] == titles[j]:
                            table.append(data[i].split())
                    else:
                        if data[i][0] == titles[j][0] and data[i][1] == titles[j][1]:
                            table.append(data[i].split())
        else:
            table = [['x'], ['dx'], ['y'], ['dy']]
            titles = ['x', 'dx', 'y', 'dy']
            first_line = data[0]
            first_line = first_line.lower()
            list_first_line = first_line.split()
            indexs = []
            for i in range(0, 4):
                indexs.append(list_first_line.index(titles[i]))
            for line in data:
                line = line.lower()
                list_line = line.split()
                if list_line == []:
                    break
                if list_line == list_first_line:
                    continue
                for i in range(0, 4):
                    table[i].append(list_line[indexs[i]])
        for row in table:
            for i in range(1, len(row)):
                row[i] = float(row[i])
        return table

    def calculate_x_hat(x, dx, y, dy):
        sum_mone = 0
        sum_mechane = 0
        for i in range(1, len(x)):
            sum_mone = sum_mone + (x[i] / (dy[i]) ** 2)
            sum_mechane = sum_mechane + (1 / (dy[i]) ** 2)
        x_hat = sum_mone / sum_mechane
        return x_hat

    def calculate_x2_hat(x, dx, y, dy):
        sum_mone = 0
        sum_mechane = 0
        for i in range(1, len(x)):
            sum_mone = sum_mone + ((x[i]) ** 2 / (dy[i]) ** 2)
            sum_mechane = sum_mechane + (1 / (dy[i]) ** 2)
        x2_hat = sum_mone / sum_mechane
        return x2_hat

    def calculate_xy_hat(x, dx, y, dy):
        sum_mone = 0
        sum_mechane = 0
        for i in range(1, len(x)):
            sum_mone = sum_mone + ((x[i] * y[i]) / (dy[i]) ** 2)
            sum_mechane = sum_mechane + (1 / (dy[i]) ** 2)
        xy_hat = sum_mone / sum_mechane
        return xy_hat

    def calculate_y_hat(x, dx, y, dy):
        sum_mone = 0
        sum_mechane = 0
        for i in range(1, len(y)):
            sum_mone = sum_mone + (y[i] / (dy[i]) ** 2)
            sum_mechane = sum_mechane + (1 / (dy[i]) ** 2)
        y_hat = sum_mone / sum_mechane
        return y_hat

    def calculate_dy2_hat(x, dx, y, dy):
        sum_mone = 0
        sum_mechane = 0
        for i in range(1, len(y)):
            sum_mone = sum_mone + ((dy[i]) ** 2 / (dy[i]) ** 2)
            sum_mechane = sum_mechane + (1 / (dy[i]) ** 2)
        dy2_hat = sum_mone / sum_mechane
        return dy2_hat

    def find_a(input_file):
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        a = 0
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        xy_hat = calculate_xy_hat(table[0], table[1], table[2], table[3])
        x_hat = calculate_x_hat(table[0], table[1], table[2], table[3])
        y_hat = calculate_y_hat(table[0], table[1], table[2], table[3])
        x2_hat = calculate_x2_hat(table[0], table[1], table[2], table[3])
        a = (xy_hat - (x_hat * y_hat)) / (x2_hat - (x_hat) ** 2)
        return a

    def find_b(input_file):
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        a = 0
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        x_hat = calculate_x_hat(table[0], table[1], table[2], table[3])
        y_hat = calculate_y_hat(table[0], table[1], table[2], table[3])
        a = find_a(input_file)
        b = y_hat - (x_hat * a)
        return b

    def find_da(input_file):
        import math
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        a = 0
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        N = len(table[0]) - 1
        dy2_hat = calculate_dy2_hat(table[0], table[1], table[2], table[3])
        x2_hat = calculate_x2_hat(table[0], table[1], table[2], table[3])
        x_hat = calculate_x_hat(table[0], table[1], table[2], table[3])
        da2 = dy2_hat / (N * (x2_hat - (x_hat ** 2)))
        da = math.sqrt(da2)
        return da

    def find_db(input_file):
        import math
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        a = 0
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        N = len(table[0]) - 1
        dy2_hat = calculate_dy2_hat(table[0], table[1], table[2], table[3])
        x2_hat = calculate_x2_hat(table[0], table[1], table[2], table[3])
        x_hat = calculate_x_hat(table[0], table[1], table[2], table[3])
        db2 = (dy2_hat * x2_hat) / (N * (x2_hat - (x_hat ** 2)))
        db = math.sqrt(db2)
        return db

    def find_chi2_red(input_file):
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        if check(input_file) == False:
            return None
        for i in range(0, len(data)):
            data[i] = data[i].lower()
        table = create_table(input_file, data)
        N = len(table[0]) - 1
        chi2 = find_chi2(input_file)
        chi2_red = chi2 / (N - 2)
        return chi2_red

    def show_graph(input_file):
        file_open = open(input_file, 'r')
        data = file_open.readlines()
        table = create_table(input_file, data)
        x_axis = data[len(data) - 2]
        y_axis = data[len(data) - 1]
        x_axis = x_axis[7:].strip()
        y_axis = y_axis[7:].strip()
        x = table[0]
        if 'x' in x:
            x.remove('x')
        dx = table[1]
        if 'dx' in dx:
            dx.remove('dx')
        y = table[2]
        if 'y' in y:
            y.remove('y')
        y_lin = []
        for i in range(0, len(x)):
            y_lin.append(a * x[i] + b)
        dy = table[3]
        if 'dy' in dy:
            dy.remove('dy')
        pyplot.plot(x, y_lin, 'r')
        pyplot.errorbar(x, y, xerr=dx, yerr=dy, ecolor='b', fmt='None')
        pyplot.xlabel(x_axis)
        pyplot.ylabel(y_axis)
        pyplot.savefig("linear_fit.SVG", format='SVG')
        pyplot.show()

    if check(input_file):
        a = find_a(input_file)
        da = find_da(input_file)
        print("a = {0} +- {1}".format(a, da))
        b = find_b(input_file)
        db = find_db(input_file)
        print("b = {0} +- {1}".format(b, db))
        chi2 = find_chi2(input_file)
        print("chi2 = {0}".format(chi2))
        chi2_red = find_chi2_red(input_file)
        print("chi2_reduced = {0}".format(chi2_red))
        show_graph(input_file)


# main program
print("Please enter input file name(without .txt):")
input_text = input() + ".txt"
fit_linear(input_text)