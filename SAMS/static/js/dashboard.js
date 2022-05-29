$(document).ready(function () {
  $(".input-daterange").datepicker({
    format: "dd-mm-yyyy",
    todayHighlight: true,
  });
});

const renderChart1 = (data, labels) => {
  var cntx = document.getElementById("myChart2").getContext("2d");
  var myChart2 = new Chart(cntx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Students",
          data: data,
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        title: {
          display: true,
          text: "Students per session",
          font: {
            size: 16,
          },
        },
      },
    },
  });
};

const renderChart2 = (data, labels) => {
  var cntx = document.getElementById("myChart3").getContext("2d");
  var myChart3 = new Chart(cntx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Students",
          data: data,
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        title: {
          display: true,
          text: "Students per branch",
          font: {
            size: 16,
          },
        },
      },
    },
  });
};
const renderChart3 = (data, labels) => {
  var cntx = document.getElementById("myChart4").getContext("2d");
  var myChart4 = new Chart(cntx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Students",
          data: data,
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
          ],
          hoverOffset: 4,
        },
      ],
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Students per course",
          font: {
            size: 16,
          },
        },
      },
    },
  });
};

const getChartData1 = () => {
  fetch("/chart-data1")
    .then((res) => res.json())
    .then((results) => {
      const students_data = results.data;
      const [labels, data] = [
        Object.keys(students_data),
        Object.values(students_data),
      ];
      renderChart1(data, labels);
    });
};

const getChartData2 = () => {
  fetch("/chart-data2")
    .then((res) => res.json())
    .then((results) => {
      const students_data = results.data;
      const [labels, data] = [
        Object.keys(students_data),
        Object.values(students_data),
      ];
      renderChart2(data, labels);
    });
};

const getChartData3 = () => {
  fetch("/chart-data3")
    .then((res) => res.json())
    .then((results) => {
      const students_data = results.data;
      const [labels, data] = [
        Object.keys(students_data),
        Object.values(students_data),
      ];
      renderChart3(data, labels);
    });
};

document.onload = getChartData1();
document.onload = getChartData2();
document.onload = getChartData3();
