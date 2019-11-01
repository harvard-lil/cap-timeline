<template>
  <div class="app-container" :class="eventSelected ? 'event-selected event-selected-'+eventSelected : ''">
    <nav class="navbar navbar-dark fixed-top">
      <div class="navbar-brand">
        <span class="nav-title">
          <router-link to="/">
          U.S. IMMIGRATION TIMELINE
        </router-link>
        </span>
        <span class="nav-title-blue" v-if="currentYear">{{currentYear}}</span>

      </div>
    </nav>
    <div class="subtitle-bar"></div>
    <nav class="sidebar">
      <toggles></toggles>
      <ul class="year-list">
        <li class="year">
              <span @click="setCurrentYear()"
                    :class="currentYear || eventSelected ? 'active' : 'active selected'">
                ALL
              </span>
        </li>
        <li v-for="year in years" :key="year" class="year">
              <span v-if="currentYear === year" class="active selected">
                {{ year }}
              </span>
          <span v-else-if="activeYears.includes(year)"
                @click="setCurrentYear(year)"
                class="active">{{ year }}</span>
          <span v-else>{{ year }}</span>
        </li>
      </ul>
    </nav>
    <main class="main">
      <router-view :currentYear="currentYear"
                   :selectedEvent="eventSelected">
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
      getActiveYears() {
        this.$http.get('http://localhost:8000/years')
            .then((response) => {
              this.activeYears = response.body;
              this.minYear = this.activeYears[0];
              this.maxYear = this.activeYears[this.activeYears.length - 1];
              this.backfillYears();
            })
      },
      backfillYears() {
        for (let i = 0; i < this.maxYear - this.minYear + 1; i++) {
          this.years.push(this.minYear + i)
        }
      },
      getYear(date) {
        return Number(date.split('-')[0])
      },
      setCurrentYear(year) {
        this.currentYear = year;
        store.commit('setSelectedYear', year);
        // TODO: is this right???
        store.commit('setSelectedEvent', null);
      }
    },
    data() {
      return {
        events: {},
        minYear: 9999,
        maxYear: 0,
        activeYears: [],
        years: [],
        currentYear: Number(this.$route.query.year),
      }
    },
    computed: {
      activeGroups() {
        return store.getters.getActiveGroups;
      },
      eventSelected() {
        return store.getters.getSelectedEvent;
      },
      yearSelected() {
        return store.getters.getSelectedYear;
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
      yearSelected(year) {
        let newQuery = Object.assign({}, this.$route.query);
        if (year) {
          newQuery.year = year;
        } else {
          delete newQuery['year']
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
      this.getActiveYears();
    },
  };
</script>