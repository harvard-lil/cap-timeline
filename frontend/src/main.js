import Vue from 'vue'
import App from './App.vue'
import Resource from 'vue-resource';
import './assets/css/styles.scss';
import router from '../router';


Vue.use(Resource);
Vue.config.productionTip = false;

new Vue({
  router: router,
  render: h => h(App),
}).$mount("#app");