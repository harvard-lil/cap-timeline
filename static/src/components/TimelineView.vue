<template>
  <div class="timeline">
    <div class="container-wrapper">
      <template v-for="(year, idx) in years">
        <div v-if="year === '-'"
             class="year-label squiggle "
             :class="'col-'+getIdx(idx)">
          <svgicon icon="squiggle"
                   title="Skipping years"
                   class=""
                   width="165" height="24">
          </svgicon>

        </div>
        <div v-else
             class="year-label"
             v-bind:key="year"
             :class="'col-'+getIdx(idx)"> {{year}}
        </div>
        <template v-for="event in events[year]">
          <timeline-event v-bind:key="event.id" :event="event"
                          :class="['event-type-'+event.type, 'span' + getLength(event), 'col-'+getIdx(idx)]">
          </timeline-event>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
  import './icons/squiggle';

  import Vue from 'vue';
  import store from '../store';
  import TimelineEvent from "./TimelineEvent"

  export default {
    name: "TimelineView",
    components: {TimelineEvent},
    data() {
      return {
        years: [],
        activeYears: [],
        events: {},
      }
    },
    methods: {
      getData() {
        let url = 'http://localhost:8000/data/events';
        this.$http.get(url)
            .then((response) => {
              for (let i = 0; i < response.body.length; i++) {
                let year = this.getYear(response.body[i].start_date);
                if (year in this.events) {
                  this.events[year].push(response.body[i]);
                  Vue.set(this.events, year, this.events[year])
                } else {
                  Vue.set(this.events, year, [response.body[i]])
                }
              }
              this.getYears();
            })
      },
      getActiveYears() {
        let url = 'http://localhost:8000/data/years';
        this.$http.get(url)
            .then((response) => {
              for (let i = 0; i < response.body.length; i++) {
                this.activeYears.push(response.body[i]);
                if (response.body[i + 1] !== response.body[i] + 1) {
                  this.activeYears.push('-')
                }
              }
              this.getYears();
            })

      },
      getLength(event) {
        if (!(event.end_date)) {
          return 1;
        }
        let startYear = this.getYear(event.start_date);
        let endYear = this.getYear(event.end_date);
        return endYear - startYear;
      },
      getYear(date) {
        return Number(date.split('-')[0])
      },
      getIdx(idx) {
        return idx + 1;
      },
      getYears() {
        let year = this.minYear;
        this.years = [];
        if (this.zoomLevel === 1) {
          for (let i = 0; i < this.activeYears.length; i++) {
            if (this.activeYears[i] === '-') {
              if (this.years[this.years.length-1] !== '-') {
                // avoid too many squiggly lines
                this.years.push('-');
              }
            } else {
              if (this.activeYears[i] >= this.minYear && this.activeYears[i] <= this.maxYear) {
                this.years.push(this.activeYears[i])
              }
            }
          }
        } else if (this.zoomLevel === 0) {
          while (year < this.maxYear + 1) {
            this.years.push(year);
            year += 1;
          }
        }

      },
    },
    computed: {
      minYear() {
        return store.getters.getMinYear;
      },
      maxYear() {
        return store.getters.getMaxYear;
      },
      zoomLevel() {
        return store.getters.getZoomLevel;
      }

    },
    watch: {
      minYear() {
        this.getYears();
      },
      maxYear() {
        this.getYears();
      },
      zoomLevel() {
        this.getYears();
      }
    },

    created() {
      this.getData();
      this.getActiveYears();
    },
  }
</script>