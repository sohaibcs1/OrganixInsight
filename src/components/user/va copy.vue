<template>
  <div class="q-pa-md">
    <q-stepper v-model="step" vertical done-color="grey-6" active-color="primary" animated>
      <!-- Step 1: List of Studies -->
      <q-step :name="1" title="List of Studies" icon="list" :done="step > 1">
        <div>
          <q-list  padding class="rounded-borders text-center">
            <q-item
              v-for="(item, index) in data"
              :key="index"
              clickable
              v-ripple
              active-class=""
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
          <q-list  padding class="rounded-borders text-black">
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
                  :class="{'bg-grey-4': selectedSubItem[exp.random_id] === 'Factors'}"
                  clickable
                  v-ripple
                  @click="selectSubItem(exp.random_id, 'Factors'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-black-5">
                    <span><q-icon name="scatter_plot" class="q-mr-sm" />Factors</span>
                  </q-item-section>
                </q-item>

                <q-item
                  :class="{'bg-grey-4': selectedSubItem[exp.random_id] === 'Visualization'}"
                  clickable
                  v-ripple
                  @click="selectSubItem(exp.random_id, 'Visualization'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-deep-black-5">
                    <span><q-icon name="bar_chart" class="q-mr-sm" />Visualization</span>
                  </q-item-section>
                </q-item>

                <q-item
                  :class="{'bg-grey-4': selectedSubItem[exp.random_id] === 'Heatmap'}"
                  clickable
                  v-ripple
                  @click="selectSubItem(exp.random_id, 'Heatmap'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-black-6">
                    <span><q-icon name="heatmap" class="q-mr-sm" />Heatmap</span>
                  </q-item-section>
                </q-item>

                <q-item
                  :class="{'bg-grey-4': selectedSubItem[exp.random_id] === 'Upload'}"
                  clickable
                  v-ripple
                  @click="selectSubItem(exp.random_id, 'Upload'); step = 3"
                >
                  <q-item-section class="q-ml-lg text-black-5">
                    <span><q-icon name="cloud_upload" class="q-mr-sm" />Upload Data</span>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-expansion-item>
          </q-list>
        </div>
        <q-stepper-navigation>
          <q-btn @click="step = 1" color="blue-4" label="Back" />
        </q-stepper-navigation>
      </q-step>

      <!-- Step 3: Dynamic Data Display -->
      <q-step :name="3" :title="`Details for: ${selectedSubItemType}`" icon="info">
        <div v-if="selectedSubItemType === 'Factors'"></div>
        <div v-if="dynamicData && dynamicData.length">
          <q-card>
            <q-card-section>
            
              <div v-if="selectedSubItemType === 'Factors'">
                <q-card flat  class="q-mb-md text-black">
                  <studies_expList
                  :id_row="dynamicData[0].study_id" :study_name="dynamicData[0].name"
                  class="fit"
                ></studies_expList>
                </q-card>
              </div>

              <div v-else-if="selectedSubItemType === 'Visualization'">
                <visualization_list :random_id="dynamicData[0].random_id"></visualization_list>
              </div>
              <div v-else-if="selectedSubItemType === 'Heatmap'">
                
                <heatmap :random_id="dynamicData[0].random_id"></heatmap>
              </div>
              <div v-else-if="selectedSubItemType === 'Upload'">
                <!-- <q-btn
                  label="Download File"
                  icon="cloud_download"
                  @click="downloadData"
                  color="black"
                /> -->
                <fileUpload :random_id="dynamicData[0].random_id"></fileUpload>
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
        <q-stepper-navigation>
          <q-btn @click="step = 2" color="blue-4" label="Back" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </div>
</template>


<script>
import { ref, computed } from "vue";
import API from "src/api";
import studies_expList from "src/components/user/studies_expList_list";
import visualization_list from "src/components/user/visualization_list";
import heatmap from "src/components/user/heatmap_list";
import fileUpload from "src/components/user/fileUpload_list";

export default {
  components: { studies_expList ,visualization_list,heatmap,fileUpload},
  setup() {
    const step = ref(1);
    const data = ref([]);
    const experiments = ref([]);
    const selectedStudy = ref(null);
    const selectedSubItem = ref({});
    const selectedSubItemType = ref("");
    const dynamicData = ref(null);

    const fetchStudies = async () => {
      const response = await API("auth.study_details");
      data.value = response;
    };

    const fetchExperiments = async (studyId) => {
      const response = await API("auth.ExperimentDetials_id", { key: studyId });
      experiments.value = response;
    };

    const fetchDynamicData = async (randomId) => {
      const response = await API("auth.ExperimentDetials_randomid", { key: randomId });
      dynamicData.value = response; // Update the dynamic data for Step 3
    };

    const selectStudy = (item) => {
      selectedStudy.value = item;
      fetchExperiments(item.uuid);
    };

    const selectSubItem = (randomId, subItem) => {
      selectedSubItemType.value = subItem;
      fetchDynamicData(randomId);
    };

    // Filter unique experiments by `random_id`
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
      selectedSubItem,
      selectedSubItemType,
      dynamicData,
      selectStudy,
      selectSubItem,
    };
  },
};
</script>
