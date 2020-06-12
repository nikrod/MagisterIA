#Nicolas Rodriguez Ormazabal

empleados = ['Tom', 'David', 'Jeremy', 'Ron', 'Joe', 'Bill', 'Fred', 'Bob', 'Mario', 'Ed', 'Carol', 'Janet', 'Tracy', 'Marilyn', 'Carolyn', 'Cathy','Inez', 'Jean', 'Heather', 'Juliet']
azafatos = ['Tom', 'David', 'Jeremy', 'Ron', 'Joe', 'Bill', 'Fred', 'Bob', 'Mario', 'Ed']
azafatas = ['Carol', 'Janet', 'Tracy', 'Marilyn', 'Carolyn', 'Cathy', 'Inez','Jean', 'Heather', 'Juliet']

frances = ['Bill','Inez','Jean','Juliet']
aleman = [ 'Tom','Jeremy','Mario','Cathy','Juliet']
espanol = ['Joe','Bill','Fred', 'Mario','Marilyn','Inez','Heather']

vuelos = [
    [1,4,1,1,1,1,1],
    [2,5,1,1,1,1,1],
    [3,5,1,1,1,1,1],
    [4,6,2,2,1,1,1],
    [5,7,3,3,1,1,1],
    [6,4,1,1,1,1,1],
    [7,5,1,1,1,1,1],
    [8,6,1,1,1,1,1],
    [9,6,2,2,1,1,1],
    [10,7,3,3,1,1,1]]

def listarVuelos():
    len = 10
    for i in range(len):
        print('Vuelo'+ str(i+1)+'\t'+ str((vuelos)[i]))
           
def main():
   interaciones = 100
   listarVuelos()

main()
