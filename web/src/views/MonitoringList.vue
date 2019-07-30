<template>
  <div class="container w-full mx-auto pt-10">
    <div class="w-full px-4 md:px-0 md:mt-8 mb-16 text-gray-700 leading-normal">
      <!--Console Content-->

      <div class="flex flex-wrap">
        <div class="w-full md:w-1/2 xl:w-1/4 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-1 text-center">
                <h5 class="uppercase text-grey">Active Endpoint Monitors</h5>
                <h3 class="text-3xl">{{ monitors.length }}</h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/4 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-1 text-center">
                <h5 class="uppercase text-grey">Healthy Endpoints</h5>
                <h3 class="text-3xl">
                  {{
                    monitors.filter(item => {
                      return item.status === 0;
                    }).length
                  }}
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/4 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-1 text-center">
                <h5 class="uppercase text-grey">Unhealthy Endpoints</h5>
                <h3 class="text-3xl">
                  {{
                    monitors.filter(item => {
                      return item.status !== 0;
                    }).length
                  }}
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/4 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-1 text-center">
                <h5 class="uppercase text-grey">
                  Days since last outage
                </h5>
                <h3 class="text-3xl">17 days</h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
      </div>
    </div>
    <div>
      <div
        class="w-full flex-grow lg:flex lg:items-center lg:w-auto mt-2 lg:mt-0 bg-white z-20"
        id="nav-content"
      >
        <ul class="list-reset lg:flex flex-1 items-center px-4 md:px-0">
          <li class="mr-6 my-2 md:my-0">
            <a
              href="#"
              class="block py-1 md:py-3 pl-1 align-middle text-indigo-700 text-gray-500 no-underline hover:text-gray-900"
            >
              <i class="fas fa-tasks fa-fw mr-3"></i
              ><span class="pb-1 md:pb-0 text-sm">All Monitors</span>
            </a>
          </li>
          <li class="mr-6 my-2 md:my-0">
            <a
              href="#"
              class="block py-1 md:py-3 pl-1 align-middle text-gray-500 no-underline hover:text-gray-900"
            >
              <i class="fa fa-exclamation-triangle fa-fw mr-3"></i
              ><span class="pb-1 md:pb-0 text-sm">Unhealthy Monitors</span>
            </a>
          </li>
        </ul>
        <div class="relative pull-right pl-4 px-4 md:px-0">
          <div>
            <a
              href="#"
              @click.prevent="addMonitor = !addMonitor"
              class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-transparent bg-indigo-500 hover:bg-indigo-700 mt-4 lg:mt-0"
              >{{ addMonitor ? "Cancel" : "Add monitor" }}</a
            >
          </div>
        </div>
      </div>
    </div>
    <div v-if="addMonitor" class="px-4 md:px-0">
      <AddMonitor @mon:created="handleMonitorAdded"></AddMonitor>
    </div>
    <div class="px-4 md:px-0">
      <h1 class="text-lg my-4">api.islandcivil.com</h1>
      <template v-for="(monitor, i) in monitors">
        <monitor-list-card
          :id="monitor.id"
          :name="monitor.name"
          :status="monitor.status"
          :endpoint="monitor.endpoint"
          :key="i"
          @mon:deleted="handleMonitorDeleted"
        ></monitor-list-card>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { Component, Prop, Vue } from "vue-property-decorator";
import MonitorListCard from "@/components/MonitorListCard.vue";
import AddMonitor from "@/components/AddMonitor.vue";

@Component({
  components: {
    "monitor-list-card": MonitorListCard,
    AddMonitor
  }
})
export default class MonitoringHome extends Vue {
  addMonitor = false;
  monitors = [];

  handleMonitorAdded() {
    this.addMonitor = false;
    this.fetchMonitors();
  }

  handleMonitorDeleted() {
    this.fetchMonitors();
  }

  fetchMonitors() {
    axios
      .get("http://localhost:8000/api/v1/monitors")
      .then(r => {
        this.monitors = r.data;
      })
      .catch(e => {});
  }

  created() {
    this.fetchMonitors();
  }
}
</script>

<style lang="scss"></style>
