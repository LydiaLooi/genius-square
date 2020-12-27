from random import choice

BLOCK = "[]"

D1 = [(3,3), (3,4), (4,3), (2,4), (5,3), (4,4)]
D2 = [(6,1), (1,6), (6,1), (1,6), (6,1), (1,6)]
D3 = [(2,5), (3,5), (3,6), (1,4), (6,6), (4,6)]
D4 = [(2,6), (1,5), (5,1), (1,5), (6,2), (6,2)]
D5 = [(6,3), (4,1), (5,2), (1,1), (4,2), (3,1)]
D6 = [(5,4), (5,5), (5,6), (4,5), (6,5), (6,4)]
D7 = [(1,2), (1,3), (2,1), (2,2), (3,2), (2,3)]

DICE = [D1, D2, D3, D4, D5, D6, D7]

class Board:
    def __init__(self):
        self.board = self.createBoard()
        self.placed = []
        self.blockersPlaced = False

    def isValidPlacement(self, piece, coords):
        ci = coords[0]
        cj = coords[1]
        for i, j in piece.pieces:
            iCoord = i + ci
            jCoord = j + cj


            if (iCoord < 0) or (jCoord < 0) or (iCoord > 5) or (jCoord > 5):
                return False
            if self.board[iCoord][jCoord] != " ":
                return False
        return True

    def placeBlock(self, piece, coords):
        if self.isValidPlacement(piece, coords):
            ci = coords[0]
            cj = coords[1]
            # print(piece.pieces)
            for i, j in piece.pieces:
                self.board[i + ci][j + cj] = piece.symbol
            self.placed.append(piece)
        else:
            print("[Invalid placement]")
        

    def removeBlock(self, piece):
        if piece in self.placed:
            self.placed.remove(piece)
            for i, row in enumerate(self.board):
                for j, c in enumerate(row):
                    if c == piece.symbol:
                        self.board[i][j] = " "

            print("AAA")
            print(self.placed)

        else:
            print("[Block could not be placed]")


    def createBoard(self):
        return [[" " for _ in range(6)] for _ in range(6)]

    def setupBlockers(self):
        if not self.blockersPlaced:
            for dice in DICE:
                i, j = choice(dice)
                i -= 1
                j -= 1
                self.board[i][j] = "X"
            self.blockersPlaced = True
        else:
            print("[Blockers already set up]")
            
    def showPossibleBlockers(self):
        board = self.createBoard()
        i = 1
        for dice in DICE:
            for i, j in dice:
                i -= 1
                j -= 1
                board[i][j] = i
            i += 1
        print(self.printBoard(board))

    def isFinished(self):
        for row in self.board:
            for c in row:
                if c == " ":
                    return False
        return True


    def printBoard(self, board):
        output = "  012345 \n --------\n"
        # for row in board:
        #     output += str(row) + "\n"
        i = 0
        for row in board:
            line = f"{i}|"
            i += 1
            for x in row:
                line += x
            line += "|\n"
            output += line
        output += " --------"
        return output

    def __str__(self):
        return self.printBoard(self.board)



class Piece:
    def __init__(self, symbol, pieces=[]):
        self.pieces = pieces
        self.symbol = symbol
        self.array = [["  " for _ in range(5)] for _ in range(5)]
        for i, j in self.pieces:
            block = "[]"
            if i == 0 and j == 0 :
                block = "{}"
            i += 2
            j += 2
            self.array[i][j] = block

    def rotateAnti(self):
        new_matrix = []
        for i in range(len(self.array[0]), 0, -1):
            new_matrix.append(list(map(lambda x: x[i-1], self.array)))
        self.array = new_matrix
        self.setNewPieces()

    def rotate(self):
        new_matrix = []
        for i in range(len(self.array[0])):
            li = list(map(lambda x: x[i], self.array))
            li.reverse()
            new_matrix.append(li)
        self.array = new_matrix
        self.setNewPieces()

    def flipVert(self):
        self.array.reverse()
        self.setNewPieces()

    def flipHori(self):
        for row in self.array:
            row.reverse()
        self.setNewPieces()
            
    def setNewPieces(self):
        newPieces = []

        for i, row in enumerate(self.array):
            
            for j, x in enumerate(row):
                if x == "[]" or x == "{}":
                    newPieces.append((i-2, j-2))
        self.pieces = newPieces

    def __str__(self):
        
        output = ""
        for row in self.array:
            for b in row:
                output += b
            output += "\n"
        return output

    def __repr__(self):
        return self.symbol


