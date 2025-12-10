// Global variables
let cards = [];
let targetCard = null;
let guesses = [];
const maxGuesses = 6;
const guessInput = document.getElementById('guessInput');
const submitGuess = document.getElementById('submitGuess');
const feedbackGrid = document.getElementById('feedbackGrid');
const messageEl = document.getElementById('message');
const scoreEl = document.getElementById('score');
const shareBtn = document.getElementById('shareBtn');
const resetBtn = document.getElementById('resetBtn');
const targetCardEl = document.getElementById('targetCard');
const previewContainer = document.getElementById('previewContainer');
const previewImg = document.getElementById('previewImg');

// Placeholder image
const placeholderImg = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2NjYyIvPjwvc3ZnPg==';

// Load data from JSON
async function loadData() {
    try {
        const response = await fetch('./kartlar_tam.json');
        if (!response.ok) throw new Error('Failed to load JSON');
        cards = await response.json();
        console.log('Data loaded:', cards.length, 'cards');
    } catch (error) {
        console.error('Error loading data:', error);
        cards = [];
        showMessage('Error loading cards. Please refresh.', 'error');
    }
}

// Get daily target using date-based seed
function getDailyTarget() {
    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    const seed = today.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const index = Math.abs(seed) % cards.length;
    return cards[index];
}

// Check if same day
function isSameDay(dateStr) {
    return new Date().toISOString().split('T')[0] === dateStr;
}

// Restore state for current day
function restoreState() {
    const today = new Date().toISOString().split('T')[0];
    const saved = localStorage.getItem(`lorldle-${today}`);
    if (saved) {
        const state = JSON.parse(saved);
        guesses = state.guesses || [];
        renderGuesses();
        updateUI();
    }
}

// Save state
function saveState() {
    const today = new Date().toISOString().split('T')[0];
    localStorage.setItem(`lorldle-${today}`, JSON.stringify({ guesses }));
}

// Show message
function showMessage(text, type = 'info') {
    messageEl.textContent = text;
    messageEl.className = type; // Add classes like 'win', 'error' for styling if needed
    messageEl.setAttribute('role', 'alert');
}

// Update UI: guesses remaining, submit state
function updateUI() {
    const remaining = maxGuesses - guesses.length;
    scoreEl.textContent = `Guesses remaining: ${remaining}`;
    submitGuess.disabled = remaining === 0 || gameWon();
    guessInput.disabled = remaining === 0 || gameWon();
    if (gameWon()) {
        showMessage(`Congratulations! You guessed ${targetCard.isim} in ${guesses.length} guesses!`, 'win');
        shareBtn.style.display = 'inline-block';
        revealTarget();
    } else if (guesses.length === maxGuesses) {
        showMessage(`Game over! The card was ${targetCard.isim}.`, 'lose');
        shareBtn.style.display = 'inline-block';
        revealTarget();
    }
}

// Check if game won (last guess is exact)
function gameWon() {
    return guesses.length > 0 && guesses[guesses.length - 1].exact;
}

// Render all guess feedback rows
function renderGuesses() {
    feedbackGrid.innerHTML = '';
    guesses.forEach(guess => renderFeedbackRow(guess));
    // Add empty rows for remaining guesses
    for (let i = guesses.length; i < maxGuesses; i++) {
        const emptyRow = document.createElement('div');
        emptyRow.className = 'feedback-row';
        for (let j = 0; j < 8; j++) { // 8 attributes: Name, Folder, Type, Energy, Power, Might, Nadir, Path (gray)
            const tile = document.createElement('div');
            tile.className = 'feedback-tile';
            emptyRow.appendChild(tile);
        }
        feedbackGrid.appendChild(emptyRow);
    }
    // Highlight current row
    if (guesses.length < maxGuesses) {
        const rows = feedbackGrid.querySelectorAll('.feedback-row');
        rows[guesses.length].classList.add('current');
    }
}

// Render feedback for a single guess
function renderFeedbackRow(guess) {
    const row = document.createElement('div');
    row.className = 'feedback-row' + (guess.exact ? ' win' : guesses.length === maxGuesses && !gameWon() ? ' incorrect' : '');

    const attributes = ['isim', 'klasor', 'tip', 'energy', 'power', 'might', 'nadir', 'dosya_yolu'];
    attributes.forEach(attr => {
        const tile = document.createElement('div');
        tile.className = 'feedback-tile';
        let value = guess.card[attr];
        if (attr === 'dosya_yolu') value = 'Path'; // Abbreviate
        tile.textContent = value.substring(0, 4).toUpperCase(); // Shorten for tile

        // Determine match color
        let matchClass = getMatchClass(guess.card, targetCard, attr);
        tile.classList.add(matchClass);

        row.appendChild(tile);
    });

    feedbackGrid.appendChild(row);
}

