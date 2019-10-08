<template>
  <div class="event-list-container">
    <key></key>
    <ul class="event-list">
      <li class="event-list-item"
          v-for="eventObj in events"
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
  import Key from "./Key"
  import store from '../store';

  export default {
    name: "events",
    components: {Event, Key},
    // props: ["currentYear"],
    data() {
      return {
        events: [],
        // currentYear: store.getters.getSelectedYear,
        selectedEventObj: null,
        selectedEvent: false,
      }
    },
    computed: {
      storedSelectedEvent() {
        return store.state.event;
      },
      currentYear() {
        return store.getters.getSelectedYear;
      }
    },
    watch: {
      storedSelectedEvent(newEvent) {
        this.getDetails(newEvent)
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
        this.selectedEvent = Number(event);
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
