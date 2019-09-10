<template>
  <div class="app-container">
    <nav class="navbar navbar-dark fixed-top">
      <div class="navbar-brand">
        <a href="#">
          Immigration in U.S.
        </a>
      </div>
    </nav>
    <nav class="sidebar">
      <div class="sidebar-sticky">
        <ul class="year-list">
          <li class="year">
              <span @click="setCurrentYear(undefined)"
                    :class="currentYear === undefined ? 'active selected' :  'active'">
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
      </div>
    </nav>
    <main class="main">
      <router-view></router-view>
    </main>
  </div>
</template>
<script>
  export default {
    name: 'App',
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
        if (year)
          this.$router.push({name: 'events', query: {year: year}});
        else {
          this.$router.push({name: 'events'})
        }
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

    created() {
      this.getData();
      this.getActiveYears();
    },
  };
</script>