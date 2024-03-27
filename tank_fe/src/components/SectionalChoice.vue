<template>
  <section class="features-icons bg-light text-center">
    <div class="container">
      <div class="row">
        <div class="col-lg-4">
          <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
            <div class="features-icons-icon d-flex"><i class="bi bi-droplet m-auto text-primary"></i></div>
            <h3>Daily Volume</h3>
            <p class="lead mb-0">Check Tank Volumes</p>
            <button type="button" class="btn btn-primary mt-2" @click="$emit('change-component', 'TankVolumes')">Tank
              Volumes
            </button>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
            <div class="features-icons-icon d-flex"><i class="bi bi-currency-dollar m-auto text-primary"></i></div>
            <h3>Daily Tank Sales</h3>
            <p class="lead mb-0">See daily sales by tank</p>
            <button type="button" class="btn btn-primary mt-2" @click="$emit('change-component', 'DailyTankSales')">
              Daily Tank Sales
            </button>

          </div>
        </div>
        <div class="col-lg-4">
          <div class="features-icons-item mx-auto mb-0 mb-lg-3">
            <div class="features-icons-icon d-flex"><i class="bi bi-calendar-date m-auto text-primary"></i></div>
            <h3>Average Tank Values</h3>
            <p class="lead mb-0">Choose a date to see the avg</p>
            <button type="button" class="btn btn-primary mt-2" @click="$emit('change-component', 'AverageDaily')">Daily
              Tank Sales
            </button>

          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
.features-icons {
  padding-top: 3rem;
  padding-bottom: 7rem;
}

.features-icons .features-icons-item {
  max-width: 20rem;
}

.features-icons .features-icons-item .features-icons-icon {
  height: 7rem;
}

.features-icons .features-icons-item .features-icons-icon i {
  font-size: 4.5rem;
}
</style>
<script setup>
</script>