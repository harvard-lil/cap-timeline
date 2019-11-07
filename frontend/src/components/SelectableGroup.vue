<template>
  <div class="selectable-group" :class="[slug, {active: status}]"
       @click="toggleOn()">
    <span class="group-name">
      <svgicon :icon="symbolTranslation[slug]"
               :class="'group-symbol group-name-' + slug + ' symbol-' + symbolTranslation[slug]"
               width="18" height="18">
      </svgicon>
     {{fullName}}
    </span>
  </div>
</template>

<script>
  import store from '../store'

  export default {
    name: "SelectableGroup",
    props: ["slug"],
    data() {
      return {
        queryName: "groups",
        status: true,
      }
    },
    computed: {
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      },
      fullName() {
        return store.getters.getGroup(this.slug).name
      }

    },
    methods: {
      toggleOn() {
        this.status = !this.status;
        let data = {slug: this.slug, status: this.status};
        store.commit('setGroupStatus', data);
      },
    },
  }
</script>