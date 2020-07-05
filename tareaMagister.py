#Nicolas Rodriguez Ormazabal

from ortools.constraint_solver import pywrapcp

nombresEmpleados = ['Tom', 'David', 'Jeremy', 'Ron', 'Joe', 'Bill', 'Fred', 'Bob', 'Mario', 'Ed', 'Carol', 'Janet', 'Tracy', 'Marilyn', 'Carolyn', 'Cathy','Inez', 'Jean', 'Heather', 'Juliet']
azafatos = ['Tom', 'David', 'Jeremy', 'Ron', 'Joe', 'Bill', 'Fred', 'Bob', 'Mario', 'Ed']
azafatas = ['Carol', 'Janet', 'Tracy', 'Marilyn', 'Carolyn', 'Cathy', 'Inez','Jean', 'Heather', 'Juliet']

frances = ['Bill','Inez','Jean','Juliet']
aleman = [ 'Tom','Jeremy','Mario','Cathy','Juliet']
espanol = ['Joe','Bill','Fred', 'Mario','Marilyn','Inez','Heather']

vuelos = [
    [4,1,1,1,1,1], #requerimientos de vuelo
    [5,1,1,1,1,1],
    [5,1,1,1,1,1],
    [6,2,2,1,1,1],
    [7,3,3,1,1,1],
    [4,1,1,1,1,1],
    [5,1,1,1,1,1],
    [6,1,1,1,1,1],
    [6,2,2,1,1,1],
    [7,3,3,1,1,1]]

trabajadores = [
    [1,0,0,0,1], # [azafato - azafata - frances- aleman- espanol]
    [1,0,0,0,0],
    [1,0,0,0,1],
    [1,0,0,0,0],
    [1,0,0,1,0],
    [1,0,1,1,0],
    [1,0,0,1,0],
    [1,0,0,0,0],
    [1,0,0,1,1],
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,0,1,1],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,1,1,1],
    [0,1,1,0,0],
    [0,1,0,1,1],
    [0,1,1,0,0]]

estructuraRespuestas = [
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #Respuestas
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

numeroVuelos = len(vuelos) #10
numeroEmpleados = len(nombresEmpleados) #20

def solucion(sols):

    #se definen las variables
    solver = pywrapcp.Solver('tripulacion')

    tripulacion = {} #Matriz que contiene la estructura de la solucion
    for i in range(numeroVuelos):
        for j in range(numeroEmpleados):
            tripulacion[(i,j)] = solver.IntVar(0, 1, 'tripulacion[%i,%i]' % (i, j)) #Se genera matriz con valores de dominio entre 0 y 1

    crew_flat=[] #se crea arreglo con todos los valores de la matriz
    for i in range(numeroVuelos) :
        for j in range(numeroEmpleados):
            crew_flat.append(tripulacion[i,j])
    #print(len(crew_flat))

    #crew_flat2 = [tripulacion[(i,j)] for i in range(numeroVuelos) for j in range(numeroEmpleados)] #se puede cambiar por que se hizo
    #print(len(crew_flat2))

    dominioCantidadEmpleados = solver.IntVar(1, numeroEmpleados)
    #print(dominioCantidadEmpleados)

    # Se verifica que la cantidad de empleados no sea mayor que 20
    solver.Add(dominioCantidadEmpleados == solver.Sum(
                            [solver.IsGreaterOrEqualCstVar(solver.Sum([tripulacion[(f,p)]
                                    for f in range(numeroVuelos)]), 1)
                                for p in range(numeroEmpleados)]))

    #print(solver.Sum([solver.IsGreaterOrEqualCstVar(    solver.Sum( [tripulacion[(f,p)] for f in range(numeroVuelos)]), 1) for p in range(numeroEmpleados)] ))

    for f in range(numeroVuelos):
        # se agrega condicion para cantidad de tripulacion
        tmp = [tripulacion[(f,i)] for i in range(numeroEmpleados)]
        solver.Add(solver.Sum(tmp) == vuelos[f][0])

        # se verifica los atributos de cada trabajador
        for j in range(5):
            tmp = [trabajadores[i][j]*tripulacion[(f,i)] for i in range(numeroEmpleados) ]
            #print(solver.Sum(tmp))
            solver.Add(solver.Sum(tmp) >= vuelos[f][j+1])


    # after a flight, break for at least two flights
    for f in range(numeroVuelos-2):
        for i in range(numeroEmpleados):
            solver.Add(tripulacion[f,i] + tripulacion[f+1,i] + tripulacion[f+2,i] <= 1)


    #solution and search
    solution = solver.Assignment()
    solution.Add(crew_flat)
    solution.Add(dominioCantidadEmpleados)

    db = solver.Phase(crew_flat,solver.CHOOSE_FIRST_UNBOUND,solver.ASSIGN_MIN_VALUE)
    solver.NewSearch(db)
    num_solutions = 0

    while solver.NextSolution():
        num_solutions += 1
        print ("Solution #%i" % num_solutions)
        print ("Number working:", dominioCantidadEmpleados.Value())
        for i in range(numeroVuelos):
            for j in range(numeroEmpleados):
                (tripulacion[i,j].Value()),
            print ('\n')

        if num_solutions >= sols:
            break
    solver.EndSearch()

    print ("num_solutions:", num_solutions)
    print ("failures:", solver.Failures())
    print ("branches:", solver.Branches())
    print ("WallTime:", solver.WallTime())
           
def main():
    num_solutions_to_show = 2
    solucion(num_solutions_to_show)

main()
