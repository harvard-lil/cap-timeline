<template>
  <div class="detail-view">
    <h1>{{year}}</h1>
    <div class="event-details-container" tabindex="0" :class="'event-type-'+event.type">
      <div class="col-1">
        <div class="event-type">{{event.type}}</div>
        <div class="event-content">
          <h4 class="small-title">Date</h4>
          {{event.start_date_parsed}}<span v-if="event.end_date_parsed">&#8211;{{event.end_date_parsed}}</span>
          <h4 v-if="event.citations && event.citations.length" class="small-title">Sources</h4>
          <template v-if="event.citations">
            <p v-for="citation in event.citations"
               :key="citation.id">
              {{citation.type.charAt(0).toUpperCase()+ citation.type.slice(1)}}: <a :href="citation.url"
                                                                                    target="_blank">{{citation.title}}</a>
            </p>
          </template>

          <!--Groups affected-->
          <h4 class="small-title" v-if="event.groups && 
          event.groups.length">Groups affected</h4>
          <div class="group-relationships" v-if="event.groups && event.groups.length">
            <ul class="group-list">
              <group v-for="slug in event.groups"
                     :key="slug"
                     :showName="true"
                     :slug="slug">
              </group>
            </ul>
          </div>

          <!--Themes-->
          <h4 class="small-title" v-if="event.themes">Themes</h4>
          <div class="thematic-relationships" v-if="event.themes">
            <ul class="theme-list">
              <li v-for="(themeName, themeSlug) in event.themes">
                <svgicon icon="circle-3"
                         :title="themeName"
                         :class="themeSlug"
                         width="18" height="18">
                </svgicon>
                {{themeName}}
              </li>
            </ul>
          </div>

          <!--Relationships, preceding-->
          <h4 class="small-title" v-if="relationships.preceding && relationships.preceding.length>0">Related,
            preceding</h4>
          <div v-for="preceding in relationships.preceding" v-bind:key="preceding.id">
            <a class="related-event"
               @click="goToRelatedEvent(preceding.id)">
              {{preceding.name}}
            </a>
            ({{preceding.type}}, {{preceding.start_date.split('-')[0]}})
          </div>

          <!--Relationships, succeeding-->
          <h4 class="small-title"
              v-if="relationships.succeeding && relationships.succeeding.length>0">Related,
            succeeding</h4>
          <div v-for="succeeding in relationships.succeeding" v-bind:key="succeeding.id">
            <a class="related-event" @click="goToRelatedEvent(succeeding.id)">
              {{succeeding.name}}
            </a>
            ({{succeeding.type}}, {{succeeding.start_date.split('-')[0]}})
          </div>
        </div>
      </div>
      <div class="col-2">
        <h1>{{event.name}}</h1>
        <h5 v-if="event.type === 'caselaw'">{{event.caselaw_citation}}</h5>
        <div class="event-description-long" v-if="event.description_long">
          <h4 class="small-title">Description</h4>
          <span v-html="event.description_long"></span>
        </div>
      </div>
    </div>
    <h2 v-if="relationships.preceding && relationships.preceding.length>0">Preceding</h2>
    <ul class="event-list event-list-detail-view">
      <event v-for="(related_event, idx) in relationships.preceding"
             :tabindex="idx"
             v-on:keyup.enter="goToRelatedEvent(related_event.id)"
             :key="related_event.id"
             :data="related_event">
      </event>

    </ul>
    <h2 v-if="relationships.succeeding && relationships.succeeding.length>0">Succeeding</h2>
    <ul class="event-list event-list-detail-view">
      <event v-for="(related_event, idx) in relationships.succeeding"
             :tabindex="idx"
             v-on:keyup.enter="goToRelatedEvent(related_event.id)"
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
        let url = 'http://localhost:8000/data/events/' + store.getters.getSelectedEvent;
        this.$http.get(url)
            .then((response) => {
              this.event = response.body['event'];
              this.relationships = response.body.related_events;
              this.year = Number(this.event.start_date.substring(0, 4));
            })
      },
      goToRelatedEvent(id) {
        this.$router.push({params: {event_id: id}});
        this.$router.go();
      }
    },
    beforeMount() {
      this.getData();
    }
  }
</script>
