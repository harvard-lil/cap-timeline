<template>
  <div class="event-list-container">
    <key></key>
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
  </div>
</template>

<script>
  import Event from "./Event"
  import Key from "./Key"

  export default {
    name: "events",
    components: {Event, Key},
    data() {
      return {
        events: [],
        currentYear: Number(this.$route.query.year),
        zoomInEvent: false,
      }
    },
    watch: {
      '$route'(to) {
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
              })
            }).then(() => {
          if (this.$route.query.event) {
            for (let i = 0; i < this.events.length; i++) {
              if (this.events[i].id === this.$route.query.event) {
                this.zoomInEvent = this.events[i];
                break;
              }
            }
          }

        })

      },
      getYear(date) {
        return Number(date.split('-')[0])
      },
    },
    beforeMount() {
      this.getData();
    },
  }
</script>
