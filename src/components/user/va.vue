<template>
  <div class="q-pa-md bg-primary">
    <q-stepper v-model="step" vertical done-color="grey-6" active-color="primary" animated>
      <!-- Step 1: List of Studies -->
      <q-step :name="1" title="List of Studies" icon="list" :done="step > 1">
        <div>
          <q-list padding class="rounded-borders text-center">
            <q-item
              v-for="(item, index) in data"
              :key="index"
              clickable
              v-ripple
              :class="{'bg-grey-4': selectedStudy === item}"
              @click="selectStudy(item); step = 2"
              dense
            >
              <q-badge>
                <q-item-section class="text-white">
                  <q-badge> {{ index + 1 }}. {{ item.name }}</q-badge>
                </q-item-section>
              </q-badge>
            </q-item>
          </q-list>
        </div>
      </q-step>

      <!-- Step 2: Experiments List -->
      <q-step :name="2" :title="`Experiments Under Study: ${selectedStudy?.name || ''}`" icon="science">
        <div>
          <q-list padding class="rounded-borders text-black">
            <q-expansion-item
              v-for="(exp, index) in uniqueExperiments"
              :key="exp.random_id"
              :label="`${index + 1}. ${exp.experiment_name}`"
              text-size="11px"
              expand-separator
              dense
              :default-opened="index === 0"
              header-class="text-subtitle2 bg-grey-4"
              style="max-width: 550px"
            >
              <!-- Sub-tree structure -->
              <q-list dense>
                <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'Factors' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'Factors'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-black-5">
                    <span><q-icon name="scatter_plot" class="q-mr-sm" />Factors</span>
                  </q-item-section>
                </q-item>

                <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'Visualization' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'Visualization'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-deep-black-5">
                    <span><q-icon name="bar_chart" class="q-mr-sm" />Visualization</span>
                  </q-item-section>
                </q-item>

                <!-- <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'Heatmap' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'Heatmap'); step = 3"
                  v-if="(exp.ex_type === '3D morphogenesis' || exp.ex_type === '3D Experiment') && (exp.magnification === '40x'|| exp.magnification === null)"
                >
                  <q-item-section class="q-ml-lg text-black-6" >
                    <span><q-icon name="heatmap" class="q-mr-sm" />Heatmap</span>
                  </q-item-section>
                </q-item> -->

                <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'Upload' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'Upload'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-black-5">
                    <span><q-icon name="cloud_upload" class="q-mr-sm" />Upload Data</span>
                  </q-item-section>
                </q-item>


                <!-- <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'CellCount' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'CellCount'); step = 3"
                  v-if="exp.ex_type=='2D Simple Experiment' || exp.ex_type=='2D Experiment' ||
                       (exp.ex_type === '3D Experiment' && exp.magnification === '10x')|| (exp.ex_type === '3D Simple Experiment' && exp.magnification === '10x')"
                >
                  <q-item-section class="q-ml-lg text-black-6" >
                    <span><q-icon name="heatmap" class="q-mr-sm" />Cell Count / Protiene Measuments</span>
                  </q-item-section>
                </q-item> -->


                      <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'analysis' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'analysis'); step = 3"
                  v-if="exp.ex_type=='2D Simple Experiment' || exp.ex_type=='2D Experiment' ||
                       (exp.ex_type === '3D Experiment' && exp.magnification === '10x')|| (exp.ex_type === '3D Simple Experiment' && exp.magnification === '10x')"
                >
                  <q-item-section class="q-ml-lg text-black-6" >
                    <span><q-icon name="heatmap" class="q-mr-sm" />Analysis</span>
                  </q-item-section>
                </q-item>


                   <q-item
                  :class="{'bg-grey-4': selectedSubItemType.type === 'analysis3d' && selectedSubItemType.index === index}"
                  clickable
                  v-ripple
                  @click="selectSubItem(index, 'analysis3d'); step = 3"
                  v-if="(exp.ex_type === '3D morphogenesis' || exp.ex_type === '3D Experiment') && (exp.magnification === '40x'|| exp.magnification === null)"
                >
                  <q-item-section class="q-ml-lg text-black-6" >
                    <span><q-icon name="heatmap" class="q-mr-sm" />Analysis</span>
                  </q-item-section>
                </q-item>


              </q-list>
            </q-expansion-item>
          </q-list>
        </div>
        <q-stepper-navigation>
          <q-btn @click="step = 1" icon="arrow_back" color="red" label="Back" />
        </q-stepper-navigation>
      </q-step>

      <!-- Step 3: Dynamic Data Display -->
      <q-step :name="3" :title="`Details for: ${selectedSubItemType.type}`" icon="info">

        <q-stepper-navigation class="q-mb-xs">
          <q-btn @click="step = 2" icon="arrow_back" color="red" label="Back"/>
        </q-stepper-navigation>

        <div v-if="isDataLoaded && selectedSubItemType.index !== null">
          <q-card>
            <q-card-section>
              <div v-if="selectedSubItemType.type === 'Factors'">
                <studies_expList
                  :id_row="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                  :study_name="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.name"
                  class="fit"
                ></studies_expList>
              </div>
              <div v-else-if="selectedSubItemType.type === 'Visualization'">
                <visualization_list
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></visualization_list>
              </div>
              <!-- <div v-else-if="selectedSubItemType.type === 'Heatmap'">
                <heatmap
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></heatmap>
              </div> -->

               <div v-else-if="selectedSubItemType.type === 'analysis3d'">
                <analysis3d
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></analysis3d>
              </div>

              <div v-else-if="selectedSubItemType.type === 'Upload'">
                <fileUpload
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></fileUpload>
              </div>

              <!-- <div v-else-if="selectedSubItemType.type === 'CellCount'">
                <cellcount
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></cellcount>
              </div> -->

               <div v-else-if="selectedSubItemType.type === 'analysis'">
                <analysis
                  :random_id="dynamicDataMap[uniqueExperiments[selectedSubItemType.index]?.random_id]?.[0]?.random_id"
                ></analysis>
              </div>

              <div v-else>
                <p>Unsupported data type.</p>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div v-else>
          <p class="text-center text-grey">No data available.</p>
        </div>

      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import API from "src/api";
