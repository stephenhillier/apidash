<template>
  <div class="w-full">
    <form
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
      @submit.prevent="handleAddMonitor"
    >
      <div class="mb-4">
        <label
          class="block text-gray-800 text-sm font-bold mb-2"
          for="monitorName"
        >
          Monitor name
        </label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:shadow-outline"
          id="monitorName"
          type="text"
          placeholder="A name for this monitor"
          v-model="form.name"
        />
      </div>
      <div class="mb-4">
        <label
          class="block text-gray-800 text-sm font-bold mb-2"
          for="endpoint"
        >
          Endpoint URL
        </label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:shadow-outline"
          id="endpoint"
          type="text"
          placeholder="Endpoint URL (e.g. https://example.com/api/v1/users)"
          v-model="form.endpoint"
        />
      </div>
      <div class="w-full md:w-1/3 mb-4">
        <label class="block text-gray-800 text-sm font-bold mb-2" for="method">
          HTTP Method
        </label>
        <div class="relative">
          <select
            class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-800 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="method"
            v-model="form.method"
          >
            <option value="get">GET</option>
          </select>
          <div
            class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-800"
          ></div>
        </div>
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Add Monitor
        </button>
      </div>
    </form>
  </div>
</template>
<script lang="ts">
import axios from "axios";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MonitorListCard extends Vue {
  form = {
    name: "",
    endpoint: "",
    method: "get"
  };
  handleAddMonitor() {
    axios
      .post("http://localhost:8000/api/v1/monitors", this.form)
      .then(r => {
        this.$emit("mon:created");
      })
      .catch(e => {});
  }
}
</script>

<style lang="scss"></style>
