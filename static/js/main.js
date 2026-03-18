document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    const toggleButton = document.querySelector('.navbar-toggler');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Example of dynamic content loading
    fetch('/api/city-data')
        .then(response => response.json())
        .then(data => {
            console.log('City Data:', data);
            // Implement dynamic content update here
        });
});
