'''
1. Реализовать функцию генерации графов сетей, позволяющую создавать случайный граф топологии кольцо, звезда и полносвязный, произвольной. 
2. Реализовать функцию, позволяющую визуализировать случайный граф в пакете graphvis. 
3. Реализовать классы тропических полуколец и функции алгоритмов решения систем линейных алгебраических уравнений над ними. 
4. В отчете привести результаты решения четырех примеров задачи сетевого планирования на графах с разной топологией. 
Сделать выводы о целесообразности применения аппарата тропической алгебры для решения задач сетевого планирования. 
Входные данные: топология графа.
Выходные данные: матрица смежности сгенерированного графа, результат решения задачи сетевого планирования на основе сгенерированных данных, промежуточные данные для последующей визуализации графа в программе graphvis.
'''

class Rmax: #
  zero = -float('inf') #тут пишем бесконечность
  
  
  def __init__(self,value=-float('inf')): #оператор инициализации
     self.value = value
  def __str__(self): #строку возвращаем
    return 'Rmax[' + str(self.value) + ']'
  def __add__(self,other): #оператор перегрузки сложение +
    return Rmax(max(self.value, other.value))
  def __mul__(self,other): #оператор перегрузки умножение *
    return Rmax(self.value + other.value)#Rmдax впереди,чтоб тип переопределить
  def __gt__(self,other): #оператор сравнения x>y возвращает true false
    return (self.value > other.value)
  def __truediv__(self,other): #оператор перегрузки деление /
    return Rmax(self.value - other.value)#Rmax впереди,чтоб тип переопределить
  def inv(self):
    return Rmax(-self.value)
  def  __eq__(self, other): # x == y
    return (self.value == other.value)
  def  __ne__(self, other): # x != y
    return (self.value != other.value)
  #def GenerateGraph(matrix):
    #return true
  
Rmax.unit = Rmax(0) #доп способ опр-я бесконечности  точка-принадлежность объекта к свойству классу
Rmax.zero = Rmax(-float('inf')) #бесконечность

class Matrix: #создаем класс матриц
  def __init__(self,rows=0,cols=0,data=[], T=Rmax): #в кач-ве свойст матрицы добавили размер - строка и столбец
    self.rows = rows #инициализации стр и столбца
    self.cols = cols
    if len(data) > 0:
      self.data = data #массив для хранения матрицы
    else:
      self.data = [[T() for j in range(cols)] for i in range(rows)]
    self.T = T # T обощение (способ сделать матрицу над другим типом) сейчас над Rmax
  def __str__(self): #строку возвращаем
    out= 'Matrix[\n'
    
    for i in range(self.rows):
      out += '\n'
      for j in range(self.cols):
        out+=str(self.data[i][j])  + ' '
    out += '\n]'
    return out
    
  def __add__(self,other): #оператор перегрузки сложение +
    result= Matrix(self.rows,self.cols,self.data,self.T)
    
    for i in range(self.rows):
      for j in range(self.cols):
        result.data[i][j]=self.data[i][j]+other.data[i][j]
    return result
    
  def __gt__(self,other): #оператор сравнения x>y возвращает true false
    result= Matrix(self.rows,self.cols,self.data,self.T)
    f=false
    for i in range(self.rows):
      for j in range(self.cols):
        f=(self.data[i][j]>other.data[i][j])
    return f 
    
  def  __eq__(self, other): # x == y
    result= Matrix(self.rows,self.cols,self.data,self.T)
    f=false
    for i in range(self.rows):
      for j in range(self.cols):
        f=(self.data[i][j]==other.data[i][j])
    return f 

  def  __ne__(self, other): # x != y
    result= Matrix(self.rows,self.cols,self.data,self.T)
    f=false
    for i in range(self.rows):
      for j in range(self.cols):
        f=(self.data[i][j]!=other.data[i][j])
    return f 

  def __mul__(self,other): #оператор перегрузки умножение * (для его работы перегрузим оператор >)
    
    result=Matrix(self.rows,self.cols,T=Rmax)
    for i in range(self.rows):
      maxM=Rmax(-float('inf'))
      for j in range(self.cols):
        sumM=Rmax(-float('inf'))
        for k in range(self.cols):
          if(other.data[k][j]==Rmax(0)):
            sumM=result.T.zero
          else:
            sumM=other.data[k][j]*self.data[i][k]
          if(sumM>maxM):
            maxM=sumM
          
          sumM=Rmax(-float('inf'))
          result.data[i][j]=maxM 
          
        maxM=Rmax(-float('inf'))
    #print(result)
    return result
  
  # if (self.data[i][k]!=Rmax(0)):
            #if (other.data[k][j]!=Rmax(0)):
                      #else: 
          #  sumM=result.T.zero
           # print(sumM)
  
  
  #def __mul__(self,other): #оператор перегрузки умножение *
    #result= Matrix(self.rows,self.cols,self.data,self.T)
    
    #for i in range(self.rows):
      #for j in range(self.cols):
        #sumM=Rmax(0)
        #for k in range(self.cols):
          #sumM+=self.data[i][k]*other.data[k][j]
          #result.data[i][j]=sumM
    #return result



  def __setitem__(self,key,item):
    self.data[key] = item
  
  def __getitem__(self, key):
    return self.data[key]

