// radhe radhe
let draggedPiece = null;
let sourceSquare = null;

// Add drag start event to all pieces
document.querySelectorAll('.piece').forEach(piece => {
    piece.addEventListener('dragstart', (e) => {
        draggedPiece = e.target;
        sourceSquare = e.target.parentElement.dataset.square;
        e.dataTransfer.effectAllowed = 'move';
        e.target.classList.add('dragging');
        console.log(`Started dragging ${e.target.dataset.piece} from ${sourceSquare}`);
    });

    piece.addEventListener('dragend', (e) => {
        e.target.classList.remove('dragging');
    });
});

// Add drag over event to all squares
document.querySelectorAll('[data-square]').forEach(square => {
    square.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    });

    square.addEventListener('drop', (e) => {
        e.preventDefault();
        const targetSquare = e.currentTarget.dataset.square;
        
        if (draggedPiece && targetSquare) {
            // Remove piece from old square
            draggedPiece.parentElement.removeChild(draggedPiece);
            
            // Clear target square if it has a piece
            const existingPiece = e.currentTarget.querySelector('.piece');
            if (existingPiece) {
                e.currentTarget.removeChild(existingPiece);
            }
            
            // Add piece to new square
            e.currentTarget.appendChild(draggedPiece);
            
            console.log(`Moved ${draggedPiece.dataset.piece} from ${sourceSquare} to ${targetSquare}`);
        }
        
        draggedPiece = null;
        sourceSquare = null;
    });
});

// Flip board functionality
document.getElementById('flipBtn').addEventListener('click', () => {
    const boardContainer = document.getElementById('boardContainer');
    boardContainer.classList.toggle('flipped');
});
