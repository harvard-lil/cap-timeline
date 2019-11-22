<template>
  <div class="app-container" :class="eventSelected ? 'event-selected event-selected-'+eventSelected : ''">
    <nav class="navbar main-nav fixed-top">
      <div class="navbar-brand">
        <span class="nav-title">
          <router-link to="/t">
          U.S. IMMIGRATION TIMELINE
        </router-link>
        </span>
      </div>
    </nav>
    <div class="subtitle-bar"></div>
    <nav class="sidebar">
      <toggles></toggles>
    </nav>
    <main class="main">
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
        let newQuery = {};
        newQuery = Object.assign({}, this.$route.query);
        if (newGroups.length > 0) {
          // TODO: check if newgroups are same as old groups
          if (this.$route.query.groups && newGroups.length === this.$route.query.groups.split(',').length)
            return;
          newQuery['groups'] = newGroups.join(',')
        } else {
          if (!(this.$route.query.groups))
            return;
          delete newQuery['groups']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});
      },
      minYear(year) {
        let newQuery = Object.assign({}, this.$route.query);
        if (year) {
          if (Number(this.$route.query.minyear) === Number(year))
            return;
          newQuery.minyear = year;
        } else {
          delete newQuery['minyear']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});
      },
      maxYear(year) {
        let newQuery = Object.assign({}, this.$route.query);
        if (year) {
          if (Number(this.$route.query.maxyear) === Number(year))
            return;

          newQuery.maxyear = year;
        } else {
          delete newQuery['maxyear']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});
      },
      activeEvents(newEvents) {
        // updating route to match active groups
        let newQuery = {};
        newQuery = Object.assign({}, this.$route.query);
        if (newEvents.length > 0) {
          // TODO: check if newgroups are same as old groups
          if (this.$route.query.events && newEvents.length === this.$route.query.events.split(',').length)
            return;
          newQuery['events'] = newEvents.join(',')
        } else {
          delete newQuery['events']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});
      },
      zoom(newZoom, oldZoom) {
        if (newZoom === oldZoom)
          return;
        let newQuery = {};
        newQuery = Object.assign({}, this.$route.query);
        newQuery['zoom'] = newZoom;
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});

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