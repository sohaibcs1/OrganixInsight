<template>

  <!--
  Forked from:
  https://quasar.dev/vue-components/table#Example--Popup-editing
-->
  <div>
    <div class="q-pa-sm q-gutter-sm">
      <!-- <q-btn label="server check" @click="call_serverfunction_processf"></q-btn> -->
      <div class="text-h6 text-center text-black bg-grey-6 ">Heatmap</div>

            <!-- Select Study -->
            <div class="text-center" >
      <q-select
        filled
        v-model="model"
        use-input
        input-debounce="0"
        label="Select Study"
        :options="options"
        @filter="filterFn"
        
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
      <q-btn label="Search" class="q-mt-sm text-black" @click="handleButtonClick" /> 
    </div>
       <!-- Select Study END -->

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
      <!-- {{ selected }} -->
      <q-table  :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="k-id" max-width="100%"
        binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
        class="q-table--dense" :pagination="pagination"  selection="multiple" v-model:selected="selected" >


      <template v-slot:body-cell-desc="props">
        <q-td key="desc" :props="props">
             <!-- <div><q-badge color="green" v-if="props.row.uuid"> Experiment Id: {{ props.row.uuid }}</q-badge></div>  -->
             <!-- <div><q-badge color="green" v-if="props.row.experiment_name"> experiment Name: {{ props.row.experiment_name}}</q-badge></div>  -->
              <!-- <div><q-badge color="green" v-if="props.row.experiment_design_date"> experiment design date: {{ props.row.experiment_design_date}}</q-badge></div>  -->
              <!-- <q-badge color="primary" v-if="props.row.experiment_design_date">{{ props.row.experiment_design_date}}</q-badge> -->
              <q-badge color="secondary" v-if="props.row.name">{{ props.row.name }}</q-badge>
                <q-badge color="red" v-if="props.row.time"> {{ props.row.time }} {{ props.row.unit_harvest }}</q-badge>
                <!-- <q-badge color="warning" v-if="props.row.type"> type: {{ props.row.type }}</q-badge> -->
                <q-badge color="accent" v-if="props.row.counterstain"> counterstain: {{ props.row.counterstain }}</q-badge>
                <q-badge color="dark" v-if="props.row.drug"> drug: {{ props.row.drug }} {{  props.row.concentration }}{{ props.row.unit_drug }}</q-badge>
                <q-badge color="positive" v-if="props.row.primary"> Primary: {{ props.row.primary  }}</q-badge>
                <q-badge color="teal" v-if="props.row.secondary"> Secondary: {{ props.row.secondary }}</q-badge>
                <!-- <q-badge color="info" v-if="props.row.treatment_group"> treatment group: {{ props.row.treatment_group }}</q-badge> -->
                <!-- <q-badge color="black" v-if="props.row.treatment_group"> Exp: {{props.row.files[0].experiment_id }}</q-badge> -->

                
              
            </q-td>

    </template>



        <template v-slot:body-cell-actions="props">
                <q-td key="actions" :props="props">
                <div >
                <q-img  :src="`http://134.197.75.35:6085/${props.row.files[0].max_encrypt_image}`" spinner-color="white" style="height: 50px; width: 50px ;border: 1px solid #ccc;"/>
            
              </div> 
                
              </q-td>
        </template>
<!-- 
          <template v-slot:body-cell-heatmap="props">
            <q-td key="heatmap" :props="props">
                    <q-btn @click="show_heatmap=true">heatmap</q-btn>
                  </q-td>   
          </template> -->

      </q-table>
    </div>
      <div class="text-center q-mt-sm q-mb-sm" v-if="selected.length > 0"> <q-btn @click="dialogHeatmap">Generate heatmap</q-btn></div> 
    <!-- <div class="text-center q-mt-sm">
      <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
          <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

    </div> -->
    <q-dialog v-model="show_heatmap">
  <q-card style="background-color: #F5F5F5; max-width: 2000px;width: 2000px;" class="q-dialog-plugin q-dialog-centered">
    <q-card-section class="text-center">
      <div class="text-weight-thin">Heatmap</div>
      <q-img
        :src="'data:image/png;base64,' + base64Image"
        fit
        width="600px"
        height="600px"
        class="q-ma-md"
      />
    </q-card-section>

    <q-card-section class="text-center">
      <div class="text-weight-thin">Heatmap Details</div>
      <q-table
        :rows="tableRows1"
        :columns="tableColumns"
        row-key="experiment_id"
        flat
        bordered
        dense
        style="font-size: 12px;"
        :rows-per-page-options="[20]"
      />
    </q-card-section>
  </q-card>
