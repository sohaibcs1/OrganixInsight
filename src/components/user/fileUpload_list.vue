<template>

  <div>
    <!-- {{random_id}} -->
    <div class="q-pa-sm q-gutter-sm" v-if="uploadactivity">

      <div class="q-ml-sm  q-gutter-md bg-grey-4 text-black">
        <div v-if="data.length > 0">
          <p><strong>Experiment Name:</strong> {{ tableTitles.experiment_name || 'N/A' }}</p>
          <p><strong>Experiment Date:</strong> {{ tableTitles.experiment_design_date || 'N/A' }}</p>
          <p><strong>Experiment Type:</strong> {{ tableTitles.ex_type || 'N/A' }}</p>
          <p><strong>Type:</strong> {{ tableTitles.type || 'N/A' }}</p>
          <p><strong>CoCulture:</strong> {{ tableTitles.coCulture || 'N/A' }}</p>
          <p><strong>Costain:</strong> {{ tableTitles.costain || 'N/A' }}</p>
          <p><strong>Counterstain:</strong> {{ tableTitles.counterstain || 'N/A' }}</p>
          <p><strong>Virus:</strong> {{ tableTitles.virus || 'N/A' }}</p>
          <p><strong>Primary Antibody:</strong> {{ tableTitles.primary || 'N/A' }}</p>
          <p><strong>Secondary Antibody:</strong> {{ tableTitles.secondary || 'N/A' }}</p>
          <p><strong>Phase Info:</strong> {{ tableTitles.phase_info || 'N/A' }}</p>
          <!-- <p><strong>Magnification:</strong> {{ tableTitles.magnification || 'N/A' }}</p> -->
          <!-- <p><strong>Treatment Group:</strong> {{ tableTitles.treatment_group || 'N/A' }}</p> -->

          <p><strong>em exposure:</strong> {{ tableTitles.em_exposure || 'N/A' }}</p>
          <p><strong>unit_em_exposure:</strong> {{ tableTitles.unit_em_exposure || 'N/A' }}</p>
          <p><strong>voltage:</strong> {{ tableTitles.voltage || 'N/A' }}</p>
          <p><strong>pulse width:</strong> {{ tableTitles.pulse_width || 'N/A' }}</p>
          <p><strong>no.of pluses:</strong> {{ tableTitles.no_of_pluses || 'N/A' }}</p>
          <p><strong>time between pulses:</strong> {{ tableTitles.time_bt_pulses || 'N/A' }}</p>
          <p><strong>capacitance:</strong> {{ tableTitles.capacitance || 'N/A' }}</p>
        </div>
      </div>

<!-- <div>jjjjj</div> -->
       <div class="text-center" v-if="modelstudyid">
      <q-select
        filled
        v-model="modelexp"
        use-input
        input-debounce="0"
        label="Select Experiment"
        :options="optionsexp"
        @filter="filterFnexp"

        behavior="dialog"
      >


        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              No results
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      <q-btn label="Get Experiments" class="q-mt-sm text-black" @click="getExp" />
    </div>
      <!-- <q-btn color="purple" label="Download CSV" @click="exportTable" /> -->
       <div class="q-pa-md bg-grey-3 text-dark text-center">
        <q-checkbox  v-model="upload" label="Plate upload" color="primary" class="q-mr-lg"/>
                <!-- {{tableTitles}} -->

        <q-btn dense color="green" label="Plate upload"   v-if="upload && hasAnyWells"

        @click="show_upload_dialog_bulk=true"
/>
       </div>


