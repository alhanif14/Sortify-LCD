import { CountUp } from "./countUp.min.js";

function startCountUp(id, value) {
    const options = { startVal: 0, duration: 2.5, useEasing: true, suffix: "%" };
    const countUp = new CountUp(id + "-number", value, options);

    const bar = document.getElementById(id + "-fill");
    if (bar) {
        setTimeout(() => {
            bar.style.height = value + "%";  // Progress naik ke atas
        }, 100);
    }

    if (!countUp.error) {
        countUp.start();
    } else {
        console.error("Error CountUp.js:", countUp.error);
    }
}

function checkElementsAndStartCountUp(root = document) {
    console.log("Checking elements...");

    const countUpIds = ["count1", "count2", "count3", "count4"];
    let allElementsExist = true;

    countUpIds.forEach(id => {
        if (!root.querySelector("#" + id + "-number")) {
            console.error(`Element ${id}-number not found.`);
            allElementsExist = false;
        }
    });

    if (allElementsExist) {
        countUpIds.forEach(id => {
            const element = root.querySelector("#" + id + "-number");
            const value = parseInt(element.getAttribute("data-value"));
            startCountUp(id, value);
        });
    } else {
        console.error("Some required elements are missing.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    checkElementsAndStartCountUp();
});

document.addEventListener("htmx:afterSwap", function () {
    console.log("HTMX content swapped");
    checkElementsAndStartCountUp();
});

