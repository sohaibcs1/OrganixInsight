<template>

  <!--
  Forked from:
  https://quasar.dev/vue-components/table#Example--Popup-editing
-->
  <div>
    <div class="q-pa-sm q-gutter-sm">

       <!-- select Exp -->
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
       <!-- select Exp END -->
      <!-- {{ exp_pass_uploadImg }} -->
         <!-- v-if="(data.ex_type === '3D Experiment')" -->

            <!-- <div class="row justify-center" v-if="(data?.[0]?.ex_type === '3D Experiment' || data?.[0]?.ex_type === '3D morphogenesis')&& (data?.[0]?.magnification === '40x'|| data?.[0]?.magnification === null)">
            <q-btn color="primary" @click="sendbasal"  label="Run Analysis for Basal/Non-basal" class="q-mr-lg" />
            <q-btn color="secondary" @click="sendpositive"  label="Run Analysis for Positive Cells" />

          </div> -->


      <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="uuid" max-width="100%"
        binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
        class="q-table--dense" :pagination="pagination">
        <template v-slot:top>

          <div class="q-pa-sm q-gutter-sm">


            <q-dialog v-model="show_dialog">
              <q-card  text-center>
                <q-card-section>

                  <!-- <div class="text-h6 text-center bg-grey-5">Biospecimen {{ id_row }} Attributes</div> -->
                </q-card-section>

                <!-- add Camra Details Start -->
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
                <!-- add Camra Details END -->

                <q-card-actions align="center">

                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>

        </template>



        <template v-slot:body="props">
          <q-tr :props="props">

            <q-td key="desc" :props="props">
             <!-- <div><q-badge color="orange">Study Id: {{ props.row.study_id }}</q-badge></div>  -->
             <!-- <div><q-badge color="green" v-if="props.row.uuid"> Experiment Id: {{ props.row.uuid }}</q-badge></div>
             <div><q-badge color="green" v-if="props.row.experiment_name"> experiment Name: {{ props.row.experiment_name}}</q-badge></div>
              <div><q-badge color="green" v-if="props.row.experiment_design_date"> experiment design date: {{ props.row.experiment_design_date}}</q-badge></div>  -->


              <!-- <div><q-badge color="green" v-if="props.row.uuid"> Experiment Id: {{ props.row.uuid }}</q-badge></div>  -->
              <div><q-badge color="purple" v-if="props.row.name">  {{ props.row.name }}</q-badge></div>
              <!-- <div><q-badge color="orange" v-if="props.row.passage"> passage: {{ props.row.passage }}</q-badge></div> -->
              <!-- <div><q-badge color="purple" v-if="props.row.costain"> costain: {{ props.row.costain }}</q-badge></div> -->
              <!-- <div><q-badge color="purple" v-if="props.row.type"> type: {{ props.row.type }}</q-badge></div> -->
                <div><q-badge color="green" v-if="props.row.virus"> virus: {{ props.row.virus }}</q-badge></div>
                <div><q-badge color="green" v-if="props.row.virus_concentration"> virus concentration: {{ props.row.virus_concentration }} {{ props.row.unit_virus}}</q-badge></div>

                <div><q-badge color="green" v-if="props.row.plasmid"> plasmid: {{ props.row.plasmid }}</q-badge></div>
                <div><q-badge color="primary" v-if="props.row.plasmid_concentration"> plasmid concentration: {{ props.row.plasmid_concentration }} {{ props.row.unit_plasmid}}</q-badge></div>

              <div><q-badge color="teal" v-if="props.row.counterstain"> counterstain: {{ props.row.counterstain }}</q-badge></div>
              <div><q-badge color="primary" v-if="props.row.drug"> drug: {{ props.row.drug }} </q-badge></div>
              <div><q-badge color="primary" v-if="props.row.drug"> concentration: {{  props.row.concentration }} {{ props.row.unit_drug }}</q-badge></div>

              <div><q-badge color="red" v-if="props.row.time"> Time: {{ props.row.time }} {{ props.row.unit_harvest }}</q-badge></div>
