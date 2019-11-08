<template>
  <li class="list-inline-item group" :title="fullName + ' migrants'">
    <span class="group-name" :class="{active: status}">
      <svgicon :icon="symbolTranslation[slug]"
               :title="fullName + ' migrants'"
               :class="'group-symbol group-name-' + slug + ' symbol-' + symbolTranslation[slug]"
               width="18" height="18">
      </svgicon>
    </span>
    <span v-if="showName" class="group-name">{{fullName}}</span>
  </li>
</template>
<script>
  import store from '../store'

  export default {
    name: "Group",
    props: ["slug", "showName"],
    computed: {
      symbolTranslation() {
        return store.getters.getSymbolTranslation
      },
      fullName() {
        let groupObj = store.getters.getGroup(this.slug);
        if (groupObj) {
          return groupObj.name
        }
      }
    },
    data() {
      return {
        status: true,
      }
    },

  }
</script>