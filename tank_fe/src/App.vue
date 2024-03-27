<template>
  <div id="app">
    <SiteNavigation />
    <ContentMastHead :current-component="currentComponent" @change-component="changeComponent" />
    <SectionalChoice @change-component="changeComponent" />
  </div>
</template>

<script>
import SiteNavigation from "./components/SiteNavigation.vue";
import ContentMastHead from "./components/ContentMastHead.vue";
import SectionalChoice from "./components/SectionalChoice.vue";

export default {
  name: "App",
  components: {
    SectionalChoice,
    ContentMastHead,
    SiteNavigation,
  },
  data() {
    return {
      currentComponent: "TankVolumes",
    };
  },
  methods: {
    changeComponent(componentName) {
      this.currentComponent = componentName;
    },
  },
};
</script>