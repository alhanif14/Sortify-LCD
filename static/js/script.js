window.timerInterval = null;
window.timerValue = 60;

window.startTimer = function() {
    clearInterval(window.timerInterval);
    window.timerValue = 60;
    window.timerInterval = setInterval(function() {
        if (window.timerValue <= 0) {
            clearInterval(window.timerInterval);
            document.getElementById("timer").innerHTML = "Time's up!";
            
            setTimeout(function() {
                window.location.href = '/';
            }, 1000);
        } else {
            document.getElementById("timer").innerHTML = window.timerValue + "s";
        }
        window.timerValue -= 1;
    }, 1000);
};

window.resetTimer = function() {
    window.startTimer();
};

document.body.addEventListener('htmx:afterSettle', function(evt) {
    if (document.getElementById('timer')) {
        startTimer();
    }
});
