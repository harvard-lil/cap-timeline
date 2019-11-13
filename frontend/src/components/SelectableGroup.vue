<template>
  <div class="selectable-group" :class="[slug, {active: status}]"
       @click="toggleOn()">
    <span class="group-name">
      <svgicon :icon="symbolTranslation[slug]"
               :class="'group-symbol group-name-' + slug + ' symbol-' + symbolTranslation[slug]"
               width="18" height="18">
      </svgicon>
     {{slug}}
    </span>
  </div>
</template>

<script>
  export default {
    name: "SelectableGroup",
    props: ["slug", "status"],
    data() {
      return {
        queryName: "groups",
      }
    },
    computed: {
      symbolTranslation() {
        return this.$store.getters.getSymbolTranslation
      },
      // fullName() {
      //   let groupObj = this.$store.getters.getGroup(this.slug);
      //   if (groupObj) {
      //     return groupObj.name
      //   }
      // }
    },
    methods: {
      toggleOn() {
        this.$store.commit('setGroupStatus', {slug: this.slug, status: !this.status});
      },
    },
  }
</script>