<!-- {{columns}} -->
      <q-table title="Treats" :rows="filteredRows" :columns="filteredColumns" :dense="$q.screen.lt.md" row-key="uuid" max-width="100%"
         table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
        class="q-table--dense compact-table" :pagination="pagination">
        <template v-slot:top>

          <div class="q-pa-sm q-gutter-sm">


            <q-dialog v-model="show_dialog">
              <q-card  text-center>
                <q-card-section>

                  <div class="text-h6 text-center bg-grey-5">Biospecimen {{ id_row }} Attributes</div>
                </q-card-section>

                <q-card-section>

                  <div class="row ">
                    <q-input v-model="editedItem.uuid" label="Id:" hidden />

                        <q-select class="fit" outlined v-model="editedItem.immortal" input-debounce="0"  @filter="filterImmortal" use-input multiple :options="optionsImmortal"   counter max-values="1"
                      hint="Max 1 selection" label="Immortal:" stack-label dense  />
                        <q-space />
                        <q-select class="fit"  outlined v-model="editedItem.source" input-debounce="0"  @filter="filterSource" use-input multiple :options="optionsSource"   counter max-values="1"
                      hint="Max 1 selection" label="Source:" stack-label dense  /><q-space />

                      <q-select class="fit"  outlined v-model="editedItem.organism" input-debounce="0"  @filter="filterOrganism" use-input multiple :options="optionsOrganism"   counter max-values="1"
                      hint="Max 1 selection" label="Organism:" stack-label dense  /><q-space />

                      <q-select class="fit"  outlined v-model="editedItem.subtype" input-debounce="0"  @filter="filterSubtype" use-input multiple :options="optionsSubtype"   counter max-values="1"
                      hint="Max 1 selection" label="Subtype:" stack-label dense  /><q-space />

                      <q-select  class="fit q-mb-sm"
                      outlined v-model="editedItem.passage" input-debounce="0"  use-chips @filter="filterPassage" use-input multiple :options="optionsPassage" label="Passage:" stack-label dense create /><q-space />

                      <q-input class="fit "  outlined  v-model="editedItem.transfected"  stack-label
                      :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="transfected" /><q-space />

                      <q-input  class="fit"  outlined  v-model="editedItem.patient_id"  stack-label
                      :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Patient Id"/><q-space />

                      <q-input  class="fit" outlined  v-model="editedItem.distribution_id"  stack-label
                      :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Distribution Id"/><q-space />

                      <q-input class="fit"  outlined  v-model="editedItem.hyperlink"  stack-label
                      :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Hyperlink"/><q-space />
                  </div>
                </q-card-section>


              </q-card>
            </q-dialog>
          </div>

        </template>


        <!-- <template v-slot:body-cell-mergedHarvestTime="props">
      <q-td :props="props" >
        {{ mergedHarvestTime[props.rowIndex] }}
      </q-td>
    </template> -->
    <template v-slot:body-cell-microscope="props">
      <q-td :props="props" >
        {{ microscope[props.rowIndex] }}
      </q-td>
    </template>

    <template v-slot:body-cell-well_number="props">
      <q-td :props="props">
        <q-select
        filled
        v-model="props.row.well_number"
        :options="filteredWellOptions"
        use-chips
        use-input
        multiple
        dense
        stack-label
        @filter="filterWellOptions"
        @update:model-value="val => updateWellAndUI(props.row.uuid, val)"
        />
      </q-td>
    </template>

        <template v-slot:body-cell-actions="props">
        <q-td :props="props" >

          <q-btn
          :disable="upload"
          dense
            v-model="realtimecheck"
            size="10px"
            icon="cloud_upload"
            :label="getInitialLabel(props.row.uuid)"
            :color="getInitialColor(props.row.uuid)"
            @click="passValues(true, props.row.uuid, props.row.study_id, props.row.phase_info, props.row.counterstain, props.row.ex_type,props.row.magnification,props.row.random_id)"

          ></q-btn>
        </q-td>
    </template>

      </q-table>



    </div>


    <q-dialog v-model="show_upload_dialog" >
        <q-card >
          <!-- {{ prop_st_id }} {{pro_phase_info}} {{pro_ex_type}} -->
          <q-card-section align="center" >
            <div class="row text-center">

              <uploadbtn :passUuid="prop_uuid"  :passStudy_id="prop_st_id" :pro_phase_info="pro_phase_info" :pro_counterstain="pro_counterstain" :passEx_type="pro_ex_type" :pro_magnification="pro_magnification" :pro_random_id="pro_random_id" @close-dialog="show_upload_dialog = false" ></uploadbtn>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>


       <q-dialog v-model="show_upload_dialog_bulk" >
        <q-card >
          <q-card-section align="center" >
            <div class="row text-center">

              <uploadbtnb :passUuid="tableTitles.random_id" @close-dialog="show_upload_dialog_bulk = false" ></uploadbtnb>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

  </div>

</template>

<script>
import { ref, reactive, watch,onMounted } from 'vue';

import API from 'src/api'
import { exportFile, useQuasar } from 'quasar'
import uploadbtn from 'src/components/user/uploadbtn_list';
import visulizesingle from 'src/components/user/visulizeSingle';

import uploadbtnb from 'src/components/user/uploadbtnbulk_list';


var stringOptions = [
  'Study 1', 'Study 2', 'Study 3', 'Study 4', 'Study 5'
]
const stringOptionswell= ['C1','C2']

var stringOptionsexp = [
  'Experiment 1', 'Experiment 2', 'Experiment 3', 'Experiment 4', 'Experiment 5'
]

const columns = [
  {
    name: 'desc',
    required: true,
    label: 'Experiment ID',
    align: 'center',
    field: row => row.uuid,
    format: val => `${val}`,
    sortable: true
  },

  { name: 'one', align: 'center', label: 'study ID', field: 'study_id', sortable: true },
  { name: 'two', align: 'center', label: 'experiment_name', field: 'experiment_name', sortable: true },
  { name: 'three', align: 'center', label: 'experiment_design_date', field: 'experiment_design_date', sortable: true },

  { name: 'three1', align: 'center', label: 'name', field: 'name', sortable: true },
  { name: 'four', align: 'center', label: 'primary', field: 'primary', sortable: true },
  { name: 'five', align: 'center', label: 'secondary', field: 'secondary', sortable: true },
  { name: 'six', align: 'center', label: 'treatment_group', field: 'treatment_group', sortable: true },

  { name: "actions", align: 'center', label: "Actions", field: "actions" }

]

