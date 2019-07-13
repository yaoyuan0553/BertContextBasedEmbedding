import 'reflect-metadata';

import Vue from 'vue';
import 'font-awesome/css/font-awesome.css';
import 'jquery';
// import BootstrapVue from 'bootstrap-vue';
import 'bootstrap';
import 'bootstrap-fileinput';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap-fileinput/css/fileinput.css';
// import 'bootstrap-fileinput/themes/fas/theme';


import App from './App.vue';


Vue.config.productionTip = false;
// Vue.use(BootstrapVue);


const vm: Vue = new Vue({
  render: (h) => h(App),
});

vm.$mount('#app');
