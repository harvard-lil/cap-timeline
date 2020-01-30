<template>
    <div class="detail-view">
        <h1>{{year}}</h1>
        <div class="event-details-container" tabindex="0" :class="['event-type-'+event.type, 'color-'+eventColors[event.type]]">
            <div class="col-1">
                <div class="event-type">{{event.type}}</div>
                <div class="event-info">
                    <h4 class="small-title">Date</h4>
                    {{event.start_date_parsed}}<span
                        v-if="event.end_date_parsed">&#8211;{{event.end_date_parsed}}</span>
                    <template v-if="event.citations">
                        <h4 class="small-title">Sources</h4>
                        <p v-for="citation in event.citations"
                           :key="citation.id">
                            {{ citation.type.charAt(0).toUpperCase()+ citation.type.slice(1) }}:
                            <a :href="citation.url" target="_blank">{{ citation.title }}</a>
                            <span v-if="citation.author_name">, {{ citation.author_name }}</span>
                        </p>
                    </template>

                    <!--Groups affected-->
                    <template v-if="event.groups && event.groups.length">
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
                    </template>

                    <!--Themes-->
                    <template v-if="event.themes && Object.keys(event.themes).length">
                        <h4 class="small-title">Themes</h4>
                        <div class="thematic-relationships">
                            <ul class="theme-list">
                                <li v-for="(themeName, themeSlug) in event.themes" v-bind:key="themeSlug">
                                    <svgicon icon="circle-3"
                                             :title="themeName"
                                             :class="themeSlug"
                                             width="18" height="18">
                                    </svgicon>
                                    {{themeName}}
                                </li>
                            </ul>
                        </div>
                    </template>
                    <!--Relationships list in event view card, preceding-->
                    <template v-if="relationships.preceding && relationships.preceding.length>0">
                        <h4 class="small-title">
                            Related, preceding
                        </h4>
                        <div v-for="preceding in relationships.preceding" v-bind:key="preceding.id">
                            <router-link class="related-event"
                                         :to="'/' + slug + '/events/' + preceding.id" replace>
                                {{preceding.name}}
                            </router-link>
                            ({{preceding.type}}, {{preceding.start_date.split('-')[0]}})
                        </div>
                    </template>
                    <!--Relationships, succeeding-->
                    <template v-if="relationships.succeeding && relationships.succeeding.length>0">
                        <h4 class="small-title">Related,
                            succeeding</h4>
                        <div v-for="succeeding in relationships.succeeding" v-bind:key="succeeding.id">
                            <router-link class="related-event" :to="'/' + slug + '/events/' + succeeding.id" replace>
                                {{succeeding.name}}
                            </router-link>
                            ({{succeeding.type}}, {{succeeding.start_date.split('-')[0]}})
                        </div>
                    </template>
                    <br/>
                </div>
            </div>
            <div class="col-2 event-main-content">
                <div class="event-content">
                    <h1>{{event.name}}</h1>
                    <h5 v-if="event.type === 'caselaw'">{{event.caselaw_citation}}</h5>
                    <div class="event-description-long" v-if="event.description_long">
                        <h4 class="small-title">Description</h4>
                        <div v-html="event.description_long"></div>
                    </div>
                </div>
            </div>
        </div>
        <!--    Related events:    -->
        <!--    Preceding    -->
        <template v-if="relationships.preceding && relationships.preceding.length>0">
            <h2>Preceding</h2>
            <ul class="event-list event-list-detail-view">
                <event v-for="(related_event, idx) in relationships.preceding"
                       v-bind:key="related_event.id"
                       :tabindex="idx"
                       :data="related_event">
                </event>
            </ul>
        </template>
        <!--    Succeeding    -->
        <template v-if="relationships.succeeding && relationships.succeeding.length>0">
            <h2>Succeeding</h2>
            <ul class="event-list event-list-detail-view">
                <event v-for="(related_event, idx) in relationships.succeeding"
                       :tabindex="idx"
                       :key="related_event.id"
                       :data="related_event">
                </event>
            </ul>
        </template>
    </div>
</template>

<script>
  import axios from 'axios';
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
    computed: {
      slug() {
        return store.getters.getSlug;
      },
      eventColors() {
        return store.getters.getEventColors;
      }
    },
    watch: {
      $route(to, from) {
        if (to.name === from.name) {
          this.getData();
        }
      }
    },
    methods: {
      getData() {
        store.commit('setSelectedEvent', this.$route.params.event_id);
        let url = process.env.VUE_APP_BACKEND_DATA_URL + this.slug + '/events/' + store.getters.getSelectedEvent;
        axios.get(url)
            .then((response) => {
              this.event = response.data['event'];
              this.relationships = response.data.related_events;
              this.year = Number(this.event.start_date.substring(0, 4));
            })
      },
    },
    beforeMount() {
      this.getData();
    },
  }
</script>