<template>
  <!-- <div
    class="w-full flex-grow lg:flex lg:items-center lg:w-auto mt-2 bg-white border rounded shadow p-2"
  >
    <i
      class="status"
      :class="{
        ok: status === stats.OK,
        warning: status === stats.WARN,
        error: status === stats.ERR
      }"
    ></i>
    <span class="font-semibold">{{ name }}</span
    ><span class="ml-3">{{ endpoint }}</span>
    <div class="relative pull-right pl-4 pr-4 md:pr-0">
      <div>
        <a
          href="#"
          @click.prevent="addMonitor = !addMonitor"
          class="inline-block text-sm px-4 py-2 leading-none text-indigo-500 hover:text-indigo-700 mt-4 lg:mt-0"
          >Delete</a
        >
      </div>
    </div>
  </div> -->
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
    <div class="w-full lg:w-1/6 bg-white"></div>
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
</style>
