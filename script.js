

function choice(choices) {
    let index = Math.floor(Math.random() * choices.length);
    return choices[index];
  }

const D1 = [(3,3), (3,4), (4,3), (2,4), (5,3), (4,4)]
const D2 = [(6,1), (1,6), (6,1), (1,6), (6,1), (1,6)]
const D3 = [(2,5), (3,5), (3,6), (1,4), (6,6), (4,6)]
const D4 = [(2,6), (1,5), (5,1), (1,5), (6,2), (6,2)]
const D5 = [(6,3), (4,1), (5,2), (1,1), (4,2), (3,1)]
const D6 = [(5,4), (5,5), (5,6), (4,5), (6,5), (6,4)]
const D7 = [(1,2), (1,3), (2,1), (2,2), (3,2), (2,3)]

const DICE = [D1, D2, D3, D4, D5, D6, D7]


class Board {
    constructor() {

    }
}

class Piece {
    constructor(symbole, pieces) {
        this.pieces = pieces;
        this.symbol = this.symbol;
        this.array = [];
        for (let i = 0; i < 5; i++) {
            this.array.push(["  ", "  ", "  ", "  ", "  ", "  "]);
        }

        for (let i = 0; i < this.pieces.length; i++) {
            let coords = this.pieces[i];
            let k = coords[0];
            let j = coords[1];
            let block = "[]";
            if (k == 0 && j == 0) {
                block = "{}";
            }
            k += 2;
            j += 2;
            this.array[k][j] = block;
        }
    }
}

Piece.prototype.toString = function pieceToString() {
    let output = "";
    for (let i = 0; i < this.array.length; i++) {
        let row = this.array[i];
        for (let j = 0; j < row.length; j++) {
            let b = row[j];
            output = output.concat(b);
        }
        output = output.concat("\n");
    }
    return output;
}

const TEE = new Piece("T",[[0,0],[0,-1],[-1,0],[0,1]]);




console.log(TEE.toString());
