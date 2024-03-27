<template>
  <header class="masthead">
    <div class="container position-relative">
      <div class="row justify-content-center">
        <div class="col-sm-8">
          <div class="text-center text-white">
            <component :is="currentComponent" />



          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import TankVolumes from "./TankVolumes.vue";
import DailyTankSales from "./DailyTankSales.vue";
import AverageDaily from "./AverageDaily.vue";

export default {
  name: "ContentMastHead",
  components: {
    TankVolumes,
    DailyTankSales,
    AverageDaily,
  },
  props: {
    currentComponent: {
      type: String,
      required: true,
    },
  },
};
</script>

<style>
header.masthead {
  position: relative;
  background-color: #343a40;
  background-size: cover;
  padding-top: 8rem;
  padding-bottom: 8rem;
  min-height: 440px;
}

header.masthead:before {
  content: "";
  position: absolute;
  background-color: #1c375e;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  opacity: 0.5;
}

header.masthead h1, header.masthead .h1 {
  font-size: 2rem;
}

@media (min-width: 768px) {
  header.masthead {
    padding-top: 2rem;
    padding-bottom: 4rem;
  }

  header.masthead h1, header.masthead .h1 {
    font-size: 3rem;
  }
}
</style>