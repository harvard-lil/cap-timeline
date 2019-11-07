<template>
  <div class="sidebar-sticky toggles-menu">
    <!--year slider-->
    <h3>Years</h3>
    <vue-slider v-model="yearValue"
                :min="yearMin"
                :max="yearMax"
                :enable-cross="false">
    </vue-slider>
    <hr/>
    <!--Groups-->
    <h3>Groups</h3>
    <ul class="group-types list-group">
      <li class="list-item" v-for="(status, group) in groups" v-bind:key="group">
        <selectable-group :slug="group"
                          :icon=symbolTranslation[group]>
        </selectable-group>
      </li>
    </ul>
    <hr/>
    <!--Event types-->
    <h3>Event Types</h3>
    <ul class="event-types list-group">
      <selectable-event v-for="(status, eventType) in eventTypes"
                        v-bind:key="eventType"
                        :name="eventType"
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
        yearMin: 1800,
        yearMax: 1930,
        yearValue: [1800, 1930],
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
      groupTranslation() {
        return store.getters.getGroupTranslation;
      },
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      }
    },
    watch: {
      yearValue(newYearValue) {
        store.commit('setMinYear', Number(newYearValue[0]));
        store.commit('setMaxYear', Number(newYearValue[1]));
      }
    }

  }
</script>
<style>
  .vue-slider-process,
  .vue-slider-dot-handle,
  .vue-slider-dot-tooltip-inner {
    background-color: #007AFF;
  }
  .vue-slider.vue-slider-ltr {
    padding: 0 0.5em !important;
  }

</style>