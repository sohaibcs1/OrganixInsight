<template>
  <div class="q-pa-md">
    <div class="text-h6 text-center text-black bg-grey-6">Analytics</div>

    <div class="q-mt-sm">
    <q-option-group
      :options="options"
      type="checkbox"
      v-model="group"
      class="text-black"
    />
  </div>
  <div>Selected: {{ group }}</div>
  <div class="text-center">
  <q-btn label="Analyse" class="q-mt-sm text-black"  /></div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    return {
      group: ref([]),
      options: [
        { label: 'Morphometric assay', value: 'Morphometric assay' },
        { label: 'Viability assay', value: 'Viability assay'},
        { label: 'Polarity assay', value: 'Polarity assay'},
        { label: 'Phenotypic classification assay', value: 'Phenotypic classification assay', color: 'red' },
        { label: '3D Viewer', value: '3D Viewer', color: 'green' }
      ]
    }
  }
}
</script>
