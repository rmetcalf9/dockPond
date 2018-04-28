<template>
  <q-page padding class="card-examples row items-start" v-if="datastoreState === 'LOGGED_IN_SERVERDATA_LOADED'">
    <q-card inline class="q-ma-sm">
      <q-card-title>
        Server Info
        <span slot="subtitle">EBO Information</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr><td align="right">Number APIs Loaded:</td><td>{{ serverInfo.EBOs.NumberLoaded }}</td></tr>
          <tr><td align="right">Number APIs Not OK:</td><td>{{ serverInfo.EBOs.NumberNotOK }}</td></tr>
        </table>
      </q-card-main>
    </q-card>
  </q-page>
</template>

<script>
import globalStore from '../store/globalStore'

export default {
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    serverInfo () {
      var ret = globalStore.getters.serverInfo
      return ret
    },
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  }
}
</script>

<style>
</style>
