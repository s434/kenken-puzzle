import operator
 
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,  # use operator.div for Python 2
    '%': operator.mod,
    '^': operator.xor,
}

size_n = 4
board = [[4, 0, 0, 0],
        [0, 0, 3, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]]
definition = [[(0,1), (0, 2), (0, 3), (6, '*')],
        [(1,0), (1, 1), (1, '-')],
        [(1,3), (2,3), (2, '/')],
        [(2,0),(2,1),(3, 0),(3, 1), (11, '+')],
        [(2,2), (3,2), (2, '/')]]

 
# domain is 1-size_n for size_nxsize_n board for each variable i.e for each empty square
domain = []
def formDomain():
    for i in range(0, size_n*size_n):
        s = int(i/size_n)
        t = int(i % size_n)
        if board[s][t] != 0:
            domain.insert(i, [board[s][t]])
            continue
        domain.insert(i, list(range(1, size_n + 1)))
        
def domainReduction():
    
    # domain reduction
    for a in definition:
        a_len = len(a)-1
        res = a[a_len][0]
        oper = a[a_len][1]

        for b in range(0, a_len):
            s = a[b][0]
            t = a[b][1]

            i = size_n*s + t

            if oper == '*':
                domain[i] = [val for val in domain[i] if val%res == 0 or res%val == 0]
            elif oper == '/':
                domain[i] = [val for val in domain[i] if val<res and res*val <= size_n or val%res == 0]
                # so we should have nos less than quotient(res), and the multiples of res greater than or equal to res
                # second condition to ensure that the number less than res will give rise to second num that will fit the bounds of domain (1,9)
            elif oper == '+':
                domain[i] = [val for val in domain[i] if val<res]
 
 
def find_empty(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return (i, j)  # row, col
    return None
 
 
# constraint : arithmatic - formed on the basis of definition
#            : row-column - each row and column must have distinct values from 1-4

def isValid(puzzle, num, pos):
 
    # pos holds (row,col)
    # Check row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == num and pos[1] != i:
            return False
 
    # Check column
    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == num and pos[0] != i:
            return False
 
    for x in definition:
        if pos in x:
            # if all spaces in the block are filled, it must be equal to the constraint, i.e. if second last element has value
            q = definition.index(x)
            p = definition[q].index(pos)
            len_x = len(x)
            if p == (len_x - 2):
                # arithmetic condition comes in
                result = x[len_x-1][0]
                op = x[len_x-1][1]
                # addition / subtraction
                l = 0
                # multiplication/division
                if op == '*' or op == '/':
                    l = 1
                for y in zip(x, range(len_x - 1)):
                    # because y gives the tuple value with the index the tuple is at
                    # y[0] - tuple vale
                    # y[1] - index of tuple
                    a = y[0][0]
                    b = y[0][1]
                    #(a,b)
                    if puzzle[a][b] == 0:
                        break
                    l = ops[op](puzzle[a][b], l)
                l = ops[op](num, l)
                if abs(l) == result:
                    return True
                elif op == '/' and (1/l) == result:
                    return True
                else:
                    return False
    return True
    
 
 
def solve(puzzle):
    find = find_empty(puzzle)
    if not find:
        return True
    else:
        row, col = find
 
    i = row*size_n + col
 
    for val in domain[i]:
        if isValid(puzzle, val, (row, col)):
            puzzle[row][col] = val
           
            if solve(puzzle):
                return True
            puzzle[row][col] = 0
    return False
 
 

