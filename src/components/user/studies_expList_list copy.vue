<template>

    <div>

      <div class="q-pa-sm q-gutter-sm text-black" v-if="expShow">
        <div class="text-h6 text-center bg-grey-6">List of Experiments</div>
        <q-table  title="Treats" :rows="filteredRows" :columns="filteredColumns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
          class="q-table--dense compact-table" :pagination="pagination">
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
<!-- 
          <template v-slot:body-cell-five3="props">
            <q-td v-if="props.row.five3" :props="props">
              <q-badge outline color="black">
                {{ props.row.five3 }}
              </q-badge>
            </q-td>
          </template> -->

  
          <!-- <template v-slot:body="props">
            <q-tr :props="props">
              
              <q-td key="desc" :props="props">
                <q-badge outline color="black"> {{ props.row.name ? props.row.name: 'N/A' }}</q-badge>
              </q-td>
  
              <q-td key="one" :props="props">
                <q-badge  outline color="pink"> {{ props.row.type ? props.row.type: 'N/A' }}</q-badge>
              </q-td>
        
             
              <q-td key="four" :props="props">
                <q-badge outline color="accent"> {{ props.row.primary ? props.row.primary: 'N/A' }}</q-badge>
              </q-td>

              <q-td key="five" :props="props">
                <q-badge outline color="accent"> {{ props.row.secondary ? props.row.secondary: 'N/A' }}</q-badge>
              </q-td>

              <q-td key="five22" :props="props">
                <q-badge outline color="primary">   {{ (props.row.time && props.row.unit_harvest) ? (props.row.time + " "+ props.row.unit_harvest): 'N/A'}}</q-badge>
              </q-td>

              <q-td key="five2" :props="props">
                <q-badge outline color="warning">  {{ props.row.coCulture ? props.row.coCulture: 'N/A' }}</q-badge>
              </q-td>
  
              <q-td key="five3" :props="props">
                <q-badge outline color="green"> {{ (props.row.drug &&  props.row.concentration && props.row.unit_drug) ? (props.row.drug + "-" + props.row.concentration +props.row.unit_drug) : 'N/A' }}</q-badge>
              </q-td>
              <q-td key="five4"  :props="props">
                <q-badge outline color="brown">   {{ props.row.comment_drug ? props.row.comment_drug : 'N/A'}}</q-badge>
              </q-td>
              <q-td key="five5" :props="props">
                <q-badge outline color="pink">  {{ props.row.counterstain ? props.row.counterstain : 'N/A'}}</q-badge>
              </q-td>
              
  
              <q-td key="six" :props="props">
                <q-badge outline color="black"> {{ props.row.treatment_group ? props.row.treatment_group : 'N/A'}}</q-badge>
              </q-td>

              <q-td key="six" :props="props">
                <q-badge outline color="red"> {{ props.row.experiment_design_date ? props.row.experiment_design_date : 'N/A'}}</q-badge>
              </q-td>
              
    
            </q-tr>
          </template> -->

          
          <template v-slot:body-cell-mergedDrugUnit="props">
      <q-td :props="props" >
        {{ mergedDrugUnit[props.rowIndex] }}
      </q-td>
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



        </q-table>
    
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
      label: 'Biospecimen',
      align: 'center',
      field: row => row.name,
      format: val => `${val}`,
      sortable: true
    },
    { name: 'one', align: 'center', label: 'Type', field: 'type', sortable: true },
    // { name: 'two', align: 'center', label: 'experiment_name', field: 'experiment_name', sortable: true },
    // { name: 'three', align: 'center', label: 'experiment_design_date', field: 'experiment_design_date', sortable: true },
    // { name: 'three1', align: 'center', label: 'biospecimen', field: 'name', sortable: true },

    // { name: 'three11', align: 'center', label: 'harvest time', field: 'time', sortable: true },
    // { name: 'three22', align: 'center', label: 'Unit Harvest', field: 'unit_harvest', sortable: true },

 
    { name: 'four', align: 'center', label: 'Primary antibody', field: 'primary', sortable: true },
    { name: 'five', align: 'center', label: 'Secondary antibody', field: 'secondary', sortable: true },
    // { name: 'five1', align: 'center', label: 'counterstain', field: 'counterstain', sortable: true },
    { name: 'five22', align: 'center', label: 'Harvest Time', field: 'unit_harvest', sortable: true },
    { name: 'five2', align: 'center', label: 'CoCulture', field: 'coCulture', sortable: true },
  //  { name: 'five3', align: 'center', label: 'Drug', field: 'drug', sortable: true },
  //   { name: 'five4', align: 'center', label: 'Microschope', field: 'comment_drug', sortable: true },
    { name: 'five5', align: 'center', label: 'Counterstain', field: 'counterstain', sortable: true },
    { name: 'six', align: 'center', label: 'Treatment group', field: 'treatment_group', sortable: true },
    { name: 'three', align: 'center', label: 'Design date', field: 'experiment_design_date', sortable: true },

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

mergedDrugUnit() {
      return this.data.map(row => `${row.concentration} ${row.unit_drug}`);
    },
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
      key !== 'name' && 
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
           if (this.data.length > 0 && this.data[0].hasOwnProperty('name') && this.data[0].time) {
              columns.splice(2, 0, { // Insert at the third index (index 2)
                name: 'Biospecimen',
                align: 'center',
                label: 'Biospecimen',
                field: 'name',
                sortable: true,
              });
            }

            


            if (this.data.length > 0 && this.data[0].hasOwnProperty('unit_drug')&& this.data[0].time) {
        // 'time' property exists, add the new column
        columns.push({
          name: 'mergedDrugUnit',
          align: 'center',
          label: 'Drug Unit',
          field: 'mergedDrugUnit',
          sortable: true,
          // You can customize additional properties as needed
        });
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

  return columns;
}
  },
  
    mounted() {
    // API("auth.createArirports", { name:"DeliAir", latLong:"-873.45",noOfRunWay:"3",typesOfAircraft:"full",runWayConstType:"simple",AtcFacility:"fine",refuling:"ok" });
      // console.log(key)
      key=this.id_row
      // console.log(key+"kkkkkkk")
      API('auth.ExperimentDetials_id',{key}).then(res => {
        this.data = res
        console.log(res,"dsfsdf" )
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
  
  <style>
  .compact-table td {
    padding: 0px 0px !important; /* Reduces cell padding */
  }
  
  </style>