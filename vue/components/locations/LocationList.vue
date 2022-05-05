<template>
  <div class="locationPage">
    <Filters
      v-model="filters"
      @clear="clearFilters"
      :filter-options="filterOptions"
    >
      <a-col :span="24" :lg="4" v-if="!$route.params.id && depth != 0">
        <a-form-item label="Country">
          <LocationsSelect
            v-model="filters.descendants_of"
            show-search
            :showFullName="false"
            :depth="0"
          />
        </a-form-item>
      </a-col>
      <a-col
        :span="24"
        :lg="4"
        v-if="
          filters.descendants_of &&
          !$route.params.id &&
          depth != 0 &&
          depth != 1
        "
      >
        <a-form-item label="Region">
          <LocationsSelect
            v-model="filters.parent_id"
            show-search
            :parent_id="filters.descendants_of"
            :depth="1"
            :showFullName="false"
          />
        </a-form-item>
      </a-col>
    </Filters>
    <a-table
      :columns="columns"
      :row-key="(record) => record.id"
      :data-source="items"
      :pagination="pagination"
      :loading="loading"
      @change="onUpdateTable"
    >
      <template #status="{ text }">
        <span>
          <a-tag :color="text ? 'green' : 'grey'">{{
            text ? 'Active' : 'Not active'
          }}</a-tag>
        </span>
      </template>
      <template #depth="{ text }">
        <span>
          {{ text == 0 ? 'Country' : text == 1 ? 'Region' : 'City' }}
        </span>
      </template>
      <template #operation="{ record }">
        <div class="editable-row-operations">
          <span>
            <span
              class="link"
              @click="
                $router.push({
                  name: 'LocationProfile',
                  params: { id: record.id },
                })
              "
              >View</span
            >
          </span>
        </div>
      </template>
      <template v-slot:footer>
        <Filters
          disable-search
          :clearable="false"
          v-model="filters"
          :filter-options="[
            {
              field: 'paginate',
              label: 'Per page',
              options: [
                { value: 20, title: '20' },
                { value: 50, title: '50' },
                { value: 100, title: '100' },
              ],
            },
          ]"
        ></Filters>
      </template>
    </a-table>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import useTable from '@/composables/useTable'
import { strToBool } from '@/helpers'
import Filters from '@/components/Filters.vue'
import LocationsSelect from '@/components/locations/LocationsSelect.vue'

export default {
  components: { Filters, LocationsSelect },
  props: {
    depth: { type: Number, default: null },
    parent_id: { type: Number, default: null },
  },
  setup(props) {
    const route = useRoute()
    const store = useStore()
    const staticParams = route.params.id
      ? {
          depth: props.depth,
          parent_id: props.parent_id,
        }
      : {
          depth: props.depth,
        }

    const filters = ref({
      is_active: strToBool(route.query.is_active),
      descendants_of: Number(route.query.descendants_of) || null,
      parent_id: Number(route.query.parent_id) || null,
    })
    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        slots: {
          customRender: 'id',
        },
      },
      {
        title: 'Name',
        dataIndex: 'name',
        slots: {
          customRender: 'name',
        },
        sorter: true,
      },
      {
        title: 'Status',
        dataIndex: 'is_active',
        slots: {
          customRender: 'status',
        },
      },
      {
        title: 'Depth',
        dataIndex: 'depth',
        slots: {
          customRender: 'depth',
        },
      },
      {
        title: 'Parent',
        dataIndex: 'parent.name',
        slots: {
          customRender: 'parent',
        },
      },

      {
        title: '',
        dataIndex: 'operation',
        slots: {
          customRender: 'operation',
        },
      },
    ]

    const filterOptions = [
      {
        field: 'is_active',
        label: 'Is active',
        options: [
          { value: true, title: 'Is active' },
          { value: false, title: 'Not active' },
        ],
      },
    ]

    const fetchData = async (params) => {
      return store.dispatch('locations/getLocationsList', params)
    }

    const { items, loading, pagination, onUpdateTable, clearFilters } =
      useTable({
        staticParams,
        filters,
        fetchData,
      })

    watch(
      () => filters.value.descendants_of,
      () => {
        filters.value.parent_id = null
      }
    )

    return {
      loading,
      items,
      pagination,
      onUpdateTable,
      columns,
      filters,
      filterOptions,
      clearFilters,
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/components/_location';
</style>
