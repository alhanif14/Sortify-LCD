import { CountUp } from "./countUp.min.js";

window.updateAvailability = function(id, value) {
    const numberElement = document.getElementById(id + "-number");
    const barElement = document.getElementById(id + "-fill");

    if (!numberElement || !barElement) {
        console.error(`Elemen untuk ID ${id} tidak ditemukan.`);
        return;
    }

    const oldValue = parseInt(numberElement.textContent) || 0;

    const options = { 
        startVal: oldValue, 
        duration: 1.5,
        useEasing: true, 
        suffix: "%" 
    };
    const countUp = new CountUp(numberElement, value, options);

    if (!countUp.error) {
        countUp.start();
        barElement.style.height = value + "%";
    } else {
        console.error("Error pada CountUp.js:", countUp.error);
    }
}

function initialCountUp(root = document) {
    console.log("Inisialisasi CountUp saat halaman dimuat...");
    const countUpIds = ["count1", "count2", "count3", "count4"];
    
    countUpIds.forEach(id => {
        const element = root.querySelector("#" + id + "-number");
        if (element) {
            const initialValue = parseInt(element.getAttribute("data-value")) || 0;
            window.updateAvailability(id, initialValue);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => initialCountUp());

document.addEventListener("htmx:afterSwap", () => initialCountUp());