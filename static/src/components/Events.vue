<template>
  <div class="event-list-container">
    <template v-for="(events_per_year, year) in events">
      <year v-if="(year >= $parent.minYear) && year <= ($parent.maxYear)"
            v-bind:key="year"
            :value="year"
            :events="events_per_year"
            :minYear="minYear"
            :maxYear="maxYear"
            :selectedEvent="selectedEvent">
      </year>
    </template>
  </div>
</template>

<script>
  import Vue from 'vue';
  import Year from "./Year"
  import store from '../store';

  export default {
    name: "events",
    components: {Year},
    props: ["selectedEvent"],
    data() {
      return {
        events: {},
        years: {}
      }
    },
    methods: {
      getGroups() {
        let url = process.env.VUE_APP_BACKEND_DATA_URL + this.slug + '/groups';
        this.$http.get(url)
            .then((response) => {
              this.groups = response.body;
            })
      },

      getData() {
        let url = process.env.VUE_APP_BACKEND_DATA_URL + this.slug + '/events';
        this.$http.get(url)
            .then((response) => {
              for (let i = 0; i < response.body.length; i++) {
                let year = this.getYear(response.body[i].start_date);
                if (year in this.events) {
                  this.events[year].push(response.body[i]);
                  Vue.set(this.events, year, this.events[year])
                } else {
                  Vue.set(this.events, year, [response.body[i]])
                }
              }
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
      },
      slug() {
        return store.getters.getSlug;
      }
    },
    watch: {
      slug() {
        this.getData();
        this.getGroups();
      }
    },
  }
</script>
