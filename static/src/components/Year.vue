<template>
  <div v-show="oneOrMoreShown()">
    <h1 class="event-year event-year-section">
      {{value}}
    </h1>
    <ul class="event-list">
      <event v-for="eventObj in events"
             :class="'event-list-item event-type-' + eventObj.type"
             :key="eventObj.id"
             :minYear="minYear"
             :maxYear="maxYear"
             :selectedEvent="selectedEvent"
             :data="eventObj">
      </event>
    </ul>
  </div>

</template>

<script>
  import Vue from 'vue';
  import {EventBus} from '../event-bus.js';
  import Event from "./Event"

  export default {
    name: "year",
    props: ["value", "events", "selectedEvent", "minYear", "maxYear"],
    components: {Event},
    data() {
      return {
        eventsStatus: {},
      }
    },
    methods: {
      oneOrMoreShown() {
        for (let event in this.eventsStatus) {
          if (this.eventsStatus[event]) {
            return true;
          }
        }
        return false;
      },
    },
    beforeMount() {
      for (let i = 0; i < this.events.length; i++) {
        Vue.set(this.eventsStatus, this.events[i].id, true)
      }
      EventBus.$on("updateHideStatus", (data) => {
        if (data.id in this.eventsStatus) {
          this.eventsStatus[data.id] = !(data.hide);
          this.oneOrMoreShown();
        }
      })
    }
  }
</script>

