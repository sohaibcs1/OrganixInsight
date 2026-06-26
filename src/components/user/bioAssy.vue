<template>
  <!-- <div>{{ filteredRows }}</div> -->
  <!-- {{exp_pass_assy_prop}} -->
    <div class="text-black q-ml-lg fit"  v-if="bioas">

      <div class="text-center q-mb-sm" >
        <q-btn rounded color="red" label="Cancel" icon-right="cancel" @click="refreshPage" ></q-btn>
      </div>

      <q-table
        ref="tableRef"
        flat bordered
        title=""
        :rows="filteredRows"
        :columns="filteredColumns"
        row-key="uuid"
        dense
        table-header-style="background-color: #C0C0C0"
        :pagination="{ rowsPerPage: 30 }"
      >

        <template v-slot:body-cell-[name]="props">
        {{ props.row[name] }}
      </template>
      <!-- <template v-slot:body-cell-mergedHarvestTime="props">
      <q-td :props="props">
        {{ mergedHarvestTime[props.rowIndex] }}
      </q-td>
    </template> -->
      <!-- <template v-slot:body-cell-actions="props">
          <q-td key="actions" :props="props">
                <q-btn label="upload" size="12px" dense @click="show_upload_dialog=true"></q-btn>

          </q-td>
        </template> -->

        <template v-slot:body-cell-phase="props">
          <q-td key="phase" :props="props">
            <span v-if="props.row.phase.includes(',')">
              <div v-for="part in props.row.phase.split(',')" :key="part"><q-badge outline color="accent">{{ part }}</q-badge></div>
            </span>
            <span v-else><q-badge outline color="accent">{{ props.row.phase }}</q-badge></span>
          </q-td>
        </template>

        <template v-slot:body-cell-magnification="props">
          <q-td key="magnification" :props="props">
            <span v-if="props.row.magnification.includes(',')">
              <div v-for="part in props.row.magnification.split(',')" :key="part"><q-badge outline color="accent">{{ part }}</q-badge></div>
            </span>
            <span v-else><q-badge outline color="accent">{{ props.row.magnification }}</q-badge></span>
          </q-td>
        </template>

        <template v-slot:body-cell-primary="props">
          <q-td key="primary" :props="props">
            <span v-if="props.row.primary.includes(',')">
              <div v-for="part in props.row.primary.split(',')" :key="part">  <q-badge outline color="primary">{{ part }}</q-badge> </div>
            </span>
            <span v-else><q-badge outline color="secondary">{{ props.row.primary }}</q-badge> </span>
          </q-td>
        </template>

        <template v-slot:body-cell-secondary="props">
          <q-td key="secondry" :props="props">
            <span v-if="props.row.secondary.includes(',')">
              <div v-for="part in props.row.secondary.split(',')" :key="part"><q-badge outline color="primary">{{ part }}</q-badge></div>
            </span>
            <span v-else><q-badge outline color="secondary">{{ props.row.secondary }}</q-badge></span>
          </q-td>
        </template>


      </q-table>


      <div class="text-center">

            <q-btn color="dark" style="min-width:210px ;" @click="addcheck"  label="Save Experiment" icon-right="skip_next" class="q-mt-sm q-mr-lg q-mt-2" ></q-btn>
            <!-- {{ exp_pass_assy_prop }} -->
          </div>
      <q-dialog v-model="show_upload_dialog" >
          <q-card >

            <!-- add Camra Details Start -->
            <q-card-section align="center" >
              <div class="row text-center">
                <!-- Define attributes table -->
                <uploadbtn></uploadbtn>
                <!-- attributes table END -->
              </div>
            </q-card-section>
            <!-- add Camra Details END -->
          </q-card>
        </q-dialog>
      <!-- Button Press and Next -->
            <!-- <div class="text-center q-mt-sm"  >
              <q-btn name="sssnn" style="width: 210px;"  color="black" label="Update"   @click="imageStanning=true;combination=false;"/>
            </div> -->
    </div>

    <div v-if="uploadImg">
      <fileUpload_list :random_id="randomId"></fileUpload_list>

    </div>

  </template>

  <script>
    import API from 'src/api'
    import { ref, onMounted } from 'vue'
    import uploadbtn from 'src/components/user/uploadbtn';
    import fileUpload_list from 'src/components/user/fileUpload_list';

    const stringOptionsTreatment=['Control','Negative Control','Positive Control','Solvent','Treated']
    var dummyArry=[]
    let originalRows = [];

    const columns = [

    {
        name: 'desc', size:"20px",
        required: true,
        label: 'Cell Culture',
        align: 'left',
        field: row => row.name,
        format: val => `${val}`,
        sortable: true,
        headerStyle:"22px"
      },
      { name: 'second', align: 'center',label: 'concValue', field: 'concValue', sortable: true },
      { name: 'third', align: 'center',label: 'concUnit', field: 'concUnit', sortable: true },
      { name: 'thirda', align: 'center',label: 'coCulture', field: 'coCulture', sortable: true },
      { name: 'four', align: 'center',label: 'Type', field: 'type', sortable: true },
      { name: 'five', align: 'center',label: 'Passage', field: 'passage', sortable: true },
      // { name: 'six', align: 'center',label: 'Time', field: 'time', sortable: true },
      // { name: 'seven', align: 'center',label: 'Time Unit', field: 'unit_harvest', sortable: true },
      { name: 'eight', align: 'center',label: 'Stiffness', field: 'stiffness', sortable: true },
      { name: 'nine', align: 'center',label: 'Unit Stiffness', field: 'unit_stiffness', sortable: true },
      { name: 'ten', align: 'center',label: 'Drug', field: 'drug', sortable: true },
      { name: 'eleven', align: 'center',label: 'costain', field: 'costain', sortable: true },
      { name: 'twel', align: 'center',label: 'Unit Drug', field: 'unit_drug', sortable: true },

      { name: 'thirteen', align: 'center',label: 'Primary Antibody', field: 'primary', sortable: true },
      { name: 'fourteen', align: 'center',label: 'secondry Antibody', field: 'secondry', sortable: true },
      { name: 'fifteen', align: 'center',label: 'Costain', field: 'costain', sortable: true },
      { name: 'sixteen', align: 'center',label: 'costain', field: 'counterstain', sortable: true },

      { name: 'seventeen', align: 'center',label: 'Treatment Group', field: 'treatmentgroup', sortable: true },
      // { name: 'actions', align: 'center', label: 'Actions', field: 'actions' },

    ]



  export default {


    props: {
  exp_pass_assy_prop:Array,
  receivedArray1: String,

},

    setup () {
      const treatmentGroupOptions= ref(stringOptionsTreatment)



      return {

        selected:ref([]),
        columns,
        treatmentGroupOptions,
        rows:ref([]),
        imageStanning:ref(false),
        bioas:ref(true),
        uploadImg:ref(false),
        show_upload_dialog:ref(false),
        experiment_received:[],
        randomId: null,


      }
    },
    created(){
          const length = 8; // Adjust the length as needed
          const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
          let result = '';
          for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
          }
          this.randomId = result;
    },
    mounted(){
        const a=this.receivedArray1;
        dummyArry=a;
        this.rows=a;

          //Exp pass
      const exp_pass__propGlobal=[...this.exp_pass_assy_prop];
      this.experiment_received=exp_pass__propGlobal;

    //   this.mergeArrays();
    // console.log('Merged Arrayaa:', this.receivedArray1);


    },
    components: {
      uploadbtn,fileUpload_list
      },
      methods:{

        nextpage(){
          this.bioas=false;
          this.uploadImg=true;
      },
        mergeArrays() {
            if (this.receivedArray1.length > 0) {
              const firstItem = this.experiment_received[0];

              // Create a new array with merged objects
              const newArrayWithMergedProps = this.receivedArray1.map((item) => {
                // Merge the properties of the first item from experiment_received into each item in receivedArray1
                return { ...item, ...firstItem };
            


                  if (merged.stroma && merged.stroma.trim() !== '' || merged.stroma && merged.stroma.trim() !== 'Null') {
                    merged.name = `${merged.name} | ${merged.stroma}`;
                  }

                  return merged;
                });
              // Return the new array
              // console.log(newArrayWithMergedProps)
              return newArrayWithMergedProps;
            }

            // Return an empty array if receivedArray1 is empty
            return [];
          },

          addcheck() {
  try {

    const a = this.mergeArrays();
    console.log(a,'arr')
    a.forEach((experiment) => {
      const {
        experiment_name,
        ex_type,
        experiment_description,
        experiment_design_date,
        time,
        unit_harvest,
        name,
        type,
        passage,
        coCulture,
        drug,
        unit_drug,
        concentration,
        virus,
        unit_virus,
        stroma,
        virus_concentration,
        plasmid,
        unit_plasmid,
        plasmid_concentration,
        comment_plasmid,
        costain,
        comment_cellCulture,
        comment_virus,
        concUnit,
        concValue,
        counterstain,
        primary,
        secondary,
        treatment_group,
        study_id,
        phase,
        magnification,
        em_exposure,
        unit_em_exposure,
        comment_em_exposure,
        voltage,
        pulse_width,
        no_of_pluses,
        time_bt_pulses,
        capacitance,
      } = experiment;

      const random_id=this.randomId;
       const stromaClean =
  stroma &&
  stroma.trim() !== "" &&
  stroma.trim().toLowerCase() !== "null";

const finalName = stromaClean
  ? `${name} | ${stroma}`
  : name;

    // console.log(random_id,"randomId")
      // Make the API call with the extracted values
      API("auth.create_obj_experimentnocheck", {
        experiment_name,
        ex_type,
        experiment_description,
        experiment_design_date,
        time,
        unit_harvest,
        name: finalName,
        type,
        passage,
        coCulture,
        drug,
        unit_drug,
        concentration,
        virus,
        unit_virus,
        virus_concentration,
        plasmid,
        unit_plasmid,
        plasmid_concentration,
        comment_plasmid,
        costain,
        comment_cellCulture,
        comment_virus,
        phase_info:`${phase}`,
        magnification:`${magnification}`,
        concUnit,
        concValue,
        counterstain,
        primary,
        secondary,
        treatment_group,
        study_id,
        random_id,
        em_exposure,
        unit_em_exposure,
        comment_em_exposure,
        voltage,
        pulse_width,
        no_of_pluses,
        time_bt_pulses,
        capacitance,
      });
    });

    // If the loop completes without errors, show the notification
    this.$q.notify({
      message: 'Experiment Saved',
      color: 'green', // You can change the color to indicate success
      icon: 'announcement',
    });

    setTimeout(() => {
        this.nextpage();
      }, 1000);

  } catch (error) {
    // If an error occurs, you can handle it here
    console.error('Error in addcheck:', error);

    this.$q.notify({
      message: 'Error occurred while saving experiment',
      color: 'red',
      icon: 'announcement',
    });
  }
},

          refreshPage() {
          window.location.reload();
        },
          handel(){
            this.imageStanning=true
            this.combination=false
          },
      },

          computed:{

            mergedHarvestTime() {
    return this.rows.map(row => `${row.time} ${row.unit_harvest}`);
  },

 filteredRows() {
  return this.rows
    .filter(row => {
      for (const key in row) {
        if (row[key] === null) {
          return false;
        }
      }
      return true;
    })
    .map(row => {
      const stroma = row.stroma;

      // Safe validation: must exist AND not empty AND not "null"
      const stromaClean =
        stroma &&
        stroma.trim() !== "" &&
        stroma.trim().toLowerCase() !== "null";

      if (stromaClean) {
        return {
          ...row,
          name: `${row.name} | ${row.stroma}`
        };
      }

      return row;
    });
},


            filteredColumns() {
    const columns = [];
    for (const key in this.rows[0]) {
      if (
        key !== 'uuid' &&
        key !== 'comment_cellCulture' &&
        key !== 'comment_drug' &&
        key !== 'comment_harvest' &&
        key !== 'comment_radiation' &&
        key !== 'treatment_group' // Exclude 'treatment_group' from the loop
        &&
        key !== 'costain' &&
        key !== 'passage' &&
        key !== 'concValue'
        &&
        key !== 'isCombinationDrug' &&
        key !== 'comment_plasmid' &&
        key !== 'comment_em_exposure' &&
        key !== 'concUnit'&&
        key !== 'stroma' &&
        key !== "unit_harvest" &&
        key !== "numCells"

        // key !== 'time'
        // key !== 'unit_harvest'
      ) {
        columns.push({
          name: key,
          align: 'center',
          label: key,
          field: key,
          sortable: true,
        });
      }
    }


      // Add a new column for "Harvest Time + Time Unit"
  // Add a new column for "Harvest Time + Time Unit"

//   if (this.rows.length > 0 && this.rows[0].hasOwnProperty('time')) {
//   // 'time' property exists, add the new column
//   columns.push({
//     name: 'mergedHarvestTime',
//     align: 'center',
//     label: 'Harvest Time',
//     field: 'mergedHarvestTime',
//     sortable: true,
//     // You can customize additional properties as needed
//   });
// }
    // Add a new column for "Treatment Group" outside of the loop
    columns.push({
      name: 'treatment_group',
      align: 'center',
      label: 'Treatment Group',
      field: 'treatment_group',
      sortable: true,
    });
    // columns.push({
    //   name: 'actions',
    //   align: 'center',
    //   label: 'Action',
    //   field: 'actions',
    //   sortable: true,
    // });

    // console.log(columns,"kkk123")
    return columns;
  }

  },
  }
  </script>
