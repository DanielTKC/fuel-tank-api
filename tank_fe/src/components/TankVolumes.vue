<template>
  <div class="tank-volume-container">
    <div class="tank-volume-content">
      <h3>Tank Volumes</h3>
      <div style="max-height: 300px; overflow-y: auto;">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Tank ID</th>
              <th scope="col">Date</th>
              <th scope="col">Volume</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tankVolume, index) in paginatedTankVolumes" :key="tankVolume.id">
              <td>{{ tankVolume.id }}</td>
              <td>
                <a :href="getTankUrl(tankVolume.tank_id)" target="_blank">
                  {{ getTankId(tankVolume.tank_id) }}
                </a>
              </td>
              <td>{{ formatDate(tankVolume.created_at) }}</td>
              <td>{{ tankVolume.volume }}</td>
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
      tankVolumes: [],
      currentPage: 1,
      perPage: 10
    };
  },
  computed: {
    paginatedTankVolumes() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.tankVolumes.slice(start, end);
    }
  },
  methods: {
    async getData() {
      try {
        const response = await axios.get('http://localhost:8000/api/tank-volumes/');
        this.tankVolumes = response.data;
      } catch (error) {
        console.log(error);
      }
    },
    formatDate(dateString) {
      const options = {year: 'numeric', month: 'long', day: 'numeric'};
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    getTankUrl(tankId) {
      return `http://localhost:8000/api/tanks/${tankId}`;
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