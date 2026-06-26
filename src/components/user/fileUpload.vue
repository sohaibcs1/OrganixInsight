<template>

  <!--
  Forked from:
  https://quasar.dev/vue-components/table#Example--Popup-editing
-->
  <div>
    <div class="q-pa-sm q-gutter-sm" v-if="uploadactivity">
      <div class="text-h6 text-center text-black bg-grey-6">Image Upload</div>
      <!-- {{ exp_pass_uploadImg }} -->
      <!-- <div>sdfjkkj</div> -->
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

      <q-table title="Treats" :rows="filteredRows" :columns="filteredColumns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
        binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
        class="q-table--dense" :pagination="pagination">
        <template v-slot:top>

          <div class="q-pa-sm q-gutter-sm">


            <q-dialog v-model="show_dialog">
              <q-card  text-center>
                <q-card-section>

                  <div class="text-h6 text-center bg-grey-5">Biospecimen {{ id_row }} Attributes</div>
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
                  <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
                  <!-- <div class="text-center q-mr-lg"><q-btn  dense color="black" v-close-popup
                      label="Cancel"></q-btn></div>
                  <div class="text-center"><q-btn  dense color="black" v-close-popup label="OK"
                      @click="addRow"></q-btn></div> -->
                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>

        </template>


        <template v-slot:body-cell-mergedHarvestTime="props">
      <q-td :props="props" >
        {{ mergedHarvestTime[props.rowIndex] }}
      </q-td>
    </template>
    <template v-slot:body-cell-microscope="props">
      <q-td :props="props" >
        {{ microscope[props.rowIndex] }}
      </q-td>
    </template>

        <template v-slot:body-cell-actions="props">
        <q-td :props="props" >
          <!-- <q-btn icon="cloud_upload" label="upload"  size="10px" dense @click="passValues(true, props.row.uuid, props.row.study_id,props.row.phase_info, props.row.ex_type)"></q-btn> -->
          <q-btn
      icon="cloud_upload"
      label="upload"
      size="10px"
      dense
      @click="passValues({
        uuid: props.row.uuid,
        study_id: props.row.study_id,
        phase_info: props.row.phase_info,
        ex_type: props.row.ex_type,
        status: true
      })">
    </q-btn>
        </q-td>
    </template>
        <!-- <template v-slot:body="props">
          <q-tr :props="props">

            <q-td key="desc" :props="props" v-if="props.row.uuid">
              {{ props.row.uuid }}
            </q-td>

            <q-td key="one" :props="props" v-if="props.row.study_id">
              {{ props.row.study_id }}
            </q-td>

            <q-td key="two" :props="props" v-if="props.row.experiment_name">
              {{ props.row.experiment_name}}
            </q-td>
            <q-td key="three" :props="props" v-if="props.row.experiment_design_date">
              {{ props.row.experiment_design_date }}

            </q-td>


            <q-td key="three1" :props="props" v-if="props.row.name">
              {{ props.row.name }}

            </q-td>
            <q-td key="four" :props="props" v-if="props.row.primary">
              {{ props.row.primary }}
            </q-td>
            <q-td key="five" :props="props" v-if="props.row.secondary">
              {{ props.row.secondary }}
            </q-td>

            <q-td key="six" :props="props" v-if="props.row.treatment_group">
              {{ props.row.treatment_group }}
            </q-td>


            <q-td key="actions" :props="props">
              <q-btn label="upload" size="12px" dense @click="passValues(true, props.row.uuid, props.row.study_id)"></q-btn>
            </q-td>
          </q-tr>
        </template> -->
      </q-table>

      <div class="text-center">

        <!-- <q-btn color="dark" style="min-width:210px ;" @click="visulizedata=true; uploadactivity=false;" label="Visulize Data" icon-right="skip_next" class="q-mt-sm q-mr-lg q-mt-2" ></q-btn> -->
        </div>

    </div>
    <div v-if="visulizedata">
    <visulizesingle :random_expts_id="exp_pass_uploadImg"></visulizesingle>
    </div>
    <!-- <div class="text-center q-mt-sm">
      <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
          <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

    </div> -->
    <q-dialog v-model="show_upload_dialog" >
        <q-card >

          <!-- add Camra Details Start -->
          <q-card-section align="center" >
            <div class="row text-center">
              <!-- Define attributes table -->
              <uploadbtn :passUuid="prop_uuid"  :passStudy_id="prop_st_id" :pro_phase_info="pro_phase_info" :passEx_type="pro_ex_type" ></uploadbtn>
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
import uploadbtn from 'src/components/user/uploadbtn';
import visulizesingle from 'src/components/user/visulizeSingle';

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
    label: 'Experiment ID',
    align: 'center',
    field: row => row.uuid,
    format: val => `${val}`,
    sortable: true
  },
  // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
  // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
  // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
  { name: 'one', align: 'center', label: 'study ID', field: 'study_id', sortable: true },
  { name: 'two', align: 'center', label: 'experiment_name', field: 'experiment_name', sortable: true },
  { name: 'three', align: 'center', label: 'experiment_design_date', field: 'experiment_design_date', sortable: true },
  // { name: 'three11', align: 'center', label: 'Time', field: 'time', sortable: true },
    // { name: 'three22', align: 'center', label: 'Unit Harvest', field: 'unit_harvest', sortable: true },
  { name: 'three1', align: 'center', label: 'name', field: 'name', sortable: true },
  { name: 'four', align: 'center', label: 'primary', field: 'primary', sortable: true },
  { name: 'five', align: 'center', label: 'secondary', field: 'secondary', sortable: true },
  { name: 'six', align: 'center', label: 'treatment_group', field: 'treatment_group', sortable: true },
  // { name: 'six', align: 'center', label: 'passage', field: 'passage', sortable: true },
  // { name: 'seven', align: 'center', label: 'organism', field: 'organism', sortable: true },
  // { name: 'eight', align: 'center', label: 'transfected', field: 'transfected', sortable: true },
  // { name: 'nine', align: 'center', label: 'Hyperlink', field: 'hyperlink', sortable: true },
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

  },

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
      rowsPerPage: 200 // current rows per page being displayed
    },

     modelstudyid:ref(null),
    //Search Study Start
      model: ref(null),
      modelexp: ref(null),
      stringOptions,
      pro_phase_info:ref(null),
      pro_ex_type:ref(null),
      stringOptionsexp,
      options,
      optionsexp,

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
    visulizedata:ref(false),
    prop_uuid:ref(null),
    prop_st_id:ref(null),
    show_upload_dialog:ref(false),
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
  components: {uploadbtn,visulizesingle},
  methods: {

    async getExp(){
      const key = this.modelexp.value;
      // console.log(key)
      API('auth.ExperimentDetials_randomid', { key }).then(res => {
        this.data = res;
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
//     passValues(showDialog, uuid, studyId,phase_info,ex_type) {
//   this.show_upload_dialog = showDialog;
//   this.prop_uuid=uuid;
//   this.prop_st_id=studyId;
//   this.pro_phase_info=phase_info;
//   this.pro_ex_type=ex_type;
// // console.log(  this.prop_uuid,this.prop_st_id)
// },
passValues(data) {
    console.log("Received Data:", data);

    // Access values using object keys
    const { status, uuid, study_id, phase_info, ex_type } = data;
      this.show_upload_dialog = status;
      this.prop_uuid=uuid;
      this.prop_st_id=study_id;
      this.pro_phase_info=phase_info;
      this.pro_ex_type=ex_type;
      console.log("Updated Props:", this.prop_uuid, this.prop_st_id, this.pro_phase_info, this.pro_ex_type);

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
      key !== 'unit_drug'&&
      key !== 'concentration'&&
      key !== 'passage'&&
      key !== 'unit_harvest'&&
      key !== 'time' && key !== 'comment_drug') {
      // Check if any row has a null value for the current column
      const hasNull = this.data.some(row => row[key] === null);

      if (!hasNull) { // Only include the column if there are no null values
        columns.push({
          name: key,
          align: 'center',
          label: key,
          field: key,
          sortable: true,
        });
      }
    }


  }

    // Add a new column for "Harvest Time + Time Unit"
     if (this.data.length > 0 && this.data[0].hasOwnProperty('time')&& this.data[0].time) {
        // 'time' property exists, add the new column
        columns.push({
          name: 'mergedHarvestTime',
          align: 'center',
          label: 'Harvest Time',
          field: 'mergedHarvestTime',
          sortable: true,
          // You can customize additional properties as needed
        });
      }

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

  columns.push({
    name: 'actions',
    align: 'center',
    label: 'actions',
    field: 'actions',
    sortable: true,
  });
  return columns;
}

},

  mounted() {

      // let key = this.exp_pass_uploadImg[0].study_id;
    let key=this.exp_pass_uploadImg
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

      API('auth.study_details').then(res => {
      const optionsArray = res.map(item => {
        return { label: item.name, value: item.uuid };
      });
      stringOptions = optionsArray;
      console.log(res, "dsfsdf");
    })



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

