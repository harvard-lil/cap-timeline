<template>
  <div v-show="!hide" v-bind:key="event.id"
       @click="getDetails()"
       class="event-container"
       :title="event.name + ': ' + event.start_date_parsed + '(' + event.type + ')'">
    <div class="event-type" :class="'event-type-'+event.type">{{event.type}}</div>
    <div class="event-contents">
      <div class="event-name">{{event.name}}</div>
      <div class="event-description-short"
           v-if="event.description_short && event.description_short.length < 80"
           v-html="event.description_short"></div>

      <div class="event-description-short"
           v-else-if="event.description_short" v-html="event.description_short.substr(0,80) + '...'"></div>
    </div>
    <div class="group-relationships">
      <ul class="group-list">
        <group v-for="slug in event.groups"
               :key="slug" :slug="slug">
        </group>
      </ul>
    </div>
  </div>
</template>

<script>
  import Group from "./Group";
  import {EventBus} from '../event-bus.js';

  export default {
    name: "TimelineEvent",
    components: {Group},
    props: ["event"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
        hideStatus: {
          byGroups: false,
          bySelectedEvent: false,
          byEventType: false,
        },
        groups: [],
        activeGroups: new Set(),
        eventTranslation: {
          legislation: 'legislation',
          caselaw: 'caselaw',
          us: 'U.S. event',
          world: 'world event',
        }
      }
    },
    methods: {
      updateHide() {
        // Complicated logic about when to hide event
        // Hiding depends on year, event types, and groups
        this.hideStatus.byEventType = this.eventTypeStatus;
        if (!this.hideStatus.byEventType) {
          this.hide = true;
          return;
        }

        this.hideStatus.byGroups = this.activeGroups.size === 0 && this.groups.length > 0;
        if (this.hideStatus.byGroups) {
          this.hide = true;
          return;
        }
        this.hide = false
      },
      getYears() {
        this.startYear = Number(this.event.start_date.split('-')[0]);
        if (this.event.end_date) {
          this.endYear = Number(this.event.end_date.split('-')[0])
        }
      },
      getDetails() {
        // this.$parent.selectedEvent = this.event.id;
        this.$store.commit('setSelectedEvent', this.event.id);
        this.$router.push({name: 'eventview', params: {event_id: this.event.id}});
        this.$router.go();
      },
      updateActiveGroups() {
        for (let i = 0; i < this.groups.length; i++) {
          let group = this.groups[i];
          this.topLevelActiveGroups.indexOf(group) > -1 ? this.activeGroups.add(group) : this.activeGroups.delete(group);
        }
        this.updateHide();
      },

    },
    computed: {
      eventTypeStatus() {
        return this.$store.getters.getEventTypes[this.event.type];
      },
      topLevelActiveGroups() {
        return this.$store.getters.getActiveGroups;
      }
    },
    watch: {
      selectedEvent() {
        this.updateHide();
      },
      eventTypeStatus() {
        this.updateHide();
      },
      topLevelActiveGroups() {
        this.updateActiveGroups();
      },
      hide() {
        EventBus.$emit("updateHideStatus", {id: this.event.id, hide: this.hide})
      }
    },
    beforeMount() {
      this.groups = this.event.groups;
      this.updateActiveGroups();
    }
  }
</script>
