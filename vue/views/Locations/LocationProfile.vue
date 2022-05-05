<template>
  <div class="">
    <div v-if="locationData.parent" class="breadcrumbs row start">
      <span
        v-if="locationData.parent"
        class="link"
        @click="backToParent(locationData.parent.id)"
        >{{ locationData.parent.name }}
      </span>
      <span class="delimiter" v-if="locationData.parent">/</span>
      <span>{{ locationData.name }}</span>
    </div>
    <div class="row between">
      <h1>{{ locationData.name }}</h1>
      <EditOutlined
        v-if="canEdit"
        @click="handleLocationInfoView"
        :style="{ fontSize: '24px' }"
      />
    </div>
    <LocationForm
      v-if="locationData.id"
      :readonly="readonly"
      :locationData="locationData"
      @handleCancel="handleLocationInfoView"
      @save="handleUpdateInfo"
    />
    <span
      v-if="locationData.depth != 2"
      class="ant-btn ant-btn-primary"
      @click="createChildLocation"
      >Create
      {{
        locationData.depth === 0
          ? 'region'
          : locationData.depth === 1
          ? 'city'
          : ''
      }}</span
    >
    <LocationList v-if="depth != null && depth != 2" :parent_id="parent_id" />
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import useError from '@/composables/useError'
import { ref, onMounted } from 'vue'

import LocationForm from '@/components/locations/LocationForm.vue'
import LocationList from '@/components/locations/LocationList.vue'
import { EditOutlined } from '@ant-design/icons-vue'

export default {
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const raiseError = useError()

    const locationData = ref({})
    const readonly = ref(true)
    const depth = ref(null)
    const parent_id = ref(null)

    const hasPermission = store.getters['hasPermission']

    const canEdit = hasPermission(['update-location'])

    onMounted(() => {
      store
        .dispatch('locations/getLocationProfile', {
          id: route.params.id,
        })
        .then((response) => {
          locationData.value = response.data
          parent_id.value = locationData.value.id
          depth.value = locationData.value.depth
        })
        .catch((error) => {
          raiseError(404, 'Page not found')
        })
    })

    const handleUpdateInfo = (payload) => {
      store.dispatch('locations/saveLocationInfo', {
        id: locationData.value.id,
        info: payload,
      })
    }

    const handleLocationInfoView = () => {
      readonly.value = !readonly.value
    }

    const backToParent = (parent_id) => {
      router.push({
        name: 'LocationProfile',
        params: { id: parent_id },
      })
    }

    const createChildLocation = () => {
      router.push({
        name:
          locationData.value.depth === 0
            ? 'CreateRegion'
            : locationData.value.depth === 1
            ? 'CreateCity'
            : '',
        query: {
          parent_id: locationData.value.id,
        },
      })
    }

    return {
      locationData,
      readonly,
      depth,
      parent_id,
      handleUpdateInfo,
      handleLocationInfoView,
      backToParent,
      createChildLocation,
      canEdit,
    }
  },

  components: {
    LocationForm,
    EditOutlined,
    LocationList,
  },
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/view/pages';
:deep(.table) {
  margin-top: 30px;
}
</style>