<!--
              <div><q-badge color="teal" v-if="props.row.primary"> Primary: {{ props.row.primary  }}</q-badge></div>
              <div><q-badge color="teal" v-if="props.row.secondary"> Secondary: {{ props.row.secondary }}</q-badge></div>  -->
                <div><q-badge color="grey" v-if="props.row.treatment_group"> Condition: {{ props.row.treatment_group }}</q-badge></div>




            </q-td>



            <q-td key="actions" :props="props" >
              <!-- <q-btn color="black" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn> -->
              <!-- <q-btn label="upload" size="12px" dense @click="passValues(true, props.row.uuid, props.row.study_id)"></q-btn> -->

              <div class="row">

              <div v-for="file in props.row.files" :key="file.file_name" class="q-mr-lg text-center">

                <div >


                  <!-- {{file.max_encrypt_image}} -->
                    <!-- <q-img :src="`http://127.0.0.1:6080/${file.max_encrypt_image.replace(/\\/g, '/')}`" spinner-color="white" style="height: 200px; width: 200px ;border: 1px solid #ccc;"/> -->
                    <!-- <q-img
                      :src="`${BASE_URL}/${file.middle_encrypt_image}`"
                      spinner-color="white"
                      style="height: 160px; width: 160px; border: 1px solid #ccc;"
                    /> -->
                    <thumbnail :src="`${BASE_URL}/${file.middle_encrypt_image}`" :alt="file.file_name" />


                    <!-- <q-img :src="`http://134.197.75.35:6085/${file.middle_encrypt_image}`" spinner-color="white" style="height: 160px; width: 160px ;border: 1px solid #ccc;"/> -->
                  <q-tooltip >
                    {{ file.file_name }}
                  </q-tooltip>
                  <div  @click="passValues(true, props.row.uuid, file.file_name)"  class="bg-blue" style="cursor: pointer;">2D Viewer
                    <q-tooltip class="bg-blue">
                    open
                  </q-tooltip></div>

                   <div  @click="passValuesLog(true, props.row.random_id, file.file_name)"  class="bg-warning" style="cursor: pointer;" v-if="props.row.ex_type=='2D non-quantitative Experiment' || props.row.ex_type=='2D Experiment' ||
                       (props.row.ex_type === '3D Experiment' && props.row.magnification === '10x')|| (props.row.ex_type === '3D non-quantitative Experiment' && props.row.magnification === '10x')">Log Filter
                    <q-tooltip class="bg-blue">
                    open
                  </q-tooltip></div>

                  <div class="bg-red" @click="call_paraview(file,file.file_name)" style="cursor: pointer;"
                  v-if="(props.row.ex_type === '3D morphogenesis' || props.row.ex_type === '3D Experiment') && (props.row.magnification === '40x'|| props.row.magnification === null)">3D Viewer

                    <q-tooltip class="bg-red">
                      open
                  </q-tooltip>
                  <q-spinner
                    color="white"
                    size="1em"
                    :thickness="8"
                    v-if="file.loading"
                  /></div>

                  <div class="bg-teal text-subtitle1" @click="call_analysis(file,file.file_name),passValues_analysis(true, props.row.uuid, file.file_name)" style="cursor: pointer;"
                  v-if="(props.row.ex_type === '3D morphogenesis' || props.row.ex_type === '3D Experiment') && (props.row.magnification === '40x'|| props.row.magnification === null)" > <q-icon name="query_stats"  /> Analysis Details
                    <q-tooltip class="bg-teal">
                      open
                  </q-tooltip>
                    <q-spinner
                    color="white"
                    size="1em"
                    :thickness="8"
                    v-if="file.loadingd"
                  /> </div>


                    <div class="bg-orange text-subtitle1" @click="openMarkerDialog(file, props.row)" style="cursor: pointer;"
                  v-if="(props.row.ex_type === '3D morphogenesis' || props.row.ex_type === '3D Experiment') && (props.row.magnification === '40x'|| props.row.magnification === null)" > <q-icon name="sync"  /> Run Analysis
                    <q-tooltip class="bg-teal">
                      open
                  </q-tooltip>
                    <q-spinner
                    color="white"
                    size="1em"
                    :thickness="8"
                    v-if="file.loadingd"
                  /> </div>

                </div>

            </div>


            </div>

            </q-td>


            <q-td key="delete" :props="props">
              <q-btn color="red" icon="delete" label="Delete Data" size="10px" dense @click="deleteData(props.row.uuid)" v-if="props.row.files[0]"/>
            </q-td>

          </q-tr>
        </template>
      </q-table>
    </div>


