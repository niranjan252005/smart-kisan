// Manual Login
async function manualLogin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.success) {
        window.location.href = "/dashboard";
    } else {
        alert("Invalid Credentials");
    }
}

// Google Login
function googleLogin() {
    google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleResponse,
    });
    google.accounts.id.prompt(); 
}

async function handleGoogleResponse(response) {
    const res = await fetch("/auth/google-login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ credential: response.credential })
    });

    const data = await res.json();

    if (data.success) {
        window.location.href = "http://localhost:5000/auth/google/login";
    } else {
        alert("Google login failed");
    }
}
