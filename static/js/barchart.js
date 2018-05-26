var ctx_1 = document.getElementById("morris-bar-chart");
var myChart = new Chart(ctx_1, {
    type: 'bar',
    data: {
//        labels: ["{{rank_l[0]}}", "{{rank_l[1]}}", "{{rank_l[2]}}", "{{rank_l[3]}}", "{{rank_l[4]}}", "{{rank_l[5]}}","{{rank_l[6]}}"],
        labels:[1,2,3,4,5,6,7]
        datasets: [{
            label: 'Production',
            data:[1,2,3,4,5,6,7]
//            data: [{{rank_v[0]}}, {{rank_v[1]}}, {{rank_v[2]}}, {{rank_v[3]}}, {{rank_v[4]}}, {{rank_v[5]}},{{rank_v[6]}}],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                 'rgba(255, 200, 64, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 200, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
var ctx_2 = document.getElementById("morris-bar-chart2");
var myChart = new Chart(ctx_2, {
    type: 'bar',
    data: {
        labels: ["{{rank_l[0]}}", "{{rank_l[1]}}", "{{rank_l[2]}}", "{{rank_l[3]}}", "{{rank_l[4]}}", "{{rank_l[5]}}","{{rank_l[6]}}"],
        datasets: [{
            label: 'Unit Price',
            data: [{{rank_v[0]}}, {{rank_v[1]}}, {{rank_v[2]}}, {{rank_v[3]}}, {{rank_v[4]}}, {{rank_v[5]}},{{rank_v[6]}}],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                 'rgba(255, 200, 64, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 200, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
