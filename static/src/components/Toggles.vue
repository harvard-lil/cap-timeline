<template>
  <div class="sidebar-sticky toggles-menu">
    <div class="toggle-group">
      <h3>Zoom level</h3>
      <ul class="list-inline">
        <li class="list-inline-item">
          <svgicon icon="plus"
                   title="zoom in"
                   class="zoom-level-btn plus icon"
                   :class="zoom === 1 ? 'active' : ''"
                   @click="switchZoomLevel('plus')"
                   width="24" height="24">
          </svgicon>
        </li>
        <li>
          <svgicon icon="minus"
                   title="zoom out"
                   class="zoom-level-btn minus icon"
                   :class="zoom === 0 ? 'active' : ''"
                   @click="switchZoomLevel('minus')"
                   width="24" height="24">
          </svgicon>

        </li>
      </ul>
    </div>

    <!--year slider-->
    <div class="toggle-group">
      <h3>Years</h3>
      <vue-slider v-model="yearValue"
                  :min="minSliderYear"
                  :max="maxSliderYear"
                  :silent="true"
                  :height="'14px'"
                  :enable-cross="false">
      </vue-slider>
      <ul class="year-values list-inline">
        <li class="list-inline-item">
          <input type="number" :min="minSliderYear" :max="yearValue[1]" v-model="yearValue[0]">
        </li>
        <li class="list-inline-item">
          <input type="number" :max="maxSliderYear" :min="yearValue[0]" v-model="yearValue[1]">
        </li>
      </ul>
    </div>
    <br/>
    <!--Groups-->
    <div class="toggle-group">
      <h3>Groups</h3>
      <ul class="group-types list-group">
        <li class="list-item" v-for="region in groupsByRegion" v-bind:key="region.slug">
          {{region.name}}
          <ul>
            <li v-for="group in region.groups" v-bind:key="group.slug">
              <selectable-group :slug="group.slug"
                                :status="groups[group.slug]"
                                :fullName="group.name + ' migrants'"
                                :icon=symbolTranslation[group.slug]>
              </selectable-group>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <br/>
    <!--Event types-->
    <div class="toggle-group">
      <h3>Event Types</h3>
      <ul class="event-types list-group">
        <selectable-event v-for="(status, eventType) in eventTypes"
                          v-bind:key="eventType"
                          :name="eventType"
                          :status="status"
                          :fullname="eventTranslation[eventType]">
        </selectable-event>
      </ul>
    </div>
    <br/>
    <!--Themes ? -->
    <div class="toggle-group">
      <h3>Themes</h3>
      <ul class="theme-types">
        <li class="list-item" v-for="(themeName, themeSlug) in themes">
          <span class="theme-icon icon" :class="themeSlug">
            <svgicon icon="circle-3"
                     :title="themeName"
                     :class="themeSlug"
                     width="15" height="15">
            </svgicon>
          </span>
          <label class="label">{{themeName}}</label>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
  import './icons/circle';
  import './icons/circle-1';
  import './icons/circle-2';
  import './icons/circle-3';
  import './icons/diamond-1';
  import './icons/diamond-2';
  import './icons/polygon-1';
  import './icons/polygon-2';
  import './icons/square-2';

  import './icons/plus';
  import './icons/minus';

  import VueSlider from 'vue-slider-component';
  import 'vue-slider-component/theme/default.css';

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
        zoom: 1,
      }
    },
    methods: {
      switchZoomLevel(btn) {
        this.zoom = btn === 'plus' ? 1 : 0;
        store.commit('setZoomLevel', this.zoom);
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
      },
      zoomLevel() {
        return store.getters.getZoomLevel;
      },
      themes() {
        return store.getters.getThemes;
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
      this.zoom = this.zoomLevel;
    }
  }
</script>
