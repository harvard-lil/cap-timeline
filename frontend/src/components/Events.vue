<template>
  <div class="event-list-container">
    <ul class="event-list">
      <event :class="'event-list-item event-type-' + eventObj.type"
             v-for="eventObj in events"
             :key="eventObj.id"
             :currentYear="currentYear"
             :minYear="minYear"
             :maxYear="maxYear"
             :selectedEvent="selectedEvent"
             :data="eventObj">
      </event>
    </ul>
  </div>
</template>

<script>
  import Event from "./Event"
  import store from '../store';

  export default {
    name: "events",
    components: {Event},
    props: ["currentYear", "selectedEvent"],
    data() {
      return {
        events: [],
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
              this.events = response.body.sort((a, b) => {
                return this.getYear(a.start_date) - this.getYear(b.start_date)
              })
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
