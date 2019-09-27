import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    groups: {}
  },
  actions: {
    loadGroups: function (context) {
      let url = 'http://localhost:8000/groups';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroups', response.data)
          })
    }

  },
  mutations: {
    loadGroups(state, groups) {
      for (let i = 0; i < groups.length; i++) {
        state.groups[groups[i]] = true;
      }
    },
    setGroupStatus(state, groupData) {
      state.groups[groupData.name] = groupData.status;
    }
  },
  getters: {},
  modules: {}
});
export default store