def zero(matrix): #оператор обнуления матрицы
   for i in range(matrix.rows):
    for j in range(matrix.cols):
      matrix[i][j]=matrix.T.zero
  
def unit(matrix): #оператор выведения единичной матрицы
   for i in range(matrix.rows):
    for j in range(matrix.cols):
      matrix[i][j]=matrix.T.unit
      
def eye(matrix): #оператор обнуления матрицы
   for i in range(matrix.rows):
    for j in range(matrix.cols):
      if i==j:
        matrix[i][j]=matrix.T.unit
      else:
        matrix[i][j]=matrix.T.zero

def pinv(matrix): #псевдообращение матрицы:транспонировать матрицу и поставить "-" везде, кроме 0 
  result=Matrix(matrix.cols,matrix.rows,T=Rmax)
  for i in range(result.cols):
    for j in range(result.rows):
      result[j][i]=matrix[i][j]
      if result[j][i]!=result.T.zero:
        result[j][i]=matrix[i][j].inv()
  return result

      
      #http://www.webgraphviz.com/
      #digraph G {
      #"0" -> "0"
     #"0" -> "1"
      #}
    
def GenerateGraph(matrix):
  result=Matrix(matrix.rows,matrix.cols,matrix.data,T=Rmax)
  
  print('digraph G {')
  for i in range(matrix.rows):
    for j in range(matrix.cols):
      if (matrix.data[i][j]!=Rmax(0)): # && matrix.data[i][j]!=Rmax(-float('inf'))
        if (matrix.data[i][j]!=Rmax(-float('inf'))):
          #print(result.data[i][j])
          print('"',i,'"',' -> ', '"',j,'"')
    
  print('}')
  
  
def GenerateMatrix(rows,cols):
  result=Matrix(rows,cols,T=Rmax)
  randomIndex=[random.randrange(1,rows) for k in range(rows)]#это рандомные индексы,чтоб 0 и inf в случайные места матрицы добавить
  #print(randomIndex)
  for i in range(result.rows):
    for j in range(result.cols):
      if(i==randomIndex[j]):
        if(i%2==1):
          result[i][j]=Rmax(0)
        else:
          result[i][j]=Rmax(-float('inf'))
      else:
        result[i][j]=Rmax(random.randrange(1,10))
  
  return result
  
def GenerateMatrixStar(rows,cols):
  result=Matrix(rows,cols,T=Rmax)

  for i in range(result.rows):
    for j in range(result.cols):
      if(i==0 or j==0):
        result[i][j]=Rmax(random.randrange(1,10))
        #Rmax(-float('inf'))
      else:
        if(i==j):
          result[i][j]=Rmax(random.randrange(1,10))
        else:
          result[i][j]=Rmax(-float('inf'))
  return result
    
