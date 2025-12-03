function signup() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !password) {
        alert("All fields are required!");
        return;
    }

    fetch("/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Signup successful! Please login.");
            window.location.href = "/"; // Redirect to login
        } else {
            alert(data.message || "Signup failed");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error while signing up");
    });
}

function googleSignup() {
    window.location.href = "/auth/google";  
}
fetch('/signup', {
    method: "POST",
    body: formData
})
.then(async res => {
    const text = await res.text();  
    console.log("RAW RESPONSE:", text);  // 👈 shows real backend error
})
.catch(err => console.error(err));
