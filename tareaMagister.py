#Nicolas Rodriguez Ormazabal

from ortools.constraint_solver import pywrapcp

nombresEmpleados = ['Tom', 'David', 'Jeremy', 'Ron', 'Joe', 'Bill', 'Fred', 'Bob', 'Mario', 'Ed', 'Carol', 'Janet', 'Tracy', 'Marilyn', 'Carolyn', 'Cathy','Inez', 'Jean', 'Heather', 'Juliet']

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
    [1,0,0,0,1], #[azafato - azafata - frances- espanol- aleman] #Tom
    [1,0,0,0,0],#David
    [1,0,0,0,1],#Jeremy
    [1,0,0,0,0],#Ron
    [1,0,0,1,0],#Joe
    [1,0,1,1,0],#Bill
    [1,0,0,1,0],#Fred
    [1,0,0,0,0],#Bob
    [1,0,0,1,1],#Mario
    [1,0,0,0,0],#Ed
    [0,1,0,0,0],#carol
    [0,1,0,0,0],#janet
    [0,1,0,0,0],#tracy
    [0,1,0,0,1],#marilyn
    [0,1,0,0,0],#carolyn
    [0,1,0,1,0],#cathy
    [0,1,1,0,1],#ines
    [0,1,1,0,0],#jean
    [0,1,0,0,1],#HEather
    [0,1,1,1,0]]#juliet

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

    arregloTripulacion=[] #se crea arreglo con todos los valores de la matriz para ingresarla al solver
    for i in range(numeroVuelos) :
        for j in range(numeroEmpleados):
            arregloTripulacion.append(tripulacion[i,j])

    #cantidad de empleados para ingresarlo al solver
    cantidadEmpleados = solver.IntVar(1, numeroEmpleados)

    # Se verifica que la tripulacion no sea mayor que la cantidad de empleados
    cant=0
    for j in range(numeroEmpleados):#se recorre la solucion por columnas
        temp3=solver.Sum([tripulacion[(i,j)] for i in range(numeroVuelos)]) #se suman los valores de las columnas
        cant = solver.IsGreaterOrEqualCstVar(temp3,1) +cant #se guarda la suma con la condicion que sea mayor o igual a 1 en la variable cant, para avanzar a la siguiente columna
    solver.Add(cantidadEmpleados==cant) #se verifica que la cantidad de trabajadores sea igual a la cantidad de la tripulacion

    for i in range(numeroVuelos):
        # se agrega condicion para cantidad de tripulacion
        tripulacionVuelo = [tripulacion[(i,j)] for j in range(numeroEmpleados)]
        solver.Add(solver.Sum(tripulacionVuelo) == vuelos[i][0])

    for i in range(numeroVuelos):
        # se verifica los atributos de cada trabajador
        for k in range(5):
            trabajador = [trabajadores[j][k]*tripulacion[(i,j)] for j in range(numeroEmpleados) ]#se verifica si el trabajador esta en la tripulacion con 1 y 0, este valor se multiplica por el atributo
            solver.Add(solver.Sum(trabajador) >= vuelos[i][k+1])#se suman los atributos y se verifican con la matriz de requerimientos de vuelo

    # se agrega condicion para que el trabajador no pueda pertenecer a una tripulacion por los dos siguientes viajes
    for i in range(numeroVuelos-2):#se recorren los vuelos, quitandole dos, debido a la restriccion de no poder viajar por los dos siguientes vuelos
        for j in range(numeroEmpleados):#se recorren los trabajadores
            solver.Add(tripulacion[i,j] + tripulacion[i+1,j] + tripulacion[i+2,j] <= 1)#si la suma del trabajador en los tres vuelos consecutivos es menor o igual a 1 (viajo una sola vez), se agrega la solucion

    #Se configura el solver,Las variables se consideran en el orden del vector de arregloTripulacion.
    db = solver.Phase(arregloTripulacion,solver.CHOOSE_FIRST_UNBOUND,solver.ASSIGN_MIN_VALUE)
    solver.NewSearch(db)

    #Contador de soluciones encontradas
    solucionesEncontradas=0
    while solver.NextSolution():
        solucionesEncontradas=solucionesEncontradas+1
        print('\ncantidad de empleados '+str(cantidadEmpleados.Value()))
        for i in range(numeroVuelos):
            arrayTemp=[]
            for j in range(numeroEmpleados):
                arrayTemp.append(tripulacion[i,j].Value())

        for i in range(numeroVuelos):
            arrayNombres=[]
            for j in range(numeroEmpleados):
                if(tripulacion[i,j].Value()==1):
                    arrayNombres.append(nombresEmpleados[j])
            print("vuelo "+str(i+1)+": "+str(arrayNombres))

        if solucionesEncontradas>=cantidadSoluciones:
            break
        
    solver.EndSearch()
         
def main():
    cantidadSoluciones=10
    solucion(cantidadSoluciones)

main()
