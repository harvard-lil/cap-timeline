<template>
  <div class="group">
    <span class="group-name" :class="{active: status}">
      <svgicon :icon="symbolTranslation[name]"
               :class="'group-symbol group-name-' + name + ' symbol-' + symbolTranslation[name]"
               width="18" height="18">
      </svgicon>
    </span>
  </div>
</template>
<script>
  import './icons/diamond';
  import './icons/circle';
  import './icons/triangle';
  import './icons/polygon';

  import store from '../store'

  export default {
    name: "Group",
    props: ["name"],
    computed: {
      groupStatus() {
        return store.getters.getGroups[this.name]
      },
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      }
    },
    watch: {
      groupStatus() {
        this.status = this.groupStatus;
        this.$parent.updateActiveGroups();
      }
    },
    data() {
      return {
        status: true,
      }
    },

  }
</script>