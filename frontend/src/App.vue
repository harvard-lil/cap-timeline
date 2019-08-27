<template>
  <div clss="row">
    <div class="col-2">
      <ul v-for="year in years">
        <li>{{ year }}</li>
      </ul>
    </div>
    <div class="col-10">
      <ul v-for="event in events">
        <li>{{ event }}</li>
      </ul>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'App',
    components: {},
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
        console.log('getyearssss')
        for (let i=0; i<this.maxYear-this.minYear+1; i++) {
          console.log(i)
          this.years.push(this.minYear + i)
        }
        console.log(this.years)
      },
    }
    ,
    data() {
      return {
        events: {},
        minYear: 9999,
        maxYear: 0,
        years: [],
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