<!-- Bulk Run start -->
<q-dialog v-model="markerDialog">
  <q-card style="width: 90vw; max-width: 1200px;">
    <q-card-section>
      <div class="text-h6">Marker Overlay Details</div>
      <div class="text-caption">
        Middle slice with mapped marker channels
      </div>
    </q-card-section>

 <q-card-section>

  <div class="row q-col-gutter-md justify-center">

    <div
      v-for="img in markerImages"
      :key="img.label"
      class="col-12 col-sm-6 col-md-4 text-center"
    >
      <q-img
        :src="img.src"
        style="height:180px;object-fit:contain;"
        fit="contain"
      />

      <div class="text-bold q-mt-sm">
        Middle slice
      </div>


      <q-input v-model.number="model_dilation" min="0" type="number" filled outlined label="Dilation Radius" class="q-mb-sm" dense/>
      <q-btn color="deep-orange" icon="visibility" label="View Marker Overlay" @click="sendInput"/>

      <!-- server base64 start -->
  <div v-if="overlayLoading" class="q-mt-md text-grey text-center">
      Generating overlay...
    </div>

    <div
      v-if="overlayMaskSrc || overlayImageSrc"
      class="row q-col-gutter-lg q-mt-lg justify-center"
    >

      <div class="col-12 col-md-6 text-center" v-if="overlayMaskSrc">
        <q-img
          :src="overlayMaskSrc"
          fit="contain"
          style="max-width:700px; width:100%; max-height:1000px;"
        />
        <div class="text-h7 text-weight-bold q-mt-md">
          Mask Region
        </div>
      </div>

      <div class="col-12 col-md-6 text-center" v-if="overlayImageSrc">
        <q-img
          :src="overlayImageSrc"
          fit="contain"
          style="max-width:700px; width:100%; max-height:1000px;"
        />
        <div class="text-h7 text-weight-bold q-mt-md">
          Raw + Mask Overlay
        </div>
      </div>

    </div>

      <!-- server bas4 end -->
    </div>

  </div>

  <!-- Divider -->
  <q-separator class="q-my-lg" />

  <!-- Analysis Section -->
  <div class="text-h6 text-center q-mb-md">
    Bulk Image Analysis
  </div>

  <div class="row justify-center q-gutter-md">

    <q-btn
      color="primary"
      icon="hub"
      label="Basal / Non-Basal Analysis"
      @click="sendbasal"
    />

    <q-btn
      color="secondary"
      icon="biotech"
      label="Positive Cell Analysis"
      @click="sendpositive"
    />

  </div>

</q-card-section>

    <q-card-actions align="right">
      <q-btn flat label="Close" color="primary" v-close-popup />
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- Bulk Run End -->



      <q-dialog v-model="show_upload_dialog" full-width full-height >
          <q-card class="q-pa-none">
            <q-card-section class="row justify-between">
              <q-space />
              <q-btn icon="close" round dense flat v-close-popup />
            </q-card-section>
            <q-card-section align="center" class="q-pa-md">
              <div class="row text-center">
                <moreImages
                  :experiment_id="prop_exp_id"
                  :file_name="prop_file_name"
                  :exp_type="prob_exp_type"
                ></moreImages>
              </div>
            </q-card-section>
          </q-card>
        </q-dialog>
