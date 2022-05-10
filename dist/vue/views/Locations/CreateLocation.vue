<template>
  <div class="">
    <div class="row between">
      <h1>
        Create {{ depth === 0 ? 'region' : depth === 1 ? 'city' : 'country' }}
      </h1>
    </div>
    <LocationForm
      :locationData="locationData"
      @save="handleCreateLocation"
      :depth="depth"
    />
  </div>
</template>

<script>
import LocationForm from '@/components/locations/LocationForm.vue'

import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import { ref } from 'vue'

export default {
  props: {
    depth: { type: Number, default: null },
  },

  setup() {
    const store = useStore()
    const route = useRoute()

    const locationData = ref(
      route.query.parent_id ? { parent_id: Number(route.query.parent_id) } : {}
    )

    const handleCreateLocation = (payload) => {
      store.dispatch('locations/createLocation', {
        info: payload,
      })
    }
    return {
      locationData,
      handleCreateLocation,
    }
  },

  components: {
    LocationForm,
  },
}
</script>

<style lang="scss"></style>
