<template>
  <div v-show=!hide class="event-container" :class="'event-type-' + data.type">
    <h3>{{ data.name }}</h3>
    <p class="text-semibold">{{ data.start_date_parsed }}</p>
    <p>{{ data.description_short }}</p>
    <p>{{ data.type }}</p>
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
      hideOrShow() {
        this.hide = this.currentYear && this.year !== this.currentYear;
      }
    },
    watch: {
      currentYear() {
        this.hideOrShow();
      }
    },
    beforeMount() {
      this.hideOrShow();
      let date = new Date(this.data.start_date);
      return "" + date.getMonth()
    }
  }
</script>
