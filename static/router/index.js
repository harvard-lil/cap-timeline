import Vue from 'vue';
import Router from 'vue-router';
import Events from '../src/components/Events';
import EventView from '../src/components/EventView';

Vue.use(Router);
export default new Router({
  mode: 'history',
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
    {
      path: '/events/:event_id',
      name: 'eventview',
      component: EventView,
    },

  ]
});