#______________________________________
def GenerateMatrixPoln(rows,cols):
  result=Matrix(rows,cols,T=Rmax)

  for i in range(result.rows):
    for j in range(result.cols):
      if(result[i][j]==Rmax(-float('inf')) and result[j][i]==Rmax(-float('inf'))):
        if (i%2==0): 
          result[i][j]=Rmax(random.randrange(1,10))
          result[j][i]=Rmax(-float('inf'))
        else:
          result[i][j]=Rmax(-float('inf'))
          result[j][i]=Rmax(random.randrange(1,10))
        #Rmax(-float('inf'))
      else:
        result[j][i]=Rmax(random.randrange(1,10))
  return result
  #______________________________________
def GenerateMatrixRing(rows,cols):
  result=Matrix(rows,cols,T=Rmax)

  for i in range(result.rows):
    for j in range(result.cols):
      if(i==j):
        result[i][j]=Rmax(random.randrange(1,10))
        if(i!=result.rows-1 and j!=result.cols-1):#если это не последний эл-т в диагонали матрицы. -1, т.к мы ж от 0 идем до n-1
          result[i+1][j]=Rmax(random.randrange(1,10))#то ниже главной диагонали заполняем
          result[i][j+1]=Rmax(random.randrange(1,10))#и выше запоняем
        else:#а если последний эл-т в главной диагонали
          if(i==result.rows-1 and j==result.cols-1):
            result[0][result.cols-1]=Rmax(random.randrange(1,10))#то посл эл-т в 0й строке заполняем
            result[result.rows-1][0]=Rmax(random.randrange(1,10))#и посл эл-т в 0ом столбце(это для связи последней вершины в графе и нулевой,нам же кольцо нужно)
        
  return result
  
#A = Matrix(4,4, [[Rmax(8),Rmax(10),Rmax(0),Rmax(0)],[Rmax(0),Rmax(5),Rmax(4),Rmax(8)],[Rmax(6),Rmax(12),Rmax(11),Rmax(7)],[Rmax(0),Rmax(0),Rmax(0),Rmax(12)]], T=Rmax) #размер ее 4х4 ,дальше само содержимое и тип
#B = Matrix(4,1, [[Rmax(14)],[Rmax(11)],[Rmax(16)],[Rmax(15)]], Rmax)

import random
#ПРИМЕР №1
A=GenerateMatrix(4,4) #генерируем матрицу 4x4
B=GenerateMatrix(4,1) #генерируем матрицу 1x4
print('A=',A)
print('B=',B)
pinv(B)#транспонируем B по Воробьеву
C=pinv(B)*A #перемножаем строку на матрицу как на паре делали
print('C =',pinv(C)) 
print(GenerateGraph(A))#код для графа выводим
#_______________________________________________
#ПРИМЕР №2
print('Сгенерируем звезду')
S=GenerateMatrixStar(4,4)
B_Star=GenerateMatrixStar(4,1) #генерируем матрицу 1x4
print(S)
#транспонируем B по Воробьеву
C_Star=pinv(B_Star)*A #перемножаем строку на матрицу как на паре делали
print('C_Star =',pinv(C_Star))
print(GenerateGraph(S))#код для графа выводим
#_______________________________________________
#ПРИМЕР №3
print('Сгенерируем полносвязный')
P=GenerateMatrixPoln(4,4)
B_Poln=GenerateMatrix(4,1) #генерируем матрицу 1x4
print(P)
C_Poln=pinv(B_Poln)*A #перемножаем строку на матрицу как на паре делали
print('C_Poln =',pinv(C_Poln))
print(GenerateGraph(P))#код для графа выводим
#_______________________________________
#ПРИМЕР №4
print('Сгенерируем кольцо')
R=GenerateMatrixRing(4,4)
B_Ring=GenerateMatrixRing(4,1) #генерируем матрицу 1x4
print(R)
#транспонируем B по Воробьеву
C_Ring=pinv(B_Ring)*A #перемножаем строку на матрицу как на паре делали
print('C_Ring =',pinv(C_Ring))
print(GenerateGraph(R))#код для графа выводим

