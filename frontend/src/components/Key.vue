<template>
  <div class="key-container" :class="toggledOpen ? 'open' : 'closed'">
    <svgicon icon="key"
             @click="toggleOpen()"
             class="key-icon"
             width="45" height="45">
    </svgicon>
    <div class="key-content" v-if="toggledOpen">
      <b>Key: </b><span>toggle filters on or off</span>
      <ul>
        <li v-for="group in groups">
          <selectable-group :name="group"></selectable-group>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import './icons/key';
  import './icons/star8';
  import SelectableGroup from './SelectableGroup'

  export default {
    name: "key",
    components: {SelectableGroup},
    data() {
      return {
        toggledOpen: false,
        groups: []
      }
    },
    methods: {
      toggleOpen() {
        this.toggledOpen = !this.toggledOpen;
      }
    },
    beforeMount() {
      let url = 'http://localhost:8000/groups';
      this.$http.get(url)
          .then((response) => {
            this.groups = response.body;
          })


    }
  }
</script>
