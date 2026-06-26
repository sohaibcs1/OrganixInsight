<template>
  <div>
    <q-splitter
      v-model="splitterModel"
    >
    <!-- {{random_id}} -->

      <template v-slot:before>
        <div class="q-pa-md">
          <q-tree
            :nodes="simple"
            node-key="label"
            selected-color="primary"
            v-model:selected="selected"
            default-expand-all
          />
        </div>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="selected"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="Analysis">
            <!-- <div class="text-h4 q-mb-md">Select Option</div> -->

          </q-tab-panel>

          <q-tab-panel name="Cell Count/Positive Cells">
           <cellcount :random_id="random_id"></cellcount>
          </q-tab-panel>

          <q-tab-panel name="Heatmap">
            <div class="text-h4 q-mb-md">Working...</div>

          </q-tab-panel>


            <q-tab-panel name="Consensus Clustering">
           <ccClustring_list :random_id="random_id"></ccClustring_list>



          </q-tab-panel>

        </q-tab-panels>
      </template>
    </q-splitter>
  </div>
</template>

<script>
import { ref } from 'vue'
import cellcount from "src/components/user/cell_count_list.vue";
import ccClustring_list from "src/components/user/ccClustring_list.vue";


export default {
  components: { cellcount,ccClustring_list},

     props: {
    random_id: {
      type: String,
      required: true,
    }},


  setup () {
    return {
      splitterModel: ref(30),
      selected: ref('Food'),

      simple: [
        {
          label: 'Analysis',
          children: [
            {
              label: 'Cell Count/Positive Cells',
              icon: 'sample'
            },
            {
              label: 'Consensus Clustering',
              icon: 'list'
            },


          ]
        }
      ]
    }
  }
}
</script>
