<template>
  <div>
    <q-table
      title='Ebos'
      :data="eboData"
      :columns="eboTableColumns"
      :visible-columns="ebosDataTableSettings.visibleColumns"
      :filter="ebosDataTableSettings.filter"
      row-key="name"
      :pagination.sync="ebosDataTableSettings.serverPagination"
      :loading="loading"
      @request="request"
      selection="none"
      :rows-per-page-options="rowsPerPageOptions"
    >
      <template slot="top-selection" slot-scope="props">
      </template>

      <template slot="top-left" slot-scope="props">
      </template>
      <template slot="top-right" slot-scope="props">
      <q-table-columns
        color="secondary"
        class="q-mr-sm"
        v-model="ebosDataTableSettings.visibleColumns"
        :columns="eboTableColumns"
      />
      <!--<q-search clearable hide-underline v-model="ebosDataTableSettings.filter" />-->
      </template>

      <q-td slot="body-cell-apidocs" slot-scope="props" :props="props">
        <div v-if="props.row.state === 'OK' ">{{ props.apidocurl }}</div>
      </q-td>

    </q-table>
  </div>

</template>

<script>
import { Notify } from 'quasar'
import globalStore from '../store/globalStore'
import dataTableSettings from '../store/dataTableSettings'
import callbackHelper from '../callbackHelper'
import restcallutils from '../restcallutils'

export default {
  data () {
    return {
      rowsPerPageOptions: [5, 10, 25, 50, 100, 200],
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      },
      createJobModalDialog: {},
      eboTableColumns: [
        { name: 'name', required: true, label: 'EBO Name', align: 'left', field: 'name', sortable: false, filter: false },
        { name: 'sourceFileTag', required: false, label: 'Source File Tag', align: 'left', field: 'sourceFileTag', sortable: false, filter: false },
        { name: 'loadedAPITag', required: false, label: 'Loaded API Tag', align: 'left', field: 'loadedAPITag', sortable: false, filter: false },
        { name: 'state', required: false, label: 'State', align: 'left', field: 'state', sortable: false, filter: false },
        { name: 'stateMeaning', required: false, label: 'State Meaning', align: 'left', field: 'stateMeaning', sortable: false, filter: false },
        { name: 'errorStateReason', required: false, label: 'Error', align: 'left', field: 'errorStateReason', sortable: false, filter: false },
        { name: 'apidocs', required: false, label: 'API Documentation', align: 'left', field: 'apidocs', sortable: false, filter: false }
      ],
      eboData: [],
      loading: false
    }
  },
  methods: {
    request ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)
          TTT.loading = false

          // updating pagination to reflect in the UI
          TTT.ebosDataTableSettings.serverPagination = pagination
          // we also set (or update) rowsNumber
          TTT.ebosDataTableSettings.serverPagination.rowsNumber = response.data.pagination.total
          TTT.ebosDataTableSettings.serverPagination.filter = filter
          TTT.ebosDataTableSettings.serverPagination.rowsPerPage = response.data.pagination.pagesize

          dataTableSettings.commit('EBOS', TTT.ebosDataTableSettings)

          // then we update the rows with the fetched ones
          TTT.eboData = response.data.result

          // finally we tell QTable to exit the "loading" state
          TTT.loading = false
        },
        error: function (error) {
          TTT.loading = false
          Notify.create('Job query failed - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      if (pagination.page === 0) {
        pagination.page = 1
      }

      var queryParams = []

      if (filter !== '') {
        queryParams['query'] = filter
      }
      if (pagination.rowsPerPage !== 0) {
        queryParams['pagesize'] = pagination.rowsPerPage.toString()
        queryParams['offset'] = (pagination.rowsPerPage * (pagination.page - 1)).toString()
      }
      if (pagination.sortBy !== null) {
        var postfix = ''
        if (pagination.descending) {
          postfix = ':desc'
        }
        queryParams['sort'] = pagination.sortBy + postfix
      }

      var queryString = restcallutils.buildQueryString('EBOs/', queryParams)
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    },
    ebosDataTableSettings () {
      return dataTableSettings.getters.Ebos
    }
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.request({
      pagination: this.ebosDataTableSettings.serverPagination,
      filter: this.ebosDataTableSettings.filter
    })
  }
}
</script>

<style>
</style>
