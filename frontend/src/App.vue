<template>
  <div>
    <ul v-for="event in events">
      <li>{{event}}</li>
    </ul>
  </div>
</template>
<script>
  export default {
    name: 'App',
    components: {
    },
    methods: {
      getData() {
        this.$http.get('http://localhost:8000/events')
            .then((response) => {
              this.events = response.body
            })
      }
    },
    data() {
      return {
        events: {}
      }
    },
    beforeMount() {
      this.getData()
    },
  };
</script>