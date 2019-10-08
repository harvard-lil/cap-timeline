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
        hidingByGroups: false,
        hidingByYear: false,
        hidingBySelectedEvent: false,
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
      getYears() {
        this.startYear = Number(this.data.start_date.split('-')[0]);
        if (this.data.end_date) {
          this.endYear = Number(this.data.end_date.split('-')[0])
        }
      },
      hideByYear() {
        // hides event if year selected is not event's year
        if (this.hidingByGroups)
          return;
        if (this.hidingBySelectedEvent)
          return;
        if (!this.currentYear) {
          this.hide = false;
          return
        }

        if (this.endYear) {
          this.hide = !(this.currentYear >= this.startYear && this.currentYear <= this.endYear);
          return
        }

        this.hide = this.currentYear === 'all' || this.startYear !== this.currentYear;
      },
      updateIfSelectedEvent() {
        if (!this.selectedEvent) {
          this.hidingBySelectedEvent = false;
          return;
        }
        this.hidingBySelectedEvent = true;

        if (this.selectedEvent !== this.data.id) {
          this.hide = true;
          return
        }
        this.hide = false;
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
      hideByGroups() {
        if (this.activeGroups.size === 0) {
          this.hide = true;
          this.hidingByGroups = this.hide;
        } else {
          this.hidingByGroups = false;
          if (!this.hidingBySelectedEvent)
            this.hide = false;
        }

      },
      updateActiveGroups() {
        let topLevelGroups = store.getters.getGroups;
        for (let i = 0; i < this.groups.length; i++) {
          let group = this.groups[i];
          topLevelGroups[group] ?
              this.activeGroups.add(group) : this.activeGroups.delete(group);
        }
        this.hideByGroups();
      },

    },
    watch: {
      currentYear() {
        this.hideByYear();
      },
      selectedEvent() {
        this.hide = this.selectedEvent && this.selectedEvent !== this.data.id;
        this.updateIfSelectedEvent()
      },
    },
    beforeMount() {
      this.getYears();
      this.groups = this.data.groups;
      this.updateActiveGroups();
      this.hideByYear();

      let date = new Date(this.data.start_date);
      return "" + date.getMonth()

    }
  }
</script>
