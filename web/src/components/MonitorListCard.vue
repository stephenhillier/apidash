<template>
  <div class="lg:flex mt-2 bg-white border rounded shadow p-2">
    <div class="w-full lg:w-1/6 bg-white">
      <i
        class="status"
        :class="{
          ok: status === stats.OK,
          warning: status === stats.WARN,
          error: status === stats.ERR
        }"
      ></i
      >{{ name }}
    </div>
    <div class="w-full lg:w-3/6 bg-white">{{ endpoint }}</div>
    <div class="w-full lg:w-1/6 bg-white text-center">
      <i
        v-for="(s, i) in dailyStatus"
        :key="i"
        class="status-box"
        :class="{
          ok: s === stats.OK,
          warning: s === stats.WARN,
          error: s === stats.ERR
        }"
      ></i>
    </div>
    <div class="w-full lg:w-1/6 bg-white text-right">
      <a
        href="#"
        @click.prevent="handleDelete"
        class="inline-block text-sm leading-none text-indigo-500 hover:text-indigo-700"
        >Delete</a
      >
    </div>
  </div>
</template>
<script lang="ts">
import axios from "axios";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MonitorListCard extends Vue {
  @Prop(Number) readonly id!: number;
  @Prop(Number) readonly status!: number;
  @Prop(String) readonly name!: string;
  @Prop(String) readonly endpoint!: string;
  stats = {
    OK: 0,
    WARN: 1,
    ERR: 2
  };
  dailyStatus = [0, 0, 1, 0, 2, 0, 0];
  handleDelete() {
    axios
      .delete(`http://localhost:8000/api/v1/monitors/${this.id}`)
      .then(r => {
        this.$emit("mon:deleted");
      })
      .catch(e => {});
  }
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
.status-box {
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
    border-radius: 0px;
  }
}
</style>
