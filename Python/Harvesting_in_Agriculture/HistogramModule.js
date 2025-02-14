const HistogramModule = function(bins, canvas_width, canvas_height) {
    // Create the canvas object:
    const canvas = document.createElement("canvas");
    Object.assign(canvas, {
        width: canvas_width,
        height: canvas_height,
        style: "border:1px dotted",
    });
    // Append it to #elements:
    const elements = document.getElementById("elements");
    elements.appendChild(canvas);

    // Create the context and the drawing controller:
    const context = canvas.getContext("2d");

    // Prep the chart properties and series:
    const datasets = [{
        label: "Data",
        backgroundColor: "rgba(173,216,230,0.5)",  // Brighter fill color
        borderColor: "rgba(173,216,230,1)",        // Brighter border color
        borderWidth: 1,
        data: []
    }];

    // Add a zero value for each bin
    for (let i in bins) {
        datasets[0].data.push(0);
    }

    const data = {
        labels: bins,
        datasets: datasets
    };

    const options = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    // Create the chart object
    let chart = new Chart(context, {
        type: 'bar',
        data: data,
        options: options
    });

    this.render = function(data) {
        datasets[0].data = data;
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        chart = new Chart(context, {
            type: 'bar',
            data: data,
            options: options
        });
    };
};