var listLocation=[]
var listRoute=[]
const stringOptionsOrganism= ['mouse','human']
const stringOptionsSubtype= ['N/A','TNA','TNB','LA','LB','BCRA1','BRCA2','H']
const stringOptionsSource= ['mammary','pancreatic']
const stringOptionsImmortal=  ['Yes', 'No' ]
const stringOptionsPassage=[]

for (let i = 1; i <= 100; i++) {
stringOptionsPassage.push(i.toString());
}

var key

export default {


  props: {
  exp_pass_uploadImg:String,
  random_id: {
      type: String,
      required: true,
    }
  },

  setup(props) {
    // const options_well= ['C1', 'C2'];
    // const options_well = ref(stringOptionswell.map(w => ({ label: w, value: w })));
    const options_well = ref(
    Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i))
      .flatMap(letter => Array.from({ length: 11 }, (_, j) => `${letter}${j + 1}`))
  );

  const filteredWellOptions = ref([...options_well.value]);


    function filterWellOptions(val, update) {
    if (val === '') {
      update(() => {
        filteredWellOptions.value = [...options_well.value];
      });
      return;
    }

    const needle = val.toLowerCase();
    update(() => {
      filteredWellOptions.value = options_well.value.filter(opt =>
        opt.toLowerCase().includes(needle)
      );
    });
  }


    const options = ref(stringOptions)
    const optionsexp = ref(stringOptionsexp)

    const $q = useQuasar()
    const optionsOrganism= ref(stringOptionsOrganism)
    const optionsSource=ref(stringOptionsSource)
    const optionsImmortal=ref(stringOptionsImmortal)
    const optionsPassage= ref(stringOptionsPassage)
    const optionsSubtype= ref(stringOptionsOrganism)
    const matchStatus = reactive({}); // Track the status per UUID
    const experiments1 = ref([]);


    return {
      pagination: {
      rowsPerPage: 200 // current rows per page being displayed
    },
    upload: ref(false ),  // checkbox model
    options_well,
    filteredWellOptions,
    filterWellOptions,
     modelstudyid:ref(null),
     realtimecheck: null,
     matchStatus,
     experiments1,
    //  matchStatus:{},
    //Search Study Start
      model: ref(null),
      modelexp: ref(null),
      stringOptions,
      stringOptionsexp,
      options,
      optionsexp,
      tableTitles: {}, // To store extracted titles

      filterFnexp (val, update) {
        if (val === '') {
          update(() => {
            optionsexp.value = stringOptionsexp
          })
          return
        }

        update(() => {
          const needle = val.toLowerCase()
          optionsexp.value = stringOptionsexp.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },

      filterFn (val, update) {
        if (val === '') {
          update(() => {
            options.value = stringOptions
          })
          return
        }

        update(() => {
          const needle = val.toLowerCase()
          options.value = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },

       //Search Study End
    uploadactivity:ref(true),
    isMatched: false,
    prop_uuid:ref(null),
    prop_st_id:ref(null),
    pro_magnification:ref(null),
    pro_random_id:ref(null),
    pro_phase_info:ref(null),
    pro_counterstain:ref(null),
    pro_ex_type:ref(null),
    show_upload_dialog:ref(false),
    show_upload_dialog_bulk:ref(false),
    _statusRunning: false,

      listLocation,
      listRoute,
      columns,
      show_dialog: ref(false),
      editedIndex: -1,
      userD: ref(false),
      editedItem: ref({
        uuid: ref(null),
        type: ref(null),
        type_id: ref(null),
        immortal: ref(null),
        source: ref(null),
        passage: ref(null),
        transfected: "Not",
        organism: ref(null),
        subtype:ref(null),
        patient_id:ref(null),
        distribution_id:ref(null),
        hyperlink:ref(null),
        well_number:ref(null),
      }),
      defaultItem: ref({
        uuid: ref(null),
        type: ref(null),
        type_id: ref(null),
        immortal: ref(null),
        source: ref(null),
        passage: ref(null),
        transfected: "Not",
        organism: ref(null),
        subtype:ref(null),
        patient_id:ref(null),
        distribution_id:ref(null),
        hyperlink:ref(null),
        well_number:ref(null),

      }),

      optionsOrganism,
      optionsSource,
      optionsImmortal,
      optionsPassage,
      optionsSubtype,


      filterSubtype (val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsSubtype.value = stringOptionsSubtype.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },

      filterPassage (val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsPassage.value = stringOptionsPassage.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },
       filterOrganism (val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsOrganism.value = stringOptionsOrganism.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },
      filterImmortal(val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsImmortal.value = stringOptionsImmortal.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      },
      filterSource(val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsSource.value = stringOptionsSource.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      }

    }


  },
  components: {uploadbtn,uploadbtnb},

  methods: {

    updateWellAndUI(uuid, val) {
  // Clone new value
  const updatedValue = Array.isArray(val)
    ? val.map(w => w.trim().toUpperCase())
    : [val.trim().toUpperCase()];

  // Find the row in your reactive `data`
  const row = this.data.find(r => r.uuid === uuid);
  if (row) {
    // ✅ trigger reactivity via direct assignment
    row.well_number = [...updatedValue];
  }

  // Call backend update
  this.updateWellNumber(row, updatedValue);
}
,
    async updateWellNumber(row, newValue) {
    try {

      const experiment_id1= row.uuid
      // const well_number1= newValue
      const well_number1 = Array.isArray(newValue)
      ? newValue.map(w => w.trim().toUpperCase()).join(',')
      : newValue.toUpperCase();

      console.log(experiment_id1,well_number1)
      const response = await API('auth.updatewell_numberExp', {
        id1: experiment_id1,
        well_number: well_number1
      });
      // console.log('API response:', response);
      this.$q.notify({
        type: 'positive',
        message: `Well number updated to ${newValue}`
      });
    } catch (error) {
      console.error('Failed to update well_number', error);
      this.$q.notify({
        type: 'negative',
        message: 'Failed to update well number'
      });
    }
  },
     // Format CSV Value
  wrapCsvValue(val) {
    let formatted = val !== undefined && val !== null ? String(val) : '';
    formatted = formatted.replace(/"/g, '""'); // Escape double quotes
    return `"${formatted}"`; // Wrap with quotes
  },

    // Export CSV Function
    exportTable() {
      if (!this.filteredColumns_csv.length || !this.filteredRows.length) {
        this.$q.notify({
          message: 'No data available for export',
          color: 'negative',
          icon: 'warning'
        });
        return;
      }

      // Generate CSV content using filtered rows & columns
      const content = [
        this.filteredColumns_csv.map(col => this.wrapCsvValue(col.label)) // Headers
      ]
      .concat(
        this.filteredRows.map(row =>
          this.filteredColumns_csv.map(col =>
            this.wrapCsvValue(typeof col.field === 'function' ? col.field(row) : row[col.field] || '')
          ).join(',')
        )
      )
      .join('\r\n');

      const status = exportFile('filtered-data.csv', content, 'text/csv');

      if (!status) {
        this.$q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning'
        });
      }
    },

async fetchAndCheckExperiments() {
  if (this._statusRunning) return;
  this._statusRunning = true;

  try {
    const key = this.random_id;
    const response = await API('auth.ExperimentDetials_randomid', { key });
    this.experiments1 = response || [];

    const uuids = this.experiments1.map(e => e.uuid).filter(Boolean);

    // mark all as checking
    uuids.forEach(u => (this.matchStatus[u] = 'checking'));

    // run in small batches to avoid overload
    for (let i = 0; i < uuids.length; i += 3) {
      const chunk = uuids.slice(i, i + 3);
      await Promise.all(chunk.map(u => this.checkUploadStatus(u)));
    }
  } catch (e) {
    console.error('[fetchAndCheckExperiments] failed:', e);
    // if something fails, at least stop "checking" UI
    if (Array.isArray(this.experiments1)) {
      this.experiments1.forEach(ex => {
        if (ex?.uuid && this.matchStatus[ex.uuid] === 'checking') {
          this.matchStatus[ex.uuid] = 'upload well';
        }
      });
    }
  } finally {
    this._statusRunning = false;
  }
},

      //   async fetchAndCheckExperiments() {
      //   try {
      //     // Fetch all experiments using the provided random_id
      //     const key = this.random_id;
      //     const response = await API('auth.ExperimentDetials_randomid', { key });
      //       // console.log(response,"sohaib");

      //     // Populate the experiments1 array
      //     this.experiments1 = response || [];

      //     // Initialize matchStatus and check upload status for each experiment
      //     for (const experiment of this.experiments1) {
      //       this.matchStatus[experiment.uuid] = 'checking';  // Set initial status to "checking"
      //       await this.checkUploadStatus(experiment.uuid);  // Check and update the status
      //     }
      //   } catch (error) {
      //     console.error('Error fetching experiments1 on load:', error);
      //   }
      // },

      // async checkUploadStatus(uuid) {
      //   try {
      //     const response = await API('auth.getallfile_expid', { experiment_id: uuid });
      //     if (response && response.experiment_id) {
      //       const responseId = response.experiment_id.toString();
      //       this.matchStatus[uuid] = responseId === uuid.toString() ? 'done' : 'upload well';
      //     } else {
      //       this.matchStatus[uuid] = 'upload';
      //     }
      //   } catch (error) {
      //     console.error(`Error checking upload status for experiment ${uuid}:`, error);
      //     this.matchStatus[uuid] = 'upload';
      //   }
      // },

      async checkUploadStatus(uuid) {
  // helper: timeout wrapper so "checking" never hangs forever
  const withTimeout = (promise, ms = 12000) =>
    Promise.race([
      promise,
      new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), ms))
    ]);

  try {
    console.log('[checkUploadStatus] start:', uuid);

    const res = await withTimeout(
      API('auth.getallfile_expid', { experiment_id: uuid }),
      12000
    );

    console.log('[checkUploadStatus] result:', uuid, res);

    const isDone = !!res && res.experiment_id != null;
    this.matchStatus[uuid] = isDone ? 'done' : 'upload well';
  } catch (err) {
    console.error('[checkUploadStatus] error:', uuid, err);
    // ✅ IMPORTANT: set final state so UI doesn’t remain "checking"
    this.matchStatus[uuid] = 'upload well';
  }
},