<!--
          <q-dialog v-model="show_upload_dialog_log"  >
          <q-card class="q-pa-none" style="max-width: 800px; width: 100%;">
            <q-card-section class="row justify-between">
              <q-space />
              <q-btn icon="close" round dense flat v-close-popup />
            </q-card-section>
            <q-card-section align="center" class="q-pa-md">
              <div class="row text-center">

               <twoDmodel_list :experiment_id="prop_exp_id" :passEx_type="prob_exp_type" :file_name="prop_file_name"></twoDmodel_list>

              </div>
            </q-card-section>
          </q-card>
        </q-dialog> -->

<q-dialog v-model="show_upload_dialog_log">
  <q-card class="q-pa-none" style="max-width: 2000px; width: 100%; height: 100%;">
    <q-card-section class="row items-center justify-between">
      <div class="text-subtitle1">Log Filter</div>
      <q-btn icon="close" round dense flat v-close-popup @click="onDialogClose" />
    </q-card-section>

    <q-separator />

    <q-card-section class="q-pa-none" style="max-width: 2000px; width: 100%; height: 100%;">
      <!-- lightweight overlay -->
      <div
        v-show="showWaitOverlay"
        class="absolute-full flex flex-center"
        style="background: rgba(255,255,255,0.85); z-index: 2;"
      >
        <div class="text-subtitle1 text-grey-8">Please wait…</div>
      </div>

      <iframe
        v-if="logUrl"
        :key="logUrl"
        ref="logIframe"
        :src="logUrl"
        style="width:100%; height:100%; border:0;"
        @load="onIframeLoad"
      ></iframe>
    </q-card-section>

    <!-- <q-card-actions align="right">
      <q-btn v-if="logUrl" flat label="Open in new tab" @click="openInTab" />
    </q-card-actions> -->
  </q-card>
</q-dialog>





      <q-dialog v-model="show_upload_dialog_analysis" >
        <q-card >

          <!-- add Camra Details Start -->
          <q-card-section align="center" >
            <div class="row text-center">
              <div class="json-viewer">
                <q-card class="full-width">
                  <q-card-section>
                    <div class="text-weight-thin">file name: {{ prop_file_name_a }} </div>
                    <q-list bordered>
                      <!-- {{response}} -->
                      <q-item v-for="(value, key, index) in JSON.parse(response)" :key="index">
                        <q-item-section>
                          <q-item-label>{{ key }}: {{ value }} </q-item-label>
                        </q-item-section>
                      </q-item>

                    </q-list>
                  </q-card-section>
                </q-card>
              </div>
              <!-- attributes table END -->
            </div>
          </q-card-section>


          <!-- add Camra Details END -->
        </q-card>
      </q-dialog>

  </div>

</template>

<script>
import API from 'src/api'
import { ref } from 'vue'
import { exportFile, useQuasar } from 'quasar'
import moreImages from 'src/components/user/moreImages_list';
import thumbnail from 'src/components/user/thumbnail';
  // import twoDmodel_list from 'src/components/user/2dmodel_list';

// import analysis_details from 'src/components/user/analysis_details';


var stringOptions = [
  'Study 1', 'Study 2', 'Study 3', 'Study 4', 'Study 5'
]

var stringOptionsexp = [
  'Experiment 1', 'Experiment 2', 'Experiment 3', 'Experiment 4', 'Experiment 5'
]


