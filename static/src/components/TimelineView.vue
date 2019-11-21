<template>
  <div class="timeline">
    <div class="container-wrapper">
      <template v-for="idx in maxYear-minYear">
        <div class="year-label"
             v-bind:key="idx+minYear"
             :class="'col-'+getIdx(idx)"> {{idx+minYear}}
        </div>
        <template v-for="event in events[idx+minYear]">
          <div v-bind:key="event.id"
               class="event-container"
               :class="['event-type-'+event.type, 'span' + getLength(event), 'col-'+getIdx(idx)]"
               :title="event.name + ': ' + event.start_date_parsed + '(' + event.type + ')'">
            <div class="event-type" :class="'event-type-'+event.type">{{event.type}}</div>
            <div class="event-contents">
              <div class="event-name">{{event.name}}</div>
              <div class="event-description-short"
                   v-if="event.description_short"
                   v-html="event.description_short"></div>
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
      </template>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue';
  import store from '../store';
  import Group from "./Group"

  export default {
    name: "TimelineView",
    components: {Group},
    data() {
      return {
        years: [],
        events: {}
      }
    },
    methods: {
      getGroups() {
        let url = 'http://localhost:8000/data/groups';
        this.$http.get(url)
            .then((response) => {
              this.groups = response.body;
            })
      },
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
    },
    computed: {
      minYear() {
        return store.getters.getMinYear;
      },
      maxYear() {
        return store.getters.getMaxYear;
      }
    },

    created() {
      this.getData();
      this.getGroups();
    },

  }
</script>

<style scoped>

</style>