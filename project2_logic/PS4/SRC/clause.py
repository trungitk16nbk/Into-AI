# importing copy module 
import copy

# Phu dinh literal
def negative(literal:str):
    if literal[0] == '-':
        return literal[1]
    return '-' + literal[0]

#tao lop menh de vi du: A OR -B OR C
# co thuoc tinh la clause la 1 list cua literal (ta se luu duoi dang la 1 list string)
class Clause:
    def __init__(self, clause:list):
        self.clause = clause
        self.normalize() # trong luc khoi tao minh chuan hoa clause
    
    #chuan hoa cac literal trong clause duoc sap xep theo thu tu chu cai
    def normalize(self):
        self.clause = list(set(self.clause)) # dung de xoa cac literal trung nhau 
        return self.clause.sort(key=lambda x: x[-1]) # sap xep theo bang chu cai (neu dang phu dinh thi ta sap xep theo khang dinh cua no)

    # kiem tra clause co phai la mot chan ly hay khong. Neu la chan ly thi no vo nghia ta khong can phai xet
    def check(self):  
        for literal in self.clause:
            if negative(literal) in self.clause:  # ton tai cap doi khang trong 1 menh de
                return False
        return True
    
    # operator <<. Dung de in ra cac menh de dung format
    def __str__(self):
        if self.clause == []:  # truong hop tim duoc 2 menh de doi khang thi in {}
            return '{}'
        return ' OR '.join(self.clause) # in ra menh de binh thuong

    # operator ==
    def __eq__(self, obj):
        return set(obj.clause) == set(self.clause)
    
    # Ham hop giai 2 menh de
    @staticmethod
    def PL_Resolve(clause1, clause2): 
        # ta thuc hien copy cac menh de thuc hien hop giai va khong lam thay doi menh de
        # ta dung deepcopy nham tao ra file copy voi vung nho moi
        c1 = copy.deepcopy(clause1.clause)  
        c2 = copy.deepcopy(clause2.clause)

        # Ta duyet het 2 menh de 
        for i in range(len(c1)):
            for j in range(len(c2)):
                # neu tim duoc 1 cap literal doi khang giua 2 menh de thi ta xoa ca 2 di va hop giai lai thanh 1 menh de
                if i < len(c1) and j < len(c2) and c1[i] == negative(c2[j]):
                    c1.pop(i)
                    c2.pop(j)
                    return Clause(c1 + c2) # tao menh de hop giai
        return None # neu ca 2 khong co cap literal doi khang nao thi ta khong the hop giai va return None
    