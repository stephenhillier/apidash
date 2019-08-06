<template>
  <div class="bg-white border rounded shadow mt-2">
    <div class="lg:flex p-2">
      <div class="w-full lg:w-1/6 bg-white text-gray-900">
        <i
          class="status"
          :class="{
            ok: monitor.last_check === 0,
            warning: monitor.last_check === 1,
            error: monitor.last_check === 2
          }"
        ></i
        >{{ monitor.name }}
      </div>
      <div class="w-full lg:w-2/6 bg-white text-gray-900">
        {{ monitor.endpoint }}
      </div>
      <div class="w-full lg:w-1/6 bg-white">
        <svg
          v-if="monitor.last_check !== 0"
          xmlns="http://www.w3.org/2000/svg"
          x="0px"
          y="0px"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          style=" fill:#c9404d;"
          class="float-right"
        >
          <path
            style="line-height:normal;text-indent:0;text-align:start;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000;text-transform:none;block-progression:tb;isolation:auto;mix-blend-mode:normal"
            d="M 12 3.0292969 C 11.436813 3.0292969 10.873869 3.2917399 10.558594 3.8164062 L 1.7617188 18.451172 C 1.1134854 19.529186 1.94287 21 3.2011719 21 L 20.796875 21 C 22.054805 21 22.886515 19.529186 22.238281 18.451172 L 13.441406 3.8164062 C 13.126131 3.29174 12.563187 3.0292969 12 3.0292969 z M 12 5.2988281 L 20.236328 19 L 3.7636719 19 L 12 5.2988281 z M 11 9 L 11 14 L 13 14 L 13 9 L 11 9 z M 11 16 L 11 18 L 13 18 L 13 16 L 11 16 z"
            font-weight="400"
            font-family="sans-serif"
            white-space="normal"
            overflow="visible"
          ></path>
        </svg>
      </div>
      <div class="w-full lg:w-1/6 bg-white text-center text-sm">
        <i
          class="status"
          :class="{
            noCheck: monitor.last_check === null,
            ok: monitor.last_check === 0,
            warning: monitor.last_check === 1,
            error: monitor.last_check === 2
          }"
        ></i
        >{{ lastChecked }}
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
          @click.prevent="toggleExpandCard"
          class="inline-block text-sm leading-none text-indigo-500 hover:text-indigo-700"
          >More info</a
        >

        <v-popover popoverClass="info" class="inline-block ml-3">
          <button class="text-sm text-red-500">Delete</button>
          <template slot="popover">
            Are you sure? This will delete your monitor and ALL status checks!
            <div>
              <a
                href="#"
                v-close-popover
                @click.prevent="handleDelete"
                class="inline-block text-sm leading-none border rounded text-indigo-500 hover:text-indigo-700 bg-white mt-4 p-2"
                >Confirm</a
              >
            </div>
          </template>
        </v-popover>
      </div>
    </div>
    <div v-if="expanded">
      <MonitorDetails :monitor="monitor"></MonitorDetails>
    </div>
  </div>
</template>
<script lang="ts">
import axios from "axios";
import moment from "moment";
import { Component, Prop, Vue } from "vue-property-decorator";
import MonitorDetails from "./MonitorDetails.vue";

@Component({
  components: {
    MonitorDetails
  }
})
export default class MonitorListCard extends Vue {
  @Prop(Object) readonly monitor!: any;
  @Prop(Date) readonly now!: Date;
  stats = {
    OK: 0,
    WARN: 1,
    ERR: 2
  };
  dailyStatus = [0, 0, 1, 0, 2, 0, 0];
  expanded = false;
  handleDelete() {
    axios
      .delete(`http://localhost:8000/api/v1/monitors/${this.monitor.id}`)
      .then(r => {
        this.$emit("mon:deleted");
      })
      .catch(e => {});
  }
  get lastChecked() {
    if (!this.monitor.last_checked) {
      return "Never";
    }
    return this.lastCheckedUTC.from(this.nowWithJitter);
  }
  get lastCheckedUTC() {
    return moment.utc(this.monitor.last_checked);
  }
  get nowWithJitter() {
    // account for offset between server and client
    return moment(this.now).add(1, "seconds");
  }
  toggleExpandCard() {
    this.expanded = !this.expanded;
  }
}
</script>

<style lang="scss">
.tooltip {
  display: block !important;
  z-index: 10000;

  &.info {
    $color: #5a67d8 !important;

    .tooltip-inner {
      background: $color;
      color: white !important;
      padding: 24px;
      border-radius: 5px;
      box-shadow: 0 5px 30px rgba(black, 0.1) !important;
      max-width: 250px;
    }

    .tooltip-arrow {
      border-color: $color;
    }
  }

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
