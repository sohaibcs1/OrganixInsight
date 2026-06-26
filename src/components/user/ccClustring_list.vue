<template>
  <div class="q-pa-md column items-center">
    <q-img
      v-if="imageUrl"
      :src="fullUrl"
      fit="contain"
      class="q-ma-md"
      style="max-width: 100%; border-radius: 1px;"
    />
 <div
  v-else
  class="q-pa-xl column items-center justify-center"
  style="min-height: 40vh;"
>
  <q-spinner-gears size="64px" color="primary" />

  <div class="text-h4 text-weight-bold text-primary q-mt-md">
     Plotting in progress…
  </div>

  <div class="text-body2 text-grey-7 q-mt-xs">
    Preparing the consensus Plot — please wait.
  </div>

  <q-linear-progress
    indeterminate
    rounded
    color="primary"
    class="q-mt-md"
    style="width: 360px;"
  />
</div>



  </div>
</template>

<script>
import API from 'src/api'

export default {
  props: {
    random_id: { type: String, required: true },
  },

  data() {
    return {
      imageUrl: '', // e.g. "consensus_<rid>_<timestamp>.jpg"
      ts: Date.now(), // cache-buster to force reload
    }
  },

  computed: {
    fullUrl() {
      if (!this.imageUrl) return ''
      const base =
        window.location.hostname === 'localhost'
          ? 'http://localhost:6085' // Flask backend port
          : `http://${window.location.hostname}:6085`
      return `${base}/static/results/${this.imageUrl}?t=${this.ts}`
    },
  },

  methods: {
    async ccfun() {
      try {
        const id = this.random_id
        if (!id) return
        const res = await API('home.getCc', { random_id: id })
        if (res && res.status === 'ok' && res.filename) {
          this.imageUrl = res.filename
          this.ts = Date.now() // refresh even if filename reused
        } else {
          this.imageUrl = ''
        }
      } catch {
        this.imageUrl = ''
      }
    },
  },

  mounted() {
    // Auto-load when mounted (no button)
    if (this.random_id) this.ccfun()
  },

  watch: {
    // Re-run if random_id changes
    random_id(newVal, oldVal) {
      if (newVal && newVal !== oldVal) this.ccfun()
    },
  },
}
</script>
