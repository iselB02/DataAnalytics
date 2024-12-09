let histogramChart, barChart, lineChart, pieChart;

// Data for visualizations
const data = {
    labels: ['A', 'B', 'C', 'D', 'E'],
    dataset: [10, 20, 30, 40, 50],
    pieDataset: [25, 15, 35, 25]
};

// Function to open tabs
function openTab(evt, tabName) {
    let i, tabcontent, tablinks;

    // Hide all tab content
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove active class from all tab buttons
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the clicked tab content and add active class to the button
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // Render chart for the selected tab
    if (tabName === "histogram") {
        renderHistogram();
    } else if (tabName === "barChart") {
        renderBarChart();
    } else if (tabName === "lineChart") {
        renderLineChart();
    } else if (tabName === "pieChart") {
        renderPieChart();
    }
}

// Function to render Histogram
function renderHistogram() {
    const ctx = document.getElementById('histogramCanvas').getContext('2d');
    if (histogramChart) histogramChart.destroy();
    histogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Frequency',
                data: data.dataset,
                backgroundColor: '#ff69b4',
                borderColor: '#ff69b4',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Function to render Bar Chart
function renderBarChart() {
    const ctx = document.getElementById('barChartCanvas').getContext('2d');
    if (barChart) barChart.destroy();
    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Bar Chart Dataset',
                data: data.dataset,
                backgroundColor: '#ffb6c1',
                borderColor: '#ffb6c1',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Function to render Line Chart
function renderLineChart() {
    const ctx = document.getElementById('lineChartCanvas').getContext('2d');
    if (lineChart) lineChart.destroy();
    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Line Chart Dataset',
                data: data.dataset,
                borderColor: '#ff69b4',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Function to render Pie Chart
function renderPieChart() {
    const ctx = document.getElementById('pieChartCanvas').getContext('2d');
    if (pieChart) pieChart.destroy();
    pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Category 1', 'Category 2', 'Category 3', 'Category 4'],
            datasets: [{
                label: 'Pie Chart Dataset',
                data: data.pieDataset,
                backgroundColor: ['#ffb6c1', '#ff69b4', '#fac6ce', '#ffcccb'],
                borderColor: '#fff',
                borderWidth: 1
            }]
        }
    });
}

// Initialize default tab (Histogram)
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".tablinks").click();
});

// Update chart functions
function updateHistogram() {
    const color = document.getElementById('histogramColor').value;
    const bins = parseInt(document.getElementById('histogramBins').value, 10);
    if (isNaN(bins) || bins <= 0) {
        alert('Please enter a valid number of bins');
        return;
    }

    histogramChart.data.datasets[0].backgroundColor = color;
    histogramChart.data.datasets[0].data = Array(bins).fill().map(() => Math.floor(Math.random() * 20));
    histogramChart.update();
}

function updateBarChart() {
    const color = document.getElementById('barColor').value;
    const width = parseInt(document.getElementById('barWidth').value, 10);
    barChart.data.datasets[0].backgroundColor = color;
    barChart.data.datasets[0].data = Array(4).fill().map(() => Math.floor(Math.random() * 100));
    barChart.options.scales.x = { barThickness: width };
    barChart.update();
}

function updateLineChart() {
    const color = document.getElementById('lineColor').value;
    const width = parseInt(document.getElementById('lineWidth').value, 10);
    lineChart.data.datasets[0].borderColor = color;
    lineChart.data.datasets[0].data = Array(5).fill().map(() => Math.floor(Math.random() * 10));
    lineChart.data.datasets[0].borderWidth = width;
    lineChart.update();
}

function updatePieChart() {
    const color = document.getElementById('pieColor').value;
    const labelSize = parseInt(document.getElementById('pieLabel').value, 10);
    pieChart.data.datasets[0].backgroundColor = [color, '#0000ff', '#ffff00'];
    pieChart.update();
}
