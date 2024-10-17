import operator
 
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    '%' : operator.mod,
    '^' : operator.xor,
}
 
# 4x4 board
# board = [[4, 0, 0, 0],
#         [0, 0, 3, 0],
#         [0, 0, 0, 0],
#         [0, 0, 0, 1]]
board = [[0, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
 
 
# box definition for partition, last element of each set will be the ordered pair (result, operator)
# definition = [[(0,1), (0, 2), (0, 3), (6, '*')],
#           [(1,0), (1, 1), (1, '-')],
#           [(1,3), (2,3), (2, '/')],
#           [(2,0),(2,1),(3, 0),(3, 1), (11, '+')],
#           [(2,2), (3,2), (2, '/')]]
 
definition =[[(0,0), (0, 1), (1, 1), (16, '*')],
          [(0,2), (0, 3), (1,2), (7, '+')],
          [(1,0), (2,0), (2, '-')],
          [(2,1),(3, 0),(3, 1), (12, '*')],
          [(2,2), (2,3), (2, '/')],
          [(3,2), (3,3), (2, '/')]]
 
domain = []
for i in range(0, 16):
    s = int(i/4)
    t = int(i%4)
    if board[s][t] != 0:
        domain.insert(i, [board[s][t]])
        continue
    domain.insert(i, [1,2,3,4])
 
# domain reduction
for a in definition:
    a_len = len(a)
    res = a[a_len - 1][0]
    oper = a[a_len - 1][1]
 
    for b in range(0, a_len-1):
        s = a[b][0]
        t = a[b][1]
 
        i = 4*s + t
 
        if oper == '*' or oper == '/':
            for val in domain[i]:
                if res%val != 0:
                    domain[i].remove(val)
        elif oper == '+':
            domain[i] = [val for val in domain[i] if val<res]
 
 
 
 
 
 
 
 
 
 
 
 
 
# domain is 1-4 for 4x4 board for each variable i.e for each empty square
# constraint : arithmatic - formed on the basis of definition
#            : row-column - each row and column must have distinct values from 1-4
 
# only backtracking for now
 
def find_empty(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return (i, j)  # row, col
    return None
 
 
 
def isValid(puzzle, num, pos):
 
    # pos holds (i,j)
    # include arithmatic contraint as well  -- to do
    # method1
        # Check row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == num and pos[1] != i:
            return False
 
    # Check column
    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == num and pos[0] != i:
            return False
 
    print(pos)
    for x in definition:
        if pos in x:
            q = definition.index(x)
            p = definition[q].index(pos)
            len_x = len(x)
            if p == (len_x - 2):
                # arithmatic condition comes in
                result = x[len_x-1][0]
                op = x[len_x-1][1]
                # addition / subtraction
                l = 0
                if op == '*' or  op == '/':
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
                    print(puzzle[a][b], result, end = "-")
                l = ops[op](num, l)
                if abs(l) == result:
                    print("YES")
                    return True
                elif op == '/' and (1/l) == result:
                    print("YES")
                    return True    
                else:
                    print("NO")
                    return False
                print(l)
   
    return True
    # if all spaces in the block are filled, it must be equal to the constraint, i.e. if second last element has value
 
def solve(puzzle):
    find = find_empty(puzzle)
    if not find:
        return True
    else:
        row, col = find
 
    i = row*4 + col
 
    for val in domain[i]:
        if isValid(puzzle, val, (row, col)):
            puzzle[row][col] = val
            if solve(puzzle):
                return True
            puzzle[row][col] = 0
    return False
 
print(board)
solve(board)
print(board)
 
 
 
# for forward checking, you remove the value from the domain itself if the connecting row or column has already satisfied that value
 
 
 
 
 
