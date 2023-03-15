import os 
from clause import Clause, negative

# Xu ly doc file input 
# Luc doc vao can chuan hoa no ve thanh danh sach cac chuoi (tao clause) 
def readFile(filename):
    with open(filename, 'r') as fi:
        clauses = []
        # luc readline ta se nhan duoc chuoi string ta se xu ly chuoi do
        # ta can xoa cac khoang trang va tac no thanh chuoi cac string qua split("OR")
        alpha = fi.readline().splitlines()[0].replace(' ', '').split("OR")
        # them cac menh de kb
        N_KB = int(fi.readline())
        for i in range(N_KB):
            clause = Clause((fi.readline().splitlines()[0].replace(' ', '').split("OR")))
            clauses.append(clause)

        #Ta xu ly viet alpha co nhieu literal. Vi sau khi phu dinh OR -> AND 
        # vi the moi phu dinh cua literal se la mot menh de
        for i in alpha:
            clauses.append(Clause([negative(i)]))
    return clauses

#xu li hop giai va in ket qua
def PL_Resolution(filenameIN, indexFile):
    # doc file input va lay du lieu
    # print(filenameIN)
    clauses = readFile(filenameIN)
    # print("Testcase " , indexFile)

    # lay dia chi thu muc output
    pathParentOutput = '.\OUTPUT'
    # tao dia chi file output trong thu muc
    filenameOut = pathParentOutput + '\\' + 'out' + indexFile
    with open(filenameOut, 'w') as fo: # mo file de gi ket qua 
        while True:
            new = []
            # duyet het ta ca cac cap menh de
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    c1 = clauses[i]
                    c2 = clauses[j]
                    res = Clause.PL_Resolve(c1, c2) # hop giai 2 menh de
                    # kiem tra xem co tao ra menh de khong va menh de do co phai la menh de moi khong
                    if res and res.check() and res not in clauses and res not in new:
                        new.append(res)
                        #print(str(c1) + " Hop giai" + stc(c2) + " ==> " + str(res))
            # ghi ket qua. Dau tien ghi sao menh de moi duoc tao ra
            fo.write(str(len(new)) + '\n')
            if new == []: # neu khong tao ra duoc menh de moi thi ta in ra NO va dung viec hop giai
                fo.write("NO")
                break
            else:
                clauses = clauses + new # upadate lai menh de
                for literal in new:
                    fo.write(str(literal) + '\n') # in cac menh de moi duoc tao ra
            if Clause([]) in new: # neu nhu da xuat hien cap menh de doi khang thi in ra YES va dung chuong trinh
                fo.write("YES")
                break

# xu  ly viec doc cac file input
def handleReadFile():
    #lay dia chi cha cua thu muc input
    pathParentInput = os.path.join(os.curdir,'INPUT')
    dir_list = os.listdir(pathParentInput)
    for i in range(len(dir_list)):
        numInput = dir_list[i][dir_list[i].find('put'):] # lay phan sau cua file input de tao file output tuong ung
        path = os.path.join(pathParentInput,dir_list[i]) # lay dia chi file
        PL_Resolution(path, numInput)


#main
handleReadFile()
#end