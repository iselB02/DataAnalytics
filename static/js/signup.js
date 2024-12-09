import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";

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

// Sign-Up Functionality
document.getElementById("signup-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Sign-up successful!");
            console.log("User registered:", userCredential.user);
            window.location.href = "/sign-in";
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        });
});