// Get match class: green exact, yellow partial, gray none
function getMatchClass(guessCard, target, attr) {
    const gVal = guessCard[attr];
    const tVal = target[attr];

    switch (attr) {
        case 'isim':
            return gVal.toLowerCase() === tVal.toLowerCase() ? 'match-green' : 'match-gray';
        case 'tip':
            return gVal === tVal ? 'match-green' : (['Unit', 'Spell', 'Champion'].includes(gVal) && ['Unit', 'Spell', 'Champion'].includes(tVal)) ? 'match-yellow' : 'match-gray';
        case 'energy':
        case 'power':
        case 'might':
            const gNum = parseInt(gVal, 10);
            const tNum = parseInt(tVal, 10);
            if (gNum === tNum) return 'match-green';
            if (Math.abs(gNum - tNum) <= 1) return 'match-yellow';
            return 'match-gray';
        case 'nadir':
            const rarityOrder = { 'Common': 1, 'Uncommon': 2, 'Rare': 3, 'Epic': 4, 'Legendary': 5 };
            const gR = rarityOrder[gVal] || 0;
            const tR = rarityOrder[tVal] || 0;
            if (gVal === tVal) return 'match-green';
            if (Math.abs(gR - tR) === 1) return 'match-yellow';
            return 'match-gray';
        case 'klasor':
            return gVal === tVal ? 'match-green' : (gVal[0].toLowerCase() === tVal[0].toLowerCase()) ? 'match-yellow' : 'match-gray';
        case 'dosya_yolu':
            return 'match-gray'; // Always gray
        default:
            return 'match-gray';
    }
}

// Handle guess submission
async function handleGuess() {
    const input = guessInput.value.trim().toLowerCase();
    if (!input) return;

    const guessedCard = cards.find(card => card.isim.toLowerCase() === input);
    if (!guessedCard) {
        showMessage('Invalid card name. Try again.', 'error');
        guessInput.value = '';
        guessInput.focus();
        return;
    }

    const exact = guessedCard.isim === targetCard.isim;
    guesses.push({ card: guessedCard, exact });

    renderGuesses();
    saveState();
    updateUI();

    guessInput.value = '';
    guessInput.focus();

    if (!exact) {
        showMessage('Not quite! Keep guessing.', 'info');
    }
}

// Reveal target card on game end
function revealTarget() {
    targetCardEl.style.display = 'block';
    targetCardEl.innerHTML = `
        <h2>${gameWon() ? 'Well done!' : 'The answer was:'} ${targetCard.isim}</h2>
        <img src="${targetCard.dosya_yolu}" alt="${targetCard.isim} portrait" onerror="this.src='${placeholderImg}'" style="width:150px; height:150px; object-fit:cover; border-radius:8px;">
        <p><strong>Type:</strong> ${targetCard.tip} | <strong>Rarity:</strong> ${targetCard.nadir}</p>
        <p><strong>Energy:</strong> ${targetCard.energy} | <strong>Power:</strong> ${targetCard.power} | <strong>Might:</strong> ${targetCard.might}</p>
    `;
}

// Share results (Wordle-style text)
function shareResults() {
    const today = new Date().toISOString().split('T')[0];
    let shareText = `LoRdle ${today} ${guesses.length}/${maxGuesses}\n\n`;
    guesses.forEach(guess => {
        const attrs = ['isim', 'klasor', 'tip', 'energy', 'power', 'might', 'nadir', 'dosya_yolu'];
        let rowEmojis = '';
        attrs.forEach(attr => {
            const matchClass = getMatchClass(guess.card, targetCard, attr);
            if (matchClass === 'match-green') rowEmojis += '🟩';
            else if (matchClass === 'match-yellow') rowEmojis += '🟨';
            else rowEmojis += '⬜';
        });
        shareText += rowEmojis + '\n';
    });
    shareText += `\nGuess the card: http://localhost:8000`;
    navigator.clipboard.writeText(shareText).then(() => {
        showMessage('Results copied to clipboard!', 'info');
    });
}

// Event listeners
submitGuess.addEventListener('click', handleGuess);
guessInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleGuess();
});
shareBtn.addEventListener('click', shareResults);
resetBtn.addEventListener('click', () => {
    if (confirm('Start a new puzzle?')) {
        const today = new Date().toISOString().split('T')[0];
        localStorage.removeItem(`lorldle-${today}`);
        location.reload();
    }
});

// Initialize
window.addEventListener('load', async () => {
    await loadData();
    if (cards.length === 0) return;
    targetCard = getDailyTarget();
    console.log('Today\'s target:', targetCard.isim); // For debug

    // Set up preview
    if (previewImg && previewContainer) {
        previewImg.src = targetCard.dosya_yolu;
        previewImg.onerror = () => { previewImg.src = placeholderImg; };
        previewContainer.style.display = 'block';
    }

    restoreState();
    updateUI();
    guessInput.focus();
});
