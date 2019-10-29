<template>
  <div class="event-list-container">
    <ul class="event-list">
      <li class="event-list-item"
          v-for="eventObj in events"
          :class="'event-type-' + eventObj.type"
          @click="getDetails(eventObj.id)"
          :key="eventObj.id">
        <event :currentYear="currentYear"
               :selectedEvent="selectedEvent"
               :data="eventObj">
        </event>
      </li>
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
      getDetails(event) {
        if (event !== store.state.event)
          store.commit('setSelectedEvent', event);
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
    created() {
      this.getData();
      this.getGroups();
    },
  }
</script>
