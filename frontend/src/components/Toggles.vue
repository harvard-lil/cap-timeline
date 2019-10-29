<template>
  <div class="sidebar-sticky toggles-menu">
    <!--year slider-->
    <h3>Years</h3>

    <hr/>
    <!--Groups-->
    <h3>Groups</h3>
    <ul class="group-types list-group">
      <li class="list-item" v-for="(status, group) in groups" v-bind="{group: status}">
        <selectable-group :name="group" :translated="groupTranslation[group]">
        </selectable-group>
      </li>
    </ul>
    <hr/>
    <!--Event types-->
    <h3>Event Types</h3>
    <ul class="event-types list-group">
      <li class="list-item" v-for="(status, eventType) in eventTypes" v-bind="{eventType: status}">
        <selectable-event :name="eventType">
        </selectable-event>
      </li>
    </ul>
    <hr/>
    <!--Themes ? -->

  </div>
</template>

<script>
  import SelectableGroup from './SelectableGroup';
  import SelectableEvent from './SelectableEvent';
  import store from '../store';

  export default {
    name: "toggles",
    components: {SelectableGroup, SelectableEvent},
    data() {
      return {
        showingEvent: false,
      }
    },
    computed: {
      eventTypes() {
        return store.getters.getEventTypes;
      },
      eventTranslation() {
        return store.getters.getEventTranslation;
      },
      groups() {
        return store.getters.getGroups;
      },
      groupTranslation() {
        return store.getters.getGroupTranslation;
      }
    }
  }
</script>
