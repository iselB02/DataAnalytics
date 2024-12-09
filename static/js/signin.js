import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";

// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyCFpkDoaAVkg1XBFU5Dcf4SWiY10dCdOvc",
    authDomain: "crown-bi-104d5.firebaseapp.com",
    projectId: "crown-bi-104d5",
    storageBucket: "crown-bi-104d5.firebasestorage.app",
    messagingSenderId: "76328144610",
    appId: "1:76328144610:web:9941378df818849ae358bb",
    measurementId: "G-XY45Y5W55E"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Get form elements
const loginForm = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

// Login Functionality
loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    // Simple validation for empty fields
    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    // Optional: Show a loading spinner or disable the button
    const loginButton = loginForm.querySelector("button");
    loginButton.disabled = true;
    loginButton.textContent = "Logging in...";

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Login successful!");
            console.log("User logged in:", userCredential.user);
            window.location.href = "/home"; // Redirect to home page
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        })
        .finally(() => {
            // Enable the login button and reset its text
            loginButton.disabled = false;
            loginButton.textContent = "Login";
        });
});
