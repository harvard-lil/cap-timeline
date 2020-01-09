import Vue from 'vue'
import VueSVGIcon from 'vue-svgicon'
import Resource from 'vue-resource';
import App from './App.vue'
import router from '../router';
import './assets/css/styles.scss';

import store from './store'

Vue.use(Resource);
Vue.use(VueSVGIcon);

Vue.config.productionTip = false;
router.beforeEach((to, from, next) => {
  if (to.params.slug) {
    document.title = "Timeline: " + to.params.slug;
  } else {
    document.title = to.meta.title;
  }
  next()
});

new Vue({
  router: router,
  render: h => h(App),
  store
}).$mount("#app");
