<template>
  <div class="detail-view">
    <h2>{{year}}</h2>
    <div class="event-details-container" :class="'event-type-'+event.type">
      <div class="col-1">
        <h4 class="small-title">Date</h4>
        {{event.start_date}}

        <h4 v-if="event.citation" class="small-title">Source</h4>
        <template  v-if="event.citation">
          <a v-for="citation in event.citation"
             :href="citation.url"
             target="_blank"
             :key="citation.id">
              {{citation.title}}
          </a>
        </template>
        <h4 class="small-title">Groups affected</h4>
        <div class="group-relationships">
          <ul class="group-list">
            <group v-for="name in event.groups"
                   :key="name"
                   :showName="true"
                   :name="name">
            </group>
          </ul>
        </div>
      </div>
      <div class="col-2">
        <div class="event-type">{{event.type}}</div>
        <h1>{{event.name}}</h1>
        <div class="event-description-long">
          <h4 class="small-title">Description</h4>
          {{event.description_long}}
        </div>
      </div>
    </div>
    <ul class="event-list">
      <template v-for="related_event in relationships">
        <event class="event-container"
               :key="related_event.id"
               :data="related_event">

        </event>
      </template>
    </ul>
  </div>
</template>

<script>
  import store from '../store'
  import Group from "./Group"
  import Event from "./Event"

  export default {
    name: "event-view",
    components: {Group, Event},
    data() {
      return {
        event: {},
        year: null,
        relationships: []
      }
    },
    methods: {
      getData() {
        if (!store.getters.getSelectedEvent) {
          store.commit('setSelectedEvent', this.$route.params.event_id);
        }
        let url = 'http://localhost:8000/events/' + store.getters.getSelectedEvent;
        this.$http.get(url)
            .then((response) => {

              this.event = response.body['event'];
              this.relationships = response.body['related_events'];
              this.year = Number(this.event.start_date.substring(0, 4));
            })
      },
    },
    beforeMount() {
      this.getData();
    }
  }
</script>
