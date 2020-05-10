
import numpy as np
import numpy.random as r

part9  = np.array([[3,2,1,1,1,1], [2,2,2,1,1,1]])
part10 = np.array([[3,3,1,1,1,1], [3,2,2,1,1,1], [2,2,2,2,1,1]])
part11 = np.array([[3,3,2,1,1,1], [3,2,2,2,1,1], [2,2,2,2,2,1]])

tbl9  = [0,1,1,1,1,1,1,1,1]
tbl10 = [0,1,2,2,2,2,2,2,2]
tbl11 = [0,1,2,2,2,2,2,2,2]

start = [1,10,20,30,40,50,60,70,80]
end   = [9,19,29,39,49,59,69,79,90]

def generate_cards(seed_value):
    r.seed(seed_value)
    amounts = np.empty((6,9), dtype=np.int)
    amounts[:,0] = r.permutation(part9[r.choice(tbl9), :])
    for i in range(1,8):
        amounts[:,i] = r.permutation(part10[r.choice(tbl10), :])
    amounts[:,8] = r.permutation(part11[r.choice(tbl11), :])
    iter = 0
    while True:
        totals = np.sum(amounts, axis=1)
        options = [(r0, r1, c) for r0 in range(6) for r1 in range (0,6) for c in range(9) if totals[r0] < totals[r1] and amounts[r0,c] == amounts[r1,c] - 1]
        if len(options) == 0:
            break
        choice = r.randint(0, len(options))
        r0, r1, c = options[choice]
        amounts[r0, c], amounts[r1, c] = amounts[r1, c], amounts[r0, c]
        iter += 1
        assert iter < 100
    perm_decades = [list(r.permutation(np.arange(start[i], 1+end[i]))) for i in range(9)]
    numbers = [[None for _ in range(9)] for _ in range(6)]
    for col in range(9):
        for card in range(6):
            L = amounts[card, col]
            numbers[card][col] = list(sorted(perm_decades[col][:L]))
            perm_decades[col] = perm_decades[col][L:]

    # Now work to get 5 per row

    result = np.zeros((6,3,9), dtype=np.int)
    for card in range(6):
        for col in range(9):
            L = len(numbers[card][col])
            result[card, 0:L, col] = np.array(numbers[card][col])

    # Now shuffle down to get 5 per row
    for card in range(6):
        iter = 0
        while True:
            totals = np.sum((result[card,:,:] != 0), axis=1)
            options = [(col, row) for col in range(9) for row in range(2) if totals[row] > 5 and result[card, row, col] > 0 and result[card, row+1, col] == 0]
            if len(options) == 0:
                break
            choice = r.randint(0, len(options))
            col, row = options[choice]
            result[card, row+1, col] = result[card, row, col]
            result[card, row, col] = 0
            iter += 1
            assert iter < 50
    return result

