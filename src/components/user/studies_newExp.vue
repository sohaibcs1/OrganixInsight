<template>


    <div>
      <div class="text-black" v-if="expShow">
        <div class="text-center q-mb-sm" >
      <q-btn rounded color="red" label="Cancel" icon-right="cancel" @click="refreshPage" ></q-btn>
      <!-- <q-btn label="check" @click="data1"></q-btn> -->
      <!-- {{ id_row }} -->
    </div>


        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="uuid" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0"
          class="q-table--dense" :pagination="pagination">

          <template v-slot:top>

            <div class="q-pa-sm q-gutter-sm fit">
                 <div class="text-h6 text-center bg-grey-6">Add New Exeperiment for Study "{{ study_name }}"</div>
                <q-card class="fit">
                  <q-card-section>

                    <div class="row " >
                      <q-input v-model="editedItem.uuid" label="Id:" hidden />
                      <q-input v-model="editedItem.study_id" label="Id:" hidden ></q-input>

                        <q-input class="fit" outlined  v-model="editedItem.experiment_name"  stack-label
                           dense label="Experiment Name"/><q-space />
                        <q-input class="fit q-mb-sm"  outlined  v-model="editedItem.experiment_description"  stack-label
                           dense label="Experiment Description"/><q-space />

                        <q-select class="fit q-mb-sm"  v-model="editedItem.ex_type" label="Experiment Type" :options="cvOptions" stack-label
                           dense outlined></q-select>

                        <q-input class="fit " outlined  v-model="editedItem.experiment_design_date"  stack-label
                          dense label="Experiment Design Date"/><q-space />

                    </div>
                  </q-card-section>
                  <!-- add Camra Details END -->

                  <q-card-actions align="center">
                    <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
                    <!-- <div class="text-center q-mr-lg"><q-btn  dense color="black" v-close-popup
                        label="Cancel"></q-btn></div> -->
                    <div class="text-center"><q-btn style="width: 100px;"  color="black"  label="ADD"
                        @click="addRow"></q-btn></div>
                  </q-card-actions>
                </q-card>
            </div>

          </template>



          <template v-slot:body="props">

            <q-tr :props="props" >

              <!-- <div @click="expShow=false; show_biospeciman=true" style="cursor: pointer;"></div> -->
              <q-td key="desc" :props="props">
                {{ props.row.experiment_name }}
              </q-td>

              <q-td key="one" :props="props">
                {{ props.row.ex_type  }}
               </q-td>

              <q-td key="four" :props="props">
                {{ props.row.experiment_description}}
              </q-td>
              <!-- <q-td key="five" :props="props">
                {{ props.row.experiment_notes  }}

              </q-td> -->
              <q-td key="six" :props="props">
                {{ props.row.experiment_design_date }}
              </q-td>


              <q-td key="actions" :props="props">
                <!-- <q-btn color="green" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn> -->
                <q-btn color="red" label="Delete"  @click="deleteItem(props.row)" size="15px" class="q-mr-sm"></q-btn>
                <q-btn color="black" label="Define Variable"  size="15px" @click="
                expShow=false; show_biospeciman=true" icon="directions" ></q-btn>

              </q-td>
            </q-tr>
          </template>
        </q-table>

        <!-- <div class="text-center q-mt-sm">
        <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

      </div> -->
      </div>



     <div v-if="show_biospeciman" class="text-left">
        <biospecimen class="fit" :value=callselectedExperemtnValu :exp_pass="data"></biospecimen>
      </div>

    </div>

  </template>

  <script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'
  import biospecimen from "src/components/user/biospecimen";


  const date = require('date-and-time')
  const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');

  const selectedExp=""

  const columns = [
    {
      name: 'desc',
      required: true,
      label: 'Experiment Name',
      align: 'center',
      field: row => row.experiment_name,
      format: val => `${val}`,
      sortable: true
    },
    { name: 'one', align: 'center', label: 'Control Vocab', field: 'ex_type', sortable: true },
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    { name: 'four', align: 'center', label: 'Description', field: 'experiment_description', sortable: true },
    { name: 'six', align: 'center', label: 'Design Date', field: 'experiment_design_date', sortable: true },
    { name: "actions", align: 'center', label: "Actions", field: "actions" }

  ]

  var listLocation=[]
  var listRoute=[]

  const stringOptionsOrganism= ['mouse','human']
  const stringOptionsSubtype= ['TNBC','LA','LB','HER2+','NM']
  const stringOptionsSource= ['mammary','pancreatic']
  const stringOptionsImmortal=  ['Yes', 'No' ]
  const stringOptionsPassage=['1','2','3','5','7','8','10']
  // const stringcvOptions= ['Simple Experiment','Doss Response 3D Dome LoRes','Doss Response 3D H.R.s','Doss Response 2D Monolayer']
  const stringcvOptions= ['3D non-quantitative Experiment','2D non-quantitative Experiment','2D Experiment','3D Experiment']

  var key


  export default {
    components:{biospecimen},

    props: {
    id_row: String, // Adjust the type accordingly if id_row is not a string.
    study_name: String, // Define other props as needed.
  },



    setup() {
      const cvOptions= ref(stringcvOptions)
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
      cvOptions,
      // ex_type:ref(null),
      expShow:true,
        show_biospeciman:ref(false),
        listLocation,
        listRoute,
        columns,
        show_dialog: ref(false),
        editedIndex: -1,
        userD: ref(false),
        callselectedExperemtnValu:"",
        editedItem: ref({
          uuid: ref(null),
          experiment_name: ref(null),
          experiment_description:"NA",
          experiment_notes:ref(null),
          ex_type:ref(null),
          experiment_design_date:TodatDate,
          study_id:ref(null),
        }),
        defaultItem: ref({
          uuid: ref(null),
          experiment_name: ref(null),
          experiment_description:"NA",
          experiment_notes:ref(null),
          ex_type:ref(null),
          experiment_design_date:TodatDate,
          study_id:ref(null),
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
    methods: {

      data1(){
        const a=this.data;
        console.log(a,"kkk")
      },


      refreshPage() {
      window.location.reload();
    },
      async addRow() {

        const id1= this.editedItem.uuid
        // console.log(id1)
        const experiment_name1 = this.editedItem.experiment_name
        const experiment_description1 = this.editedItem.experiment_description
        const experiment_notes1= this.editedItem.experiment_notes
        const experiment_design_date1=this.editedItem.experiment_design_date
        const ex_type1=this.editedItem.ex_type

        // const type1 = "Cell"
        // const type_id1 = this.editedItem.type_id
        this.editedItem.study_id=this.id_row
        const study_id1=this.editedItem.study_id
        // console.log(study_id1,"kk")
        // const immortal1 = this.editedItem.immortal

        // const source1 = this.editedItem.source.toString()
        // const passage1 = this.editedItem.passage.toString()
        // const transfected1 = this.editedItem.transfected
        // const organism1 = this.editedItem.organism.toString()
        // const subtype1 = this.editedItem.subtype.toString()
        // const role1 = this.editedItem.role
        // const role1 = this.editedItem.role.toString()
        // const assignedCamra1 = this.editedItem.assignedCamra.toString()
        // const assignedRoute1 = this.editedItem.assignedRoute.toString()

        // console.log( role1.constructor.name+"mmmmmmm")


        const editedIndex1 = this.editedIndex
        const oldRow = this.data[editedIndex1]
        const updatedRow = this.editedItem

        if (this.editedIndex > -1) {
          Object.assign(oldRow, updatedRow);
        } else {
          // console.log(experiment_name1,experiment_description1,experiment_notes1,experiment_design_date1,study_id1)
          if (experiment_name1 && experiment_description1  && experiment_design_date1 && study_id1 && ex_type1) {


           var response=await API("auth.create_obj_experimentCheck", { experiment_name: experiment_name1, experiment_description:experiment_description1,experiment_design_date:experiment_design_date1,study_id:study_id1 });
           if(response!="exist"){this.data.push(this.editedItem);this.callselectedExperemtnValu=this.data}
           else{
                this.warning_check=true;
                    this.$q.notify({
                    message: 'This experiment name already exist.',
                    color: 'red',
                    // icon: 'announcement',
                    multiLine: true,
                    progress: true,
                    actions: [{ label: 'Cancel', color: 'yellow', handler: () => { /* ... */ } }],
                    avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',

                  })
              }
          }
          else {
            this.$q.notify({
              message: 'please Enter all Details.',
              color: 'red',
              icon: 'announcement',
              icon: 'announcement',
              multiLine: true,
              progress: true,
              actions: [{ label: 'Cancel', color: 'yellow', handler: () => { /* ... */ } }],

            })
          }
        }
        // this.close()




      },

      async deleteItem(item) {
        // console.log(id + "oooo")

        const index = this.data.indexOf(item);
        confirm("Are you sure you want to Delete this user?") &&
        this.data.splice(index, 1) ;
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
    //   if (this.id_row !== null) {
    //   this.editedItem.study_id = this.id_row;
    // }

    // API("auth.createArirports", { name:"DeliAir", latLong:"-873.45",noOfRunWay:"3",typesOfAircraft:"full",runWayConstType:"simple",AtcFacility:"fine",refuling:"ok" });
      // console.log(key)
      // key=this.id_row
      // console.log(key)
    //   API('auth.ExperimentDetials_id',{key}).then(res => {
    //     this.data = res
    //     // console.log(res+"dsfsdf" )
    //   })

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