//   async checkUploadStatus(uuid) {
//   try {
//     const res = await API('auth.getallfile_expid', { experiment_id: uuid });

//     // ✅ your backend returns {experiment_id:'...'} OR null
//     const isDone = !!res && res.experiment_id != null;

//     this.matchStatus[uuid] = isDone ? 'done' : 'upload well';
//   } catch (error) {
//     console.error(`Error checking upload status for experiment ${uuid}:`, error);
//     this.matchStatus[uuid] = 'upload well';
//   }
// }

// ,

    getInitialLabel(uuid) {
      return this.matchStatus[uuid] === 'done' ? 'Done' : this.matchStatus[uuid] === 'checking' ? 'Checking...' : 'upload well';
    },
    getInitialColor(uuid) {
      return this.matchStatus[uuid] === 'done' ? 'green' : 'red';
    },

    setTableTitles(index) {
      if (this.data[index]) {
        const { random_id,uuid,experiment_name,experiment_design_date, ex_type, type, coCulture, costain, counterstain, virus,primary, secondary, magnification, phase_info,em_exposure,unit_em_exposure,voltage,pulse_width,no_of_pluses,time_bt_pulses,capacitance  } =
          this.data[index];

        this.tableTitles = {
          random_id,
          uuid,
          experiment_name,
          experiment_design_date,
          ex_type,
          type,
          coCulture,
          costain,
          counterstain,
          virus,
          primary,
          secondary,
          magnification,
          phase_info,
          em_exposure,unit_em_exposure,voltage,pulse_width,no_of_pluses,time_bt_pulses,capacitance
        };
      }
    },
    async handleClick(uuid) {
  this.matchStatus[uuid] = 'checking'; // Immediately show "Checking..."

  try {
    const response = await API("auth.getallfile_expid", { experiment_id: uuid });

    // Check if the response is valid and contains the required property
    if (response && response.experiment_id !== undefined && response.experiment_id !== null) {
      const responseId = response.experiment_id.toString();
      this.matchStatus[uuid] = responseId === uuid.toString() ? 'done' : 'upload Well';
    } else {
      // Handle cases where response is invalid or experiment_id is missing
      console.warn(`Invalid response or missing experiment_id for uuid: ${uuid}`, response);
      this.matchStatus[uuid] = 'upload';
    }
  } catch (error) {
    console.error("Error checking match status:", error);
    this.matchStatus[uuid] = 'upload'; // Revert to "Upload" on error
  }
}
,



      isUploaded(experiment_id1) {

       const exp_indb= API("auth.getallfile_expid", { experiment_id: experiment_id1});
       console.log(exp_indb,"jjjj")

       this.isMatched = exp_indb === experiment_id1;

      },
      async checkMatchStatus(uuid) {
  try {
      const response = await API("auth.getallfile_expid", { experiment_id: uuid });

      // Direct assignment works because matchStatus is a reactive object (ref or reactive)
      matchStatus[uuid] = response === uuid;
    } catch (error) {
      console.error("Error checking match status:", error);
    }
  },


    async getExp(random_id){
      const key = this.random_id;
      // console.log(key)
      API('auth.ExperimentDetials_randomid', { key }).then(res => {

        res.forEach(row => {
          if (typeof row.well_number === 'string' && row.well_number.trim() !== '') {
          row.well_number = row.well_number
            .split(',')
            .map(w => w.trim().toUpperCase());
        } else {
          row.well_number = []; // Ensure q-select works with a clean array
        }

      });


        this.data = res;
        if (this.data.length > 0) {
        this.setTableTitles(0); // Default to first experiment initially
      }
        this.$q.notify({
          message: 'Experiments Loaded',
          color: 'positive',
          position: 'top',
          timeout: 2000 // Optional: set how long the notification should be displayed
        });
      }).catch(error => {
        // Handle any errors that may occur during the API call
        console.error('Error:', error);
      });

    },
   async handleButtonClick() {
      if (this.model !== null) {

        this.modelstudyid=this.model.value
        const modelstudyid111=this.model.value.toString();
        const res =await API('auth.ExperimentDetialsstudy_id', { modelstudyid111 });
        const optionsArray = res.map(item => {
          return {
            label: item.experiment_name,
            value: item.random_id
          };
          });

          stringOptionsexp = optionsArray;

        // console.log("Selected value:",  this.modelstudyid);
      } else {
        console.log("No value selected");
      }
    },
  passValues(showDialog, uuid, studyId,phase_info,counterstain,ex_type,magnification,random_id) {
  this.show_upload_dialog = showDialog;
  this.prop_uuid=uuid;
  this.prop_st_id=studyId;
  this.pro_phase_info=phase_info;
  this.pro_counterstain=counterstain;
  this.pro_ex_type=ex_type;
  this.pro_magnification=magnification;
  this.pro_random_id=random_id;
// console.log(  this.prop_uuid,this.prop_st_id)
},