const columns = [
  {
    name: 'desc',
    required: true,
    label: 'Experiment Details',
    align: 'center',
    field: row => row.uuid,
    format: val => `${val}`,
    sortable: true
  },

  { name: "actions", align: 'center', label: "Data", field: "actions" },
  { name: "delete", align: 'center', label: "Delete", field: "delete" }


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
    random_id: {
      type: String,
      required: true,
    }},
  // props: {
  // exp_pass_uploadImg:Array,

  // },

  setup() {

    const options = ref(stringOptions)
    const optionsexp = ref(stringOptionsexp)

    const $q = useQuasar()
    const optionsOrganism= ref(stringOptionsOrganism)
    const optionsSource=ref(stringOptionsSource)
    const optionsImmortal=ref(stringOptionsImmortal)
    const optionsPassage= ref(stringOptionsPassage)
    const optionsSubtype= ref(stringOptionsOrganism)

    return {
      pagination: {
      rowsPerPage: 30 // current rows per page being displayed
    },
    model_dilation: ref(0),
    options,
    optionsexp,
      logUrl: "",
      showWaitOverlay: false,     // <— renamed
      _waitTimer: null,           // <— renamed timer
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
      modelstudyid:ref(null),
    prop_exp_id:ref(null),
    prop_file_name:ref(null),
    prob_exp_type:ref(null),
    prop_exp_id_a:ref(null),
    prop_file_name_a:ref(null),
    show_upload_dialog:ref(false),
    show_upload_dialog_log:ref(false),
    show_upload_dialog_analysis:ref(false),
      listLocation,
      listRoute,
      response:null,
      loading: false,
      loadingd: false,
      columns,
      experiments:[],
      files:[],
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
      }),

      optionsOrganism,
      optionsSource,
      optionsImmortal,
      optionsPassage,
      optionsSubtype,
      model: ref(null),
      modelexp: ref(null),

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
  components: {moreImages,thumbnail},

  methods: {

openMarkerDialog(file, row) {
  this.selectedExperimentId = row.uuid;
  this.selectedFileName = file.file_name;

  this.markerImages = [];

  const middleImage = file.middle_encrypt_image || file.encrypt_image;

  if (middleImage) {
    this.markerImages.push({
      label: "Middle Slice",
      channel: "Original / merged view",
      src: `${this.BASE_URL}/${middleImage}`
    });
  }

  let positive = null;

  try {
    positive = typeof file.positive === "string"
      ? JSON.parse(file.positive)
      : file.positive;
  } catch (e) {
    positive = null;
  }

  if (positive && Array.isArray(positive.channels)) {
    positive.channels.forEach(ch => {
      if (!ch || ch.status === "failed") return;

      this.markerImages.push({
        label: ch.marker || ch.display_name || ch.channel_name,
        channel: ch.channel_name,
        src: `${this.BASE_URL}/${middleImage}`
      });
    });
  }

  this.markerDialog = true;
},


// async sendpositive() {
//   this.$q.notify({
//     message: 'Positive cell analysis is running in the background...',
//     color: 'info',
//     icon: 'hourglass_empty',
//     position: 'top',
//     timeout: 3000
//   });

//   try {
//     const uuids = this.data.map(row => row.uuid).join(',');
//     await API('home.getpositive', uuids);

//     this.$q.notify({
//       message: 'Positive cell analysis completed successfully',
//       color: 'positive',
//       icon: 'check_circle',
//       position: 'top',
//       timeout: 3000
//     });
//   } catch (error) {
//     this.$q.notify({
//       message: 'Positive cell analysis failed',
//       color: 'negative',
//       icon: 'error',
//       position: 'top',
//       timeout: 3000
//     });
//   }
// },
async sendpositive() {
  this.$q.notify({
    message: 'Positive cell analysis is running in the background...',
    color: 'info',
    icon: 'hourglass_empty',
    position: 'top',
    timeout: 3000
  });

  try {
    const experimentIds = this.data
      .map(row => row.uuid)
      .filter(Boolean)
      .map(String)
      .join(',');

    if (!experimentIds) {
      this.$q.notify({
        message: 'No experiment IDs found.',
        color: 'negative',
        icon: 'error',
        position: 'top',
        timeout: 3000
      });
      return;
    }

    const payload = {
      experiment_ids: experimentIds,
      dilation_radius: Number(this.model_dilation || 0)
    };

    console.log(payload, 'positivePayload');

    const result = await API('home.getpositive', payload);
    console.log(result, 'positiveResult');

    if (result?.status === 'failed') {
      this.$q.notify({
        message: result?.error || 'Positive cell analysis failed.',
        color: 'negative',
        icon: 'error',
        position: 'top',
        timeout: 5000
      });
      return;
    }

    if (result?.status === 'partial_failed') {
      this.$q.notify({
        // message: `Positive analysis finished with ${result?.failed || 0} failed file(s). Processed ${result?.processed || 0}.`,
        message: `Positive analysis Done.`,
        color: 'warning',
        icon: 'warning',
        position: 'top',
        timeout: 6000
      });
      return;
    }

    this.$q.notify({
      // message: `Positive cell analysis completed successfully. Processed ${result?.processed || 0} file(s).`,
      message: `Positive cell analysis completed successfully.`,
      color: 'positive',
      icon: 'check_circle',
      position: 'top',
      timeout: 4000
    });

  } catch (error) {
    console.error('Positive cell analysis error:', error);

    this.$q.notify({
      message: 'Positive cell analysis failed',
      color: 'negative',
      icon: 'error',
      position: 'top',
      timeout: 3000
    });
  }
}
,
async sendInput() {
  const payload = {
    experiment_id: this.selectedExperimentId,
    file_name: this.selectedFileName,
    dilation_radius: Number(this.model_dilation)
  };

  this.overlayLoading = true;
  this.overlayMaskSrc = null;
  this.overlayImageSrc = null;

  try {
    const result = await API('home.getpositive_input', payload);
    console.log(result, "serverResult");

    if (result?.status === "success") {
      this.overlayMaskSrc = `data:image/png;base64,${result.mask_image_base64}`;
      this.overlayImageSrc = `data:image/png;base64,${result.overlay_image_base64}`;
    } else {
      this.$q.notify({
        message: result?.error_message || "Overlay generation failed",
        color: "negative",
        icon: "error",
        position: "top"
      });
    }
  } finally {
    this.overlayLoading = false;
  }
},

async sendbasal() {
  this.$q.notify({
    message: 'Basal / Non-basal analysis is running in the background...',
    color: 'info',
    icon: 'hourglass_empty',
    position: 'top',
    timeout: 3000
  });

  try {
    const uuids = this.data.map(row => row.uuid).join(',');
    await API('home.getbasal', uuids);

    this.$q.notify({
      message: 'Basal / Non-basal analysis completed successfully',
      color: 'positive',
      icon: 'check_circle',
      position: 'top',
      timeout: 3000
    });
  } catch (error) {
    this.$q.notify({
      message: 'Basal / Non-basal analysis failed',
      color: 'negative',
      icon: 'error',
      position: 'top',
      timeout: 3000
    });
  }
},

async deleteData(id) {
  try {
    console.log(id, "id being passed");

    // Step 1: Prompt for user confirmation
    const userInput = prompt("Type 'DELETE' to confirm deletion:");
    if (userInput !== "DELETE") {
      alert("Deletion canceled. Please type 'DELETE' to confirm.");
      return;
    }

    console.log("User confirmed deletion, proceeding...");

    // Step 2: Call two APIs using Promise.all()
    const [response1, response2] = await Promise.all([
      API('auth.deleteFiles', { id }),  // First table deletion (processed_files, for example)
      API('auth.deleteFilesfromfile', { id })  // Second table deletion (e.g., another_files)
    ]);

    // Step 3: Check both responses
    if (response1.success && response2.success) {
      alert(`Deletion successful. Deleted ${response1.deletedCount} and ${response2.deletedCount} record(s).`);
    } else {
      const message1 = response1.success ? "" : `Failed to delete from first table: ${response1.message}`;
      const message2 = response2.success ? "" : `Failed to delete from second table: ${response2.message}`;

      alert(`Partial failure: \n${message1}\n${message2}`);
      console.error("Backend responses:", { response1, response2 });
    }

  } catch (error) {
    console.error("Error during deletion:", error);
    alert("An error occurred while trying to delete the records.");
  }
}

,

        async call_analysis(file, name) {
        try {
            file.loadingd = true; // Set loading to true
            const res = await API('auth.mask_file_process_details', { name });
            if (res) {
                this.response = res.mask_file_analysis;
            } else {
                this.response = "";
            }
        } catch (error) {
            console.error("Error fetching model files:", error);
            // Handle the error as required, e.g., show a message to the user
        } finally {
            setTimeout(() => {
                file.loadingd = false; // Set loading to false after two seconds
            }, 1000); // 2000 milliseconds = 2 seconds
        }
    },

          async call_paraview(file, name) {
          await API('auth.getmodelfiles', { name })
              .then(res => {
                  if (res) {
                      this.modelPrediction = res.model_prediction_files;
                      // console.log(this.modelPrediction);
                  } else {
                      // Set a default value for this.modelPrediction if nothing found no vtp set default from server if want
                      this.modelPrediction = "";
                      console.log("No model prediction files found, setting default:", this.modelPrediction);
                  }
              })
              .catch(error => {
                  console.error("Error fetching model files:", error);
                  // Handle the error as required, e.g., show a message to the user
              });

          file.loading = true;

          API('home.getParaviewUrl', this.modelPrediction)
              .then(res => {
                  if (res && res.url) {
                      console.log(res, "server response received");
                      const paraviewPort = res.url;
                      const paraviiewFile= res.file_name
                      const host=this.BASE_URL_IP
                      const completeURL = `${host}:${paraviewPort}/?filename=${paraviiewFile}`;

                      setTimeout(() => {
                          window.open(completeURL, '_blank');
                          file.loading = false;
                      }, 500); // 5000 milliseconds = 5 seconds
                  } else {
                      throw new Error("No Paraview URL found");
                  }
              })
              .catch(error => {
                  console.error("Error fetching Paraview URL:", error);
                  // Handle the error as required, e.g., show a message to the user
              });
      },

        async getExp(random_id) {
          try {
            const key = random_id;

            // Fetch experiment details and file details concurrently
            const [experimentDetails, fileDetails] = await Promise.all([
              API('auth.ExperimentDetials_randomid', { key }),
              API('auth.file_details_middel'),
            ]);

            // Combine the data
            const combinedData = this.combineData(experimentDetails, fileDetails);

            // Assign combinedData to this.data or use it as needed
            this.data = combinedData;
            this.prob_exp_type=this.data[0].ex_type
            // console.log( combinedData,"ddd")

            // Notify user of success
            this.$q.notify({
              message: 'Experiments Loaded',
              color: 'positive',
              position: 'top',
              timeout: 2000, // Optional: set how long the notification should be displayed
            });

          } catch (error) {
            // Log the error for debugging
            console.error('Error fetching experiment details:', error);

            // Optionally, notify the user of the error
            this.$q.notify({
              message: 'Failed to load experiments. Please try again later.',
              color: 'negative',
              position: 'top',
              timeout: 2000,
            });
          }
        }
,
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

      } else {
        console.log("No value selected");
      }
    },



    combineData(experimentDetails, fileDetails) {
  const combinedData = experimentDetails.map(experiment => {
    const experimentId = experiment.uuid.toString(); // Assuming uuid is a number
    const experimentFiles = fileDetails.filter(file => file.experiment_id === experimentId);
    return { ...experiment, files: experimentFiles };
  });

  return combinedData;
},

  passValues(showDialog, exp_id, file_name) {
  this.show_upload_dialog = showDialog;
  this.prop_exp_id=exp_id;
  this.prop_file_name=file_name;
},
// passValuesLog(showDialog, exp_id, file_name) {
//   this.show_upload_dialog_log = showDialog;
//   this.prop_exp_id=exp_id;
//   this.prop_file_name=file_name;
// },

  //  passValuesLog(showDialog, exp_id, file_name) {
  //     this.show_upload_dialog_log = !!showDialog;
  //     this.prop_exp_id = exp_id;

  //     // force .tiff extension from incoming file name
  //     const base = String(file_name || "").split("/").pop().replace(/\.[^/.]+$/, "");
  //     const tiffName = `${base}.tif`;
  //     this.prop_file_name = tiffName;

  //     // rid = "randomId<id>" (avoid double prefix)
  //     const cleanId = String(exp_id || "").replace(/^randomId/i, "");
  //     const ridParam = `randomId${cleanId}`;

  //     // build URL (cache-buster optional)
  //     this.logUrl = `http://134.197.75.35:6883/count?rid=${encodeURIComponent(
  //       ridParam
  //     )}&filename=${encodeURIComponent(tiffName)}&ts=${Date.now()}`;
  //   },

  BASE_URL_IP2() {
  // Automatically detect the correct server base URL
  const host = window.location.hostname;
  const port = 6883; // backend port
  if (host === "localhost" || host === "127.0.0.1") {
    return `http://localhost:${port}`;
  }
  return `http://${host}:${port}`;
},

