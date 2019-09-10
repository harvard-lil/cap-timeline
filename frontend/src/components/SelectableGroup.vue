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
        this.$router.push({
          // making new copy of query because mutating is not allowed
          query: Object.assign({}, this.$route.query, {[this.name]: this.toggledOn}),
        });
      }
    }
  }
</script>