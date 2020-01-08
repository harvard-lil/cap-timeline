import Vue from 'vue';
import Router from 'vue-router';
import Events from '../src/components/Events';
import EventView from '../src/components/EventView';
import TimelineView from '../src/components/TimelineView';
import HomeView from '../src/components/HomeView';
import TimelineApp from '../src/components/TimelineApp';

Vue.use(Router);
export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/:slug/',
      name: 'timelineapp',
      component: TimelineApp,
      children: [
        {
          path: '/:slug/',
          name: 'timeline',
          component: TimelineView,
        },
        {
          path: '/:slug/events',
          name: 'events',
          component: Events,
        },
        {
          path: '/:slug/events/:event_id',
          name: 'eventview',
          component: EventView,
        }
      ]
    },
  ]
});
