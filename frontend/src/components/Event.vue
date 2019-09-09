<template>
  <div v-show=!hide class="event-container" :class="'event-type-' + data.type">
    <div class="row">
      <div class="col-12">
        <h3>{{ data.name }}</h3>

      </div>
      <div class="col-12">
        <p class="text-semibold">
          <span>{{ data.start_date_parsed }}</span><span v-if="this.endYear">&ndash;{{ data.end_date_parsed}}</span></p>
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
    props: ["data", "currentYear"],
    data() {
      return {
        startYear: null,
        endYear: null,
        hide: false,
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
      hideOrShow() {
        if (!this.currentYear) {
          this.hide = false;
          return
        }
        if (this.endYear) {
          this.hide = !(this.currentYear >= this.startYear && this.currentYear <= this.endYear);
          return
        }
        this.hide = this.startYear !== this.currentYear;
      }
    },
    watch: {
      currentYear() {
        this.hideOrShow();
      }
    },
    beforeMount() {
      this.getYears();
      this.hideOrShow();
      let date = new Date(this.data.start_date);
      return "" + date.getMonth()
    }
  }
</script>
