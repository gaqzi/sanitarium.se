// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const menuOverlay = document.querySelector('.menu-overlay');
    const menuNav = document.querySelector('.menu-nav');
    const body = document.body;
    
    if (menuToggle) {
        // Toggle menu on button click
        menuToggle.addEventListener('click', function() {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            toggleMenu(!isExpanded);
        });
        
        // Close menu when clicking overlay
        if (menuOverlay) {
            menuOverlay.addEventListener('click', function() {
                toggleMenu(false);
            });
        }
        
        // Close menu when clicking menu links (on mobile)
        if (menuNav) {
            const menuLinks = menuNav.querySelectorAll('.menu-link');
            menuLinks.forEach(link => {
                link.addEventListener('click', function() {
                    // Only close on mobile
                    if (window.innerWidth <= 768) {
                        toggleMenu(false);
                    }
                });
            });
        }
        
        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && body.classList.contains('menu-open')) {
                toggleMenu(false);
            }
        });
        
        // Handle resize events
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && body.classList.contains('menu-open')) {
                toggleMenu(false);
            }
        });
    }
    
    function toggleMenu(show) {
        if (show) {
            body.classList.add('menu-open');
            menuToggle.setAttribute('aria-expanded', 'true');
            menuOverlay.classList.add('active');
            
            // Focus management for accessibility
            const firstMenuLink = menuNav.querySelector('.menu-link');
            if (firstMenuLink) {
                firstMenuLink.focus();
            }
        } else {
            body.classList.remove('menu-open');
            menuToggle.setAttribute('aria-expanded', 'false');
            menuOverlay.classList.remove('active');
            
            // Return focus to toggle button
            menuToggle.focus();
        }
    }

    // Copy button functionality for code blocks
    const copyButtons = document.querySelectorAll('.copy-button');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            // Find the code element within the same highlight div
            const highlightDiv = button.closest('.copy-enabled');
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
