import 'reflect-metadata';

import Vue from 'vue';
import 'jquery';

import 'bootstrap';
import 'bootstrap-fileinput';
import 'bootstrap-fileinput/js/locales/zh';
import 'bootstrap-fileinput/themes/fas/theme';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap-fileinput/css/fileinput.css';
import '@fortawesome/fontawesome-free/css/all.css';

import App from './App.vue';


Vue.config.productionTip = false;


const vm: Vue = new Vue({
  render: (h) => h(App),
});

vm.$mount('#app');
