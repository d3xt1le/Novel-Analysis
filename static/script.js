
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyze-form');
    const resultsList = document.getElementById('results-list');

    // Reset form and results on page load
    form.reset();
    resultsList.innerHTML = '';

    // Add event listener for form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // prevent page reload

        // Clear previous results
        const metadataSection = document.getElementById('metadata');
        const resultsList = document.getElementById('results-list');
        metadataSection.innerHTML = '';
        resultsList.innerHTML = '';

        // Get form values
        const url = document.getElementById('url').value;
        const num_words = document.getElementById('num_words').value;

        // Fetch data from the server
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, num_words })
        });

        const data = await response.json();

        // Check for errors or warnings in the response
        if (data.error) {
            const list_elem = document.createElement('li');
            list_elem.textContent = `Error: ${data.error}`;
            resultsList.appendChild(list_elem);

        } else {
            // Display metadata
            const metadataSection = document.getElementById('metadata');
            metadataSection.innerHTML = `
                <p><strong>Title:</strong> ${data.metadata.title || 'N/A'}</p>
                <p><strong>Author:</strong> ${data.metadata.author || 'N/A'}</p>
                <p><strong>Compiler:</strong> ${data.metadata.compiler || 'N/A'}</p>
                <p><strong>Release Date:</strong> ${data.metadata.release_date || 'N/A'}</p>
                <p><strong>Language:</strong> ${data.metadata.language || 'N/A'}</p>
                <p><strong>Original Publication:</strong> ${data.metadata.original_publication || 'N/A'}</p>
                <p><strong>Credits:</strong> ${data.metadata.credits || 'N/A'}</p>
            `;

            // Display word analysis results
            data.results.forEach(([word, count]) => {
                const list_elem = document.createElement('li');
                list_elem.textContent = `${word} (${count})`;
                resultsList.appendChild(list_elem);
            });
        }
    });
});
