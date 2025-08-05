window.timerInterval = null;
window.timerValue = 60;
window.timerStarted = false;

window.startTimer = function() {
    clearInterval(window.timerInterval);
    window.timerValue = 60;

    window.timerInterval = setInterval(function() {
        const timerElement = document.getElementById("timer");

        if (!timerElement) {
            clearInterval(window.timerInterval);
            return;
        }

        if (window.timerValue <= 0) {
            clearInterval(window.timerInterval);
            timerElement.innerHTML = "Time's up!";
            setTimeout(function() {
                window.location.href = '/';
            }, 1000);
        } else {
            timerElement.innerHTML = window.timerValue + "s";
        }
        window.timerValue -= 1;
    }, 1000);
};

window.resetTimer = function() {
    startTimer();
};

document.body.addEventListener('htmx:afterSettle', function(evt) {
    if (document.getElementById('timer') && !window.timerStarted) {
        window.timerStarted = true;
        startTimer();
    }
});

document.body.addEventListener('htmx:afterOnLoad', function(evt) {
    let triggerHeader = evt.detail.xhr.getResponseHeader("HX-Trigger");
    if (triggerHeader && triggerHeader.includes("qr-claimed")) {
        window.location.href = "/";
    }
});
