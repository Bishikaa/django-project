function animateNumber(el, target, duration = 800) {
    if (!el) return;
    const start = 0;
    const startTime = performance.now();
    function tick(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = (start + (target - start) * eased).toFixed(1);
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = target.toFixed(1);
    }
    requestAnimationFrame(tick);
}

function initDashboard(chartLabels, chartScores, subjectLabels, subjectScores) {
    const ctx = document.getElementById('productivityChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Productivity Score',
                    data: chartScores,
                    borderColor: '#e8836b',
                    backgroundColor: 'rgba(232, 131, 107, 0.1)',
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#e8836b',
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 900, easing: 'easeOutQuart' },
                scales: { y: { min: 0, max: 100, title: { display: true, text: 'Score' } } },
                plugins: { legend: { display: false } }
            }
        });
    }

    const subjectCtx = document.getElementById('subjectChart');
    if (subjectCtx) {
        new Chart(subjectCtx, {
            type: 'bar',
            data: {
                labels: subjectLabels,
                datasets: [{
                    label: 'Avg Productivity',
                    data: subjectScores,
                    backgroundColor: '#9cae92',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 900, easing: 'easeOutQuart' },
                scales: { y: { min: 0, max: 100 } },
                plugins: { legend: { display: false } }
            }
        });
    }

    document.querySelectorAll('.big-number[data-target]').forEach(el => {
        animateNumber(el, parseFloat(el.dataset.target));
    });
}