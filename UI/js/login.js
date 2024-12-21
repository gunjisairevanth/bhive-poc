document.getElementById('login-btn').addEventListener('click', function () {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
});

document.getElementById('register-btn').addEventListener('click', function () {
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
});
