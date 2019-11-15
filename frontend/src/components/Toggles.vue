<template>
  <div class="sidebar-sticky toggles-menu">
    <!--year slider-->
    <h3>Years</h3>
    <vue-slider v-model="yearValue"
                :min="minSliderYear"
                :max="maxSliderYear"
                :silent="true"
                :enable-cross="false">
    </vue-slider>
    <ul class="year-values list-inline">
      <li class="list-inline-item">{{yearValue[0]}}</li>
      <li class="list-inline-item">{{yearValue[1]}}</li>
    </ul>
    <br/>
    <!--Groups-->
    <h3>Groups</h3>
    <ul class="group-types list-group">
      <li class="list-item" v-for="region in groupsByRegion" v-bind:key="region.slug">
        {{region.name}}
        <ul>
          <li v-for="group in region.groups" v-bind:key="group.slug">
            <selectable-group :slug="group.slug"
                              :status="groups[group.slug]"
                              :icon=symbolTranslation[group.slug]>
            </selectable-group>
          </li>
        </ul>
      </li>
    </ul>
    <hr/>
    <!--Event types-->
    <h3>Event Types</h3>
    <ul class="event-types list-group">
      <selectable-event v-for="(status, eventType) in eventTypes"
                        v-bind:key="eventType"
                        :name="eventType"
                        :status="status"
                        :fullname="eventTranslation[eventType]">
      </selectable-event>
    </ul>
    <hr/>
    <!--Themes ? -->

  </div>
</template>

<script>
  import './icons/diamond';
  import './icons/circle';
  import './icons/triangle';
  import './icons/polygon';
  import './icons/oval';
  import './icons/star5';
  import './icons/square';
  import './icons/heptagon';
  import VueSlider from 'vue-slider-component';
  import 'vue-slider-component/theme/antd.css';

  import SelectableGroup from './SelectableGroup';
  import SelectableEvent from './SelectableEvent';
  import store from '../store';

  export default {
    name: "toggles",
    components: {SelectableGroup, SelectableEvent, VueSlider},
    data() {
      return {
        showingEvent: false,
        minSliderYear: 0,
        maxSliderYear: 100,
        yearValue: [0, 100],
      }
    },
    computed: {
      eventTypes() {
        return store.getters.getEventTypes;
      },
      eventTranslation() {
        return store.getters.getEventTranslation;
      },
      groups() {
        return store.getters.getGroups;
      },
      groupsByRegion() {
        return store.getters.getGroupsByRegion;
      },
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      },
      minYear() {
        return store.getters.getMinYear;
      },
      maxYear() {
        return store.getters.getMaxYear;
      },
      absoluteMinYear() {
        return store.getters.getAbsoluteMinYear;
      },
      absoluteMaxYear() {
        return store.getters.getAbsoluteMaxYear;
      }
    },
    watch: {
      yearValue(newYearValue) {
        store.commit('setMinYear', Number(newYearValue[0]));
        store.commit('setMaxYear', Number(newYearValue[1]));

      }
    },
    mounted() {
      this.minSliderYear = this.absoluteMinYear;
      this.maxSliderYear = this.absoluteMaxYear;

      // check on params in route
      // if minyear and maxyear exist,
      // these overwrite the selected range
      let startingMinYear = this.$route.query.minyear ? Number(this.$route.query.minyear) : this.minSliderYear;
      let startingMaxYear = this.$route.query.maxyear ? Number(this.$route.query.maxyear) : this.maxSliderYear;

      this.yearValue = [startingMinYear, startingMaxYear];

    }
  }
</script>

<style>

  .vue-slider.vue-slider-ltr {
    padding: 0 0.5em !important;
  }

</style>