window.timerInterval = null;
window.timerValue = 60;

window.startTimer = function() {
    clearInterval(window.timerInterval);
    window.timerValue = 60;
    window.timerInterval = setInterval(function() {
        if (window.timerValue <= 0) {
            clearInterval(window.timerInterval);
            document.getElementById("timer").innerHTML = "Time's up!";
            
            // Redirect ke halaman utama setelah timer habis
            setTimeout(function() {
                window.location.href = '/';  // Redirect ke halaman utama
            }, 1000);  // Tunggu 1 detik sebelum redirect
        } else {
            document.getElementById("timer").innerHTML = window.timerValue + "s";
        }
        window.timerValue -= 1;
    }, 1000);
};

window.resetTimer = function() {
    window.startTimer();
};

// 🛟 Pastikan timer berjalan setiap kali halaman baru di-load
document.body.addEventListener('htmx:afterSettle', function(evt) {
    if (document.getElementById('timer')) {  // Cek kalau ada timer di halaman
        startTimer();
    }
});
