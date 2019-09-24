<template>
  <div v-if="!hide"
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
        {{groupStatus}}
        <li v-for="(val, group) in groupStatus" :key="group">
          <span v-show="val === true">{{group}}</span>
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
  import Vue from 'vue'

  export default {
    name: "event",
    props: ["data", "currentYear", "zoomedIn"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
        hidingByGroups: false,
        hidingByYear: false,
        hidingByZoom: false,
        groups: [],
        groupStatus: {},
        zoomInEvent: false,
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
        if (this.hidingByZoom)
          return;
        if (!this.currentYear) {
          this.hide = false;
          return
        }
        this.zoomInEvent = false;
        if (this.endYear) {
          this.hide = !(this.currentYear >= this.startYear && this.currentYear <= this.endYear);
          return
        }
        this.hide = this.startYear !== this.currentYear;
      },
      updateIfZoomedIn() {

        if (!this.$route.query.event) {
          this.hidingByZoom = false;
          return;
        }
        this.hidingByZoom = true;
        this.zoomInEvent = this.$parent.zoomedInEventObj;
        if (!this.zoomInEvent) {
          return;
        }
        if (this.zoomInEvent.id !== this.data.id) {
          this.hide = true;
          return
        }
        this.hide = false;
        // TODO: add relationships
        // for (let e = 0; e < this.$parent.events.length; e++) {
        //   if (this.$parent.events[e].id === this.zoomInEvent) {
        //     zoomedInEventObj = this.$parent.events[e];
        //     break;
        //   }
        // }
        // if (!zoomedInEventObj) {
        //   return;
        // }
        // let relationships = zoomedInEventObj.relationships;
        // for (let i = 0; i < relationships.length; i++) {
        //   if (relationships[i][0] === this.data.id) {
        //     this.hide = false;
        //     this.hidingByZoom = this.hide;
        //     return
        //   }
        // }
        // this.hide = true;
      },
      hideByGroups(to) {
        if (this.hidingByZoom) {
          return
        }
        if (!this.groups.length) {
          return;
        }
        if (!to.query.groups)
          return;

        let showEvent = false;
        for (let group in this.groupStatus) {
          if (this.groupStatus[group])
            showEvent = true;
        }
        this.hide = !showEvent;
        this.hidingByGroups = this.hide;

      },
      updateGroupStatus() {
        if (!this.$route.query.groups) {
          for (let i = 0; i < this.groups.length; i++) {
            this.groupStatus[this.groups[i]] = false;
            // Vue.set(this.groupStatus, this.groups[i], false);
          }
          return;
        }
        let queryGroups = this.$route.query.groups.split(',');
        for (let x = 0; x < this.groups.length; x++) {
          // make obj key reactive
          // this.groupStatus[this.groups[x]] = queryGroups.indexOf(this.groups[x]) > -1;
          Vue.set(this.groupStatus, this.groups[x], queryGroups.indexOf(this.groups[x]) > -1);
        }
      }

    },
    watch: {
      currentYear() {
        this.hideByYear();
      },
      zoomedIn() {
        if (this.zoomedIn) {
          this.updateIfZoomedIn()
        }
      },
      '$route'(to) {
        this.updateIfZoomedIn();
        this.updateGroupStatus();
        this.hideByGroups(to);
        this.hideByYear();
      }
    },
    beforeMount() {
      this.getYears();
      this.groups = this.data.groups;
      this.updateGroupStatus();
      this.hideByYear();

      let date = new Date(this.data.start_date);
      return "" + date.getMonth()
    },
  }
</script>
