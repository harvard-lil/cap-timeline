<template>
  <li class="list-inline-item group">
    <span class="group-name" :class="{active: status}">
      <svgicon :icon="symbolTranslation[name]"
               :class="'group-symbol group-name-' + name + ' symbol-' + symbolTranslation[name]"
               width="18" height="18">
      </svgicon>
    </span>
    <span v-if="showName" class="group-name">{{nameTranslation}}</span>
  </li>
</template>
<script>
  import store from '../store'

  export default {
    name: "Group",
    props: ["name", "showName"],
    computed: {
      groupStatus() {
        return store.getters.getGroups[this.name]
      },
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      },
      nameTranslation() {
        return store.getters.getGroupTranslation[this.name]
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