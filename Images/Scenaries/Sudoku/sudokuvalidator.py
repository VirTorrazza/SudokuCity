
class sudoku:
    def __init__(self,b):
        self.board=b
        self.cbflag= True
        self.aux=[]
    
    def row_validator(self):
        listaaux2=[]
        flagbool=True
        for x in range (0, len (self.board)):
            listan=[1,2,3,4,5,6,7,8,9]
            lista= self.board[x]
            n=3
            sublists=[lista[i:i+n] for i in range (0, len(lista),n)]
            self.aux.extend(sublists)#list of lists
            sublists.clear()
            for y in range(0,len(lista)):
                if(lista[y]in listan):
                    listan.remove(lista[y])
                else:
                    flagbool=False
        return flagbool
        
    
    def column_validator(self):
        listaux2=[]
        flagbool=True
        for k in range(0, len(self.board)):
            for x in range(0,len(self.board)):
                listaux2.append(self.board[x][k])
       
            lista3=[1,2,3,4,5,6,7,8,9]
            for elem in listaux2:
            
                if (elem in lista3):
                
                    lista3.remove(elem)
                else:
                    flagbool=False
                    return flagbool

            
            listaux2.clear()
        return flagbool
    
           
    def subgrid_validator(self):
        lgrid=[]
        flagbool=True

        if (len(self.aux)==0):
            self.row_validator()
        else:
    
            for x in range(0,27,9):
                listel=[1,2,3,4,5,6,7,8,9]
                filn=0
                for y in range(0,3):
                    lgrid.extend(self.aux[filn])
                    filn+=3
                for e in lgrid:
                    if e in listel:
                        listel.remove(e)
                    else:
                        flagbool=False
                        return flagbool
                lgrid.clear()
    
        return flagbool
    
    def valid_solution(self):
        if(self.row_validator() and self.column_validator() and self.subgrid_validator()):
            self.cbflag=True
        else:
            self.cbflag= False
        
        return self.cbflag
    
    def print_isvalid(self):
        if self.valid_solution():
            print("The board is a valid sudoku")
        else:
            print("The board is not a valid suduku")

   
#a=valid sudoku example
y=[[5, 3, 4, 6, 7, 8, 9, 1, 2],
  [6, 7, 2, 1, 9, 5, 3, 4, 8],
  [1, 9, 8, 3, 4, 2, 5, 6, 7],
  [8, 5, 9, 7, 6, 1, 4, 2, 3],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 6, 1, 5, 3, 7, 2, 8, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 4, 5, 2, 8, 6, 1, 7, 9]]

a=[[0,0,0,0,0,0,0,7,6],
[0,3,7,0,0,6,9,0,5],
[5,2,0,0,0,0,8,3,0],
[0,5,4,0,0,0,0,9,8],
[0,7,0,0,0,8,3,0,0],
[0,8,0,0,3,0,0,5,0],
[2,6,0,0,0,5,0,0,4],
[0,0,0,2,0,4,0,0,3],
[0,0,0,0,7,0,0,2,0]]

c=[[0,5,6,2,0,3,8,7,0],
[2,0,0,7,6,0,0,3,0],
[3,0,0,0,0,8,0,0,0],
[4,6,0,5,0,0,7,2,0],
[0,0,0,9,8,7,4,6,5],
[0,0,0,6,0,2,0,0,8],
[6,3,2,0,0,0,0,4,0],
[0,0,5,0,0,0,0,8,0],
[0,0,0,0,0,0,5,0,0]]
#b=invalid sudoku example
b=[[5, 3, 4, 6, 7, 8, 9, 1, 2], 
  [6, 7, 2, 1, 9, 0, 3, 4, 8],
  [1, 0, 0, 3, 4, 2, 5, 6, 0],
  [8, 5, 9, 7, 6, 1, 0, 2, 0],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 0, 1, 5, 3, 7, 2, 1, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 0, 0, 4, 8, 1, 1, 7, 9]
]

s1=sudoku(a)
s2=sudoku(b)
s1.print_isvalid()
s2.print_isvalid()