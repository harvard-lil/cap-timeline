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
        queryName: "groups"
      }
    },
    methods: {
      toggleOn() {
        this.toggledOn = !this.toggledOn;
        this.updateQuery();
      },
      updateQuery() {
        let newQuery = {};
        let groups = [];
        // making new copy of query because mutating is not allowed
        newQuery = Object.assign({}, this.$route.query);
        if (this.queryName in newQuery) {
          groups = newQuery[this.queryName].split(',');
          this.toggledOn ? groups.push(this.name) : groups.splice(groups.indexOf(this.name), 1);
        } else {
          groups = this.toggledOn ? [this.name] : [];
        }
        if (groups.length > 0) {
          groups = Array.from(new Set(groups)); // make sure no duplicates
          newQuery[this.queryName] = groups.join(',');
        } else {
          delete newQuery[this.queryName];
        }
        if (Object.keys(newQuery).length > 0) {
          this.$router.push({query: newQuery});
        } else {
          this.$router.push({});
        }

      },
    },
    beforeMount() {
      this.updateQuery();
    }
  }
</script>