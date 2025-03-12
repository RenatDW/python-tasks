def main ():
    a = []
    c = []
    
    parse_file(a)
    dif = {}
    for i in range(len(a) - 1):
        if a[i + 1] - a[i] in dif:
            dif[a[i + 1] - a[i]] +=1
        else:
            dif[a[i + 1] - a[i]] = 1
    
    print(dif)
    save_in_file(c)
    
    

def parse_file(a):
    with open('input.txt') as f:
        s = f.readline()
        s = s.split(",")
        for el in s:
            a.append(int(el))
        
def save_in_file(c):
    ans = ""
    for i in range(len(c)):
        if i == 0:
            ans += str(c[i])
        else:
            ans += ", " + str(c[i])

    with open("output.txt", "w") as file:
        file.write(ans)

    
if __name__ == '__main__':
    main()