<template>
  <div class="q-pa-md bg-yellow">
    <q-stepper
      v-model="step"
      vertical
      done-color="grey-6"
      active-color="primary"
      animated
    >
      <!-- Step 1: Experiments List -->
      <q-step
        :name="1"
        :title="`Experiments for Study: ${study_name || ''}`"
        icon="science"
      >
        <div>
          <q-list padding class="rounded-borders text-black">
            <q-expansion-item
              v-for="(exp, index) in uniqueExperiments"
              :key="exp.random_id"
              expand-separator
              dense
              :default-opened="index === 0"
              header-class="bg-grey-3"
              class="q-mb-sm rounded-borders shadow-1"
              style="max-width: 650px"
            >
              <!-- Custom header: experiment title + link-like actions + delete -->
              <template v-slot:header>
                <div
                  class="row items-center justify-between q-px-sm q-py-xs"
                  style="width: 100%;"
                >
                  <!-- Left: experiment name + link row -->
                  <div class="column">
                    <div class="text-subtitle2 text-weight-medium">
                      {{ `${index + 1}. ${exp.experiment_name}` }}
                    </div>

                    <!-- Link-style buttons -->
                    <div class="row q-gutter-xs q-mt-xs">

                      <!-- Factors -->
                      <q-btn
                        dense
                        flat
                        no-caps
                        icon="scatter_plot"
                        label="Factors"
                        class="text-primary text-caption"
                        @click.stop="
                          selectSubItem(index, 'Factors');
                          step = 2;
                        "
                      />

                      <!-- Visualization -->
                      <q-btn
                        dense
                        flat
                        no-caps
                        icon="bar_chart"
                        label="Visualization"
                        class="text-primary text-caption"
                        @click.stop="
                          selectSubItem(index, 'Visualization');
                          step = 2;
                        "
                      />

                      <!-- Upload -->
                      <q-btn
                        dense
                        flat
                        no-caps
                        icon="cloud_upload"
                        label="Upload"
                        class="text-primary text-caption"
                        @click.stop="
                          selectSubItem(index, 'Upload');
                          step = 2;
                        "
                      />

                      <!-- Analysis (2D + 3D 10x) -->
                      <q-btn
                        v-if="
                          exp.ex_type === '2D Simple Experiment' ||
                          exp.ex_type === '2D Experiment' ||
                          (exp.ex_type === '3D Experiment' &&
                            exp.magnification === '10x') ||
                          (exp.ex_type === '3D Simple Experiment' &&
                            exp.magnification === '10x')
                        "
                        dense
                        flat
                        no-caps
                        icon="analytics"
                        label="Analysis"
                        class="text-primary text-caption"
                        @click.stop="
                          selectSubItem(index, 'analysis');
                          step = 2;
                        "
                      />

                      <!-- Analysis 3D (3D morphogenesis / 3D Experiment @ 40x or null) -->
                      <q-btn
                        v-if="
                          (exp.ex_type === '3D morphogenesis' ||
                            exp.ex_type === '3D Experiment') &&
                          (exp.magnification === '40x' ||
                            exp.magnification === null)
                        "
                        dense
                        flat
                        no-caps
                        icon="3d_rotation"
                        label="Analysis 3D"
                        class="text-primary text-caption"
                        @click.stop="
                          selectSubItem(index, 'analysis3d');
                          step = 2;
                        "
                      />
                    </div>
                  </div>

                  <!-- Right: delete button -->
                  <q-btn
                    dense
                    flat
                    round
                    icon="delete"
                    color="red-7"
                    @click.stop="deleteExperimnet(exp.random_id)"
                    aria-label="Delete Experiment"
                  />
                </div>
              </template>

              <!-- Optional body hint -->
              <div class="q-pa-sm text-grey-7 text-caption">
                Select one of the links above to open details.
              </div>
            </q-expansion-item>
          </q-list>
        </div>
      </q-step>

      <!-- Step 2: Dynamic Data Display -->
      <q-step
        :name="2"
        :title="`Details for: ${selectedSubItemType.type || ''}`"
        icon="info"
      >
        <q-stepper-navigation class="q-mb-xs">
          <q-btn
            @click="step = 1"
            icon="arrow_back"
            color="red"
            label="Back"
          />
        </q-stepper-navigation>

        <div v-if="isDataLoaded && selectedSubItemType.index !== null">
          <q-card>
            <q-card-section>
              <!-- Factors -->
              <div v-if="selectedSubItemType.type === 'Factors'">
                <studies_expList
                  :id_row="currentRandomId"
                  :study_name="study_name"
                  class="fit"
                />
              </div>

              <!-- Visualization -->
              <div v-else-if="selectedSubItemType.type === 'Visualization'">
                <visualization_list
                  :random_id="currentRandomId"
                />
              </div>

              <!-- Upload -->
              <div v-else-if="selectedSubItemType.type === 'Upload'">
                <fileUpload
                  :random_id="currentRandomId"
                />
              </div>

              <!-- Analysis (2D / 3D 10x) -->
              <div v-else-if="selectedSubItemType.type === 'analysis'">
                <analysis
                  :random_id="currentRandomId"
                />
              </div>

              <!-- Analysis 3D -->
              <div v-else-if="selectedSubItemType.type === 'analysis3d'">
                <analysis3d
                  :random_id="currentRandomId"
                />
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
import { ref, computed, onMounted } from "vue";
import API from "src/api";

