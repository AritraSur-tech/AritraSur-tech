// Fitness Forecast - Frontend JavaScript

let weightChart = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Set default date to today
    document.getElementById('date').value = new Date().toISOString().split('T')[0];

    // Load initial data
    loadEntries();

    // Set up form submission
    document.getElementById('weight-form').addEventListener('submit', handleSubmit);
});

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const weight = parseFloat(document.getElementById('weight').value);
    const date = document.getElementById('date').value;
    const notes = document.getElementById('notes').value;

    try {
        const response = await fetch('/api/entries', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ weight, date, notes })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Weight logged successfully!', 'success');
            document.getElementById('weight-form').reset();
            document.getElementById('date').value = new Date().toISOString().split('T')[0];
            loadEntries();
        } else {
            showToast(data.error || 'Failed to add entry', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
    }
}

// Load all entries and update UI
async function loadEntries() {
    try {
        const [entriesRes, forecastRes] = await Promise.all([
            fetch('/api/entries'),
            fetch('/api/forecast')
        ]);

        const entries = await entriesRes.json();
        const forecastData = await forecastRes.json();

        renderTable(entries);
        renderChart(entries, forecastData);
        renderStats(forecastData);
        renderForecast(forecastData);

    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Render the entries table
function renderTable(entries) {
    const tbody = document.getElementById('entries-body');
    const emptyState = document.getElementById('empty-state');

    if (entries.length === 0) {
        tbody.innerHTML = '';
        emptyState.classList.add('show');
        return;
    }

    emptyState.classList.remove('show');

    // Show entries in reverse order (newest first)
    tbody.innerHTML = [...entries].reverse().map(entry => `
        <tr>
            <td>${formatDate(entry.date)}</td>
            <td><strong>${entry.weight}</strong> kg</td>
            <td>${entry.notes || '-'}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteEntry(${entry.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

// Render the weight chart
function renderChart(entries, forecastData) {
    const ctx = document.getElementById('weight-chart').getContext('2d');

    if (entries.length === 0) {
        if (weightChart) {
            weightChart.destroy();
            weightChart = null;
        }
        return;
    }

    const labels = entries.map(e => formatDate(e.date));
    const weights = entries.map(e => e.weight);

    // Add forecast data to the chart
    let forecastLabels = [];
    let forecastWeights = [];

    if (forecastData.forecast) {
        forecastLabels = forecastData.forecast.map(f => formatDate(f.date));
        forecastWeights = forecastData.forecast.map(f => f.predicted_weight);
    }

    // Prepare datasets
    const datasets = [
        {
            label: 'Actual Weight',
            data: weights,
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.3,
            pointBackgroundColor: '#4f46e5',
            pointRadius: 5,
            pointHoverRadius: 7
        }
    ];

    // Add forecast line if available
    if (forecastData.forecast && entries.length >= 2) {
        // Create a line from last actual point to forecast points
        const lastActualWeight = weights[weights.length - 1];

        datasets.push({
            label: 'Forecast',
            data: [...Array(weights.length - 1).fill(null), lastActualWeight, ...forecastWeights],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            tension: 0.3,
            pointBackgroundColor: '#10b981',
            pointRadius: 5,
            pointHoverRadius: 7
        });
    }

    const allLabels = [...labels, ...forecastLabels];

    if (weightChart) {
        weightChart.destroy();
    }

    weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14 },
                    bodyFont: { size: 14 },
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y} kg`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + ' kg';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Render stats
function renderStats(forecastData) {
    if (forecastData.stats) {
        const stats = forecastData.stats;

        document.getElementById('stat-starting').textContent = `${stats.starting_weight} kg`;
        document.getElementById('stat-current').textContent = `${stats.current_weight} kg`;

        const changeEl = document.getElementById('stat-change');
        const change = stats.total_change;
        changeEl.textContent = `${change > 0 ? '+' : ''}${change} kg`;
        changeEl.className = 'stat-value ' + (change < 0 ? 'positive' : change > 0 ? 'negative' : '');

        const trendEl = document.getElementById('stat-trend');
        const weeklyChange = stats.weekly_change;
        trendEl.textContent = `${weeklyChange > 0 ? '+' : ''}${weeklyChange}/wk`;
        trendEl.className = 'stat-value ' + (weeklyChange < 0 ? 'positive' : weeklyChange > 0 ? 'negative' : '');
    } else {
        document.getElementById('stat-starting').textContent = '--';
        document.getElementById('stat-current').textContent = '--';
        document.getElementById('stat-change').textContent = '--';
        document.getElementById('stat-trend').textContent = '--';
    }
}

// Render forecast cards
function renderForecast(forecastData) {
    const grid = document.getElementById('forecast-grid');

    if (!forecastData.forecast) {
        grid.innerHTML = '<p style="color: #6b7280; text-align: center; grid-column: 1/-1;">Add at least 2 weight entries to see your forecast!</p>';
        return;
    }

    grid.innerHTML = forecastData.forecast.map(f => `
        <div class="forecast-card">
            <div class="forecast-weeks">${f.weeks} Weeks</div>
            <div class="forecast-weight">${f.predicted_weight} kg</div>
            <div class="forecast-date">${formatDate(f.date)}</div>
        </div>
    `).join('');
}

// Delete an entry
async function deleteEntry(id) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }

    try {
        const response = await fetch(`/api/entries/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast('Entry deleted', 'success');
            loadEntries();
        } else {
            showToast('Failed to delete entry', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
    });
}

// Show toast notification
function showToast(message, type) {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}
