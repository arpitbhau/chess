// radhe radhe
const socket = io();
socket.on("connect", () => {
    console.log("Connected to server");
});

const piece_drag_logic = () => {
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
                if (sourceSquare !== targetSquare) {
                    e.currentTarget.appendChild(draggedPiece);
                    // Emit move event to server to check if it's validate and update game state
                    socket.emit('move_piece_socket', {
                        piece: draggedPiece.dataset.piece,
                        from: sourceSquare,
                        to: targetSquare
                    });
                    // listen for server's reesponse
                    socket.on('move_piece_socket', (data) => {
                        console.log('Server response:', data);
                    });
                    console.log(`Moved ${draggedPiece.dataset.piece} from ${sourceSquare} to ${targetSquare}`);
                    
                }
            }
            
            draggedPiece = null;
            sourceSquare = null;
        });
    });
}

piece_drag_logic();

