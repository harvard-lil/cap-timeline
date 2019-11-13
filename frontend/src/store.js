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
      chinese: 'polygon',
      japanese: 'square',
      mexican: 'star5',
    },
    eventTypes: {
      us: false,
      world: false,
      legislation: false,
      caselaw: false,
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
    maxYear: 1930,
    activateAllGroupsWhenLoaded: false,
  },
  actions: {
    loadGroups(context) {
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
    loadYears(context) {
      let url = "http://localhost:8000/year-settings";
      axios.get(url)
          .then((response) => {
            context.commit('loadYears', response.data)
          })
    }
  },
  mutations: {
    loadGroups(state, groups) {
      // work around:
      // we're getting URL parameters before groups are loaded from the server
      // because of this, we're checking if groups have already been initialized with their correct status
      // otherwise we're hiding groups from view
      for (let i = 0; i < groups.length; i++) {
        if (!(state.groups[groups[i][0]]))
          if (state.activateAllGroupsWhenLoaded) {
            Vue.set(state.groups, groups[i][0], true);
          } else {
            Vue.set(state.groups, groups[i][0], false);
          }
      }
      state.activateAllGroupsWhenLoaded = false;
    },
    loadGroupsByRegion(state, groupsByRegion) {
      state.groupsByRegion = groupsByRegion;
    },
    loadYears(state, years) {
      state.minYear = years.min;
      state.maxYear = years.max;
    },
    setGroupStatus(state, groupData) {
      if (Object.keys(state.groups).indexOf(groupData.slug) < 0) {
        // state.groups has not been initialized yet, initialize group ourselves
        Vue.set(state.groups, groupData.slug, groupData.status);
      } else {
        state.groups[groupData.slug] = groupData.status;
      }
    },
    setSelectedEvent(state, event) {
      state.event = event;
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
    activateAllEvents(state) {
      for (let event in state.eventTypes) {
        state.eventTypes[event] = true;
      }
    },
    activateAllGroups(state) {
      // See "work around" note above
      if (Object.keys(state.groups).length === 0)
        state.activateAllGroupsWhenLoaded = true;
      for (let group in state.groups) {
        state.groups[group] = true;
      }
    },
  },
  getters: {
    getGroups(state) {
      return state.groups;
    },
    getActiveGroups(state) {
      // TODO: this is done for every event. Come up with a better soluton.
      return Object.keys(state.groups).filter(group => state.groups[group])
    },
    getGroup: (state) => (slug) => {
      return state.groups[slug]
    },
    getGroupName: (state) => (slug) => {
      return state.groups[slug].name
    },
    getSelectedEvent(state) {
      return state.event;
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
      return Object.keys(state.eventTypes).filter(event => state.eventTypes[event])
    },
    getEventStatus: (state) => (name) => {
      return state.eventTypes[name]
    },
    getGroupsByRegion(state) {
      return state.groupsByRegion;
    }
  },
});
export default store

