<template>
  <div>
    sdaf
  </div>
</template>
<script lang="ts">
import axios from "axios";
import moment from "moment";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MonitorListCard extends Vue {
  @Prop(Object) readonly monitor!: any;

  monitorData = [];

  getData() {
    axios
      .get(`http://localhost:8000/api/v1/monitors/${this.monitor.id}`)
      .then(r => {
        this.monitorData = r.data;
      });
  }

  created() {
    this.getData();
  }
}
</script>

<style lang="scss"></style>