passValuesLog(showDialog, exp_id, file_name) {
  this.show_upload_dialog_log = !!showDialog;
  this.prop_exp_id = exp_id ?? "";

  // Force .tif extension from incoming file name
  const base = String(file_name || "").split("/").pop().replace(/\.[^/.]+$/, "");
  const tiffName = `${base}.tif`;
  this.prop_file_name = tiffName;

  // rid = "randomId<id>" (avoid double prefix)
  const cleanId = String(exp_id || "").replace(/^randomId/i, "");
  const ridParam = `randomId${cleanId}`;

  // Build URL dynamically based on detected IP/host
  const baseUrl = this.BASE_URL_IP2();
  this.logUrl = `${baseUrl}/count?rid=${encodeURIComponent(
    ridParam
  )}&filename=${encodeURIComponent(tiffName)}&ts=${Date.now()}`;

  console.log(this.logUrl,"")
}
,
    openInTab() {
      if (this.logUrl) window.open(this.logUrl, "_blank");
    },

    onDialogClose() {
      this.logUrl = "";
    },

// analysisi
passValues_analysis(showDialog, exp_id, file_name) {
  this.show_upload_dialog_analysis = showDialog;
  this.prop_exp_id_a=exp_id;
  this.prop_file_name_a=file_name;
},

    async addRow() {

      const id1= this.editedItem.uuid

      const type1 = this.type_biosp


      const type_id1=this.id_row

      const immortal1 = this.editedItem.immortal.toString()
      const source1 = this.editedItem.source.toString()
      const passage1 = this.editedItem.passage.toString()
      const transfected1 = this.editedItem.transfected
      const organism1 = this.editedItem.organism.toString()
      const subtype1 = this.editedItem.subtype.toString()
      const patient_id1 = this.editedItem.patient_id
      const distribution_id1 = this.editedItem.distribution_id
      const hyperlink1 = this.editedItem.hyperlink



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
      console.log(id + "oooo")
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

    data: [],
    markerDialog: false,
    markerImages: [],
    selectedExperimentId: null,
    selectedFileName: null,
    overlayMaskSrc: null,
    overlayImageSrc: null,
    overlayLoading: false,
  }),

  computed: {
    BASE_URL() {
    // Automatically detect the correct server base URL
    return window.location.hostname === 'localhost'
      ? 'http://localhost:6085' // Local development
      : `http://${window.location.hostname}:6085`; // Use dynamic IP
  },
  BASE_URL_IP() {
    // Automatically detect the correct server base URL
    return window.location.hostname === 'localhost'
      ? 'http://localhost' // Local development
      : `http://${window.location.hostname}`; // Use dynamic IP
  },
  formattedTransfected() {
    return this.props.row.transfected.join(', ');
  },
},

  mounted() {

  this.getExp(this.random_id);
  console.log(this.random_id,"random_id")
  },
  watch: {
    // Watch for changes in random_id and call getExp
    random_id(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.getExp(newVal);
      }
    },
  }


}
</script>

<style lang="sass" >
.q-table--dense
  .q-table
    th
      font-size: 15px
    td
      font-size: 15px
.q-input
  .label
      font-size: 15px



</style>

