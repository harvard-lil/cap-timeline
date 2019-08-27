<template>
  <div v-show=!hide class="event-container">
    <h3>{{ data.name }}</h3>
    <p class="text-bold">{{ data.start_date }}</p>
    <p>{{ data.description_short }}</p>
  </div>
</template>

<script>
  export default {
    name: "event",
    props: ["data", "currentYear"],
    data() {
      return {
        year: this.getYear(),
        hide: false
      }
    },
    methods: {
      getYear() {
        return Number(this.data.start_date.split('-')[0])
      },
    },
    watch: {
      currentYear() {
        this.hide = this.currentYear && this.year !== this.currentYear;
      }
    }
  }
</script>

<style scoped>

</style>