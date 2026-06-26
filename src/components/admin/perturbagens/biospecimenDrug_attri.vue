<template>

    <!--
    Forked from:
    https://quasar.dev/vue-components/table#Example--Popup-editing
  -->
    <div>
      <div class="q-pa-sm q-gutter-sm">
        <div class="text-h6 text-center bg-grey-6">{{ id_row }} Perturbagens Drug Attributes</div>
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
          class="q-table--dense" :pagination="pagination">
          <template v-slot:top> 

            <div class="q-pa-sm q-gutter-sm">
            
  
              <q-dialog v-model="show_dialog">
                <q-card style="width:800px;max-width:800px;background-color: #F5F5F5" text-center>
                  <q-card-section>
                    
                    <div class="text-h6 text-center bg-grey-5">Perturbagens Drug- {{ id_row }} Attributes</div>
                  </q-card-section>
  
                  <!-- add Camra Details Start -->
                  <q-card-section>
                
       
                    
                    <div class="row ">
                      <q-input v-model="editedItem.uuid" label="Id:" hidden />

                          <!-- <q-select outlined v-model="editedItem.immortal" input-debounce="0"  @filter="filterImmortal" use-input multiple :options="optionsImmortal"   counter max-values="1"
                        hint="Max 1 selection" label="Fibroblast:" stack-label dense  /> -->
                          <q-space />
                        
                        
