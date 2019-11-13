<template>
  <div class="event-list-container">
    <template v-for="(events_per_year, year) in events" v-if="(year >= $parent.minYear) && year <= ($parent.maxYear)">
      <div class="event-year-section">
        <h1 class="event-year">{{ year}}</h1>
      </div>
      <ul class="event-list">
        <event :class="'event-list-item event-type-' + eventObj.type"
               v-for="eventObj in events_per_year"
               :key="eventObj.id"
               :currentYear="currentYear"
               :minYear="minYear"
               :maxYear="maxYear"
               :selectedEvent="selectedEvent"
               :data="eventObj">
        </event>
      </ul>
    </template>
  </div>
</template>

<script>
  import Vue from 'vue';
  import Event from "./Event"
  import store from '../store';

  export default {
    name: "events",
    components: {Event},
    props: ["currentYear", "selectedEvent"],
    data() {
      return {
        events: {},
      }
    },
    methods: {
      getGroups() {
        let url = 'http://localhost:8000/groups';
        this.$http.get(url)
            .then((response) => {
              this.groups = response.body;
            })
      },

      getData() {
        let url = 'http://localhost:8000/events';
        this.$http.get(url)
            .then((response) => {
              for (let i = 0; i < response.body.length; i++) {
                let year = this.getYear(response.body[i].start_date)
                if (year in this.events) {
                  this.events[year].push(response.body[i])
                  Vue.set(this.events, year, this.events[year])
                } else {
                  Vue.set(this.events, year, [response.body[i]])
                }
              }
              // this.events = response.body.sort((a, b) => {
              //   return this.getYear(a.start_date) - this.getYear(b.start_date)
              // })
            })
      },

      getYear(date) {
        return Number(date.split('-')[0])
      },
    },
    computed: {
      minYear() {
        return store.getters.getMinYear;
      },
      maxYear() {
        return store.getters.getMaxYear;
      }
    },
    created() {
      this.getData();
      this.getGroups();
    },
  }
</script>
