<template>
  <q-dialog :model-value="open">
    <q-card class="bg-white text-black q-pa-md" style="width: 500px">
      <q-card-section>
        <div class="text-h4">Settings</div>
      </q-card-section>
      <q-card-section>
        <q-input label="Summary Length" v-model="settings.summaryLength" />
      </q-card-section>
      <q-card-section>
        <q-btn class="bg-primary text-white" label="Save" @click="saveSettings()" />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
import API from 'src/api'
import { getToken } from 'src/utils/jwt'

export default {
  props: ['isSettingsOpen'],
  data: () => ({
    open: false,
    settings: {
      summaryLength: 100,
    }
  }),
  watch: {
    isSettingsOpen(val) {
      this.open = val
    }
  },
  methods: {
    saveSettings() {
      const payload = {
        token: getToken(),
        settings: { ...this.settings }
      };
      API('auth.saveSettings', payload).then(() => {
        this.$q.notify({
          color: 'positive',
          message: 'Settings saved'
        })
      })
    }
  },
  mounted() {
    API('auth.getSettings', {
      token: getToken(),
    }).then((settings) => {
    console.log("here", settings);
      if (!settings) {
        settings = {
          summaryLength: 100,
        }
      }
      this.settings = settings;
    });
  }
}
</script>