SINGLE = Piece("1",[(0,0)])
TEE = Piece("T",[(0,0),(0,-1),(-1,0),(0,1)])
SQUARE = Piece("Q",[(0,0),(0,1),(1,0),(1,1)])
DOUBLE = Piece("2",[(0,0),(1,0)])
TRIPLE = Piece("3",[(0,0),(1,0), (-1,0)])
QUADRA = Piece("4",[(0,0),(1,0), (-1,0), (2,0)])
STEP = Piece("S",[(0,0),(1,0),(0,1),(-1,1)])
EL = Piece("L",[(-1,0),(0,0),(0,1),(-2,0)])
CORNER = Piece("C",[(0,0),(0,1),(-1,0)])

BLOCKS = [SINGLE, TEE, SQUARE, DOUBLE, TRIPLE, QUADRA, STEP, EL, CORNER]

BLOCK_DICT = {
    "1": SINGLE,
    "T": TEE,
    "Q": SQUARE,
    "2": DOUBLE,
    "3": TRIPLE,
    "4": QUADRA,
    "S": STEP,
    "L": EL,
    "C": CORNER
}


START = """
--- Commands ---
restart - New board
setup - New board and setup blockers
stop - Stop.
----------------
info - Transformations info
rc/ra/fh/fc {block name} - Transform a block
place {block name} {down} {across} - Place block
remove {block name} - Remove block from board
clear - Remove all blocks from board
"""

TRANSFORMATIONS = """
--- Transformations ---
rc - Rotate piece clockwise
ra - Rotate piece anti-clockwise
fh - Flip horizontally
fv - Flip vertically

e.g. "rc T"
"""

WIN = """
█░░█ █▀▀█ █░░█   █░░░█ ░▀░ █▀▀▄ █
█▄▄█ █░░█ █░░█   █▄█▄█ ▀█▀ █░░█ ▀
▄▄▄█ ▀▀▀▀ ░▀▀▀   ░▀░▀░ ▀▀▀ ▀░░▀ ▄
"""
def printBlocksLine(board):
    line = ""
    for i in range(5):
        for b in BLOCKS:
            if b not in board.placed:
                array = b.array[i]
                for c in array:
                    line += c
        line += "\n"
    for b in BLOCKS:
        if b not in board.placed:
            line += f"    {b.symbol}     "
    print(line)



def main():
    board = Board()
    playing = True
    while playing:
        print(board)
        printBlocksLine(board)
        print(START)
        inp = input("Input: ")
        print("\n\n")
        inp = inp.lower()

        if inp == "stop":
            playing = False
            print("[Stop]")

        elif inp == "setup":
            board = Board()
            board.setupBlockers()
            print("\n[Blockers set up]\n")

        elif inp == "restart":
            board = Board()
            print("\n[New Board]\n")

        elif inp == "info":
            print(TRANSFORMATIONS)

        elif inp.startswith("rc"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]
                block.rotate()
            except Exception:
                print("[Invalid command]")

        elif inp.startswith("ra"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]
                block.rotateAnti()
            except Exception:
                print("[Invalid command]")

        elif inp.startswith("fh"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]
                block.flipHori()
            except Exception:
                print("[Invalid command]")

        elif inp.startswith("fv"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]
                block.flipVert()
            except Exception:
                print("[Invalid command]")

        elif inp.startswith("place"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]

                if block not in board.placed:
                    board.placeBlock(block, (int(inputs[2]), int(inputs[3])))
                    if board.isFinished():
                        print(WIN)

                else:
                    print("[Block is already on the board!]")
            except Exception:
                print("[Invalid command]")

        elif inp.startswith("remove"):
            inputs = inp.split(" ")
            try:
                block = BLOCK_DICT[inputs[1].upper()]
                if block in board.placed:
                    board.removeBlock(block)
                else:
                    print("[Block is not on the board!]")
            except Exception:
                print("[Invalid command]")

        elif inp == "clear":
            blocks = board.placed.copy()
            for b in blocks:
                board.removeBlock(b)
            print("[Blocks removed]")

        else:
            print("[No command matched]")
        print()

main()