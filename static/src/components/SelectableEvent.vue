<template>
  <li class="list-item" :class="status ? 'checked' : 'unchecked'" @click="changeStatus()">
    <span class="icon selectable-event" :class="status ? 'active' : ''">
      <svgicon :icon="status ? 'checked' : 'unchecked'"
               :class="status ? 'active' : ''"
               width="18" height="18">
      </svgicon>
    </span>

    <label class="label">{{fullname}}</label>
  </li>
</template>

<script>
  import './icons/checked';
  import './icons/unchecked';
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