// Welcome popup functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check if this is the first visit
    const hasVisited = localStorage.getItem('csvViewerVisited');
    
    if (hasVisited !== 'true') {
        // Show welcome popup after a short delay
        setTimeout(() => {
            const popup = document.getElementById('welcome-popup');
            const overlay = document.getElementById('overlay');
            
            if (popup && overlay) {
                popup.style.display = 'block';
                overlay.style.display = 'block';
                
                // Auto-hide after 5 seconds
                setTimeout(() => {
                    closeWelcomePopup();
                }, 5000);
            }
        }, 500);
        
        // Mark as visited
        localStorage.setItem('csvViewerVisited', 'true');
    }
});

function closeWelcomePopup() {
    const popup = document.getElementById('welcome-popup');
    const overlay = document.getElementById('overlay');
    
    if (popup && overlay) {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    }
}

// Parallel scrolling functionality
document.addEventListener('DOMContentLoaded', function() {
    // Find all scrollable code containers with pair IDs
    const scrollableContainers = document.querySelectorAll('.code-diff[data-pair-id], .normal-code[data-pair-id]');
    
    scrollableContainers.forEach(container => {
        container.addEventListener('scroll', function(e) {
            const pairId = this.getAttribute('data-pair-id');
            const pairedContainer = document.getElementById(pairId);
            
            if (pairedContainer && !pairedContainer.isScrolling) {
                // Prevent infinite loop by marking the paired container as scrolling
                pairedContainer.isScrolling = true;
                pairedContainer.scrollTop = this.scrollTop;
                
                // Reset the flag after a short delay
                setTimeout(() => {
                    pairedContainer.isScrolling = false;
                }, 50);
            }
        });
    });
});

async function copyCellContent(button, rowIndex, colIndex) {
    const cellContainer = button.closest('.cell-container');
    let textContent = '';
    
    // Extract text content based on cell type
    if (cellContainer.querySelector('.code-diff, .normal-code')) {
        // For code cells, extract all line content
        const lines = cellContainer.querySelectorAll('.line-content');
        textContent = Array.from(lines).map(line => line.textContent).join('\n');
    } else {
        // For regular cells, get the text content
        textContent = cellContainer.textContent.replace('Copy', '').trim();
    }
    
    try {
        await navigator.clipboard.writeText(textContent);
        
        // Show success feedback
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copy-success');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copy-success');
        }, 2000);
        
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = textContent;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            
            // Show success feedback
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            button.classList.add('copy-success');
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copy-success');
            }, 2000);
            
        } catch (fallbackErr) {
            // Show error feedback
            const originalText = button.textContent;
            button.textContent = 'Error!';
            button.classList.add('copy-error');
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copy-error');
            }, 2000);
        }
        
        document.body.removeChild(textArea);
    }
} 