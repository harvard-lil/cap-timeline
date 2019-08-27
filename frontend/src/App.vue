<template>
  <div class="container-fluid">
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">
        Immigration in U.S.
      </a>
    </nav>
    <div clss="row">
      <nav class="sidebar d-none d-md-block col-md-2">
        <div class="sidebar-sticky">
          <ul class="year-list">
            <li v-on:click="setCurrentYear(year)"
                v-for="year in years" :key="year">
              {{ year }}
            </li>
          </ul>
        </div>
      </nav>
      <main class="col-md-9 ml-sm-auto col-lg-10">
        <ul class="event-list">
          <li class="event"
              v-for="eventObj in events"
              :key="eventObj.id">
            <event :currentYear="currentYear"
                   :data="eventObj">
            </event>
          </li>
        </ul>
      </main>
    </div>
  </div>
</template>
<script>
  import Event from "./components/Event"

  export default {
    name: 'App',
    components: {Event,},
    methods: {
      getData() {
        this.$http.get('http://localhost:8000/events')
            .then((response) => {
              this.events = response.body
              this.getDates();
            }, response => {
              // error callback
            })
      },
      getDates() {
        for (let i = 0; i < this.events.length; i++) {
          let year = Number(this.events[i]['start_date'].split('-')[0]);
          this.minYear = year < this.minYear ? year : this.minYear;
          this.maxYear = year > this.maxYear ? year : this.maxYear;
        }
        this.getYears()
      },
      getYears() {
        for (let i = 0; i < this.maxYear - this.minYear + 1; i++) {
          this.years.push(this.minYear + i)
        }
      },
      getYear(date) {
        return Number(date.split('-')[0])

      },
      setCurrentYear(year) {
        this.currentYear = year;
      }
    }
    ,
    data() {
      return {
        events: {},
        minYear: 9999,
        maxYear: 0,
        years: [],
        currentYear: undefined,
      }
    }
    ,
    created() {
      this.getData()
    }
    ,
  }
  ;
</script>