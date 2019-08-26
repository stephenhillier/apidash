<template>
  <div>
    <StatusChart
      v-if="dataLoaded"
      :options="chartOptions"
      :chartData="monitorData"
    ></StatusChart>
  </div>
</template>
<script lang="ts">
import axios from "axios";
import moment from "moment";
import { Component, Prop, Vue } from "vue-property-decorator";
import StatusChart from "./StatusChart.js";
import ICheckStatus from "../interfaces";
@Component({
  components: {
    StatusChart
  }
})
export default class MonitorListCard extends Vue {
  @Prop(Object) readonly monitor!: any;
  dataLoaded = false;
  monitorData = {};
  monitorInterval = 0;
  chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      xAxes: [
        {
          type: "time",
          scaleLabel: {
            display: true,
            labelString: "Time (UTC)"
          },
          time: {
            unit: "hour",
            round: "millisecond",
            displayFormats: {
              day: "MMM D",
              hour: "MMM D hA"
            }
          }
        }
      ],
      yAxes: [
        {
          id: "statusCodeAxis",
          display: true,
          scaleLabel: {
            display: true,
            labelString: "HTTP Code"
          },
          ticks: {
            suggestedMin: 0, // minimum will be 0, unless there is a lower value.
            suggestedMax: 549
          }
        },
        {
          id: "latencyAxis",
          type: "logarithmic",
          position: "right",
          scaleLabel: {
            display: true,
            labelString: "Latency (ms)"
          },
          ticks: {
            suggestedMin: 0, // minimum will be 0, unless there is a lower value.
            suggestedMax: 1000
          }
        }
      ]
    }
  };

  transformData(data: ICheckStatus[]) {
    return {
      datasets: [
        {
          label: "Status Code",
          lineTension: 0,
          yAxisID: "statusCodeAxis",
          fill: false,
          pointBackgroundColor: (context: any) => {
            var index = context.dataIndex;
            var value = context.dataset.data[index].y;
            let color;
            if (value >= 200 && value < 300) {
              return "green";
            }

            return "red";
          },
          data: data.map((o: ICheckStatus) => {
            return {
              x: new Date(o.check_time),
              y: o.status_code
            };
          })
        },
        {
          label: "Latency",
          fill: false,
          lineTension: 0,
          pointBackgroundColor: "#5a67d8",
          backgroundColor: "#5a67d8",
          pointRadius: 2,
          yAxisID: "latencyAxis",
          data: data.map((o: ICheckStatus) => {
            return {
              x: new Date(o.check_time),
              y: o.latency
            };
          })
        }
      ]
    };
  }

  getData() {
    axios
      .get(`http://localhost:8000/api/v1/monitors/${this.monitor.id}`)
      .then(r => {
        this.monitorData = this.transformData(r.data);
        this.dataLoaded = true;
      });
  }

  created() {
    this.getData();
    this.monitorInterval = setInterval(() => {
      this.getData();
    }, 15000);
  }

  beforeDestroy() {
    clearInterval(this.monitorInterval);
  }
}
</script>

<style lang="scss"></style>
