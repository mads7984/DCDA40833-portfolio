/**
 * DCDA 40833 Skills Portfolio
 * Responsive Navigation Menu Handler
 * Vanilla JavaScript - No frameworks required
 */

// Wait for DOM to be fully loaded before running script
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the hamburger button and navigation menu
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    // Check if elements exist before adding event listener
    if (hamburger && navMenu) {
        // Toggle menu when hamburger button is clicked
        hamburger.addEventListener('click', function() {
            // Toggle 'active' class on both hamburger and menu
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Update aria-expanded for accessibility
            const isExpanded = navMenu.classList.contains('active');
            hamburger.setAttribute('aria-expanded', isExpanded);
        });
        
        // Close menu when a navigation link is clicked (improves UX on mobile)
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Remove active classes
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
        
        // Close menu when clicking outside of it
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navMenu.contains(event.target);
            const isClickOnHamburger = hamburger.contains(event.target);
            
            // If click is outside nav and hamburger, close the menu
            if (!isClickInsideNav && !isClickOnHamburger && navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Handle window resize - reset menu state when switching to desktop view
        let resizeTimer;
        window.addEventListener('resize', function() {
            // Debounce resize events
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                // If window is wider than 768px, ensure menu is in correct state
                if (window.innerWidth > 768) {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            }, 250);
        });
    }
});
