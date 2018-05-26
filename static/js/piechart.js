  var ctx = document.getElementById("morris-donut-chart");
    var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Scallop', 'Squid', 'Salmonids', 'Other_fish', 'Rock lobster', 'Oyster',
           'Tuna', 'Crab', 'Abalone', 'Prawns', 'Other_Molluscs', 'Other_Curstaceans'],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ['rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(230, 120, 132, 0.2)',
                'rgba(200, 140, 132, 0.2)',
                'rgba(180, 160, 132, 0.2)',
                'rgba(160, 180, 132, 0.2)',
                'rgba(140, 200, 132, 0.2)',
                'rgba(120, 220, 132, 0.2)',
                'rgba(120, 220, 70, 0.2)',
                'rgba(120, 220, 90, 0.2)'],
        data: [2478,5267,734,784,433]
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Predicted world population (millions) in 2050'
      }
    }
});
