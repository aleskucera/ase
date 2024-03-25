def read_numbers_from_file(file_name):
    numbers = []
    with open(file_name, 'r') as file:
        for line in file:
            # Split the line by spaces assuming each number is separated by spaces
            line_numbers = line.split(';')
            for num in line_numbers:
                # Convert ASCII representation to integer
                numbers.append(float(num))
    return numbers


file_name = 'measurements.txt'  # Change this to the path of your text file
numbers_array = read_numbers_from_file(file_name)

ntc1 = []
ntc2 = []
pt100 = []
egr_sens = []
meas_time = []

print(type(int(len(numbers_array) / 5)))
print(int(len(numbers_array) / 5))

for i in range(int(len(numbers_array) / 5)):
    for j in range(5):
        if j == 0:
            meas_time.append(numbers_array[i * 5 + j])
        elif j == 1:
            ntc2.append(numbers_array[i * 5 + j])
        elif j == 2:
            ntc1.append(numbers_array[i * 5 + j])
        elif j == 3:
            egr_sens.append(numbers_array[i * 5 + j])
        elif j == 4:
            pt100.append(numbers_array[i * 5 + j])

print("ntc1 = ", ntc1)
print("ntc2 = ", ntc2)
print("pt100 = ", pt100)
print("egr_sens = ", egr_sens)
print("meas_time = ", meas_time)
