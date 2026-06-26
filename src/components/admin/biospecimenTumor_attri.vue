<template>

    <!--
    Forked from:
    https://quasar.dev/vue-components/table#Example--Popup-editing
  -->
    <div>
      <div class="q-pa-sm q-gutter-sm">
        <div class="text-h6 text-center bg-grey-6">{{ id_row }} Tumor Attributes</div>
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
          class="q-table--dense" :pagination="pagination">
          <template v-slot:top> 

            <div class="q-pa-sm q-gutter-sm">
            
  
              <q-dialog v-model="show_dialog">
                <q-card  text-center>
                  <q-card-section>
                    
                    <div class="text-h6 text-center bg-grey-5">Biospecimen Tumor- {{ id_row }} Attributes</div>
                  </q-card-section>
  
                  <!-- add Camra Details Start -->
                  <q-card-section>
                
       
                    
                    <div >
                      <q-input v-model="editedItem.uuid" label="Id:" v-if="uuid" hidden />

                          <!-- <q-select outlined v-model="editedItem.immortal" input-debounce="0"  @filter="filterImmortal" use-input multiple :options="optionsImmortal"   counter max-values="1"
                        hint="Max 1 selection" label="Fibroblast:" stack-label dense  /> -->
                        <q-select class="fit q-mb-sm"  v-model="editedItem.source" label="source" :options="optionsSource" stack-label
                           dense outlined></q-select>
                        
  
                           <q-select class="fit q-mb-sm"  v-model="editedItem.organism" label="organism" :options="optionsOrganism" stack-label
                           dense outlined></q-select>

                           <q-select class="fit q-mb-sm"  v-model="editedItem.subtype" label="subtype" :options="optionsSubtype" stack-label
                           dense outlined></q-select>
                          <!-- <q-space />
                          <q-select outlined v-model="editedItem.source" input-debounce="0"  @filter="filterSource" use-input multiple :options="optionsSource"   counter max-values="1"
                        hint="Max 1 selection" label="Source:" stack-label dense  /><q-space />
                        

                        <q-select outlined v-model="editedItem.organism" input-debounce="0"  @filter="filterOrganism" use-input multiple :options="optionsOrganism"   counter max-values="1"
                        hint="Max 1 selection" label="Organism:" stack-label dense  /><q-space />

                        <q-select outlined v-model="editedItem.subtype" input-debounce="0"  @filter="filterSubtype" use-input multiple :options="optionsSubtype"   counter max-values="1"
                        hint="Max 1 selection" label="Subtype:" stack-label dense  /><q-space /> -->

                        <q-input outlined  v-model="editedItem.description"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Description"/><q-space />


                        <q-input outlined  v-model="editedItem.mouse_id"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Mouse Id"/><q-space />

                        <q-input outlined  v-model="editedItem.tumor_id"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Tumor Id"/><q-space />
                        
                        
  
                     
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
                {{ props.row.source }}
              </q-td>
  
              <!-- <q-td key="third" :props="props">
                {{ props.row.passage }}
              </q-td> -->
              
              <q-td key="one" :props="props">
                {{ props.row.organism}}
              </q-td>
              <q-td key="two" :props="props">
                {{ props.row.subtype  }}
               
              </q-td>
              <!-- <q-td key="seven" :props="props">
                {{ props.row.lot_no }}
              </q-td> -->
              <q-td key="three" :props="props">
                {{ props.row.description }}
              </q-td>
              <q-td key="four" :props="props">
                {{ props.row.mouse_id }}
              </q-td>
              <q-td key="five" :props="props">
                {{ props.row.tumor_id }}
              </q-td>

              <!-- <q-td key="nine" :props="props">
                {{ props.row.hyperlink }}
              </q-td> -->
  
  
              <q-td key="actions" :props="props">
                <q-btn color="green" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn>
                <q-btn color="red" label="Delete"  @click="deleteItem(props.row)" size="11px"></q-btn>
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </div>

      <div class="text-center q-mt-sm">
        <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>

      </div>
  
    </div>
  
  </template>
  
  <script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'
  
  
  
  const columns = [
    {
      name: 'desc',
      required: true,
      label: 'source',
      align: 'center',
      field: row => row.source,
      format: val => `${val}`,
      sortable: true
    },
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    // { name: 'second', align: 'center', label: 'source', field: 'source', sortable: true },
    { name: 'one', align: 'center', label: 'organism', field: 'organism', sortable: true },
    { name: 'two', align: 'center', label: 'Subtype', field: 'subtype', sortable: true },
    { name: 'three', align: 'center', label: 'Description', field: 'description', sortable: true },
    { name: 'four', align: 'center', label: 'mouse_id', field: 'mouse_id', sortable: true },
    { name: 'five', align: 'center', label: 'tumor_id', field: 'tumor_id', sortable: true },
    { name: "actions", align: 'center', label: "Actions", field: "actions" }

  ]
  
  var listLocation=[]
  var listRoute=[]
   
  const stringOptionsOrganism= ['mouse','human']
  const stringOptionsSubtype= ['N/A','TNA','TNB','LA','LB','BCRA1','BRCA2']
  const stringOptionsSource= ['mammary','pancreatic']
  const stringOptionsImmortal=  ['Yes', 'No' ]
  const stringOptionsPassage=[]

