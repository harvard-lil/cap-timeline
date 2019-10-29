<template>
  <div class="key-container"
       :class="{open: toggledOpen, disabled: showingEvent}">
    <svgicon icon="key"
             @click="toggleOpen()"
             class="key-icon"
             width="45" height="45">
    </svgicon>
    <div class="key-content">
      <b>Key: </b><span>toggle filters on or off</span>
      <ul>
        <li v-for="(status, group) in groups">
          <selectable-group :name="group" :translated="groupTranslation[group]">
          </selectable-group>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import './icons/key';
  import './icons/star8';
  import SelectableGroup from './SelectableGroup'
  import store from '../store'
  export default {
    name: "key",
    components: {SelectableGroup},
    data() {
      return {
        toggledOpen: false,
        groups: {},
        showingEvent: false,
        groupTranslation: {}
      }
    },
    watch: {
      '$route'(to) {
        if (to.query.event) {
          this.toggledOpen = false;
          this.showingEvent = true;
        } else {
          this.showingEvent = false;
        }
      }
    },

    methods: {
      toggleOpen() {
        this.toggledOpen = !this.toggledOpen;
      }
    },

  }
</script>
