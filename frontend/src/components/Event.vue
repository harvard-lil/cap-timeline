<template>
  <div v-show="!hide"
       class="event-container"
       :class="'event-type-' + data.type">
    <div class="event-title">
      <h3>{{ data.name }}</h3>

    </div>
    <div class="event-date">
      <p class="text-semibold">
        <span>{{ data.start_date_parsed }}</span>
        <span v-if="this.endYear">&ndash;{{ data.end_date_parsed}}</span></p>
      <p>{{ data.description_short }}</p>

    </div>
    <div class="event-type">

      <svgicon :icon="symbolTranslation[data.type]"
               :class="'event-symbol event-type-' + data.type + ' symbol-' + symbolTranslation[data.type]"
               width="18" height="18"></svgicon>
      {{ eventTranslation[data.type] }}

    </div>
    <div class="event-relationships" v-if="data.relationships.length > 0">
      <ul>
        <li v-for="relationship in data.relationships">
          <a href="">
            <!--TODO: link to specific event!-->
            <svgicon :icon="symbolTranslation[relationship[1]]"
                     :class="'event-symbol event-type-' + relationship[1] + ' symbol-' + symbolTranslation[relationship[1]]"
                     width="18" height="18">
            </svgicon>
          </a>
        </li>
      </ul>
    </div>
    <div class="group-relationships">
      <ul class="group-list">
        <li v-for="name in groups" :key="name">
          <group :name="name"></group>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
  import './icons/diamond';
  import './icons/circle';
  import './icons/triangle';
  import './icons/polygon';
  import Group from "./Group"
  import store from '../store'

  export default {
    name: "event",
    components: {Group},
    props: ["data", "currentYear", "selectedEvent"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
        hideStatus: {
          byGroups: false,
          byYear: false,
          bySelectedEvent: false,
        },
        groups: [],
        activeGroups: new Set(),
        symbolTranslation: {
          legislation: 'diamond',
          caselaw: 'triangle',
          world: 'circle',
          us: 'polygon'
        },
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
        // Hiding depends on year, groups, and event selected
        this.hideStatus.bySelectedEvent = !!(this.selectedEvent) && this.selectedEvent !== this.data.id;
        if (this.endYear) {
          this.hideStatus.byYear = this.currentYear && !(this.currentYear >= this.startYear && this.currentYear <= this.endYear);
        } else {
          this.hideStatus.byYear = this.currentYear && this.currentYear !== this.startYear;
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
        if (this.hideStatus.bySelectedEvent) {
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

      updateIfSelectedEvent() {
        // TODO: add relationships
        // for (let e = 0; e < this.$parent.events.length; e++) {
        //   if (this.$parent.events[e].id === this.zoomInEvent) {
        //     selectedEventEventObj = this.$parent.events[e];
        //     break;
        //   }
        // }
        // if (!selectedEventEventObj) {
        //   return;
        // }
        // let relationships = selectedEventEventObj.relationships;
        // for (let i = 0; i < relationships.length; i++) {
        //   if (relationships[i][0] === this.data.id) {
        //     this.hide = false;
        //     this.hidingBySelectedEvent = this.hide;
        //     return
        //   }
        // }
        // this.hide = true;
      },

      updateActiveGroups() {
        let topLevelGroups = store.getters.getGroups;
        for (let i = 0; i < this.groups.length; i++) {
          let group = this.groups[i];
          topLevelGroups[group] ?
              this.activeGroups.add(group) : this.activeGroups.delete(group);
        }
        this.updateHide();
      },

    },
    watch: {
      currentYear() {
        this.updateHide();
      },
      selectedEvent() {
        this.updateHide();
      },
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
