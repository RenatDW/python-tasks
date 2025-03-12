def main ():
   dict = parse_file()

def parse_file():
    with open('input.txt') as f:
        s = f.readlines()
        dict = {}
        ans = [[]]
        a = [[0]*3]* len(s)
        for i in range(len(s)):
            line = s[i].split(" ")
            a[i] = list(map(int, line))
            if float(line[1]) == 0:
                return
            coef = float(line[0])/float(line[1])
            if coef in dict:
                dict[coef] += 1
            else:
                dict[coef] = 1

    for third in a:
        if float(third[0]/third[1]) == max(dict,key=dict.get):
            ans.append(third)
    print(ans[1:])
    return a
   
def save_in_file(c):
    ans = ""
    a = []
    for i in range(len(c)):
        for j in range(len(c[0])):
            if j == 0:
                ans += str(c[i][j])
            else:
                ans += " " + str(c[i][j])
        ans += "\n"
        

    with open("output.txt", "w") as file:
        file.write(ans)

    
if __name__ == '__main__':
    main()