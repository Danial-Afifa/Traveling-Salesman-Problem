document.getElementById('runBtn').addEventListener('click', runSimulation);

function runSimulation() {
    fetch('/run', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('output').innerText = `Best solution: ${data.solution} with fitness: ${data.fitness}`;
        })
        .catch(error => console.error('Error:', error));
}