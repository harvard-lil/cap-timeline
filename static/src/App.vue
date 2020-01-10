<template>
    <div class="app-container" :class="'route-'+$route.name">
        <main id="main-content" class="main" :class="'route-'+$route.name">
            <router-view></router-view>
        </main>
    </div>
</template>
<script>

  export default {
    name: 'App',
    metaInfo: {
      title: 'Timelines',
    },
  };
</script>
