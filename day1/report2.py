
with open('input.txt', 'r') as f: 
    lines = f.readlines()

numbers = [int(l.strip()) for l in lines]

def go():
    for i in range(len(numbers)): 
        for j in range(i, len(numbers)):
            for k in range(j, len(numbers)):
                if numbers[i]+numbers[j]+numbers[k] == 2020:
                    print(numbers[i]*numbers[j]*numbers[k])
                    return
                k += 1
            j += 1
        i += 1
    
go()

