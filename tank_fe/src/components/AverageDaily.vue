<template>
  <div class="row justify-content-center">
    <div class="col-4">
      <div class="form-group">
        <label for="tank-select">Select Tank:</label>
        <select class="form-control" id="tank-select" v-model="selectedTankId">
          <option v-for="tank in tanks" :value="tank.id" :key="tank.id">{{ tank.name }}</option>
        </select>
      </div>
    </div>
    <div class="col-4">
      <div class="form-group">
        <label for="datepicker">Select Date:</label>
        <div class="input-group">
          <input type="text" class="form-control" id="datepicker" placeholder="Select Date" v-model="selectedDate" readonly ref="datepicker">
          <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" @click="showDatepicker">
              <i class="bi bi-calendar"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="averageSales !== null">
    <h4>Average Sales for {{ displayDate }}</h4>
    <p>{{ averageSales }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-datepicker/dist/css/bootstrap-datepicker.css';
import 'bootstrap-datepicker';
import $ from 'jquery';

export default {
  data() {
    return {
      tanks: [],
      selectedTankId: null,
      selectedDate: '',
      averageSales: null,
      displayDate: '',
    };
  },
  mounted() {
    this.fetchTanks();
    this.$nextTick(() => {
      this.initializeDatepicker();
    });
  },
  methods: {
    async fetchTanks() {
      try {
        const response = await axios.get('http://localhost:8000/api/tanks/');
        this.tanks = response.data;
        if (this.tanks.length > 0) {
          this.selectedTankId = this.tanks[0].id;
        }
      } catch (error) {
        console.log(error);
      }
    },
    initializeDatepicker() {
      $(this.$refs.datepicker).datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        startDate: '2023-01-01', // Set the start date to January 1, 2023
      }).on('changeDate', this.onDateChange);
    },
    showDatepicker() {
      $(this.$refs.datepicker).datepicker('show');
    },
    async onDateChange(event) {
      this.selectedDate = event.format();
      this.displayDate = new Date(this.selectedDate).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });

      if (this.selectedTankId) {
        try {
          const response = await axios.get(`http://localhost:8000/api/tanks/${this.selectedTankId}/average-sales/${this.selectedDate}/`);
          this.averageSales = response.data.average_sales;
        } catch (error) {
          console.log(error);
        }
      }
    },
  },
};
</script>