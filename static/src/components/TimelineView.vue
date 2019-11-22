<template>
  <div class="timeline">
    <div class="container-wrapper">
      <template v-for="idx in maxYear-minYear">
        <div class="year-label"
             v-bind:key="idx+minYear"
             :class="'col-'+getIdx(idx)"> {{idx+minYear}}
        </div>
        <template v-for="event in events[idx+minYear]">
          <timeline-event v-bind:key="event.id" :event="event"
                          :class="['event-type-'+event.type, 'span' + getLength(event), 'col-'+getIdx(idx)]">
          </timeline-event>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue';
  import store from '../store';
  import TimelineEvent from "./TimelineEvent"

  export default {
    name: "TimelineView",
    components: {TimelineEvent},
    data() {
      return {
        years: [],
        events: {},
        groups: {},
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
                  this.events[year].push(response.body[i]);
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

<style scoped>

</style>