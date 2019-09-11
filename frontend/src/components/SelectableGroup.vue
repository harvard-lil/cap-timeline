<template>
  <div class="selectable-group"
       @click="toggleOn()">
    <span class="group-name" :class="{active: toggledOn}">{{name}}</span>
  </div>
</template>

<script>
  export default {
    name: "SelectableGroup",
    props: ["name"],
    data() {
      return {
        toggledOn: true,
      }
    },
    methods: {
      toggleOn() {
        this.toggledOn = !this.toggledOn;
        let newQuery = {};
        if (this.toggledOn) {
          // making new copy of query because mutating is not allowed
          newQuery = Object.assign({}, this.$route.query);
          delete newQuery[this.name]
        }
        else {
          newQuery = Object.assign({}, this.$route.query, {[this.name]: this.toggledOn})
        }
        this.$router.push({query: newQuery});

      }
    }
  }
</script>