__author__ = 'went'
import  datetime
'''
some notations:A Sudoku puzzle is a grid of 81 squares.The majority of ethusiasts label the column 1-9,
the rows A-I,and call a collectin of squares(row,col and box) a unit and the squares that share a unit the
peers. A puzzle leaves some squares blank and fill other with digits,the whole idea is:
    A puzzle is solved if the squares in each uint are fill with a permutation of ths digits 1-9.
That is, no digit can appear twice in a unit,and every digit must appear once.This impies that every square
must have a different value from any of its peers.
'''
__Times = 0
def cross(A,B):
    return [a + b for a in A for b in B]

digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
squares = cross(rows,cols)
unitlist = ([cross(rows,c) for c in cols] + [cross(r,cols) for r in rows] +
           [cross(r1,c1) for r1 in ("ABC","DEF","GHI") for c1 in ("123","456","789")])
units = dict((s,[u for u in unitlist if s in u]) for s in squares)
peers = dict((s,set(sum(units[s],[]))-set([s])) for s in squares)

def gridvalues(grid):
    chars = [c for c in grid if c in digits or c in "0."]
    assert len(chars)==81
    return dict(zip(squares,chars))

def parsegrid(grid):
    values = dict((s,digits) for s in squares)
    for s,d in gridvalues(grid).items():
        if(d in digits and not assign(values,s,d)):
            return False
    return values

def eliminate(values,s,d):
    '''
    :param values: sudoku square
    :param s: current position
    :param d: value to eliminate
    :return:
    '''
    if(d not in values[s]):     #d already eliminated from values[s]
        return values
    values[s] = values[s].replace(d,"") #eliminate d from values[s]
    if(len(values[s])==0):  #if all value in square values[s] has been elimianted,sudoku is false
        return False
    if(len(values[s])==1): #if values[s] is reduced to one digit d2,then eliminate all d2 from peers[s]
        d2 = values[s]
        if(not all(eliminate(values,s2,d2) for s2 in peers[s])):
            return False

    #if a unit u is reduce to only one place for a value d,then put it there
    for u in units[s]:
        dplaces = [s1 for s1 in u if d in values[s1]]
        if(len(dplaces)==0):
            return False
        elif(len(dplaces)==1):
            # d can only in one place in a unit,put it there
            if(not assign(values,dplaces[0],d)):
                return False
    return values


def assign(values,s,d):
    '''
    eliminate all the other values(except d) from values[s]
    :param values:
    :param s:
    :param d:
    :return:
    '''
    othervalues = values[s].replace(d,"")
    if(all(eliminate(values,s,d2) for d2 in othervalues)):
        return values
    else:
        return  False


def display(values):
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * width * 3] * 3)
    for r in rows:
        print(''.join((values[r + c].center(width) + ('|' if c in '36' else '') for c in cols)))
        if(r in 'CF'):
            print(line)
    print

def test():
    "A set of unit tests."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print 'All tests pass.'


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
#display(parsegrid(grid1))




grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
gridHardest = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
#display(parsegrid(grid2))

def solve(grid):
    return search(parsegrid(grid))

def some(seq):
    for e in seq:
        if e:
            return e
    return False

def search(values):
    global __Times
    __Times += 1
    if(values is False):
        return False
    if(all(len(values[s])==1 for s in squares)):
        return values
    n,s = min((len(values[s]),s) for s in squares if(len(values[s])>1))
    return some(search(assign(values.copy(),s,d)) for d in values[s])

t1 = datetime.datetime.now()
display(solve(gridHardest))
t2 = datetime.datetime.now()
print('time:' + str(t2-t1))
print('search times:' + str(__Times))
