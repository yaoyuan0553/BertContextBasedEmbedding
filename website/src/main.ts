import Vue from 'vue';
import App from './App.vue';

Vue.config.productionTip = false;

const vm: Vue = new Vue({
  render: (h) => h(App),
});

vm.$mount('#app');

// const app = vm.$children[0] as App;
// const bodyTag: HTMLBodyElement = document.getElementsByTagName('body')[0];
//
// bodyTag.onkeyup = (e: KeyboardEvent) => {
//   if (e.key === 'Enter') {
//       // app.$refs.computeButton.$refs.computeButton.click();
//   }
// };
