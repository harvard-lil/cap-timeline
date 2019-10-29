<template>
  <div class="selectable-group" :class="name"
       @click="toggleOn()">
    <span class="group-name" :class="{active: status}">
      <svgicon :icon="symbolTranslation[name]"
               :class="'group-symbol group-name-' + name + ' symbol-' + symbolTranslation[name]"
               width="18" height="18">
      </svgicon>
     {{translated}}
    </span>
  </div>
</template>

<script>
  import store from '../store'

  export default {
    name: "SelectableGroup",
    props: ["name", "translated"],
    data() {
      return {
        queryName: "groups",
        status: true,
      }
    },
    computed: {
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      }
    },
    methods: {
      toggleOn() {
        this.status = !this.status;
        let data = {name: this.name, status: this.status};
        store.commit('setGroupStatus', data);
      },
    },
    beforeMount() {
      let data = {name: this.name, status: true};
      store.commit('setGroupStatus', data);
    }
  }
</script>