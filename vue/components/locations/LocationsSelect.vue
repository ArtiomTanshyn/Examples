<template>
  <ExtendedSelect
    v-bind="$attrs"
    :options="options"
    @search="onSearch"
    :loading="loading"
    allow-clear
    :mode="mode"
    :disabled="readonly"
  >
    <template #option="{ label, is_active }">
      <div style="display: flex">
        <span>{{ label }}</span>
        <active-tag :is-active="is_active" style="margin-left: auto" />
      </div>
    </template>
  </ExtendedSelect>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import ExtendedSelect from '@/components/ExtendedSelect.vue'
import ActiveTag from '@/components/common/ActiveTag.vue'
import debounce from 'lodash/debounce'

export default {
  components: { ExtendedSelect, ActiveTag },
  props: {
    depth: { type: Number, default: null },
    mode: { type: String, default: null },
    readonly: { type: Boolean, default: false },
    parent_id: { type: Number, default: null },
    descendants_of: { type: Number, default: null },
    showFullName: { type: Boolean, default: true },
  },
  setup(props, { slots, attrs }) {
    const store = useStore()
    const options = ref([])
    const loading = ref(true)

    const prepareOptions = (data) => {
      return data.map((item) => ({
        ...item,
        value: item.id,
        label: props.showFullName ? fullName(item) : item.name,
      }))
    }

    const fetchOptions = async ({ ids = null, search = null }) => {
      loading.value = true
      if (search || ids == null || ids.length == 0) {
        // Fetch for search or initial unfiltered list
        const { data } = await store.dispatch('locations/getLocationsList', {
          search,
          depth: props.depth,
          parent_id: props.parent_id,
          descendants_of: props.descendants_of,
          paginate: 200,
        })
        options.value = prepareOptions(data.data)
      } else {
        // Fetch by specific id or list of id
        ids = Array.isArray(ids) ? ids : [ids]
        const response = await Promise.all(
          ids.map((id) =>
            store.dispatch('locations/getLocationProfile', { id })
          )
        )
        options.value = prepareOptions(response.map((item) => item.data))
      }
      loading.value = false
    }

    const fullName = (item) => {
      return !item.parent
        ? item.name
        : item.parent && !item.parent.parent
        ? `${item.parent.name} / ${item.name}`
        : `${item.parent.parent.name} / ${item.parent.name} / ${item.name}`
    }

    const onSearch = debounce((search) => {
      fetchOptions({ search })
    }, 800)

    onMounted(() => {
      fetchOptions({ ids: attrs.modelValue })
    })

    watch(
      () => attrs.modelValue,
      () => {
        if (!attrs.modelValue || attrs.modelValue.length == 0) {
          fetchOptions({ ids: attrs.modelValue })
        }
      }
    )

    watch(
      () => props.parent_id,
      () => {
        fetchOptions({ ids: [] })
      }
    )

    return {
      options,
      onSearch,
      loading,
    }
  },
}
</script>

<style></style>
