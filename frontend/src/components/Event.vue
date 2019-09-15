<template>
  <div v-if="!hide"
       class="event-container"
       :class="'event-type-' + data.type">
    <div class="row">
      <div class="col-12">
        <h3>{{ data.name }}</h3>

      </div>
      <div class="col-12">
        <p class="text-semibold">
          <span>{{ data.start_date_parsed }}</span>
          <span v-if="this.endYear">&ndash;{{ data.end_date_parsed}}</span></p>
        <p>{{ data.description_short }}</p>

      </div>
      <div class="col-6">
        <p>
          <svgicon :icon="symbolTranslation[data.type]"
                   :class="'event-symbol event-type-' + data.type + ' symbol-' + symbolTranslation[data.type]"
                   width="18" height="18"></svgicon>
          {{ eventTranslation[data.type] }}
        </p>

      </div>
      <div class="col-6" v-if="data.relationships.length > 0">
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
      <div class>{{data.groups}}</div>

    </div>
  </div>
</template>

<script>
  import './icons/diamond';
  import './icons/circle';
  import './icons/triangle';
  import './icons/polygon';

  export default {
    name: "event",
    props: ["data", "currentYear", "zoomInEvent"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
        groups: [],
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
        if (!this.zoomInEvent) {
          this.hide = false;
          this.hideByYear();
          return
        }
        if (this.zoomInEvent.id === this.data.id) {
          this.hide = false;
          return
        }
        let relationships = this.zoomInEvent.relationships;
        for (let i = 0; i < relationships.length; i++) {
          if (relationships[i][0] === this.data.id) {
            this.hide = false;
            return
          }
        }
        this.hide = true;
      },
      hideByGroups(to) {
        if (!this.groups.length) {
          return;
        }
        for (let i = 0; i < this.groups.length + 1; i++) {
          if (this.groups[i] in to.query) {
            this.hide = true;
            break;
          } else {
            this.hideByYear()
          }
        }

      }

    },
    watch: {
      currentYear() {
        this.hideByYear();
      },
      zoomInEvent() {
        this.updateIfZoomedIn();
      },
      '$route'(to) {
        this.hideByGroups(to);
      }
    },
    beforeMount() {
      this.getYears();
      this.hideByYear();
      this.updateIfZoomedIn();
      this.groups = this.data.groups;
      let date = new Date(this.data.start_date);
      return "" + date.getMonth()
    }
  }
</script>
