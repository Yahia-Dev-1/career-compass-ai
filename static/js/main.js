// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenu = document.getElementById('mobileMenu');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileMenu && navLinks) {
        mobileMenu.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Add fade-in animation to elements using Intersection Observer
    const fadeElements = document.querySelectorAll('.feature-card, .recommendation-card, .glass-card, .fade-in');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Also keep the manual style override for elements that don't use the class
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(el => {
            if (el) {
                // If it doesn't have the fade-in class, apply initial styles manually
                if (!el.classList.contains('fade-in')) {
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(20px)';
                    el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                }
                observer.observe(el);
            }
        });
    } else {
        // Fallback for older browsers
        fadeElements.forEach(el => {
            if (el) {
                el.classList.add('visible');
                el.style.opacity = '1';
            }
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (navbar) {
            if (window.scrollY > 20) {
                navbar.style.padding = '0.5rem 0';
                navbar.style.background = 'rgba(15, 23, 42, 0.9)';
            } else {
                navbar.style.padding = '0.75rem 0';
                navbar.style.background = 'rgba(15, 23, 42, 0.8)';
            }
        }
    });
});
