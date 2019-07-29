<template>
  <div class="w-full py-1">
    <!--Metric Card-->
    <div class="bg-white border rounded shadow p-2">
      <i
        class="status"
        :class="{
          ok: status === stats.OK,
          warning: status === stats.WARN,
          error: status === stats.ERR
        }"
      ></i>
      <span class="font-semibold">{{ name }}</span>
    </div>
    <!--/Metric Card-->
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MonitorListCard extends Vue {
  @Prop(Number) readonly status!: number;
  @Prop(String) readonly name!: string;
  stats = {
    OK: 0,
    WARN: 1,
    ERR: 2
  };
}
</script>

<style scoped lang="scss">
.status {
  &.ok:before {
    background-color: #94e185;
    border-color: #78d965;
  }

  &.warning:before {
    background-color: #ffc182;
    border-color: #ffb161;
  }

  &.error:before {
    background-color: #c9404d;
    border-color: #c42c3b;
  }

  &:before {
    content: " ";
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 10px;
    border: 1px solid #000;
    border-radius: 7px;
  }
}
</style>
