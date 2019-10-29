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
      western_european: true,
      dissidents: true,
    },
    groupTranslation: {
      mexican: "Mexican migrants",
      chinese: "Chinese migrants",
      japanese: "Japanese migrants",
      jewish: "Jewish migrants",
      eastern_european: "Eastern European migrants",
      western_european: "Western European migrants",
      dissidents: "Political dissidents",
    },
    symbolTranslation: {
      jewish: 'diamond',
      indian: 'triangle',
      eastern_european: 'circle',
      chinese: 'polygon',
      japanese: 'square',
      western_european: 'oval',
      mexican: 'triangle_right',
    },
    eventTypes: {
      us: true,
      world: true,
      legislation: true,
      caselaw: true,
    },
    eventTranslation: {
      us: "U.S. Event",
      world: "World Event",
      legislation: "Legislation",
      caselaw: "Case Law"
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
    getGroupTranslation(state) {
      return state.groupTranslation
    },
    getSelectedEvent(state) {
      return state.event;
    },
    getSelectedYear(state) {
      return state.year
    },
    getSymbolTranslation(state) {
      return state.symbolTranslation
    },
    getEventTypes(state) {
      return state.eventTypes
    },
    getEventTranslation(state) {
      return state.getEventTranslation
    }
  },
  modules: {}
});
export default store

