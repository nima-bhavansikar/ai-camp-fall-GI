// darkmode.js

// darkmode.js
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const body = document.body;

    // Function to toggle dark mode class and save user preference to the server
    function toggleDarkMode() {
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');

        // Send an AJAX request to save the dark mode preference to the server
        fetch('/accounts/toggle-dark-mode/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': "{{ csrftoken }}",  // Include CSRF token for security
            },
            body: JSON.stringify({ dark_mode: isDarkMode }),
        });
    }

    // Event listener for the dark mode toggle button
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }

    // Check user's preference from the server and set dark mode accordingly
    fetch('/accounts/get-dark-mode/')
        .then(response => response.json())
        .then(data => {
            if (data.dark_mode) {
                body.classList.add('dark-mode');
            }
        });

});


/*
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const body = document.body;

    function toggleDarkMode() {
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('dark-mode', isDarkMode);
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }

    const isDarkModeStored = localStorage.getItem('dark-mode');
    if (isDarkModeStored === 'true') {
        body.classList.add('dark-mode');
    }
});
*/