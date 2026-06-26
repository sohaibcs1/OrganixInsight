<template>

    <!--
    Forked from:
    https://quasar.dev/vue-components/table#Example--Popup-editing
  -->
    <div>
        <!-- <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section> -->

      <div class="q-pa-sm q-gutter-sm text-black" v-if="expShow" >
        <div class="text-h6 text-left" >Harvest Time: </div>
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
          class="q-table--dense" :pagination="pagination">
          <template v-slot:top> 

            <div class="q-pa-sm q-gutter-sm">
            
  
              <q-dialog v-model="show_dialog">
               
                <q-card style="background-color: #F5F5F5" text-center>
                 
                  
                  <q-card-section>
                    
                    <div class="text-h6 text-center bg-grey-5">Add/Edit Exeperiment for Study "{{ study_name }}" </div>
                  </q-card-section>
  
                  <!-- add Camra Details Start -->
                  <q-card-section>
                
       
                    
                    <div class="row ">
                      <q-input v-model="editedItem.uuid" label="Id:" hidden />

                        <q-input class="fit" outlined  v-model="editedItem.experiment_name"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Experiment Name"/><q-space />
                        <q-input type="textarea" class="fit" outlined  v-model="editedItem.experiment_description"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Experiment Description"/><q-space />
                        <!-- <q-input type="textarea" class="fit"  outlined  v-model="editedItem.experiment_notes"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Experiment Notes"/><q-space /> -->
                        <q-input outlined class="fit" v-model="editedItem.experiment_design_date"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Experiment Design Date"/><q-space />
                        
                    </div>
                  </q-card-section>
                  <!-- add Camra Details END -->
  
                  <q-card-actions align="center">
                    <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
                    <div class="text-center q-mr-lg"><q-btn  dense color="black" v-close-popup
                        label="Cancel"></q-btn></div>
                    <div class="text-center"><q-btn  dense color="black" v-close-popup label="OK"
                        @click="addRow"></q-btn></div>
                  </q-card-actions>
                </q-card>
              </q-dialog>
            </div>
  
          </template>

   
  
          <template v-slot:body="props">
            <q-tr :props="props">
              
              <q-td key="desc" :props="props">
                {{ props.row.time }}
              </q-td>
  
              <!-- <q-td key="one" :props="props">
                {{ props.row.time }}  
              </q-td>
               -->
              <q-td key="two" :props="props">
                {{ props.row.unit_harvest }}
              </q-td>
             
              <!-- <q-td key="three22" :props="props">
                {{ props.row.unit_harvest }}
               
              </q-td> -->
            
       
  
              <!-- <q-td key="actions" :props="props">
                <q-btn color="black" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn>
                <q-btn label="upload" size="12px" dense @click="passValues(true, props.row.uuid, props.row.study_id)"></q-btn>
              </q-td> -->
            </q-tr>
          </template>
        </q-table>
      
        <!-- <div class="text-center q-mt-sm">
        <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

      </div> -->
      </div>

      

     <div v-if="show_biospeciman" class="text-left">
        <biospecimen class="fit"></biospecimen>
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
  
  
  const columns = [
  {
      name: 'desc',
      required: true,
      label: 'Time',
      align: 'center',
      field: row => row.time,
      format: val => `${val}`,
      sortable: true
    },
    // { name: 'one', align: 'center', label: 'Time', field: 'time', sortable: true },
    { name: 'two', align: 'center', label: 'UNIT', field: 'unit_harvest', sortable: true },
    // { name: 'three', align: 'center', label: 'comment', field: 'experiment_design_date', sortable: true },


  ]
  
  var listLocation=[]
  var listRoute=[]
   
  const stringOptionsOrganism= ['mouse','human']
  const stringOptionsSubtype= ['TNBC','LA','LB','HER2+','NM']
  const stringOptionsSource= ['mammary','pancreatic']
  const stringOptionsImmortal=  ['Yes', 'No' ]
  const stringOptionsPassage=['1','2','3','5','7','8','10']
  
  var key
  
  export default {
    components:{biospecimen},
  
    props: ['id_row','study_name'],
  
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
      expShow:true,
        show_biospeciman:ref(false),
        listLocation,
        listRoute,
        columns,
        show_dialog: ref(false),
        editedIndex: -1,
        userD: ref(false),
        editedItem: ref({
          uuid: ref(null),
          experiment_name: ref(null),
          experiment_description:"NA",
          experiment_notes:ref(null),
          experiment_design_date:TodatDate,
        }),
        defaultItem: ref({
          uuid: ref(null),
          experiment_name: ref(null),
          experiment_description:"NA",
          experiment_notes:ref(null),
          experiment_design_date:TodatDate,
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
  

  
      async addRow() {
  
        const id1= this.editedItem.uuid
        // console.log(id1)
        const experiment_name1 = this.editedItem.experiment_name
        const experiment_description1 = this.editedItem.experiment_description
        const experiment_notes1= this.editedItem.experiment_notes
        const experiment_design_date1=this.editedItem.experiment_design_date

        // const type1 = "Cell"
        // const type_id1 = this.editedItem.type_id
        const study_id1=this.id_row
        // console.log(study_id1,"bbbb")
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
          Object.assign(oldRow, updatedRow) && API("auth.update_experiment", { id1: id1,experiment_name: experiment_name1,experiment_description:experiment_description1, experiment_design_date: experiment_design_date1,study_id:study_id1});
        } else {
          // console.log(experiment_name1,experiment_description1,experiment_notes1,experiment_design_date1,study_id1)
          if (experiment_name1 && experiment_description1  && experiment_design_date1 && study_id1 ) {
            
            var response=await API("auth.create_obj_experiment", { experiment_name: experiment_name1,experiment_description:experiment_description1, experiment_design_date: experiment_design_date1,study_id:study_id1});
            if(response!="exist"){this.data.push(this.editedItem)}
            else{
                  this.$q.notify({
                  message: 'Already Exist.',
                  color: 'red',
                  icon: 'announcement',
                })
             }
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
        this.data.splice(index, 1) && await API('auth.deleteExperiment', { id });
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
    // API("auth.createArirports", { name:"DeliAir", latLong:"-873.45",noOfRunWay:"3",typesOfAircraft:"full",runWayConstType:"simple",AtcFacility:"fine",refuling:"ok" });
      // console.log(key)
      key=this.id_row
      // console.log(key+"kkkkkkk")
      API('auth.ExperimentDetials_id',{key}).then(res => {
        this.data = res
        // console.log(res,"dsfsdf" )
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
  
  