<template>
  <div class="timeline">
    <div class="container-wrapper">
      <template v-for="(year,idx) in years">
        <div class="year-label" :class="'col-'+getIdx(idx)">{{year}}</div>
        <template v-for="event in events[year]">
          <div class="event-container"
               :class="['event-type-'+event.type, 'span' + getLength(event), 'col-'+getIdx(idx)]">
            <div class="event-type">{{event.type}}</div>
            {{event.name}}
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue';

  export default {
    name: "TimelineView",
    data() {
      return {
        years: [],
        events: {}
      }
    },
    methods: {
      getGroups() {
        let url = 'http://localhost:8000/data/groups';
        this.$http.get(url)
            .then((response) => {
              this.groups = response.body;
            })
      },
      getData() {
        let url = 'http://localhost:8000/data/events';
        this.$http.get(url)
            .then((response) => {
              for (let i = 0; i < response.body.length; i++) {
                let year = this.getYear(response.body[i].start_date);
                if (year in this.events) {
                  this.events[year].push(response.body[i])
                  Vue.set(this.events, year, this.events[year])
                } else {
                  Vue.set(this.events, year, [response.body[i]])
                }
              }
            })
      },
      getLength(event) {
        if (!(event.end_date)) {
          return 1;
        }
        let startYear = this.getYear(event.start_date);
        let endYear = this.getYear(event.end_date);
        return endYear - startYear;
      },
      getYear(date) {
        return Number(date.split('-')[0])
      },
      getIdx(idx) {
        return idx + 1;
      }
    },
    beforeMount() {
      for (const x of Array(20).keys()) {
        this.years.push(x + 1905)
      }
    },
    created() {
      this.getData();
      this.getGroups();
    },

  }
</script>

<style scoped>

</style>