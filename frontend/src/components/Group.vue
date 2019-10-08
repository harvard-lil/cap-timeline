<template>
  <div class="group">
    <span class="group-name" :class="{active: status}">
      {{name}}
    </span>
  </div>
</template>
<script>
  import store from '../store'
  export default {
    name: "Group",
    props: ["name"],
    computed: {
      groupStatus() {
        return store.getters.getGroups[this.name]
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