import { CountUp } from "./countUp.min.js";

window.updateAvailabilityUI = function(id, value) {
    const numberElement = document.getElementById(id + "-number");
    if (!numberElement) return;

    const startValue = parseInt(numberElement.textContent) || 0;
    const countUp = new CountUp(numberElement, value, {
        startVal: startValue,
        duration: 1.5,
        suffix: "%"
    });

    const bar = document.getElementById(id + "-fill");
    if (bar) {
        bar.style.transition = 'height 1.5s ease-in-out';
        bar.style.height = value + "%";
    }

    if (!countUp.error) {
        countUp.start();
    } else {
        console.error(`CountUp Error:`, countUp.error);
    }
}

function initializeCounters() {
    console.log("Initializing counters...");
    ["count1", "count2", "count3", "count4"].forEach(id => {
        const element = document.getElementById(id + "-number");
        if(element) {
            const initialValue = parseInt(element.getAttribute("data-value")) || 0;
            window.updateAvailabilityUI(id, initialValue);
        }
    });
}

document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.querySelector(".avail-page-content")) {
        initializeCounters();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector(".avail-page-content")) {
        initializeCounters();
    }
});