<template>
  <li v-show="!hide"
      class="event-container"
      :class="['event-type-'+data.type, {expanded: this.selectedEvent === data.id}]"
      @click="getDetails()">
    <div class="event-type" :class="'event-type-'+data.type">
      {{ eventTranslation[data.type] }}
    </div>
    <div class="event-title">
      <h3>{{ data.name }}</h3>

    </div>
    <div class="event-date">
        {{ data.start_date_parsed }}
         <span v-if="this.endYear">&ndash;{{ data.end_date_parsed}}</span>
    </div>
    <div class="event-description-short"
         v-html="data.description_short"></div>

    <div class="group-relationships">
      <ul class="group-list">
        <group v-for="slug in groups"
               :key="slug" :slug="slug">
        </group>
      </ul>
    </div>
  </li>
</template>

<script>
  import Group from "./Group"
  import {EventBus} from '../event-bus.js';

  export default {
    name: "event",
    components: {Group},
    props: ["data","selectedEvent", "minYear", "maxYear"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
        hideStatus: {
          byGroups: false,
          byYear: false,
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
        if (this.endYear) {
          this.hideStatus.byYear = this.startYear < this.minYear || this.startYear > this.maxYear || this.endYear > this.maxYear || this.endYear < this.minYear;
        } else {
          this.hideStatus.byYear = this.startYear < this.minYear || this.startYear > this.maxYear;
        }

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
        if (this.hideStatus.byYear) {
          this.hide = true;
          return
        }
        this.hide = false
      },
      getYears() {
        this.startYear = Number(this.data.start_date.split('-')[0]);
        if (this.data.end_date) {
          this.endYear = Number(this.data.end_date.split('-')[0])
        }
      },
      getDetails() {
        // this.$parent.selectedEvent = this.data.id;
        this.$store.commit('setSelectedEvent', this.data.id);
        this.$router.push({ name: 'eventview', params: { event_id: this.data.id } });
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
        return this.$store.getters.getEventTypes[this.data.type];
      },
      topLevelActiveGroups() {
        return this.$store.getters.getActiveGroups;
      }
    },
    watch: {
      selectedEvent() {
        this.updateHide();
      },
      minYear() {
        this.updateHide();
      },
      maxYear() {
        this.updateHide();
      },
      eventTypeStatus() {
        this.updateHide();
      },
      topLevelActiveGroups() {
        this.updateActiveGroups();
      },
      hide() {
        EventBus.$emit("updateHideStatus", {id: this.data.id, hide: this.hide})
      }
    },
    beforeMount() {
      this.getYears();
      this.groups = this.data.groups;
      this.updateActiveGroups();
      let date = new Date(this.data.start_date);
      return "" + date.getMonth()
    }
  }
</script>
