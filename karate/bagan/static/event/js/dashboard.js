console.log('hello world')

const dashboardSlug = document.getElementById('dashboard-slug').textContent.trim()
const user = document.getElementById('user').textContent.trim()
const dataInput = document.getElementById('data-input')
const submitBtn = document.getElementById('submit-btn')
const dataBox = document.getElementById('data-box')

const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}`);

socket.onmessage = function(e) {
    const {message, sender} = JSON.parse(e.data)
    dataBox.innerHTML += `<p>${sender}: ${message}</p>`;
    updateChart()
};

submitBtn.addEventListener('click', ()=> {
    const dataValue = dataInput.value
    console.log(user, dataValue)
    socket.send(JSON.stringify({
        'sender': user,
        'message': dataValue,
    }));
})

const ctx = document.getElementById('myChart').getContext("2d");
let chart;

const fetchChartData = async() => {
    const response = await fetch(window.location.href + '/chart')
    const data = await response.json()
    console.log(data)
    return data
}

const drawChart = async () => {
    const data = await fetchChartData();
    const { chartData, chartLabels } = data;

    chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: '% of contribution',
                data: chartData,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
};

const updateChart = async() => {
    if (chart) {
        chart.destroy()
    }

    await drawChart()
}

drawChart()