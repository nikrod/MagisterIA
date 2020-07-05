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

def solucion(cantidadSoluciones):

    #se definen las variables
    solver = pywrapcp.Solver('tripulacion')

    tripulacion = {} #Matriz que contiene la estructura de la solucion
    for i in range(numeroVuelos):
        for j in range(numeroEmpleados):
            tripulacion[(i,j)] = solver.IntVar(0, 1, 'tripulacion[%i,%i]' % (i, j)) #Se genera matriz con valores de dominio entre 0 y 1

    arregloTripulacion=[] #se crea arreglo con todos los valores de la matriz
    for i in range(numeroVuelos) :
        for j in range(numeroEmpleados):
            arregloTripulacion.append(tripulacion[i,j])

    cantidadEmpleados = solver.IntVar(1, numeroEmpleados)

    # Se verifica que la tripulacion no sea mayor que la cantidad de empleados
    solver.Add(cantidadEmpleados == solver.Sum(
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
            solver.Add(solver.Sum(tmp) >= vuelos[f][j+1])

    # se agrega condicion para que el trabajador no pueda pertenecer a una tripulacion por los dos siguientes viajes
    for i in range(numeroVuelos-2):
        for j in range(numeroEmpleados):
            solver.Add(tripulacion[i,j] + tripulacion[i+1,j] + tripulacion[i+2,j] <= 1)


    #solution and search
    solution = solver.Assignment()
    solution.Add(arregloTripulacion)
    solution.Add(cantidadEmpleados)

    db = solver.Phase(arregloTripulacion,solver.CHOOSE_FIRST_UNBOUND,solver.ASSIGN_MIN_VALUE)
    solver.NewSearch(db)

    while solver.NextSolution():
        solucionesEncontradas=0
        solucionesEncontradas=solucionesEncontradas+1
        for i in range(numeroVuelos):
            for j in range(numeroEmpleados):
                (tripulacion[i,j].Value()),
            print ('\n')

        if cantidadSoluciones>=solucionesEncontradas:
            break

    solver.EndSearch()
         
def main():
    cantidadSoluciones=1
    solucion(cantidadSoluciones)

main()
