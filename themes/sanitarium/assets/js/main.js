// Copy button functionality for code blocks
document.addEventListener('DOMContentLoaded', function() {
    const copyButtons = document.querySelectorAll('.copy-button');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            // Find the code element within the same highlight div
            const highlightDiv = button.closest('.highlight');
            const codeElement = highlightDiv.querySelector('pre code');
            
            if (!codeElement) {
                console.error('Could not find code element to copy');
                return;
            }
            
            const textToCopy = codeElement.textContent;
            
            try {
                if (navigator.clipboard && window.isSecureContext) {
                    // Use modern clipboard API
                    await navigator.clipboard.writeText(textToCopy);
                } else {
                    // Fallback for older browsers or non-secure contexts
                    const textArea = document.createElement('textarea');
                    textArea.value = textToCopy;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    textArea.style.top = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    document.execCommand('copy');
                    textArea.remove();
                }
                
                // Show "Copied!" feedback
                button.classList.add('copied');
                button.setAttribute('aria-label', 'Code copied to clipboard');
                
                // Reset after 2 seconds
                setTimeout(() => {
                    button.classList.remove('copied');
                    button.setAttribute('aria-label', 'Copy code to clipboard');
                }, 2000);
                
            } catch (error) {
                console.error('Failed to copy code:', error);
                
                // Show error feedback briefly
                const copyText = button.querySelector('.copy-text');
                const originalText = copyText.textContent;
                copyText.textContent = 'Failed';
                button.style.color = '#dc3545'; // Error color
                
                setTimeout(() => {
                    copyText.textContent = originalText;
                    button.style.color = '';
                }, 2000);
            }
        });
    });
});
