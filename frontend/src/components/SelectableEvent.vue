<template>
  <li class="list-item" :class="status ? 'checked' : 'unchecked'" @click="changeStatus()">
    <svgicon :icon="status ? 'checked' : 'unchecked'"
             :class="status ? 'checked' : 'unchecked'"
             width="18" height="18">
    </svgicon>

    <span>{{fullname}}</span>
  </li>
</template>

<script>
  import './icons/unchecked';
  import './icons/checked';
  export default {
    name: "SelectableEvent",
    props: ["name", "fullname", "status"],
    methods: {
      changeStatus() {
        this.$store.commit("setEventStatus", {name: this.name, status: !this.status})
      }
    }
  }
</script>