import studies_expList from "src/components/user/studies_expList_list";
import visualization_list from "src/components/user/visualization_list";
// import heatmap from "src/components/user/heatmap_list";
// import cellcount from "src/components/user/cell_count_list.vue";
import analysis from "src/components/user/analysis_vis_list.vue";
import analysis3d from "src/components/user/analysis_vis_3d_list.vue";

import fileUpload from "src/components/user/fileUpload_list";

export default {
  components: { studies_expList, visualization_list, fileUpload ,analysis,analysis3d},
  setup() {
    const step = ref(1);
    const data = ref([]);
    const experiments = ref([]);
    const selectedStudy = ref(null);
    const selectedSubItemType = ref({ type: "", index: null });
    const dynamicDataMap = ref({});
    const isDataLoaded = ref(false);

    // const fetchStudies = async () => {
    //   const response = await API("auth.study_details");
    //   data.value = response;
    // };
    const fetchStudies = async () => {
  const response = await API("auth.study_details", {
    notes: localStorage.getItem("username")
  });
  data.value = response;
};

    const fetchExperiments = async (studyId) => {
      const response = await API("auth.ExperimentDetials_id", { key: studyId });
      experiments.value = response;
    };

    const fetchDynamicData = async (randomId) => {
      isDataLoaded.value = false;
      if (!dynamicDataMap.value[randomId]) {
        const response = await API("auth.ExperimentDetials_randomid", { key: randomId });
        dynamicDataMap.value[randomId] = response;
        console.log("Dynamic Data Map:", dynamicDataMap.value);

      }
      isDataLoaded.value = true;
    };

    const selectStudy = (item) => {
      selectedStudy.value = item;
      fetchExperiments(item.uuid);
    };

    const selectSubItem = (index, subItem) => {
      selectedSubItemType.value = { type: subItem, index };
      fetchDynamicData(uniqueExperiments.value[index]?.random_id);
    };

    const uniqueExperiments = computed(() => {
      const seen = new Set();
      return experiments.value.filter((exp) => {
        if (seen.has(exp.random_id)) return false;
        seen.add(exp.random_id);
        return true;
      });
    });

    fetchStudies();

    return {
      step,
      data,
      experiments,
      uniqueExperiments,
      selectedStudy,
      selectedSubItemType,
      dynamicDataMap,
      isDataLoaded,
      selectStudy,
      selectSubItem,
    };
  },
};
</script>
