# square-kufic "لبنة" on a cell grid. rows top->bottom, cols left->right.
def word():
    cells=set()
    base=5
    for x in range(3,13): cells.add((x,base))          # baseline
    for y in range(1,6): cells.add((12,y))              # ل
    for y in range(3,6): cells.add((9,y))               # ب tooth
    for y in range(3,6): cells.add((6,y))               # ن tooth
    for x in range(0,4): cells.add((x,3)); cells.add((x,5))  # ة ring
    cells.add((0,4)); cells.add((3,4))
    dots={(9,7),(6,1),(1,1),(2,1)}                      # ب below, ن above, ة two above
    return cells,dots
