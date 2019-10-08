import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    groups: {
      mexican: true,
      chinese: true,
      japanese: true,
      jewish: true,
      eastern_european: true,
      dissidents: true,
    },
    event: null,
    year: null,
  },
  actions: {
    loadGroups: function (context) {
      let url = 'http://localhost:8000/groups';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroups', response.data)
          })
    },


  },
  mutations: {
    loadGroups(state, groups) {
      for (let i = 0; i < groups.length; i++) {
        state.groups[groups[i]] = true;
      }
    },
    setGroupStatus(state, groupData) {
      state.groups[groupData.name] = groupData.status;
    },
    setSelectedEvent(state, event) {
      state.event = event;
    },
    setSelectedYear(state, year) {
      state.year = year;
    }
  },
  getters: {
    getGroups(state) {
      return state.groups;
    },
    getActiveGroups(state) {
      // TODO: this is done for every event. Come up with a better soluton.
      return Object.keys(state.groups).filter(group => state.groups[group])
    },
    getSelectedEvent(state) {
      return state.event;
    },
    getSelectedYear(state) {
      return state.year
    }
  },
  modules: {}
});
export default store

