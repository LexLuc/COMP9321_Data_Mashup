var ctx = document.getElementById('morris-line-chart1').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["2005", "2006", "2007", "2008", "2009", "2010", "2011","2012","2013","2014"],
        datasets: [{
            label: "Unit Price for Export",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor:'rgb(255, 99, 132)',
            data: [],
            fill:false
        },
         {label: "Cost Value",
            backgroundColor: 'rgb(100, 99, 132)',
            borderColor:'rgb(100, 99, 132)',
            data: [],
            fill:false
            }
        ]
    },

    // Configuration options go here
    options: {}
});
var ctx = document.getElementById('morris-line-chart2').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["2005", "2006", "2007", "2008", "2009", "2010", "2011","2012","2013","2014"],
        datasets: [{
            label: "Production",
            backgroundColor: 'rgb(200, 99, 100)',
            borderColor:'rgb(200, 99, 100)',
            data: [],
            fill:false
        },
         {label: "Sales volume",
            backgroundColor: 'rgb(30, 99, 22)',
            borderColor:'rgb(30, 99, 22)',
            data: [],
            fill:false
            }
        ]
    },

    // Configuration options go here
    options: {}
});
