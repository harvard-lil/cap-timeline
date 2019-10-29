<template>
  <div :class="status ? 'checked' : 'unchecked'" @click="status=!status">
    <svgicon :icon="status ? 'checked' : 'unchecked'"
             :class="status ? 'checked' : 'unchecked'"
             width="18" height="18">
    </svgicon>

    <span>{{name}}</span>
  </div>
</template>

<script>
  import './icons/checked';
  import './icons/unchecked';
  export default {
    name: "SelectableEvent",
    props: ["name"],
    data() {
      return {
        status: true
      }
    }
  }
</script>