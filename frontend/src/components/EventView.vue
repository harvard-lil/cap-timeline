<template>
  <div class="detail-view">
    <h2>{{year}}</h2>
    <div class="event-details-container" :class="'event-type-'+event.type">
      <div class="col-1">
        <h4 class="small-title">Date</h4>
        {{event.start_date_parsed}}
        <h4 v-if="event.citations && event.citations.length" class="small-title">Sources</h4>
        <template v-if="event.citations">
          <a v-for="citation in event.citations"
             :href="citation.url"
             target="_blank"
             :key="citation.id">
            {{citation.title}}
          </a>
        </template>
        <h4 class="small-title">Groups affected</h4>
        <div class="group-relationships">
          <ul class="group-list">
            <group v-for="slug in event.groups"
                   :key="slug"
                   :showName="true"
                   :slug="slug">
            </group>
          </ul>
        </div>
        <h4 class="small-title" v-if="relationships.preceding && relationships.preceding.length>0">Related,
          preceding</h4>
        <div v-for="preceding in relationships.preceding">
          <a class="related-event" @click="goToRelatedEvent(preceding.id)">
            {{preceding.name}}
          </a>
          ({{preceding.type}}, {{preceding.start_date.split('-')[0]}})
        </div>
        <h4 class="small-title" v-if="relationships.succeeding && relationships.succeeding.length>0">Related,
          succeeding</h4>
        <div v-for="succeeding in relationships.succeeding">
          <a class="related-event" @click="goToRelatedEvent(succeeding.id)">
            {{succeeding.name}}
          </a>
          ({{succeeding.type}}, {{succeeding.start_date.split('-')[0]}})
        </div>
      </div>
      <div class="col-2">
        <div class="event-type">{{event.type}}</div>
        <h1>{{event.name}}</h1>
        <div class="event-description-long">
          <h4 class="small-title">Description</h4>

          <span v-html="event.description_long"></span>
        </div>
      </div>
    </div>
    <h2 v-if="relationships.preceding && relationships.preceding.length>0">Preceding</h2>
    <ul class="event-list event-list-detail-view">
      <event v-for="related_event in relationships.preceding"
             :key="related_event.id"
             :data="related_event">
      </event>
    </ul>
    <h2 v-if="relationships.succeeding && relationships.succeeding.length>0">Succeeding</h2>
    <ul class="event-list event-list-detail-view">
      <event v-for="related_event in relationships.succeeding"
             :key="related_event.id"
             :data="related_event">
      </event>
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
              this.relationships = response.body.related_events;
              this.year = Number(this.event.start_date.substring(0, 4));
            })
      },
      goToRelatedEvent(id) {
        this.$router.push({ name: 'eventview', params: { event_id: id }});
        this.$router.go();
      }
    },
    beforeMount() {
      this.getData();
    }
  }
</script>
