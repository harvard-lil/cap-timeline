<template>
  <div class="selectable-group" :class="[slug, {active: status}]"
       @click="toggleOn()">
    <span class="group-name icon" :class="status ? 'active' : ''">
      <svgicon :icon="symbolTranslation[slug]"
               :class="'group-symbol group-name-' + slug + ' symbol-' + symbolTranslation[slug]"
               width="18" height="18">
      </svgicon>
    </span>
    <label class="label">
      {{fullName}}
    </label>
  </div>
</template>

<script>
  import store from '../store';

  export default {
    name: "SelectableGroup",
    props: ["slug", "status", "fullName"],
    data() {
      return {
        queryName: "groups",
      }
    },
    computed: {
      symbolTranslation() {
        return this.$store.getters.getSymbolTranslation
      },
      activeGroups() {
        return store.getters.getActiveGroups;
      }
    },
    methods: {
      toggleOn() {
        this.$store.commit('setGroupStatus', {slug: this.slug, status: !this.status});
      },
    },
  }
</script>