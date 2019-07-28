<template>
  <div class="container w-full mx-auto pt-20">
    <div class="w-full px-4 md:px-0 md:mt-8 mb-16 text-gray-700 leading-normal">
      <!--Console Content-->

      <div class="flex flex-wrap">
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-green-dark">
                  <i class="fa fa-wallet fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">Total Revenue</h5>
                <h3 class="text-3xl">
                  $3249
                  <span class="text-green"
                    ><i class="fas fa-caret-up"></i
                  ></span>
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-orange-dark">
                  <i class="fas fa-users fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">Total Users</h5>
                <h3 class="text-3xl">
                  249
                  <span class="text-orange"
                    ><i class="fas fa-exchange-alt"></i
                  ></span>
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-yellow-dark">
                  <i class="fas fa-user-plus fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">New Users</h5>
                <h3 class="text-3xl">
                  2
                  <span class="text-yellow-dark"
                    ><i class="fas fa-caret-up"></i
                  ></span>
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-blue-dark">
                  <i class="fas fa-server fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">Server Uptime</h5>
                <h3 class="text-3xl">152 days</h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-indigo-dark">
                  <i class="fas fa-tasks fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">To Do List</h5>
                <h3 class="text-3xl">7 tasks</h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
        <div class="w-full md:w-1/2 xl:w-1/3 p-3">
          <!--Metric Card-->
          <div class="bg-white border rounded shadow p-2">
            <div class="flex flex-row items-center">
              <div class="flex-shrink pr-4">
                <div class="rounded p-3 bg-red-dark">
                  <i class="fas fa-inbox fa-2x fa-fw fa-inverse"></i>
                </div>
              </div>
              <div class="flex-1 text-right md:text-center">
                <h5 class="uppercase text-grey">Issues</h5>
                <h3 class="text-3xl">
                  3
                  <span class="text-red"><i class="fas fa-caret-up"></i></span>
                </h3>
              </div>
            </div>
          </div>
          <!--/Metric Card-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "home",
  components: {}
};
</script>