import studies_expList from "src/components/user/studies_expList_list";
import visualization_list from "src/components/user/visualization_list";
import fileUpload from "src/components/user/fileUpload_list";
import analysis from "src/components/user/analysis_vis_list.vue";
import analysis3d from "src/components/user/analysis_vis_3d_list.vue";

export default {
  name: "StudyExperimentsStepperSingle",
  props: ["id_row", "study_name"],
  components: {
    studies_expList,
    visualization_list,
    fileUpload,
    analysis,
    analysis3d,
  },
  methods: {
    async deleteExperimnet(id) {
      try {
        console.log(id, "id being passed");

        const userInput = prompt("Type 'DELETE' to confirm deletion:");
        if (userInput === "DELETE") {
          console.log("User confirmed deletion, proceeding...");

          const response = await API("auth.deleteExperimentRandomid", { id });

          if (response.success) {
            alert(
              `Deletion successful. Deleted ${response.deletedCount} record(s).`
            );
            // Optionally refresh experiment list here if needed
          } else {
            alert(`Failed to delete. ${response.message}`);
            console.error("Backend response:", response);
          }
        } else {
          alert("Deletion canceled. Please type 'DELETE' to confirm.");
        }
      } catch (error) {
        console.error("Error during deletion:", error);
        alert("An error occurred while trying to delete the record.");
      }
    },
  },
  setup(props) {
    const step = ref(1);
    const experiments = ref([]);
    const selectedSubItemType = ref({ type: "", index: null });
    const dynamicDataMap = ref({});
    const isDataLoaded = ref(false);

    const fetchExperiments = async () => {
      if (!props.id_row) {
        console.error("id_row is not provided or invalid");
        return;
      }
      try {
        const response = await API("auth.ExperimentDetials_id", {
          key: props.id_row,
        });
        experiments.value = response;
      } catch (error) {
        console.error("Failed to fetch experiments:", error);
      }
    };

    const fetchDynamicData = async (randomId) => {
      isDataLoaded.value = false;
      if (!dynamicDataMap.value[randomId]) {
        try {
          const response = await API("auth.ExperimentDetials_randomid", {
            key: randomId,
          });
          dynamicDataMap.value[randomId] = response;
          console.log("Dynamic Data Map:", dynamicDataMap.value);
        } catch (error) {
          console.error("Failed to fetch dynamic data:", error);
        }
      }
      isDataLoaded.value = true;
    };

    const uniqueExperiments = computed(() => {
      const seen = new Set();
      return experiments.value.filter((exp) => {
        if (seen.has(exp.random_id)) return false;
        seen.add(exp.random_id);
        return true;
      });
    });

    const selectSubItem = (index, subItem) => {
      selectedSubItemType.value = { type: subItem, index };
      const exp = uniqueExperiments.value[index];
      if (exp && exp.random_id) {
        fetchDynamicData(exp.random_id);
      }
    };

    const currentRandomId = computed(() => {
      const idx = selectedSubItemType.value.index;
      const exp = uniqueExperiments.value[idx];
      if (!exp) return null;
      const arr = dynamicDataMap.value[exp.random_id];
      return arr?.[0]?.random_id || null;
    });

    onMounted(fetchExperiments);

    return {
      step,
      experiments,
      uniqueExperiments,
      selectedSubItemType,
      dynamicDataMap,
      isDataLoaded,
      selectSubItem,
      currentRandomId,
    };
  },
};
</script>
