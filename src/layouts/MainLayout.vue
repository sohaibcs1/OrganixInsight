<style>
.q-header .q-tab__content {
  min-width: 20px !important;
}
</style>
<template>
  <q-layout view="hHr lpR fFf">
    <q-header v-if="auth" elevated class="bg-black text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <!-- <router-link class="text-black " :style="{textDecoration: 'none', fontSize: '20px' }" to="/"
            ><q-icon name="travel_explore" size="30px"/>Zambeel</router-link> -->
            <router-link class="text-white " :style="{textDecoration: 'none', fontSize: '20px' }" to="/"
            ><q-icon name="travel_explore" size="30px"/>3D OrganixInsight</router-link>
        </q-toolbar-title>
        <q-tabs inline-label align="center">
          <!-- <q-route-tab to="/home" label="Home" /> -->
          <!-- <q-btn-dropdown label="Tools" flat>
            <q-list>
              <q-item>
                <q-btn flat label="Settings" @click="isSettingsOpen = !isSettingsOpen" :style="{width: '100%'}" />
              </q-item>
            </q-list>
          </q-btn-dropdown> -->
          <q-tab label="Logout" icon="logout" @click="logout()" v-if="auth" />
        </q-tabs>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
      <Settings :isSettingsOpen="isSettingsOpen" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { STORAGE_TOKEN } from "src/constants";
import event from "../utils/event";
import Settings from '../components/SettingsDialog';

export default {
  name: "MainLayout",
  components: {
    Settings,
  },
  data: () => ({
    auth: false,
    isSettingsOpen: false
  }),
  watch: {
    search(val) {
      event.emit("search", val);
    },
    $route() {
      this.auth = localStorage.getItem(STORAGE_TOKEN) ? true : false;
    },
  },
  methods: {
    logout() {
      localStorage.removeItem(STORAGE_TOKEN);
      this.$router.push("/login");
    }
  },
  mounted() {
    this.auth = localStorage.getItem(STORAGE_TOKEN) ? true : false;
    event.on('summarySelection', itemsLength => {
      this.summarySelectedItems = itemsLength
    });
  },
};
</script>
