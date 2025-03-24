const cells = document.querySelectorAll('[data-cell]');
const board = document.querySelector('.board');
const resetButton = document.getElementById('reset');
let currentPlayer = 'X';
let boardState = ['', '', '', '', '', '', '', '', ''];

const winningCombinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
    [0, 4, 8], [2, 4, 6] // diagonals
];

function handleClick(event) {
    const cell = event.target;
    const index = [...cells].indexOf(cell);
    if (boardState[index] !== '' || currentPlayer === 'O') return;
    cell.textContent = currentPlayer;
    boardState[index] = currentPlayer;
    if (checkWin()) {
        alert(`${currentPlayer} wins!`);
        resetGame();
    } else if (boardState.every(cell => cell !== '')) {
        alert('Draw!');
        resetGame();
    }
    currentPlayer = 'O';
    computerTurn();
}

function computerTurn() {
    const availableCells = [...cells].filter(cell => cell.textContent === '');
    if (availableCells.length === 0) return;
    const randomCell = availableCells[Math.floor(Math.random() * availableCells.length)];
    const index = [...cells].indexOf(randomCell);
    randomCell.textContent = currentPlayer;
    boardState[index] = currentPlayer;
    if (checkWin()) {
        alert(`${currentPlayer} wins!`);
        resetGame();
    } else if (boardState.every(cell => cell !== '')) {
        alert('Draw!');
        resetGame();
    }
    currentPlayer = 'X';
}

function checkWin() {
    return winningCombinations.some(combination => {
        const [a, b, c] = combination;
        return boardState[a] && boardState[a] === boardState[b] && boardState[a] === boardState[c];
    });
}

function resetGame() {
    cells.forEach(cell => cell.textContent = '');
    boardState = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
}

cells.forEach(cell => cell.addEventListener('click', handleClick));
resetButton.addEventListener('click', resetGame);