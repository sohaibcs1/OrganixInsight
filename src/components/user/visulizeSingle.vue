<template>

    <!--
    Forked from:
    https://quasar.dev/vue-components/table#Example--Popup-editing
  -->
    <div>
      <div class="q-pa-sm q-gutter-sm">
        <!-- <q-btn label="server check" @click="call_serverfunction_processf"></q-btn> -->
        <div class="text-h6 text-center text-black bg-grey-6">Image Viewer</div>
        <!-- {{ exp_pass_uploadImg }} -->
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
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



          <template v-slot:body="props">
            <q-tr :props="props">

              <q-td key="desc" :props="props">
               <!-- <div><q-badge color="orange">Study Id: {{ props.row.study_id }}</q-badge></div>  -->
               <div><q-badge color="green"> Experiment Id: {{ props.row.uuid }}</q-badge></div>
               <div><q-badge color="green"> experiment Name: {{ props.row.experiment_name}}</q-badge></div>
                <div><q-badge color="green"> experiment design date: {{ props.row.experiment_design_date}}</q-badge></div>

                <!-- <div><q-badge color="blue"> Time: {{ props.row.time }}</q-badge></div>
                <div><q-badge color="blue"> Time Unit: {{ props.row.unit_harvest }}</q-badge></div> -->

                <div><q-badge color="purple"> Name: {{ props.row.name }}</q-badge></div>
                <div><q-badge color="purple"> passage: {{ props.row.passage }}</q-badge></div>
                <div><q-badge color="purple"> costain: {{ props.row.costain }}</q-badge></div>
                <div><q-badge color="purple"> type: {{ props.row.type }}</q-badge></div>
                <div><q-badge color="primary"> counterstain: {{ props.row.counterstain }}</q-badge></div>
                <div><q-badge color="primary"> drug: {{ props.row.drug }} {{  props.row.concentration }}{{ props.row.unit_drug }}</q-badge></div>
                <div><q-badge color="teal"> Primary: {{ props.row.primary  }}</q-badge></div>
                <div><q-badge color="teal"> Secondary: {{ props.row.secondary }}</q-badge></div>
                  <div><q-badge color="teal"> treatment group: {{ props.row.treatment_group }}</q-badge></div>




              </q-td>

              <!-- <q-td key="one" :props="props">
                {{ props.row.study_id }}
              </q-td>

              <q-td key="two" :props="props">
                {{ props.row.experiment_name}}
              </q-td>
              <q-td key="three" :props="props">
                {{ props.row.experiment_design_date }}

              </q-td> -->
              <!-- <q-td key="three1" :props="props">
                {{ props.row.name }}

              </q-td>
              <q-td key="four" :props="props">
                {{ props.row.primary }}
              </q-td>
              <q-td key="five" :props="props">
                {{ props.row.secondary }}
              </q-td>

              <q-td key="six" :props="props">
                {{ props.row.treatment_group }}
              </q-td> -->


              <q-td key="actions" :props="props">
                <!-- <q-btn color="black" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn> -->
                <!-- <q-btn label="upload" size="12px" dense @click="passValues(true, props.row.uuid, props.row.study_id)"></q-btn> -->

                <div class="row">

                <div v-for="file in props.row.files" :key="file.file_name" class="q-mr-lg text-center">

                  <div  @click="passValues(true, props.row.uuid, file.file_name)" >

                    <!-- {{file.max_encrypt_image}} -->
                      <!-- <q-img :src="`http://127.0.0.1:6080/${file.max_encrypt_image.replace(/\\/g, '/')}`" spinner-color="white" style="height: 200px; width: 200px ;border: 1px solid #ccc;"/> -->

                      <q-img :src="`http://127.0.0.1:6085/${file.max_encrypt_image}`" spinner-color="white" style="height: 200px; width: 200px ;border: 1px solid #ccc;"/>
                    <q-tooltip>
                      {{ file.file_name }}
                    </q-tooltip>
                    <div class="bg-blue">Click More..</div>
                  </div>

              </div>


              </div>

              </q-td>
            </q-tr>
          </template>
        </q-table>
      </div>

      <!-- <div class="text-center q-mt-sm">
        <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

      </div> -->
      <q-dialog v-model="show_upload_dialog" >
          <q-card style="width: 2000px; max-width: 2000px">

            <!-- add Camra Details Start -->
            <q-card-section align="center" >
              <div class="row text-center">
                <!-- Define attributes table -->
                <moreImages :experiment_id="prop_exp_id"  :file_name="prop_file_name" ></moreImages>

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
  import moreImages from 'src/components/user/moreImages';



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
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    // { name: 'one', align: 'center', label: 'study ID', field: 'study_id', sortable: true },
    // { name: 'two', align: 'center', label: 'experiment_name', field: 'experiment_name', sortable: true },
    // { name: 'three', align: 'center', label: 'experiment_design_date', field: 'experiment_design_date', sortable: true },
    // { name: 'three1', align: 'center', label: 'name', field: 'name', sortable: true },
    // { name: 'four', align: 'center', label: 'primary', field: 'primary', sortable: true },
    // { name: 'five', align: 'center', label: 'secondary', field: 'secondary', sortable: true },
    // { name: 'six', align: 'center', label: 'treatment_group', field: 'treatment_group', sortable: true },
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
    random_expts_id:String,

    },

    setup() {
      const $q = useQuasar()
      const optionsOrganism= ref(stringOptionsOrganism)
      const optionsSource=ref(stringOptionsSource)
      const optionsImmortal=ref(stringOptionsImmortal)
      const optionsPassage= ref(stringOptionsPassage)
      const optionsSubtype= ref(stringOptionsOrganism)

      return {
        pagination: {
        rowsPerPage: null // current rows per page being displayed
      },
      prop_exp_id:ref(null),
      prop_file_name:ref(null),
      show_upload_dialog:ref(false),
        listLocation,
        listRoute,
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

    //   getMaxEncryptImage(files) {
    //   if (files && files.length > 0) {
    //     return files[0].file_name; // Assuming you want the first max_encrypt_image
    //   }
    //   return '';
    // },


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
  // console.log(  this.prop_exp_id,this.prop_file_name)
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
  },

    mounted() {
      const key= this.random_expts_id
      const experimentDetailsPromise = API('auth.ExperimentDetials_id',{key});
    const fileDetailsPromise = API('auth.file_details_middel');

    Promise.all([experimentDetailsPromise, fileDetailsPromise])
      .then(([experimentDetails, fileDetails]) => {
        // Combine the data here
        const combinedData = this.combineData(experimentDetails, fileDetails);

        // Assign combinedData to this.data or use it as needed
        this.data = combinedData;

        console.log(combinedData, "Combined Data");
      })
      .catch(error => {
        console.error(error);
      });

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

