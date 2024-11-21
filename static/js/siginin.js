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

// Login Functionality
document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Login successful!");
            console.log("User logged in:", userCredential.user);
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        });
});
