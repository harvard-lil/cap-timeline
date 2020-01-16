<template>
    <div class="timeline">
        <nav class="navbar main-nav fixed-top">
            <a id='skip-nav' class='screenreader-text' href='#main-content'>
                Skip to content
            </a>

            <span class="navbar-brand">
                <span class="nav-title">
                  <router-link :to="'/'+slug">
                    {{title}}
                  </router-link>
                </span>
            </span>
            <span class="home-link">
                <router-link to="/">
                  <svgicon class='icon symbol-home' icon="home"
                           width="18" height="18">
                  </svgicon>
                </router-link>
            </span>
        </nav>

        <nav class="sidebar" v-if="inTimeline()">
            <toggles></toggles>
        </nav>
        <router-view></router-view>
    </div>
</template>

<script>
  import store from "../store";
  import Toggles from './Toggles';
  import './icons/home';

  export default {
    name: "TimelineApp",
    components: {Toggles},
    data() {
      return {
        events: {},
        activeYears: [],
        years: [],
      }
    },

    methods: {
      getYear(date) {
        return Number(date.split('-')[0])
      },
      updateParams(param, val) {
        if (!(this.inTimeline())) {
          return
        }
        let newQuery = Object.assign({}, this.$route.query);
        if (val) {
          newQuery[param] = val;
        }
        if (Object.keys(newQuery).length && JSON.stringify(newQuery) !== JSON.stringify(this.$route.query)) {
          this.$router.push({query: newQuery});
        }
      },
      inTimeline() {
        return this.$route.name === 'timeline';
      }
    },
    computed: {
      activeGroups() {
        return store.getters.getActiveGroups;
      },
      eventSelected() {
        return store.getters.getSelectedEvent;
      },
      minYear() {
        return store.getters.getMinYear;
      },
      maxYear() {
        return store.getters.getMaxYear;
      },
      activeEvents() {
        return store.getters.getActiveEvents;
      },
      zoom() {
        return store.getters.getZoomLevel;
      },
      slug() {
        return store.getters.getSlug;
      },
      title() {
        return store.getters.getTitle;
      }
    },
    watch: {
      minYear(year) {
        this.updateParams('minyear', year.toString())
      },
      maxYear(year) {
        this.updateParams('maxyear', year.toString())
      },
      activeEvents(newEvents) {
        let events = newEvents.join(',');
        if (newEvents.length) {
          if (this.$route.query.groups && newEvents.length === this.$route.query.groups.split(',').length)
            return;
        } else {
          if (!(this.$route.query.groups))
            return;
          events = '';
        }
        this.updateParams('events', events)
      },
      activeGroups() {
        this.updateParams('groups', this.activeGroups.join(','));
      },
      zoom(newZoom) {
        this.updateParams('zoom', newZoom)
      },
    },
    beforeCreate() {
      let slug = window.location.pathname.split('/')[1];
      store.dispatch('setTimelineSlug', slug);
      store.dispatch('setMetadata');
      store.dispatch('loadYears');
      store.dispatch('loadEventTypes');
      store.dispatch('loadGroupsByRegion');
      store.dispatch('loadThemes');

      if (this.$route.query.event)
        store.commit('setSelectedEvent', Number(this.$route.query.event));

      if (this.$route.query.events) {
        // if specific events are mentioned, activate those
        let startingActiveEvents = this.$route.query.events.split(',');
        for (let i = 0; i < startingActiveEvents.length; i++) {
          store.commit("setEventStatus", {name: startingActiveEvents[i], status: true})
        }
      } else {
        // otherwise activate all events
        store.commit("activateAllEvents")
      }

      if (this.$route.query.groups) {
        let startingGroups = this.$route.query.groups.split(',');
        for (let i = 0; i < startingGroups.length; i++) {
          store.commit("setGroupStatus", {slug: startingGroups[i], status: true})
        }
        store.dispatch('loadGroups', false);
      } else {
        // otherwise activate all groups
        store.dispatch('loadGroups', true);
      }
    },
  }
</script>
