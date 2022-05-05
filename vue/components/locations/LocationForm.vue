<template>
  <div class="forms">
    <div class="block">
      <div class="block-item">
        <div class="forms-item">
          <p>Name:</p>
          <a-input
            :disabled="readonly"
            v-model:value="locationDataLocal.name"
            placeholder="Name"
          />
        </div>
      </div>
      <div class="block-item">
        <div class="forms-item">
          <label class="radio-wrapper">
            Active
            <a-switch
              :disabled="readonly"
              v-model:checked="locationDataLocal.is_active"
            />
          </label>
        </div>
      </div>
      <div class="block-item" v-if="depthLocal != null">
        <p>Parent:</p>
        <LocationsSelect
          :readonly="readonly"
          :depth="depthLocal"
          :showFullName="true"
          v-model="locationDataLocal.parent_id"
          show-search
          style="width: 100%"
        />
      </div>
    </div>
    <div v-if="!readonly" class="forms-action-buttons">
      <a-button @click="handleSaveData" size="large" type="primary">
        {{ locationData.id ? 'Save' : 'Create' }}
      </a-button>

      <a-button @click="handleCancel" size="large">Cancel</a-button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LocationsSelect from '@/components/locations/LocationsSelect.vue'

export default {
  name: 'LocationForm',
  components: {
    LocationsSelect,
  },
  emits: ['handleCancel', 'save'],
  props: {
    locationData: { type: Object, required: true },
    depth: { type: Number, default: null },
    readonly: { type: Boolean, default: false },
  },

  setup(props, { emit }) {
    const locationDataLocal = ref({ ...props.locationData })
    const depthLocal = ref(null)

    onMounted(() => {
      depthLocal.value =
        locationDataLocal.value.depth > 0
          ? locationDataLocal.value.depth - 1
          : props.depth
    })

    const handleSaveData = () => {
      var saveData = {}
      if (locationDataLocal.value.parent_id != null) {
        saveData = {
          name: locationDataLocal.value.name,
          is_active: locationDataLocal.value.is_active || false,
          parent_id: locationDataLocal.value.parent_id,
        }
      } else {
        saveData = {
          name: locationDataLocal.value.name,
          is_active: locationDataLocal.value.is_active || false,
        }
      }
      emit('save', saveData)
    }

    const handleCancel = () => {
      emit('handleCancel')
    }

    return {
      locationDataLocal,
      depthLocal,
      handleSaveData,
      handleCancel,
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/components/_location';
</style>
