function appendToDisplay(value) {
    document.getElementById('display').value += value;
}

function clearDisplay() {
    document.getElementById('display').value = '';
}

function calculate() {
    const display = document.getElementById('display');
    try {
        display.value = eval(display.value);
    } catch (e) {
        display.value = 'Error';
    }
}

// Add keyboard event listener for calculator
document.addEventListener('keydown', function(event) {
    const key = event.key;
    if (!isNaN(key) || key === '.') {
        appendToDisplay(key);
    } else if (key === 'Enter') {
        calculate();
    } else if (key === 'Backspace') {
        const display = document.getElementById('display');
        display.value = display.value.slice(0, -1); // Remove the last character
    } else if (['+', '-', '*', '/'].includes(key)) {
        appendToDisplay(key);
    }
});

// Allow using '=' key to calculate
document.addEventListener('keypress', function(event) {
    if (event.key === '=') {
        calculate();
    }
});