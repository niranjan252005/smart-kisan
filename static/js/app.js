document.getElementById('manual-btn').addEventListener('click', async ()=>{
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if(!email || !password){ alert('enter credentials'); return; }
    const res = await fetch('/login', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if(res.ok){ window.location.href = '/dashboard'; }
    else { alert(data.message || 'Login failed'); }
});

document.getElementById('google-btn').addEventListener('click', ()=>{
    window.location.href = '/google/login';
});
