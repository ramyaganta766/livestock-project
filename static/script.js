<script>
window.onload = function() {
    document.getElementById("loginModal").style.display = "flex";
}

function showSignup() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "block";
    document.getElementById("formTitle").innerText = "📝 Sign Up";
}

function showLogin() {
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("formTitle").innerText = "🔐 Login";
}

function goDashboard() {
    window.location.href = "/dashboard";
}
</script>
