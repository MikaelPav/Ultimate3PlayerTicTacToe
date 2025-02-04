const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 600;
canvas.height = 600;

const GRID_SIZE = 3;
const CELL_SIZE = canvas.width / (GRID_SIZE * GRID_SIZE);
const colors = ["red", "green", "blue"];
const players = ["X", "O", "Δ"];
let currentPlayer = 0;

let board = Array(9).fill(null).map(() => Array(3).fill(null).map(() => Array(3).fill(null)));
let miniGridWinners = Array(9).fill(null);
let forcedBoard = null;

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "black";

    for (let i = 1; i < GRID_SIZE * GRID_SIZE; i++) {
        ctx.lineWidth = (i % GRID_SIZE === 0) ? 4 : 1;
        ctx.beginPath();
        ctx.moveTo(i * CELL_SIZE, 0);
        ctx.lineTo(i * CELL_SIZE, canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * CELL_SIZE);
        ctx.lineTo(canvas.width, i * CELL_SIZE);
        ctx.stroke();
    }

    // Highlight forced mini-grid
    if (forcedBoard !== null && miniGridWinners[forcedBoard] === null) {
        let bigR = Math.floor(forcedBoard / 3);
        let bigC = forcedBoard % 3;
        ctx.strokeStyle = "yellow";
        ctx.lineWidth = 5;
        ctx.strokeRect(bigC * 3 * CELL_SIZE, bigR * 3 * CELL_SIZE, 3 * CELL_SIZE, 3 * CELL_SIZE);
    }

    // Display current player
    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText(`Current Player: ${players[currentPlayer]}`, 10, 20);
}

function checkWinner(grid) {
    for (let p of players) {
        for (let r = 0; r < 3; r++) {
            if (grid[r][0] === p && grid[r][1] === p && grid[r][2] === p) return p;
        }
        for (let c = 0; c < 3; c++) {
            if (grid[0][c] === p && grid[1][c] === p && grid[2][c] === p) return p;
        }
        if (grid[0][0] === p && grid[1][1] === p && grid[2][2] === p) return p;
        if (grid[0][2] === p && grid[1][1] === p && grid[2][0] === p) return p;
    }
    return null;
}

canvas.addEventListener("click", function (event) {
    let x = event.offsetX;
    let y = event.offsetY;

    let bigC = Math.floor(x / CELL_SIZE / 3);
    let bigR = Math.floor(y / CELL_SIZE / 3);
    let smallC = Math.floor((x % (CELL_SIZE * 3)) / CELL_SIZE);
    let smallR = Math.floor((y % (CELL_SIZE * 3)) / CELL_SIZE);
    let miniGridIndex = bigR * 3 + bigC;

    if ((forcedBoard === null || forcedBoard === miniGridIndex) && board[miniGridIndex][smallR][smallC] === null) {
        board[miniGridIndex][smallR][smallC] = players[currentPlayer];
        let winner = checkWinner(board[miniGridIndex]);
        if (winner) {
            miniGridWinners[miniGridIndex] = winner;
        }
        forcedBoard = miniGridWinners[smallR * 3 + smallC] !== null ? null : smallR * 3 + smallC;
        currentPlayer = (currentPlayer + 1) % 3;
        drawGrid();
        drawBoard();
    }
});

function drawBoard() {
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    for (let bigR = 0; bigR < 3; bigR++) {
        for (let bigC = 0; bigC < 3; bigC++) {
            let miniGridIndex = bigR * 3 + bigC;
            if (miniGridWinners[miniGridIndex]) {
                ctx.fillStyle = colors[players.indexOf(miniGridWinners[miniGridIndex])];
                ctx.fillRect(bigC * 3 * CELL_SIZE, bigR * 3 * CELL_SIZE, 3 * CELL_SIZE, 3 * CELL_SIZE);
            }
            for (let smallR = 0; smallR < 3; smallR++) {
                for (let smallC = 0; smallC < 3; smallC++) {
                    let symbol = board[miniGridIndex][smallR][smallC];
                    if (symbol) {
                        let x = (bigC * 3 + smallC) * CELL_SIZE + CELL_SIZE / 2;
                        let y = (bigR * 3 + smallR) * CELL_SIZE + CELL_SIZE / 2;
                        ctx.fillStyle = colors[players.indexOf(symbol)];
                        ctx.fillText(symbol, x, y);
                    }
                }
            }
        }
    }
}

drawGrid();
