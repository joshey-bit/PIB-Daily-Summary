
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


const API_BASE = "http://localhost:8000"; // Change if backend runs elsewhere



async function fetchAndRender(date) {
    // Get current time in user's local time (24h format)
    const now = new Date();
    const hour = now.getHours();
    let needUpdate = false;
    if (hour >= 21) {
        // After 9:00 PM, always update
        needUpdate = true;
    }
    try {
        const res = await fetch(`${API_BASE}/summaries/${date}`);
        if (!res.ok) throw new Error();
        if (needUpdate) {
            // After 9:00 PM, always POST to update
            document.getElementById("summaryContainer").innerHTML = "<p>Updating summaries for this date...</p>";
            const postRes = await fetch(`${API_BASE}/run-pipeline`, { method: 'POST' });
            if (postRes.ok) {
                setTimeout(() => fetchAndRender(date), 1200000);
                return;
            } else {
                document.getElementById("summaryContainer").innerHTML = "<p>Failed to update summaries. Please try again later.</p>";
                return;
            }
        }
        const data = await res.json();
        renderSummaries(data.summaries);
    } catch (e) {
        // If not found, try to trigger the pipeline
        document.getElementById("summaryContainer").innerHTML = "<p>Generating summaries for this date...</p>";
        try {
            const postRes = await fetch(`${API_BASE}/run-pipeline`, { method: 'POST' });
            if (postRes.ok) {
                setTimeout(() => fetchAndRender(date), 1200000);
            } else {
                document.getElementById("summaryContainer").innerHTML = "<p>Failed to generate summaries. Please try again later.</p>";
            }
        } catch (err) {
            document.getElementById("summaryContainer").innerHTML = "<p>Failed to generate summaries. Please try again later.</p>";
        }
    }
}

document.getElementById("datePicker").addEventListener("change", function() {
    const selectedDate = this.value;
    fetchAndRender(selectedDate);
});


window.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().slice(0, 10);
    document.getElementById('datePicker').value = today;
    fetchAndRender(today);

    // WebSocket for live updates
    const ws = new WebSocket('ws://localhost:8000/ws/updates');
    ws.onmessage = function(event) {
        if (event.data === 'update') {
            const date = document.getElementById('datePicker').value;
            fetchAndRender(date);
        }
    };
});
