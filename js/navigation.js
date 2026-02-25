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

    // =========================
    // Dark Mode Toggle Handler
    // =========================

    // I have some pretty basic JavaScript knowledge, but at first glance this was confusing to understand. The AI already provided comments for this code, which helped with my understanding of how it works and reminded me of the syntax of JavaScript. I've become very used to coding in Python, but I've been able to draw connections between the two languages to translate what is being done.
    const themeSwitch = document.getElementById('theme-switch');
    
    // Check if theme switch exists before adding functionality
    if (themeSwitch) {
        // Check for saved theme preference or default to light mode
        const currentTheme = localStorage.getItem('theme') || 'light';
        
        // Apply saved theme on page load
        if (currentTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeSwitch.checked = true;
        }
        
        // Toggle dark mode when switch is clicked
        themeSwitch.addEventListener('change', function() {
            if (this.checked) {
                // Enable dark mode
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                // Enable light mode
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
        
        // Optional: Listen for system theme preference changes
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        
        // Only apply system preference if user hasn't set their own preference
        if (!localStorage.getItem('theme')) {
            if (prefersDarkScheme.matches) {
                document.body.classList.add('dark-mode');
                themeSwitch.checked = true;
            }
        }
        
        // Listen for changes to system preference
        prefersDarkScheme.addEventListener('change', function(e) {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                if (e.matches) {
                    document.body.classList.add('dark-mode');
                    themeSwitch.checked = true;
                } else {
                    document.body.classList.remove('dark-mode');
                    themeSwitch.checked = false;
                }
            }
        });
    }
});
