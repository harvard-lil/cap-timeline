<template>
    <div class="home-container">
        <nav class="navbar main-nav fixed-top">
            <a id='skip-nav' class='screenreader-text' href='#main-content'>
                Skip to content
            </a>

            <span class="navbar-brand">
                <span class="nav-title">
                  <router-link :to="'/'">
                    Timelines
                  </router-link>
                </span>
            </span>
        </nav>

        Available timelines:
        <ul class="timeline-list">
            <li v-for="meta in metas" v-bind:key="meta.slug">
                <router-link :to="'/' + meta.slug">
                    {{meta.title}}
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script>
  import axios from "axios";

  export default {
    name: "homeview",
    data() {
      return {
        metas: [],
      }
    },

    beforeCreate() {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + 'metas';
      axios.get(url)
          .then((response) => {
            this.metas = response.data;
          })
    }
  }
</script>

<style scoped>

</style>