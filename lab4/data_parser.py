def read_numbers_from_file(file_name):
    numbers = []
    with open(file_name, 'r') as file:
        for line in file:
            # Split the line by spaces assuming each number is separated by spaces
            line_numbers = line.split(' ')
            for num in line_numbers:
                # Convert ASCII representation to integer
                numbers.append(int(num))
    return numbers

file_name = '30cm.txt'  # Change this to the path of your text file
numbers_array = read_numbers_from_file(file_name)

lidar_lin = []
timestamp_lin = []
ultras_lin = []


print(type(int(len(numbers_array)/5)))
print(int(len(numbers_array)/5))

for i in range(int(len(numbers_array)/4)):
    for j in range(4):
        if(j==0):
            timestamp_lin.append(numbers_array[i*4+j])
        if(j==1):
            ultras_lin.append(numbers_array[i*4+j])
        if(j==2):
            lidar_lin.append(numbers_array[i*4+j])



print("timestamp_30 = ", timestamp_lin)
print("ultras_30 = ", ultras_lin)
print("lidar_30 = ", lidar_lin)

