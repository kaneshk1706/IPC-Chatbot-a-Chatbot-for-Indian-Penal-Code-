function displayOffenses() {
    const userInput = document.getElementById('userInput').value.toLowerCase();
    fetch('/offenses?keyword=' + userInput)
        .then(response => response.json())
        .then(data => {
            const offensesDiv = document.getElementById('offenses');
            offensesDiv.innerHTML = '';
            if (data.length > 0) {
                offensesDiv.innerHTML = '<h2>Matching Offenses:</h2>';
                data.forEach((offense, index) => {
                    offensesDiv.innerHTML += `<p onclick="getOffenseDetails('${offense}')">${index + 1}. ${offense}</p>`;
                });
            } else {
                offensesDiv.innerHTML = '<p>No matching offenses found.</p>';
            }
        });
}

function getOffenseDetails(offense) {
    fetch('/offense_details?offense=' + offense)
        .then(response => response.json())
        .then(data => {
            const detailsDiv = document.getElementById('details');
            detailsDiv.innerHTML = `<h3>Offense Description:</h3><p>${data.description}</p><h3>Punishment:</h3><p>${data.punishment}</p><h3>IPC Section:</h3><p>${data.section}</p>`;
            translateDetails(offense);
        });
}

function translateDetails(offense) {
    fetch('/translate_offense_details?offense=' + offense)
        .then(response => response.json())
        .then(data => {
            const translationDiv = document.getElementById('translation');
            translationDiv.innerHTML = `<h3>Translated Description:</h3><p>${data.description}</p><h3>Translated Punishment:</h3><p>${data.punishment}</p><h3>Translated IPC Section:</h3><p>${data.ipc_section}</p>`;
        });
}


