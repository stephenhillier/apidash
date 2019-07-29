import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// import { library } from '@fortawesome/fontawesome-svg-core';
// import { faWallet } from '@fortawesome/free-solid-svg-icons';

import "@/assets/tailwind.css";

/* tslint:disable:no-var-requires */
// const fontawesome = require('@fortawesome/vue-fontawesome');

// library.add(faWallet);

// Vue.component('font-awesome-icon', fontawesome.FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
