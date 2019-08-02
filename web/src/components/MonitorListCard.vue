<template>
  <div class="lg:flex mt-2 bg-white border rounded shadow p-2">
    <div class="w-full lg:w-1/6 bg-white text-gray-900">
      <i
        class="status"
        :class="{
          ok: monitor.current_status === 0,
          warning: monitor.current_status === 1,
          error: monitor.current_status === 2
        }"
      ></i
      >{{ monitor.name }}
    </div>
    <div class="w-full lg:w-3/6 bg-white text-gray-900">
      {{ monitor.endpoint }}
    </div>
    <div class="w-full lg:w-1/6 bg-white text-center">
      <i
        v-for="(s, i) in monitor.weekly"
        :key="i"
        class="status-box"
        v-tooltip.top-center="
          `Date: ${s.date}, Successful: ${s.num_ok}, Errors: ${s.num_fail}`
        "
        :class="{
          noCheck: s.num_fail + s.num_ok === 0,
          ok: s.num_fail === stats.OK && s.num_fail + s.num_ok > 0,
          warning: s.num_fail === stats.WARN && s.num_fail + s.num_ok > 0,
          error: s.num_fail >= stats.ERR && s.num_fail + s.num_ok > 0
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
  @Prop(Object) readonly monitor!: any;
  stats = {
    OK: 0,
    WARN: 1,
    ERR: 2
  };
  dailyStatus = [0, 0, 1, 0, 2, 0, 0];
  handleDelete() {
    axios
      .delete(`http://localhost:8000/api/v1/monitors/${this.monitor.id}`)
      .then(r => {
        this.$emit("mon:deleted");
      })
      .catch(e => {});
  }
}
</script>

<style lang="scss">
.tooltip {
  display: block !important;
  z-index: 10000;

  .tooltip-inner {
    background: #d7dbfa;
    color: #333333;
    border-radius: 16px;
    padding: 5px 10px 4px;
  }

  .tooltip-arrow {
    width: 0;
    height: 0;
    border-style: solid;
    position: absolute;
    margin: 5px;
    border-color: black;
    z-index: 1;
  }

  &[x-placement^="top"] {
    margin-bottom: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 0 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      bottom: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="bottom"] {
    margin-top: 5px;

    .tooltip-arrow {
      border-width: 0 5px 5px 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-top-color: transparent !important;
      top: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="right"] {
    margin-left: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 5px 0;
      border-left-color: transparent !important;
      border-top-color: transparent !important;
      border-bottom-color: transparent !important;
      left: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[x-placement^="left"] {
    margin-right: 5px;

    .tooltip-arrow {
      border-width: 5px 0 5px 5px;
      border-top-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      right: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &.popover {
    $color: #f9f9f9;

    .popover-inner {
      background: $color;
      color: black;
      padding: 24px;
      border-radius: 5px;
      box-shadow: 0 5px 30px rgba(black, 0.1);
    }

    .popover-arrow {
      border-color: $color;
    }
  }

  &[aria-hidden="true"] {
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.15s, visibility 0.15s;
  }

  &[aria-hidden="false"] {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.15s;
  }
}
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
  &.noCheck:before {
    background-color: #c7c7c7;
    border-color: #a3a3a3;
  }
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
