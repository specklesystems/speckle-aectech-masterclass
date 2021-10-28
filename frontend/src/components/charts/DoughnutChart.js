import { Doughnut, mixins } from 'vue-chartjs'
import Chart from "chart.js"
const { reactiveProp } = mixins

export default {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: ['options'],
  data(){
    return {
      oldClick: Chart.defaults.global.legend.onClick
    }
  },
  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, this.options)
  }
}