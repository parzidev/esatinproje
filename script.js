document.addEventListener('DOMContentLoaded', () => {
    let cards = [];
    let targetCard = null;
    let guesses = [];
    let gameOver = false;

    const searchInput = document.getElementById('searchInput');
    const autocompleteList = document.getElementById('autocomplete-list');
    const guessesContainer = document.getElementById('guesses-container');
    const winModal = document.getElementById('winModal');
    const winMessage = document.getElementById('winMessage');
    const modalTitle = document.getElementById('modalTitle');
    const playAgainBtn = document.getElementById('playAgainBtn');
    const closeModal = document.querySelector('.close');
    const targetCardImage = document.getElementById('target-card-image');
    const giveUpBtn = document.getElementById('giveUpBtn');
    const modalImage = document.getElementById('modalImage');

    // Placeholder image (gray square)
    const placeholderImg = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZmZmIj4/PC90ZXh0Pjwvc3ZnPg==';

    // Load JSON data
    fetch('kartlar_tam.json')
        .then(response => response.json())
        .then(data => {
            cards = data;
            initGame();
        })
        .catch(error => console.error('Error loading cards:', error));

    function getImagePath(card) {
        if (!card.dosya_yolu) return '';
        let path = card.dosya_yolu.replace(/\\/g, '/');
        if (path.startsWith('Unit/')) {
            path = path.replace('Unit/', 'Units/');
        }
        return `cards/${path}`;
    }

    function initGame() {
        // Pick a random card
        if (cards.length > 0) {
            targetCard = cards[Math.floor(Math.random() * cards.length)];
            console.log('Target Card:', targetCard.isim); // For debugging

            // Set target image
            const imgPath = getImagePath(targetCard);
            targetCardImage.src = imgPath;
            targetCardImage.onerror = function () { this.src = placeholderImg; };

            // Reset blur
            updateBlur(0);
        }
        guesses = [];
        gameOver = false;
        guessesContainer.innerHTML = '';
        searchInput.value = '';
        searchInput.disabled = false;
        winModal.style.display = 'none';
        giveUpBtn.disabled = false;
        if (modalImage) modalImage.style.display = 'none';
    }

    function updateBlur(guessCount) {
        // Initial blur 8px (more recognizable). Decrease by 2px every guess.
        let blurAmount = Math.max(0, 8 - guessCount * 2);
        targetCardImage.style.filter = `blur(${blurAmount}px)`;
    }

    // Search Input Event Listener
    searchInput.addEventListener('input', function () {
        const val = this.value;
        closeAllLists();
        if (!val) return false;

        const matches = cards.filter(card =>
            card.isim.toLowerCase().startsWith(val.toLowerCase())
        );

        // Limit to 10 results
        matches.slice(0, 10).forEach(card => {
            const div = document.createElement('div');
            const imgPath = getImagePath(card);

            div.innerHTML = `
                <img src="${imgPath}" alt="${card.isim}" onerror="this.src='${placeholderImg}'">
                <span>${card.isim}</span>
            `;
            div.addEventListener('click', function () {
                submitGuess(card);
                closeAllLists();
                searchInput.value = '';
            });
            autocompleteList.appendChild(div);
        });
    });

    function closeAllLists() {
        autocompleteList.innerHTML = '';
    }

    // Close autocomplete when clicking outside
    document.addEventListener('click', function (e) {
        if (e.target !== searchInput) {
            closeAllLists();
        }
    });

    function submitGuess(guessedCard) {
        if (gameOver) return;

        guesses.push(guessedCard);
        renderGuess(guessedCard);
        updateBlur(guesses.length);

        if (guessedCard.isim === targetCard.isim) {
            endGame(true);
        }
    }

    function renderGuess(card) {
        const row = document.createElement('div');
        row.className = 'guess-row';

        // 1. Card Image/Name
        const imgPath = getImagePath(card);
        const cardBox = createAttributeBox(
            `<img src="${imgPath}" class="card-thumb" title="${card.isim}" onerror="this.src='${placeholderImg}'">`,
            card.isim === targetCard.isim ? 'correct' : 'incorrect',
            0
        );

        // 2. Type (Tip)
        let typeClass = 'incorrect';
        if (card.tip === targetCard.tip) {
            typeClass = 'correct';
        } else if (card.tip.includes(targetCard.tip) || targetCard.tip.includes(card.tip)) {
            typeClass = 'partial';
        }

        const typeMap = {
            'Unit': 'type/unit.webp',
            'Champion Unit': 'type/unit.webp',
            'Signature Unit': 'type/unit.webp',
            'Token Unit': 'type/unit.webp',
            'Spell': 'type/spell.webp',
            'Signature Spell': 'type/spell.webp',
            'Gear': 'type/gear.webp',
            'Battlefield': 'type/battlefield.webp',
            'Basic Rune': 'type/rune.webp',
            'Legend': 'type/legend.webp',
            'Token Card': 'type/spell.webp'
        };

        // Normalize type for mapping (handle potential variations if needed, but direct map is safer for now)
        // If exact match not found, try to find a key that is contained in the type string
        let typeImg = typeMap[card.tip];
        if (!typeImg) {
            // Fallback logic: check if it contains 'Unit', 'Spell', etc.
            if (card.tip.includes('Unit')) typeImg = 'type/unit.webp';
            else if (card.tip.includes('Spell')) typeImg = 'type/spell.webp';
            else if (card.tip.includes('Rune')) typeImg = 'type/rune.webp';
            else if (card.tip.includes('Legend')) typeImg = 'type/legend.webp';
        }

        const typeContent = typeImg
            ? `<div class="type-content"><img src="${typeImg}" class="type-icon" alt="${card.tip}"><span>${card.tip}</span></div>`
            : card.tip;

        const typeBox = createAttributeBox(typeContent, typeClass, 1);

        // 3. Energy (Numeric)
        const energyBox = createNumericAttributeBox(card.energy, targetCard.energy, 2);

        // 4. Power (Numeric)
        const powerBox = createNumericAttributeBox(card.power, targetCard.power, 3);

        // 5. Might (Numeric)
        const mightBox = createNumericAttributeBox(card.might, targetCard.might, 4);

        // 6. Rarity (Nadir)
        const rarityMap = {
            'Common': 'rare/common.webp',
            'Rare': 'rare/rare.webp',
            'Epic': 'rare/epic.webp',
            'Uncommon': 'rare/uncommon.webp',
            'Legendary': 'rare/showcase.webp'
        };

        const rarityImg = rarityMap[card.nadir] || '';
        const rarityContent = rarityImg
            ? `<img src="${rarityImg}" class="rarity-icon" alt="${card.nadir}" title="${card.nadir}">`
            : card.nadir;

        const rarityBox = createAttributeBox(
            rarityContent,
            card.nadir === targetCard.nadir ? 'correct' : 'incorrect',
            5
        );

        row.appendChild(cardBox);
        row.appendChild(typeBox);
        row.appendChild(energyBox);
        row.appendChild(powerBox);
        row.appendChild(mightBox);
        row.appendChild(rarityBox);

        // Prepend to show latest guess at top
        guessesContainer.prepend(row);
    }

    function createAttributeBox(content, className, delayIndex) {
        const box = document.createElement('div');
        box.className = `attribute-box ${className}`;
        box.innerHTML = content;
        // Add delay for flip animation
        box.style.animationDelay = `${delayIndex * 0.1}s`;
        return box;
    }

    function createNumericAttributeBox(guessVal, targetVal, delayIndex) {
        const g = parseInt(guessVal) || 0;
        const t = parseInt(targetVal) || 0;
        let className = 'incorrect';
        let arrow = '';

        if (g === t) {
            className = 'correct';
        } else {
            if (g < t) {
                arrow = '<span class="arrow">↑</span>'; // Need higher
            } else {
                arrow = '<span class="arrow">↓</span>'; // Need lower
            }
        }

        return createAttributeBox(`${guessVal}${arrow}`, className, delayIndex);
    }

    function endGame(isWin) {
        gameOver = true;
        searchInput.disabled = true;
        giveUpBtn.disabled = true;
        targetCardImage.style.filter = 'blur(0px)'; // Reveal completely

        if (isWin) {
            modalTitle.textContent = 'Tebrikler!';
            winMessage.textContent = `Doğru kart: ${targetCard.isim}`;
        } else {
            modalTitle.textContent = 'Oyun Bitti';
            winMessage.textContent = `Aranan kart: ${targetCard.isim}`;
        }

        if (modalImage) {
            const imgPath = getImagePath(targetCard);
            modalImage.src = imgPath;
            modalImage.style.display = 'block';
        }

        showWinModal();
    }

    function showWinModal() {
        winModal.style.display = 'block';
    }

    closeModal.onclick = function () {
        winModal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == winModal) {
            winModal.style.display = 'none';
        }
    }

    playAgainBtn.onclick = function () {
        initGame();
    }

    giveUpBtn.onclick = function () {
        if (!gameOver) {
            endGame(false);
        }
    }
});
