// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  ebos: {
    visibleColumns: ['name', 'loadedAPITag', 'state', 'apidocs'],
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 10,
      sortBy: null,
      descending: false
    },
    filter: ''
  }
}

export const mutations = {
  EBOS (state, ebos) {
    state.ebos = ebos
  }
}

export const actions = {
}

const getters = {
  Ebos: (state, getters) => {
    return state.ebos
  }
}

Vue.use(Vuex)

// Vuex version
export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})
