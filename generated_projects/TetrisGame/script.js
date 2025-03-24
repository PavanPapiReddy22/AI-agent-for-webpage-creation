const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
const startButton = document.getElementById('startButton');
const scoreDisplay = document.getElementById('score');

let board = Array.from({ length: 20 }, () => Array(10).fill(0));
let currentPiece;
let gameInterval;
let score = 0;

function drawBoard() {
    context.fillStyle = 'black';
    context.fillRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < board.length; r++) {
        for (let c = 0; c < board[r].length; c++) {
            if (board[r][c] !== 0) {
                context.fillStyle = board[r][c];
                context.fillRect(c * 24, r * 24, 24 - 1, 24 - 1);
            }
        }
    }
}

function update() {
    if (currentPiece) {
        currentPiece.row++;
        if (!isValidPosition(currentPiece)) {
            currentPiece.row--;
            updateBoardWithPiece();
            currentPiece = getNewPiece();
            score += 10;
            if (!isValidPosition(currentPiece)) {
                alert("Game Over!");
                clearInterval(gameInterval);
                return;
            }
        }
    }
    drawBoard();
    scoreDisplay.textContent = 'Score: ' + score;
}

function isValidPosition(piece) {
    for (let r = 0; r < piece.shape.length; r++) {
        for (let c = 0; c < piece.shape[r].length; c++) {
            if (piece.shape[r][c]) {
                let newRow = piece.row + r;
                let newCol = piece.col + c;
                if (newRow >= 20 || board[newRow][newCol] !== 0 || newCol < 0 || newCol >= 10) {
                    return false;
                }
            }
        }
    }
    return true;
}

function startGame() {
    clearInterval(gameInterval); // Ensure any previous interval is cleared
    score = 0;
    board = Array.from({ length: 20 }, () => Array(10).fill(0));
    currentPiece = getNewPiece();
    gameInterval = setInterval(update, 1000);
}

function getNewPiece() {
    const pieces = [
        { shape: [[1]], color: 'red', row: 0, col: 4 },
        { shape: [[1, 1], [1, 1]], color: 'green', row: 0, col: 4 },
        { shape: [[0, 1], [1, 1], [1, 0]], color: 'blue', row: 0, col: 4 },
        { shape: [[1, 1, 1], [0, 1, 0]], color: 'yellow', row: 0, col: 4 }
    ];
    const piece = pieces[Math.floor(Math.random() * pieces.length)];
    piece.shape = piece.shape.map(row => row.map(c => c ? piece.color : 0));
    return piece;
}

function updateBoardWithPiece() {
    for (let r = 0; r < currentPiece.shape.length; r++) {
        for (let c = 0; c < currentPiece.shape[r].length; c++) {
            if (currentPiece.shape[r][c]) {
                board[currentPiece.row + r][currentPiece.col + c] = currentPiece.color;
            }
        }
    }
}

startButton.addEventListener('click', startGame);