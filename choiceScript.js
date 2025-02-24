document.addEventListener("DOMContentLoaded", handleChoice)
const choiceID = document.currentScript.getAttribute("choiceID");
const URL = "https://script.google.com/macros/s/AKfycbyrOlaMxiyEhBDkUfp6fuO2cH3KePGox33pt2FwihLow-z93HOGdja74c0nlV9h7xCB0A/exec?command=runChoice"

function handleChoice() {
    let elem = document.getElementById("choices");
    fetch(`${URL}&choiceID=${choiceID}`)
        .then(response => response.text())
        .then(responseText => elem.innerHTML = responseText)    
};
/**
 * Set choice in spreadsheet, then return choice text.
 * @param {String} choice The choice, should be a, b, c, or d.
 */
function setChoice(choice) {
    let elem = document.getElementById("choices");
    document.querySelectorAll("button.choice").forEach(
        elem => {
            elem.textContent = "Loading choice...";
            elem.disabled = true;
        }
    )
    fetch(`${URL}&choiceID=${choiceID}&choice=${choice}`)
        .then(response => response.text())
        .then(responseText => elem.innerHTML = responseText)    
}

