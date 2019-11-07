<template>
  <div class="app-container" :class="eventSelected ? 'event-selected event-selected-'+eventSelected : ''">
    <nav class="navbar main-nav fixed-top">
      <div class="navbar-brand">
        <span class="nav-title">
          <router-link to="/">
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
        this.$http.get('http://localhost:8000/events')
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
      }

    },
    watch: {
      activeGroups(newGroups) {
        // updating route to match active groups
        let newQuery = {};
        newQuery = Object.assign({}, this.$route.query);
        if (newGroups.length > 0) {
          newQuery['groups'] = newGroups.join(',')
        } else {
          delete newQuery['groups']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});

      },
      // eventSelected(newEvent) {
      //   let newQuery = Object.assign({}, this.$route.params);
      //   if (newEvent) {
      //     newQuery.event_id = newEvent;
      //   } else {
      //     delete newQuery.event_id['event']
      //   }
      //   Object.keys(newQuery).length ?
      //       this.$router.push({params: newQuery}) : this.$router.push({});
      // },
      minYear(year) {
        let newQuery = Object.assign({}, this.$route.query);
        if (year) {
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
          newQuery.maxyear = year;
        } else {
          delete newQuery['maxyear']
        }
        Object.keys(newQuery).length ?
            this.$router.push({query: newQuery}) : this.$router.push({});
      }

    },
    beforeCreate() {
      this.$store.dispatch('loadGroups');
      if (this.$route.query.event)
        this.$store.commit('setSelectedEvent', Number(this.$route.query.event));
      if (this.$route.query.year)
        this.$store.commit('setSelectedYear', Number(this.$route.query.year))
    },
    created() {
      this.getData();
    },
  };
</script>