<template>
  <div class="daily-tank-container">
    <div class="daily-tank-content">
      <h3>Daily Tank Sales</h3>
      <div style="max-height: 300px; overflow-y: auto;">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Tank ID</th>
              <th scope="col">Date</th>
              <th scope="col">Sales</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(dailyTankSale, index) in paginatedDailyTankSales" :key="dailyTankSale.id">
              <td>{{ dailyTankSale.id }}</td>
              <td>
                <a :href="getTankUrl(dailyTankSale.tank_id)" target="_blank">
                  {{ getTankId(dailyTankSale.tank_id) }}
                </a>
              </td>
              <td>{{ formatDate(dailyTankSale.date) }}</td>
              <td>{{ dailyTankSale.sales }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dailyTankSales: [],
      currentPage: 1,
      perPage: 10
    };
  },
  computed: {
    paginatedDailyTankSales() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.dailyTankSales.slice(start, end);
    }
  },
  methods: {
    async getData() {
      try {
        const response = await axios.get('http://localhost:8000/api/daily-tank/');
        this.dailyTankSales = response.data;
      } catch (error) {
        console.log(error);
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const date = new Date(dateString);
      date.setDate(date.getDate() + 1); // Add one day to the date
      return date.toLocaleDateString(undefined, options);
    },
    getTankUrl(tankId) {
      return `http://localhost:8000/api/tanks/${tankId}/`;
    },
    getTankId(tankUrl) {
      const parts = tankUrl.split('/');
      return parts[parts.length - 2];
    }
  },
  created() {
    this.getData();
  }
};
</script>

<style scoped>
.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f9f9f9;
}
</style>