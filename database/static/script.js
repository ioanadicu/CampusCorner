document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("toggle-switch");
    const flipCard = document.getElementById("flip-card");

    toggleSwitch.addEventListener("change", function () {
        if (this.checked) {
            flipCard.classList.add("flipped");
        } else {
            flipCard.classList.remove("flipped");
        }
    });
});
