import Vue from 'vue';
import Router from 'vue-router';
import Events from '../src/components/Events';

Vue.use(Router);
export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: 'events'
    },
    {
      path: '/events',
      name: 'events',
      component: Events,
    },

  ]
});
