<template>
  <div class="app-container" :class="'route-'+$route.name">
    <nav class="navbar main-nav fixed-top">
      <div class="navbar-brand">
        <span class="nav-title">
          <router-link to="/">
          U.S. IMMIGRATION TIMELINE
        </router-link>
        </span>
      </div>
    </nav>
    <nav class="sidebar" v-if="showSidebar()">
      <toggles></toggles>
    </nav>
    <main class="main" :class="'route-'+$route.name">
      <router-view :selectedEvent="eventSelected">
      </router-view>
    </main>
  </div>
</template>
<script>
  import store from './store';
  import Toggles from './components/Toggles';

  export default {
    name: 'App',
    components: {Toggles},
    methods: {
      getData() {
        this.$http.get('http://localhost:8000/data/events')
            .then((response) => {
              this.events = response.body.sort((a, b) => {
                return this.getYear(a.start_date) - this.getYear(b.start_date)
              });
            })
      },
      getYear(date) {
        return Number(date.split('-')[0])
      },
      updateParams(param, val) {
        if (this.$route.name === 'eventview')
          return;
        let newQuery = Object.assign({}, this.$route.query);
        if (!(val)) {
          delete newQuery[param];
        } else {
          newQuery[param] = val;
        }
        this.$router.push({query: newQuery});
      },
      showSidebar() {
        if (this.$route.name === 'eventview')
          return false;
        return true;
      }
    },
    data() {
      return {
        events: {},
        activeYears: [],
        years: [],
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
      }
    },
    watch: {
      activeGroups(newGroups) {
        // updating route to match active groups
        let groups = newGroups.join(',');
        if (newGroups.length) {
          if (this.$route.query.groups && newGroups.length === this.$route.query.groups.split(',').length)
            return;
        } else {
          if (!(this.$route.query.groups))
            return;
          groups = '';
        }
        this.updateParams('groups', groups)
      },
      minYear(year) {
        this.updateParams('minyear', year)
      },
      maxYear(year) {
        this.updateParams('maxyear', year)
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
      zoom(newZoom) {
        this.updateParams('zoom', newZoom)
      }
    },
    beforeCreate() {
      if (this.$route.query.event)
        this.$store.commit('setSelectedEvent', Number(this.$route.query.event));

      if (this.$route.query.events) {
        // if specific events are mentioned, activate those
        let startingActiveEvents = this.$route.query.events.split(',');
        for (let i = 0; i < startingActiveEvents.length; i++) {
          this.$store.commit("setEventStatus", {name: startingActiveEvents[i], status: true})
        }
        // otherwise activate all events
      } else {
        this.$store.commit("activateAllEvents")
      }

      if (this.$route.query.groups) {
        let startingGroups = this.$route.query.groups.split(',');

        for (let i = 0; i < startingGroups.length; i++) {
          this.$store.commit("setGroupStatus", {slug: startingGroups[i], status: true})
        }
        // otherwise activate all groups
      } else {
        this.$store.commit("activateAllGroups")
      }


    },
    created() {
      this.getData();
    }
  };
</script>