for (let i = 1; i <= 100; i++) {
  stringOptionsPassage.push(i.toString());
}
  
  var key
  
  export default {
  
    props: ['id_row','type_biosp'],
  
    setup() {
      const $q = useQuasar()
      const optionsOrganism= ref(stringOptionsOrganism)
      const optionsSource=ref(stringOptionsSource)
      const optionsImmortal=ref(stringOptionsImmortal)
      const optionsPassage= ref(stringOptionsPassage)
      const optionsSubtype= ref(stringOptionsSubtype)
  
      return {
        pagination: {
        rowsPerPage: null // current rows per page being displayed
      },
        
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
          source: ref(null),
          organism: ref(null),
          subtype:ref(null),
          description:ref(null),
          mouse_id:ref(null),
          tumor_id:ref(null),
        }),
        defaultItem: ref({
          uuid: ref(null),
          type: ref(null),
          type_id: ref(null),
          source: ref(null),
          organism: ref(null),
          subtype:ref(null),
          description:ref(null),
          mouse_id:ref(null),
          tumor_id:ref(null),
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
    components: {},
    methods: {
  

  
      async addRow() {
  
        const id1= this.editedItem.uuid

        const type1 = this.type_biosp
        // const type_id1 = this.editedItem.type_id
        const type_id1=this.id_row

        // const immortal1 = this.editedItem.immortal
        // const immortal1 = this.editedItem.immortal.toString()
        const source1 = this.editedItem.source
        // const passage1 = this.editedItem.passage.toString()
        // const transfected1 = this.editedItem.transfected
        const organism1 = this.editedItem.organism
        const subtype1 = this.editedItem.subtype
        // const lot_no1 = this.editedItem.lot_no
        const description1 = this.editedItem.description
        const mouse_id1 = this.editedItem.mouse_id
        const tumor_id1 = this.editedItem.tumor_id
        // const hyperlink1 = this.editedItem.hyperlink
        // const assignedCamra1 = this.editedItem.assignedCamra.toString()
        // const assignedRoute1 = this.editedItem.assignedRoute.toString()
  
        // console.log( role1.constructor.name+"mmmmmmm")

        
        const editedIndex1 = this.editedIndex
        const oldRow = this.data[editedIndex1]
        const updatedRow = this.editedItem
  
        if (this.editedIndex > -1) {
          Object.assign(oldRow, updatedRow) && API("auth.updateBiospecimen_tumor", { id1: id1,type: type1,type_id:type_id1, source: source1,organism:organism1,subtype:subtype1,description:description1,mouse_id: mouse_id1,tumor_id:tumor_id1});
        } else {
          if ( source1  && organism1 && subtype1  && description1 ) {
            
            this.data.push(this.editedItem) && API("auth.create_obj_tumor", { type: type1,type_id:type_id1, source: source1,organism:organism1,subtype:subtype1,description:description1,mouse_id: mouse_id1,tumor_id:tumor_id1});
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
        this.data.splice(index, 1) && await API('auth.deleteBiospecimen_tumor', { id });
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
      // console.log(key)
      API('auth.bioSpecimen_detials_tumor_id',{key}).then(res => {
        this.data = res
        // console.log(res+"dsfsdf" )
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
  
  