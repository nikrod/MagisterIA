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
    [1,0,0,0,1], #trabajadores
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
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

numeroVuelos = len(vuelos) #10
numeroEmpleados = len(nombresEmpleados) #20

def solucion(sols):
    solver = pywrapcp.Solver('Crew')
    crew = {}
    for i in range(numeroVuelos):
        for j in range(numeroEmpleados):
            crew[(i,j)] = solver.IntVar(0, 1, 'crew[%i,%i]' % (i, j))
    crew_flat = [crew[(i,j)] for i in range(numeroVuelos) for j in range(numeroEmpleados)]
    num_working = solver.IntVar(1, numeroEmpleados, 'num_working')


    # number of working persons
    solver.Add(num_working == solver.Sum(
                       [solver.IsGreaterOrEqualCstVar(solver.Sum([crew[(f,p)]
                                    for f in range(numeroVuelos)]), 1)
                                for p in range(numeroEmpleados) ]) )

    for f in range(numeroVuelos):
        # size of crew
        tmp = [crew[(f,i)] for i in range(numeroEmpleados)]
        solver.Add(solver.Sum(tmp) == vuelos[f][0])

        # attributes and requirements
        for j in range(5):
            tmp = [trabajadores[i][j]*crew[(f,i)] for i in range(numeroEmpleados) ]
            solver.Add(solver.Sum(tmp) >= vuelos[f][j+1])


    # after a flight, break for at least two flights
    for f in range(numeroVuelos-2):
        for i in range(numeroEmpleados):
            solver.Add(crew[f,i] + crew[f+1,i] + crew[f+2,i] <= 1)

    # extra contraint: all must work at least two of the flights
    # for i in range(num_persons):
    #     [solver.Add(solver.Sum([crew[f,i] for f in range(num_flights)]) >= 2) ]


    #
    # solution and search
    #
    solution = solver.Assignment()
    solution.Add(crew_flat)
    solution.Add(num_working)

    db = solver.Phase(crew_flat,solver.CHOOSE_FIRST_UNBOUND,solver.ASSIGN_MIN_VALUE)

    solver.NewSearch(db)
    num_solutions = 0
    while solver.NextSolution():
        num_solutions += 1
        print ("Solution #%i" % num_solutions)
        print ("Number working:", num_working.Value())
        for i in range(numeroVuelos):
            for j in range(numeroEmpleados):
                print (crew[i,j].Value()),
            print ('\n')

        if num_solutions >= sols:
            break
    solver.EndSearch()

    print ("num_solutions:", num_solutions)
    print ("failures:", solver.Failures())
    print ("branches:", solver.Branches())
    print ("WallTime:", solver.WallTime())

def listarVuelos():
    for i in range(numeroVuelos):
        print('Vuelo'+ str(i+1)+'\t'+ str((vuelos)[i]))
           
def main():
    num_solutions_to_show = 1
    solucion(num_solutions_to_show)

main()