//   passValues_bulk(showDialog, uuid,phase_info,counterstain,ex_type,magnification) {
//   this.show_upload_dialog_bulk = showDialog;
//   this.prop_uuid=uuid;
//   this.pro_phase_info=phase_info;
//   this.pro_counterstain=counterstain;
//   this.pro_ex_type=ex_type;
//   this.pro_magnification=magnification;
// // console.log(  this.prop_uuid,this.prop_st_id)
// },

    async addRow() {

      const id1= this.editedItem.uuid

      const type1 = this.type_biosp
      // const type1 = "Cell"
      // const type_id1 = this.editedItem.type_id
      const type_id1=this.id_row

      // const immortal1 = this.editedItem.immortal
      const immortal1 = this.editedItem.immortal.toString()
      const source1 = this.editedItem.source.toString()
      const passage1 = this.editedItem.passage.toString()
      const transfected1 = this.editedItem.transfected
      const organism1 = this.editedItem.organism.toString()
      const subtype1 = this.editedItem.subtype.toString()
      const patient_id1 = this.editedItem.patient_id
      const distribution_id1 = this.editedItem.distribution_id
      const hyperlink1 = this.editedItem.hyperlink
      // const role1 = this.editedItem.role
      // const role1 = this.editedItem.role.toString()
      // const assignedCamra1 = this.editedItem.assignedCamra.toString()
      // const assignedRoute1 = this.editedItem.assignedRoute.toString()

      // console.log( role1.constructor.name+"mmmmmmm")


      const editedIndex1 = this.editedIndex
      const oldRow = this.data[editedIndex1]
      const updatedRow = this.editedItem

      if (this.editedIndex > -1) {
        Object.assign(oldRow, updatedRow) && API("auth.updateBiospecimen", { id1: id1,type: type1,type_id:type_id1, immortal: immortal1, source: source1,passage:passage1,transfected:transfected1,organism:organism1,subtype:subtype1,patient_id:patient_id1,distribution_id:distribution_id1,hyperlink:hyperlink1});
      } else {
        if (immortal1 && source1 &&  passage1 && transfected1 && organism1 && subtype1 && patient_id1 && distribution_id1 && hyperlink1) {

          this.data.push(this.editedItem) && API("auth.createBiospecimen", { type: type1,type_id:type_id1,immortal: immortal1, source: source1,passage:passage1,transfected:transfected1,organism:organism1, subtype:subtype1,patient_id:patient_id1,distribution_id:distribution_id1,hyperlink:hyperlink1});
        }
        else {
          this.$q.notify({
            message: 'please Enter all Details.',
            color: 'red',
            icon: 'announcement',
          })
        }
      }
      this.close()




    },

    async deleteItem(item) {
      const id = item.uuid
      // console.log(id + "oooo")
      const index = this.data.indexOf(item);
      confirm("Are you sure you want to Delete this user?") &&
      this.data.splice(index, 1) && await API('auth.deleteBiospecimen', { id });
    },
    async editItem(item) {
      this.editedIndex = this.data.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.show_dialog = true;
    },
    async close() {
      this.show_dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    }
  },

  data: () => ({

    data: []

  }),

  computed: {
 hasAnyWells() {
    return Array.isArray(this.data) && this.data.some(
      r => Array.isArray(r?.well_number) && r.well_number.length > 0
    );
  },
  formattedTransfected() {
    // Format the 'props.row.transfected' as needed
    // For example, to display a comma-separated string: "1, 8, 7, 3"
    return this.props.row.transfected.join(', ');
  },
  filteredRows() {
  return this.data.map(row => {
    const cleanedRow = {};

    // Iterate over each key-value pair in the row
    for (const key in row) {
      if (row[key] !== null) {
        cleanedRow[key] = row[key]; // Only include fields that are not null
      }
    }

    return cleanedRow; // Return the row without null values
  });
}

,
mergedHarvestTime() {
      return this.data.map(row => `${row.time} ${row.unit_harvest}`);
    },
    microscope(){
      return this.data.map(row => `${row.comment_drug}`);
    },
filteredColumns() {
  const columns = [];

  for (const key in this.data[0]) {
    if (key !== 'uuid'&&
      key !== 'experiment_description' &&
      key !== 'comment_cellCulture'&&
      key !== 'random_id'&&
      key !== 'study_id'&&
      key !== 'experiment_design_date'&&
      key !== 'experiment_name'&&
      key !== 'ex_type'&&
      key !== 'type'&&
      key !== 'ex_type'&&
      key !== 'concValue'&&
      key !== 'phase_info'&&
      // key !== 'magnification'&&
      key !== 'comment_virus'&&
      key !== 'primary'&&
      key !== 'secondary'&&
      key !== 'counterstain'&&
      key !== 'well_number'&&
      key !== 'comment_em_exposure'&&
      key !== 'unit_em_exposure'&&
      key !== 'unit_virus'&&
      key !== 'virus_concentration'&&
      key !== 'virus'&&


      // key !== 'unit_drug'&&
      // key !== 'concentration'&&
      key !== 'passage'&&
      // key !== 'unit_harvest'&&
      key !== 'coCulture'&&
      key !== 'costain'&&
      key !== 'unit_harvest'&&
      key !== 'concUnit'&&
      key !== 'treatment_group'&&
      // key !== 'time' &&
      key !== 'comment_drug'
      ) {
      // Check if any row has a null value for the current column
      const hasNull = this.data.some(row => row[key] === null);

      if (!hasNull) { // Only include the column if there are no null values
        columns.push({
          name: key,
          align: 'center',
          label: key,
          field: key,
          sortable: true,
          sort: (a, b, rowA, rowB) => {
            // if durg col then--> sepacial sort
            // parseFloat("40") = 40
            // parseFloat("160") = 160
            // return 40 - 160 = -120  // ➝ rowA comes before rowB

            if (key === 'drug') {
              const drugA = rowA.drug.toLowerCase();
              const drugB = rowB.drug.toLowerCase();

              if (drugA < drugB) return -1;
              if (drugA > drugB) return 1;

              const concA = parseFloat(rowA.concentration);
              const concB = parseFloat(rowB.concentration);
              return concA - concB;
            }

            const valA = a != null ? a.toString().toLowerCase() : '';
            const valB = b != null ? b.toString().toLowerCase() : '';

            if (!isNaN(a) && !isNaN(b)) {
              return parseFloat(a) - parseFloat(b);
            }
            return valA < valB ? -1 : valA > valB ? 1 : 0;
          }

        });
      }
    }


  }



    // Add a new column for "Harvest Time + Time Unit"
    //  if (this.data.length > 0 && this.data[0].hasOwnProperty('time')&& this.data[0].time) {
    //     columns.push({
    //       name: 'mergedHarvestTime',
    //       align: 'center',
    //       label: 'Harvest Time',
    //       field: 'mergedHarvestTime',
    //       sortable: true,
    //     });
    //   }

                  // Add a new column for "Harvest Time + Time Unit"
     if (this.data.length > 0 && this.data[0].hasOwnProperty('comment_drug') && this.data[0].comment_drug!='N/A,N/A' && this.data[0].comment_drug) {
        // 'time' property exists, add the new column
        columns.push({
          name: 'microscope',
          align: 'center',
          label: 'Microscope',
          field: 'microscope',
          sortable: true,
          // You can customize additional properties as needed
        });
      }

  // Conditionally add the 'well_number' column
  if (this.upload) {
    columns.push({
      name: 'well_number',
      align: 'center',
      label: 'Well Number',
      field: 'well_number',
      sortable: true,
    });
  }

  columns.push({
    name: 'actions',
    align: 'center',
    label: 'actions',
    field: 'actions',
    sortable: true,
  });




  return columns;
}
,
filteredColumns_csv() {
  const columns = [];
  const wellNumberExists = this.data.some(row => row.hasOwnProperty('well_number'));
  // console.log(wellNumberExists,"sohaib")

  for (const key in this.data[0]) {
    if (
      // key !== 'uuid'&&
      key !== 'experiment_description' &&
      key !== 'comment_cellCulture'&&
      key !== 'random_id'&&
      key !== 'study_id'&&
      key !== 'experiment_design_date'&&
      key !== 'experiment_name'&&
      key !== 'ex_type'&&
      key !== 'type'&&
      key !== 'ex_type'&&
      key !== 'concValue'&&
      key !== 'phase_info'&&
      key !== 'magnification'&&
      key !== 'comment_virus'&&
      key !== 'primary'&&
      key !== 'secondary'&&
      key !== 'counterstain'&&

      // key !== 'unit_drug'&&
      // key !== 'concentration'&&
      key !== 'passage'&&
      // key !== 'unit_harvest'&&
      key !== 'coCulture'&&
      key !== 'costain'&&
      key !== 'concUnit'&&
      key !== 'treatment_group'&&
      // key !== 'time' &&
      key !== 'comment_drug'
      ) {
      // Check if any row has a null value for the current column
      const hasNull = this.data.some(row => row[key] === null);

      if (!hasNull) { // Only include the column if there are no null values
        columns.push({
          name: key,
          align: 'center',
          label: key,
          field: key,
          sortable: true,
          sort: (a, b) => {
                const valA = a.toString().toLowerCase();
                const valB = b.toString().toLowerCase();

                if (!isNaN(a) && !isNaN(b)) {
                  return parseFloat(a) - parseFloat(b);
                }
                return valA < valB ? -1 : valA > valB ? 1 : 0;
              }
        });
      }


    }


  }



    // Add a new column for "Harvest Time + Time Unit"
    //  if (this.data.length > 0 && this.data[0].hasOwnProperty('time')&& this.data[0].time) {
    //     columns.push({
    //       name: 'mergedHarvestTime',
    //       align: 'center',
    //       label: 'Harvest Time',
    //       field: 'mergedHarvestTime',
    //       sortable: true,
    //     });
    //   }

                  // Add a new column for "Harvest Time + Time Unit"
     if (this.data.length > 0 && this.data[0].hasOwnProperty('comment_drug') && this.data[0].comment_drug!='N/A,N/A' && this.data[0].comment_drug) {
        // 'time' property exists, add the new column
        columns.push({
          name: 'microscope',
          align: 'center',
          label: 'Microscope',
          field: 'microscope',
          sortable: true,
          // You can customize additional properties as needed
        });
      }

// ✅ **Ensure "well_number" column is always added**
    if (wellNumberExists) {
      columns.push({
        name: "well_number",
        align: "center",
        label: "well_number",
        field: "well_number",
        sortable: true,
      });
    }


  return columns;
}

},

  mounted() {

      // let key = this.exp_pass_uploadImg[0].study_id;
    // let key=this.exp_pass_uploadImg
      // console.log(key,"mpmp")
  // API("auth.createArirports", { name:"DeliAir", latLong:"-873.45",noOfRunWay:"3",typesOfAircraft:"full",runWayConstType:"simple",AtcFacility:"fine",refuling:"ok" });
    // console.log(key)
  //   key=this.id_row
    // console.log(key)
  //   API('auth.experiment_details',{key}).then(res => {
    //   API('auth.experiment_details').then(res => {
    //     this.data = res
    //   // this.data = res.filter(item => item.study_id == '1')
    //   // console.log(res.filter(item => item.study_id = '1'),"dsfsdf" )
    // })

      // API('auth.study_details').then(res => {
      //   const nameArray = res.map(item => item.name);
      //   stringOptions=nameArray
      //   console.log(res,"dsfsdf" )
      // })

    //   API('auth.study_details').then(res => {
    //   const optionsArray = res.map(item => {
    //     return { label: item.name, value: item.uuid };
    //   });
    //   stringOptions = optionsArray;
    //   console.log(res, "dsfsdf");
    // })

    this.getExp(this.random_id);

    this.fetchAndCheckExperiments();

    // API('auth.findonlyRoute').then(res => {
    //   this.res=res
    //   // console.log(this.res)
    // })

    // API('auth.findLocID').then(res => {
    //   const objectArray = Object.entries(res);
    //   objectArray.forEach(([key, value]) => {
    //     this.listLocation.push(value)
    //   });
    // })

    // API('auth.findrouteNameID').then(res => {
    //   const objectArray = Object.entries(res);
    //   objectArray.forEach(([key, value]) => {
    //     this.listRoute.push(value.name)

    //   });
    // })



  },
  watch: {
    // Watch for changes in random_id and call getExp
    random_id(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.getExp(newVal);
      }
    },

    // show_upload_dialog(newVal, oldVal) {
    // if (!newVal && oldVal) {
    //   // Trigger when dialog is closed
    //   this.fetchAndCheckExperiments();
    // }}
    show_upload_dialog(newVal, oldVal) {
      if (!newVal && oldVal && this.prop_uuid) {
        this.matchStatus[this.prop_uuid] = 'checking';
        this.checkUploadStatus(this.prop_uuid);
      }
    }


  }


}
</script>


<style>
.compact-table td {
  padding: 0px 25px !important; /* Reduces cell padding */
}
.btn-success {
  background-color: green;
  color: white;
}
.btn-danger {
  background-color: red;
  color: white;
}

</style>
