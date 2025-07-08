
function renderSummaries(summaries) {
    const container = document.getElementById("summaryContainer");
    if (!summaries || summaries.length === 0) {
        container.innerHTML = '<p>No summaries found for this date.</p>';
        return;
    }
    container.innerHTML = summaries.map(item => {
        let tagsHtml = '';
        if (item.tags && item.tags.length) {
            tagsHtml = `<div class="tags">${item.tags.map(t => `<span class='tag'>${t}</span>`).join(' ')}</div>`;
        }
        // Format summary: each bullet point (•, -, *) to new line
        let formattedSummary = (item.summary || '<em>No summary yet.</em>')
            .replace(/\n/g, '<br>')
            .replace(/([•\-*])\s?/g, '<br>$1 ')
            .replace(/^<br>/, '');
        return `
            <div class="summary-card plycard">
                <h3>${item.title}</h3>
                <p class="ministry">${item.ministry}</p>
                <div class="summary-text">${formattedSummary}</div>
                ${tagsHtml}
            </div>
        `;
    }).join('');
}

document.getElementById("datePicker").addEventListener("change", function() {
    const selectedDate = this.value;
    fetch(`../data/${selectedDate}.json`)
        .then(res => res.json())
        .then(data => {
            renderSummaries(data.summaries);
        })
        .catch(() => {
            document.getElementById("summaryContainer").innerHTML = "<p>No data found for this date.</p>";
        });
});

window.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().slice(0, 10);
    document.getElementById('datePicker').value = today;
    const event = new Event('change');
    document.getElementById('datePicker').dispatchEvent(event);
});