<!-- 
                        <q-select outlined v-model="editedItem.organism" input-debounce="0"  @filter="filterOrganism" use-input multiple :options="optionsOrganism"   counter max-values="1"
                        hint="Max 1 selection" label="Organism:" stack-label dense  /><q-space /> -->

                        <!-- <q-select outlined v-model="editedItem.subtype" input-debounce="0"  @filter="filterSubtype" use-input multiple :options="optionsSubtype"   counter max-values="1"
                        hint="Max 1 selection" label="Subtype:" stack-label dense  /><q-space />

                        <q-input outlined  v-model="editedItem.description"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Description"/><q-space /> -->


                        <!-- <q-input outlined  v-model="editedItem.concentration"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Please Type"/><q-space /> -->
                        <!-- <q-select outlined v-model="unit" input-debounce="0"  @filter="filterSource" use-input multiple :options="optionsSource"   counter max-values="1"
                        hint="Max 1 selection" label="Select Unit:" stack-label dense  /><q-space /> -->

                        <!-- <q-input outlined  v-model="editedItem.tumor_id" placeholder="Enter Tumor Id" stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Tumor Id"/><q-space /> -->
                        
                        
  
                     
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

   
  
          <!-- <template v-slot:body="props">Drug 
            <q-tr :props="props">
              
               <q-td key="desc" :props="props">
                {{ props.row.concentration }}
              </q-td> 
  
  
              <q-td key="actions" :props="props">
                <q-btn color="green" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn>
              </q-td>
            </q-tr>
          </template> -->
          <template v-slot:body="props">
            <br>
            <q-input  type="text" outlined v-model="modellink" stack-label class="fit" :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Enter the Link"/>
              <q-input  type="text" outlined v-model="modelcomment" stack-label class="fit" :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Comment"/>
              <q-tr :props="props">
              <q-td key="desc" :props="props">
                <q-checkbox color="orange" size="xs" v-model="OptionSelections" val="small_molecule" label="Small Molecule"></q-checkbox>
                <q-checkbox color="teal" size="xs" v-model="OptionSelections" val="peptide" label="Peptide"></q-checkbox>
                <q-checkbox color="red" size="xs" v-model="OptionSelections" val="recombinant_protein" label="Recombinant Protein"></q-checkbox>
                <q-checkbox color="primary" size="xs" v-model="OptionSelections" val="nuclic_acid" label="Nucleic Acid"></q-checkbox>
                <q-checkbox color="green" size="xs" v-model="OptionSelections" val="secrtome" label="Secretome"></q-checkbox>

                <!-- <q-checkbox color="cyan"  size="xs" v-model="OptionSelections" val="ecm" label="ECM"></q-checkbox> -->
              </q-td>
            </q-tr>
          </template>
  

        </q-table>
      </div>

      <div class="text-center q-mt-sm">
        <q-btn dense color="black" v-close-popup label="Cancel" class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Ok"></q-btn>
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
      label: 'Selection',
      align: 'center',
      field: row => row.dosage,
      format: val => `${val}`,
      sortable: true
    },
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    // { name: 'second', align: 'center', label: 'source', field: 'source', sortable: true },
    // { name: 'one', align: 'center', label: 'time', field: 'time', sortable: true },
    // { name: 'two', align: 'center', label: 'dosage', field: 'subtype', sortable: true },
    // { name: 'one', align: 'center', label: 'Concentration Unit', field: 'concentration_unit', sortable: true },
    // { name: 'four', align: 'center', label: 'mouse_id', field: 'mouse_id', sortable: true },
    // { name: 'five', align: 'center', label: 'tumor_id', field: 'tumor_id', sortable: true },
    // { name: "actions", align: 'center', label: "Actions", field: "actions" }

  ]
  
  var listLocation=[]
  var listRoute=[]
   
  const stringOptionsOrganism= ['mouse','human']
  const stringOptionsSubtype= ['Empty']
  const stringOptionsSource= ['Mol','ng/ml','ug/ul','mg/ml','M','mM','nM']
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
      const optionsSubtype= ref(stringOptionsOrganism)
  
      return {
        pagination: {
        rowsPerPage: null // current rows per page being displayed
      },
      OptionSelections:ref([]),
        listLocation,
        listRoute,
        columns,
        modellink:ref(null),
        modelcomment:ref(null),
        show_dialog: ref(false),
        editedIndex: -1,
        userD: ref(false),
        editedItem: ref({
          uuid: ref(null),
          type: ref(null),
          concentration: ref(null),
          time: ref(null),
          dosage: ref(null),
          
          
        }),
        unit:ref(null),
        defaultItem: ref({
          uuid: ref(null),
          type: ref(null),
          concentration: ref(null),
          time: ref(null),
          dosage: ref(null),
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
    watch: {
    OptionSelections(newValue) {
      this.saveOptions(newValue);
      
    },
    modellink(newValue){
      this.saveLink(newValue);
    }
    ,
    modelcomment(newValue){
      this.savecommnet(newValue);
    }
  },
    components: {},
    methods: {
  
      saveOptions(selections) {
        const selections1=selections.toString()
        const type_id1=this.id_row
        // console.log(type_id1)
        API("auth.updateImmunofluorescent_nc_one_DSR", { dosage: selections1,type_id:type_id1});
      },

      saveLink(link) {
        const link1=link
        const type_id1=this.id_row
        // console.log(link1)
        API("auth.updateImmunofluorescent_nc_one_DSR_time", { time: link1,type_id:type_id1});
      },
      savecommnet(commnet) {
        const commnet1=commnet
        const type_id1=this.id_row
        // console.log(type_id1,commnet1)
        API("auth.updateImmunofluorescent_nc_one_DSR_commnet", { concentration: commnet1,type_id:type_id1});
      },
  
      async addRow() {
  
        const id1= this.editedItem.uuid

        const type1 = this.type_biosp
        // const type_id1 = this.editedItem.type_id
        const type_id1=this.id_row

        // const immortal1 = this.editedItem.immortal
        // const immortal1 = this.editedItem.immortal.toString()
        const concentration1 = this.editedItem.concentration
        const concentration_unit1 = this.editedItem.concentration_unit.toString()

        // const passage1 = this.editedItem.passage.toString()
        // const transfected1 = this.editedItem.transfected

        // const subtype1 = this.editedItem.subtype.toString()
        // // const lot_no1 = this.editedItem.lot_no
        // const description1 = this.editedItem.description
        // const mouse_id1 = this.editedItem.mouse_id
        // const tumor_id1 = this.editedItem.tumor_id
        // const hyperlink1 = this.editedItem.hyperlink
        // const assignedCamra1 = this.editedItem.assignedCamra.toString()
        // const assignedRoute1 = this.editedItem.assignedRoute.toString()
  
        // console.log( role1.constructor.name+"mmmmmmm")

        
        const editedIndex1 = this.editedIndex
        const oldRow = this.data[editedIndex1]
        const updatedRow = this.editedItem
  
        if (this.editedIndex > -1) {
          Object.assign(oldRow, updatedRow) && API("auth.updatePerturbagens_DSR", { id1: id1,type: type1,type_id:type_id1, concentration: concentration1,concentration_unit:concentration_unit1});
        } else {
          if ( concentration1 && concentration_unit1 ) {
            
            this.data.push(this.editedItem) && API("auth.create_obj_DSR", { type: type1,type_id:type_id1, concentration: concentration1});
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
        this.data.splice(index, 1) && await API('auth.deletePerturbagens_DSR', { id });
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
      // API('auth.perturbagens_detials_id_DSR',{key}).then(res => {
      //   this.data = res
      //   const estring=res[0].dosage
      //   const emissionArray = estring.split(',');
      //   // console.log(emissionArray);
      //   this.OptionSelections=emissionArray
      //   // console.log(res+"dsfsdf" )

      //   const elinkstr=res[0].time
      //   this.modellink=elinkstr
      // })
  
      API('auth.perturbagens_detials_id_DSR', { key }).then(res => {
  if (res && res.length > 0) {
    this.data = res;

    const estring = res[0]?.dosage; // Optional chaining to safely access dosage
    if (estring) {
      const emissionArray = estring.split(',');
      this.OptionSelections = emissionArray;
    } else {
      console.warn('dosage is null or undefined');
      this.OptionSelections = []; // Provide a fallback value
    }

    const elinkstr = res[0]?.time; // Optional chaining for time
    this.modellink = elinkstr || ''; // Fallback to an empty string if time is null

    const elcommnet=res[0]?.concentration
    this.modelcomment=elcommnet || '';
  } else {
    console.error('Response is empty or invalid');
    this.data = [];
    this.OptionSelections = [];
    this.modellink = '';
    this.modelcomment='';
  }
});

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
  
  