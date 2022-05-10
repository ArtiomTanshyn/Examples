<template>
  <div>
    <div class="row between">
      <h1>Regions</h1>
      <router-link
        class="ant-btn ant-btn-primary"
        :to="{ name: 'CreateRegion' }"
        >Create Region</router-link
      >
    </div>
    <LocationList :depth="depth" />
  </div>
</template>

<script>
import LocationList from '@/components/locations/LocationList.vue'

export default {
  components: {
    LocationList,
  },

  data() {
    return {
      depth: 1,
    }
  },
}
</script>
