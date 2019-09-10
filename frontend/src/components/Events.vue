<template>
  <ul class="event-list">
    <li class="event"
        v-for="eventObj in events"
        @click="getDetails(eventObj)"
        :key="eventObj.id">
      <event :currentYear="currentYear"
             :zoomInEvent="zoomInEvent"
             :data="eventObj">
      </event>
    </li>
  </ul>
</template>

<script>
  import Event from "./Event"

  export default {
    name: "events",
    components: {Event,},
    data() {
      return {
        events: [],
        currentYear: Number(this.$route.query.year),
        zoomInEvent: false,
      }
    },
    watch: {
      '$route'(to, from) {
        this.currentYear = Number(to.query.year);
        if (!to.query.event) {
          this.zoomInEvent = false;
        }
      },
    },
    methods: {
      getDetails(event) {
        this.zoomInEvent = event;
        this.$router.push({name: 'events', query: {event: event.id}});
      },
      getData() {
        let url = 'http://localhost:8000/events';
        this.$http.get(url)
            .then((response) => {
              this.events = response.body.sort((a, b) => {
                return this.getYear(a.start_date) - this.getYear(b.start_date)
              });
            })

      },
      getYear(date) {
        return Number(date.split('-')[0])

      },
    },
    created() {
      this.getData();
    }
  }
</script>
