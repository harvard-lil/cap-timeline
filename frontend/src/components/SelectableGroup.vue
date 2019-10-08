<template>
  <div class="selectable-group"
       @click="toggleOn()">
    <span class="group-name" :class="{active: status}">
      {{name}}
    </span>
  </div>
</template>

<script>
  import store from '../store'
  export default {
    name: "SelectableGroup",
    props: ["name"],
    data() {
      return {
        queryName: "groups",
        status: true,
      }
    },
    methods: {
      toggleOn() {
        this.status = !this.status;
        let data = {name: this.name, status: this.status};
        store.commit('setGroupStatus', data);

      },
    },
    beforeMount() {
      let data = {name: this.name, status: true};
      store.commit('setGroupStatus', data);
    }
  }
</script>