</q-dialog>



    <q-dialog v-model="show_upload_dialog" >
        <q-card >
  
          <!-- add Camra Details Start -->
          <q-card-section align="center" >
            <div class="row text-center">
              <!-- Define attributes table -->
              <moreImages :experiment_id="response"  :file_name="prop_file_name" ></moreImages>
              
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
import moreImages from 'src/components/user/analysis_details.vue';



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
    label: 'Experiment Factors',
    align: 'center',
    field: row => row.uuid,
    format: val => `${val}`,
    sortable: true
  },
  // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
  // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
  // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
  // { name: 'one', align: 'center', label: 'study ID', field: 'study_id', sortable: true },
  // { name: 'two', align: 'center', label: 'experiment_name', field: 'experiment_name', sortable: true },
  // { name: 'three', align: 'center', label: 'experiment_design_date', field: 'experiment_design_date', sortable: true },
  // { name: 'three1', align: 'center', label: 'name', field: 'name', sortable: true },
  // { name: 'four', align: 'center', label: 'primary', field: 'primary', sortable: true },
  // { name: 'five', align: 'center', label: 'secondary', field: 'secondary', sortable: true },
  // { name: 'six', align: 'center', label: 'treatmengetSelectedDatat_group', field: 'treatment_group', sortable: true },
  // { name: 'six', align: 'center', label: 'passage', field: 'passage', sortable: true },
  // { name: 'seven', align: 'center', label: 'organism', field: 'organism', sortable: true },
  // { name: 'eight', align: 'center', label: 'transfected', field: 'transfected', sortable: true },
  // { name: 'nine', align: 'center', label: 'Hyperlink', field: 'hyperlink', sortable: true },
  { name: "actions", align: 'center', label: "Image", field: "actions" },
  // { name: "heatmap", align: 'center', label: "Heatmaap", field: "heatmap" }

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


  // props: {
  // exp_pass_uploadImg:Array,

  // },

  setup() {
    const selected = ref([])
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
      rowsPerPage: 14// current rows per page being displayed
    },
    options,
    optionsexp,
    base64Image:'',
    selected,
    
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
    show_upload_dialog:ref(false),
    show_heatmap:ref(false),
    table_json:ref(''),
      listLocation,
      listRoute,
      modelPrediction:null,
      columns,
      experiments:[],
      response:"",
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
      loading: false,

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
  components: {moreImages},
  methods: {

    async dialogHeatmap(){
      const response1= this.selected.map(item => ({
        label: item.name + " " + item.unit_harvest + " " + item.time,
          experiment_id: item.files[0].experiment_id,
          file_name: item.files[0].file_name
        
      }));
      const response1String = JSON.stringify(response1);
      const res = await API('auth.getmodelanalysi',response1String);
      console.log(res,"aaaaaaaa++++")
      this.table_json=res
      // Ensure the response is an array before proceeding
      if (Array.isArray(res)) {
      //   const maskFileAnalysisArray = res.map(item => item.mask_file_analysis);
      //   const labelArray = res.map(item => item.label);
      //   console.log('maskFileAnalysisArray:', maskFileAnalysisArray);
      //   console.log('labelArray:', labelArray);
      // //Send to server  
 
        const sendToserver = await API('home.getHeatmap',res);
        this.base64Image=sendToserver

        this.show_heatmap=true;
      } 


    },

  // async call_paraview(file,name){

      
  //   await API('auth.getmodelfiles',{name}).then(res => {
  //     this.modelPrediction=JSON.stringify(res.model_prediction_files);
  //     console.log(this.modelPrediction)
  //   })

  //   file.loading=true;
  //   // const someVariable="4bb90dff_connected_components.vtp"

  //   API('home.getParaviewUrl',this.modelPrediction).then(res => {
  //   console.log(res,"server response receive");
  //   const paraviewUrl = res.url;
  //   console.log(paraviewUrl)
  //   setTimeout(() => {
  //     window.open(paraviewUrl, '_blank');
  //     file.loading = false; 
  //   }, 6000); // 5000 milliseconds = 5 seconds


  //   })
  //   },

  async call_analysis(file, name) {
    try {
        file.loading = true; // Set loading to true
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
            file.loading = false; // Set loading to false after two seconds
        }, 3000); // 2000 milliseconds = 2 seconds
    }
},

    async getExp(){
      const key = this.modelexp.value;
      // console.log(key)
      const experimentDetailsPromise = API('auth.ExperimentDetials_randomid',{key});
      const fileDetailsPromise = API('auth.file_details_middel');

      Promise.all([experimentDetailsPromise, fileDetailsPromise])
        .then(([experimentDetails, fileDetails]) => {
          // Combine the data here
          const combinedData = this.combineData(experimentDetails, fileDetails);

          // Assign combinedData to this.data or use it as needed
          this.data = combinedData;

          // console.log(combinedData, "Combined Data");
          this.$q.notify({
          message: 'Experiments Loaded',
          color: 'positive',
          position: 'top',
          timeout: 2000 // Optional: set how long the notification should be displayed
        });

        })
        .catch(error => {
          console.error(error);
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
  //   getMaxEncryptImage(files) {
  //   if (files && files.length > 0) {
  //     return files[0].file_name; // Assuming you want the first max_encrypt_image
  //   }
  //   return '';
  // },


//     combineData(experimentDetails, fileDetails) {
//   const combinedData = experimentDetails.map(experiment => {
//     const experimentId = experiment.uuid.toString(); // Assuming uuid is a number
//     const experimentFiles = fileDetails.filter(file => file.experiment_id === experimentId);
//     return { ...experiment, files: experimentFiles };
//   });

//   return combinedData;
// },
generateKID() {
  return 'k-' + Math.random().toString(36).substr(2, 9); // Generate a random k-id
},

// combineData(experimentDetails, fileDetails) {
//   const combinedData = [];
  
//   experimentDetails.forEach(experiment => {
//     const experimentId = experiment.uuid.toString(); // Assuming uuid is a number
//     const experimentFiles = fileDetails.filter(file => file.experiment_id === experimentId);
    
//     const combinedExperiment = { ...experiment }; // Clone the experiment details
//     combinedExperiment.files = experimentFiles; // Add the files array to the experiment
//     combinedExperiment['k-id'] = this.generateKID(); // Add a random k-id
//     combinedData.push(combinedExperiment); // Push the combined data to the result array
//   });

//   return combinedData;
// }
combineData(experimentDetails, fileDetails) {
  try {
    if (!Array.isArray(experimentDetails) || !Array.isArray(fileDetails)) {
      throw new Error("Invalid input: experimentDetails and fileDetails must be arrays.");
    }

    const combinedData = [];

    experimentDetails.forEach(experiment => {
      if (!experiment || typeof experiment.uuid === 'undefined') {
        console.error("Invalid experiment entry:", experiment);
        return; // Skip invalid experiment entries
      }

      const experimentId = experiment.uuid.toString(); // Assuming uuid is a number or string
      const experimentFiles = fileDetails.filter(file => {
        if (!file || typeof file.experiment_id === 'undefined') {
          console.error("Invalid file entry:", file);
          return false; // Skip invalid file entries
        }
        return file.experiment_id === experimentId;
      });

      const combinedExperiment = { ...experiment }; // Clone the experiment details
      combinedExperiment.files = experimentFiles; // Add the files array to the experiment
      combinedExperiment['k-id'] = this.generateKID(); // Add a random k-id
      combinedData.push(combinedExperiment); // Push the combined data to the result array
    });

    return combinedData;

  } catch (error) {
    console.error("Error combining data:", error.message);
    return []; // Return an empty array or handle as needed
  }
}

,


  passValues(showDialog, exp_id, file_name) {
  
    setTimeout(() => {
    this.show_upload_dialog = showDialog;
    this.prop_exp_id = exp_id;
    this.prop_file_name = file_name;
  }, 3000);
},

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
    },
    tableRows(details) {
      return Object.entries(details).map(([key, value]) => ({ key, value }));
    }
  },

  data: () => ({

    data: []

  }),

  computed: {
  formattedTransfected() {
    // Format the 'props.row.transfected' as needed
    // For example, to display a comma-separated string: "1, 8, 7, 3"
    return this.props.row.transfected.join(', ');
  },
  tableRows1() {
      return this.table_json.map(item => {
        const details = JSON.parse(item.mask_file_analysis);
        return {
          // experiment_id: item.experiment_id,
          label: item.label,
          Nuclear_Elongation: details['Nuclear Elongation'],
          Nuclear_Flatness: details['Nuclear Flatness'],
          Nuclear_Volume: details['Nuclear Volume'],
          Colony_Elongation: details['Colony Elongation'],
          Colony_Flatness: details['Colony Flatness'],
          Colony_total_Cells: details['Number of Cells in Colony'],
          Colony_Diameter: details['Colony Diameter'],
          Colony_Radius: details['Colony Radius'],
          Max_Neighbourhood_Distance: details['Max Neighbourhood Distance'],
          Mean_Neighbourhood_Distance: details['Mean Neighbourhood Distance'],
          Volume_of_Colony_Convex_Hull: details['Volume of Colony Convex Hull'],
          Lumen_Volume: details['Lumen Volume'],
        };
      });
    }
},

  mounted() {

    // this.$q.dialog({
    //   title: 'Welcome!',
    //   message: '3D Viewer Module is Under Development.',
    //   persistent: true, // Set to false if you want the user to close it
    // });
   
  const experimentDetailsPromise = API('auth.experiment_details');
  const fileDetailsPromise = API('auth.file_details_middel');

  Promise.all([experimentDetailsPromise, fileDetailsPromise])
    .then(([experimentDetails, fileDetails]) => {
      // Combine the data here
      const combinedData = this.combineData(experimentDetails, fileDetails);

      // Assign combinedData to this.data or use it as needed
      this.data = combinedData;
      this.files=combinedData;
      console.log(combinedData, "Combined Data");
    })
    .catch(error => {
      console.error(error);
    });

    API('auth.study_details').then(res => {
      const optionsArray = res.map(item => {
        return { label: item.name, value: item.uuid };
      });
      stringOptions = optionsArray;
      console.log(res, "dsfsdf");
    })
    //   API('auth.experiment_details').then(res => {
    //   this.data = res
    //   console.log(res,"dsfsdf" )
    // })

    // API('auth.file_details_middel').then(res => {
  
    //   console.log(res,"dsfsdf_middel")
    // })


    // console.log(this.experiments);
    
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

