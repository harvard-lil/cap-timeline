import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    groups: {},
    groupsByRegion: [],
    symbolTranslation: {
      jewish: 'diamond',
      indian: 'triangle',
      eastern_european: 'circle',
      chinese: 'polygon',
      japanese: 'square',
      western_european: 'oval',
      mexican: 'star5',
      dissidents: 'heptagon'
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
    minYear: 1800,
    maxYear: 1930
  },
  actions: {
    loadGroups (context) {
      let url = 'http://localhost:8000/groups';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroups', response.data)
          })
    },
    loadGroupsByRegion(context) {
      let url = 'http://localhost:8000/groups-by-region';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroupsByRegion', response.data)
          })

    },

    getYears: function () {
     // todo
    }
  },
  mutations: {
    loadGroups(state, groups) {
      for (let i = 0; i < groups.length; i++) {
        Vue.set(state.groups, groups[i][0], {status: true, name: groups[i][1]});
      }
    },
    loadGroupsByRegion(state, groupsByRegion) {
      state.groupsByRegion = groupsByRegion;
    },
    setGroupStatus(state, groupData) {
      state.groups[groupData.slug].status = groupData.status;
    },
    setSelectedEvent(state, event) {
      state.event = event;
    },
    setSelectedYear(state, year) {
      state.year = year;
    },
    setMinYear(state, year) {
      state.minYear = year;
    },
    setMaxYear(state, year) {
      state.maxYear = year;
    },
    setEventStatus(state, eventData) {
      state.eventTypes[eventData.name] = eventData.status;
    },
  },
  getters: {
    getGroups(state) {
      return state.groups;
    },
    getActiveGroups(state) {
      // TODO: this is done for every event. Come up with a better soluton.
      return Object.keys(state.groups).filter(group => state.groups[group].status).map(group => group)
    },
    getGroup: (state) => (slug) => {
      return state.groups[slug]
    },
    getSelectedEvent(state) {
      return state.event;
    },
    getSelectedYear(state) {
      return state.year
    },
    getMinYear(state) {
      return state.minYear
    },
    getMaxYear(state) {
      return state.maxYear
    },
    getSymbolTranslation(state) {
      return state.symbolTranslation
    },
    getEventTypes(state) {
      return state.eventTypes
    },
    getEventTranslation(state) {
      return state.eventTranslation
    },
    getActiveEvents(state) {
      return Object.keys(state.eventTypes).filter(event => state.events[event])
    },
    getGroupsByRegion(state) {
      return state.groupsByRegion;
    }
  },
  modules: {}
});
export default store

