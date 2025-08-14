/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: window.ordersLabels || [],
    datasets: [
      {
        label: 'Pedidos',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: window.ordersData || [],
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Value',
        },
      },
    },
  },
}

// change this to the id of your chart element in HMTL
const lineCtx = document.getElementById('line')
window.myLine = new Chart(lineCtx, lineConfig)

const revenueLabels = window.revenueLabels || []
const revenueData = window.revenueData || []

const revenueConfig = {
  type: 'line',
  data: {
    labels: revenueLabels,
    datasets: [
      {
        label: 'Ganancia acumulada ($)',
        backgroundColor: '#7e3af2',
        borderColor: '#7e3af2',
        data: revenueData,
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Fecha',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Ganancia acumulada ($)',
        },
      },
    },
  },
}

const lineCtx2 = document.getElementById('line2')
window.myRevenueLine = new Chart(lineCtx2, revenueConfig)
