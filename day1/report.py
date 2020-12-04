
with open('input.txt', 'r') as f: 
    lines = f.readlines()

numbers = [int(l.strip()) for l in lines]

# print(numbers)

# # not great soln
# for i in numbers: 
#     for j in numbers: 
#         if i+j == 2020:
#             print(i*j)
#             break

def go():
    for i in range(len(numbers)): 
        for j in range(i, len(numbers)):
            if numbers[i]+numbers[j] == 2020:
                print(numbers[i]*numbers[j])
                return
            j += 1
        i += 1
    
go()

