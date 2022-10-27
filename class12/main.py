import pickle
def write():
    f = open("School.dat", "wb")
    l = []
    for i in range(4):
        r = input("r")
        n = input("n")
        m = input("m")
        g = input("g")
        data = [r,n,m,g]
        l.append(data)
    pickle.dump(l,f)
    f.close()
def display():
 f = open("School.dat", "rb")
 l = pickle.load(f)
 for i in l:
     print(*i)
 f.close()

def count():
    c = 0
    f = open("School.dat", "rb")
    l = pickle.load(f)
    for i in l:
        if i[1][0] == "r":
            c+=1
    print("No of students", c)
    f.close()

def update():
    c = 0
    f = open("School.dat", "rb")
    l = pickle.load(f)
    for i in l:
        if i[1][0] == "r":
            i[2] = i[2]*120
            c+=1
    f.close()
    f = open("School.dat", "wb")
    if c>0:
        pickle.dump(l,f)
    else:
        print("No updates")
    f.close()

def delete():
    f = open("School.dat", "rb")
    l = pickle.load(f)
    c = 0
    for i in l:
        if i[2]>70:
            l.remove(i)
            c+=1
    f.close()
    f = open("School.dat", "wb")
    if c>0:
        pickle.dump(l,f)
    else:
        print("No Updates")
    f.close()


display()
count()
delete()