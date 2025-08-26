// Wait for the entire HTML document to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Select the form element from the login.html file
    const loginForm = document.querySelector('.login-container form');

    // Add an event listener for when the form is submitted
    loginForm.addEventListener('submit', (event) => {
        // Prevent the default browser behavior of refreshing the page on submit
        event.preventDefault();

        // Get the values from the email and password input fields
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // --- Simple Client-Side Validation (Optional but recommended) ---
        if (email.trim() === '' || password.trim() === '') {
            alert('Please enter both your email and password.');
            return; // Stop the function if validation fails
        }

        // --- Log the data for testing purposes ---
        console.log('Form Submitted!');
        console.log('Email:', email);
        console.log('Password:', password);

        // --- Placeholder for an API call to your backend server ---
        // In a real application, you would send this data to your server
        // to verify the user's credentials. For example, using the fetch() API:
        //
        // fetch('/api/login', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ email, password }),
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.success) {
        //         console.log('Login successful!');
        //         // Redirect the user to their dashboard or home page
        //         window.location.href = '/dashboard.html';
        //     } else {
        //         console.log('Login failed:', data.message);
        //         // Display an error message to the user
        //     }
        // })
        // .catch(error => {
        //     console.error('Error during login:', error);
        // });
    });
});