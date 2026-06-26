<template>
   <!-- <q-btn @click="printProperties" label="checkParase" ></q-btn> -->
  <!-- {{ receivedantibody }} -->
  <div class="text-black q-ml-lg fit"  v-if="combination">
    <!-- {{ exp_pass_combination_prop }}
     -->
     <!-- {{ filteredRows }} -->
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
      selection="multiple"
      v-model:selected="selected"
      table-header-style="background-color: #C0C0C0"
      :pagination="{ rowsPerPage: 30 }"
    >

    <template v-slot:body-cell-treatment_group="props">
          <q-td :props="props">
            <q-select v-model="props.row.treatment_group" :options="treatmentGroupOptions"></q-select>
          </q-td>


        </template>
        <template v-slot:body-cell-mergedHarvestTime="props">
      <q-td :props="props" >
        {{ mergedHarvestTime[props.rowIndex] }}
      </q-td>
    </template>



    </q-table>
    <!-- Button Press and Next -->
          <div class="text-center q-mt-sm" >
            <q-btn name="sssnn" style="width: 210px;"  color="black" label="Update"  @click="nextpage" />

          </div>
  </div>

  <!-- Show components -->

    <div v-if="imageStanning">
      <div class="text-center q-mb-sm" >
        <q-btn rounded color="red" label="Cancel" icon-right="cancel" @click="refreshPage" ></q-btn>
      </div>

      <div style="border: 4px solid black;"  class="q-mt-sm">
        <antidodies class="fit" @childMessage="handleChildMessage_antibody" @childMessage2="handleChildMessage_antibody2"></antidodies>
        <counterstain class="fit" @childMessage="handleChildMessage_counterstain" outline></counterstain>
        </div>
        <div style="border: 4px solid black;"  class="q-mt-lg">
          <!-- {{ receivedphase }} -->
          <brightField class="fit" @childMessage="handleChildMessage_phase"></brightField>
        </div>
        <!-- Show bioAssy and hide combinations -->
        <div class="text-center">
            <q-btn color="dark" style="min-width:210px ;"  @click="checklength" label="Submit" icon-right="skip_next" class="q-mt-sm q-mr-lg q-mt-2" ></q-btn>
        </div>
      </div>


    <div v-if="bioassy">

      <bioAssy :receivedArray1="finalMergesArray" :exp_pass_assy_prop="exp_pass_assy"></bioAssy>

    </div>

    <q-dialog
      v-model="small"
      @show="startTimer"
    >
     <q-card style="width: 300px">
        <q-card-section>
          <div class="text-h6 text-center">Making Combinations</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="text-center">
            <q-spinner-hourglass
              color="primary"
              size="4em"
            />
            <q-tooltip :offset="[0, 8]">Processing</q-tooltip>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

</template>

<script>
  import { ref, onMounted } from 'vue'
  import antidodies from 'src/components/user/antidodies';
  import counterstain from 'src/components/user/counterstain';
  import bioAssy from'src/components/user/bioAssy';
  import brightField from 'src/components/user/brightField';


  const stringOptionsTreatment=['Control','Negative Control','Media Control','Delivery Vehicle','Positive Control','Solvent','Treated','Compare']
  var dummyArry=[]
  let originalRows = [];

  const columns = [

  {
      name: 'desc', size:"20px",
      required: true,
      label: 'Cell Culture',
      align: 'left',
      field: row => row.drugs,
      format: val => `${val}`,
      sortable: true,
      headerStyle:"22px"
    },
    { name: 'second', align: 'center',label: 'concValue', field: 'concValue', sortable: true },
    { name: 'third', align: 'center',label: 'concUnit', field: 'concUnit', sortable: true },
    { name: 'thirda', align: 'center',label: 'coCulture', field: 'coCulture', sortable: true },
    { name: 'four', align: 'center',label: 'Type', field: 'type', sortable: true },
    { name: 'five', align: 'center',label: 'Passage', field: 'passage', sortable: true },
    { name: 'six', align: 'center',label: 'Harvest Time', field: 'time', sortable: true },
    { name: 'seven', align: 'center',label: 'Time Unit', field: 'unit_harvest', sortable: true },
    { name: 'eight', align: 'center',label: 'Stiffness', field: 'stiffness', sortable: true },
    { name: 'nine', align: 'center',label: 'Unit Stiffness', field: 'unit_stiffness', sortable: true },
    { name: 'ten', align: 'center',label: 'Drug', field: 'name', sortable: true },
    { name: 'eleven', align: 'center',label: 'Concentration', field: 'concentration', sortable: true },
    { name: 'ex_type', align: 'center',label: 'ex_type', field: 'ex_type', sortable: true },
    { name: 'twel', align: 'center',label: 'Unit Drug', field: 'unit_drug', sortable: true },

    { name: 'thirteen', align: 'center',label: 'Treatment Group', field: 'treatmentgroup', sortable: true }

  ]



export default {


  props: {

  exp_pass_combination_prop: Array,
  receivedArray: String,

},


  setup () {
    const treatmentGroupOptions= ref(stringOptionsTreatment)



    return {

      selected:ref([]),
      small:ref(null),
      columns,
      treatmentGroupOptions,
      rows:ref([]),
      imageStanning:ref(false),
      combination:ref(true),
      bioassy:ref(false),
      receivedantibody:"",
      receivedantibody2:"",
      receivedcounterstain:"",
      receivedphase:"",
      parsedObject: {},
      finalMergesArray:["hello"],
      exp_pass_assy:[]
    }
  },
  mounted(){
    // console.log(receivedphase,"phase")
      const a=this.receivedArray;
      dummyArry=a;
      this.rows=a;

      //Exp pass
      const exp_pass__propGlobal=[...this.exp_pass_combination_prop];
      this.exp_pass_assy=exp_pass__propGlobal

  },
  components: {
      antidodies,counterstain,bioAssy,brightField
    },
    methods:{

      checklength(){
        const anti_length=this.receivedantibody2.length
        const countetr_length=this.receivedcounterstain.length
        const phase_length=this.receivedphase.length
        // console.log(anti_length,"length")
        if((anti_length>0 && countetr_length>0) || phase_length>0){
        this.finalReadyArray();
        // this.small=true;
        this.startTimer();
        }
        else{
          this.$q.notify({
          message: 'Please fill atleast one box',
          color: 'red', // You can change the color to indicate success
          icon: 'announcement',

        });

        }
      },

      nextpage(){

        // if(this.selected.length>0 && this.selected[0].treatment_group != null){
        //   this.imageStanning=true;
        //   this.combination=false;
        // }
        if (this.selected.length > 0 && this.selected.every(item => item.treatment_group != null)) {
          this.imageStanning = true;
          this.combination = false;
        }
        else{
          this.$q.notify({
          message: 'Please make selection First',
          color: 'red', // You can change the color to indicate success
          icon: 'announcement',
        });
        }
      },
      startTimer() {

      this.$q.notify({
      message: 'Processed',
      color: 'green', // You can change the color to indicate success
      icon: 'announcement',
    });

      setTimeout(() => {
        this.bioassy=true;
        this.imageStanning=false;
        // this.small = false; // Close the dialog
      }, 1000);
    },
    handleChildMessage_phase(message) {
      this.receivedphase = message;
      // console.log( this.receivedcounterstain+"revceivecounter")
    },
      handleChildMessage_counterstain(message) {
      this.receivedcounterstain = message;
      // console.log( this.receivedcounterstain+"revceivecounter")
    },
      handleChildMessage_antibody(message) {
      this.receivedantibody = message;
      // console.log( this.receivedantibody+"revceiveAntibody")
    },

    handleChildMessage_antibody2(message) {
      this.receivedantibody2 = message;
      // console.log( this.receivedantibody+"revceiveAntibody")
    },

// 1st parse array

    parseArrays(array){
       // Convert and log the values as a JSON array
        const jsonArray = JSON.stringify(Object.values(array));
        const parsedArray = JSON.parse(jsonArray);
        // console.log('kkkk:', parsedArray);

        // Making parsing array
        const parsedDataArray = parsedArray.map(item => {
        const parsedItem = { ...item };
        for (const key in parsedItem) {
          if (Array.isArray(parsedItem[key]) && parsedItem[key].length > 0) {
            parsedItem[key] = parsedItem[key][0];
          }
        }

        return parsedItem;
      });
      // console.log('kkk'+parsedDataArray);

      return parsedDataArray;
    },

    // 2 formated arrays
        async formated_arryes(){

      const parse_antibody=this.parseArrays(this.receivedantibody);
      const parse_antibody2=this.parseArrays(this.receivedantibody2);
      const parse_counterstain=this.parseArrays(this.receivedcounterstain);
      const parse_phase=this.parseArrays(this.receivedphase);
      const parse_previous=this.parseArrays(this.selected);
      // console.log(parse_previous+"previous")
      return [
      parse_antibody,
      parse_antibody2,
      parse_counterstain,
      parse_phase,
      parse_previous
        ];
    },

    // 3rd  array length
    async arraysLength(){
            const [
          parsedAntibody,
          parse_antibody2,
          parsedCounterstain,
          parsedPhase,
          parse_previous,
        ] = await this.formated_arryes();

      var Antibodies_len=parsedAntibody.length;
      var counterstain_len=parsedCounterstain.length ;
      var phase_len=parsedPhase.length;
      var previous_len=parse_previous.length;

      if (Antibodies_len === 0) {
        Antibodies_len = 1;
      }
      if (counterstain_len === 0) {
        counterstain_len = 1;
      }
      if (phase_len === 0) {
        phase_len = 1;
      }
      if (previous_len === 0) {
        previous_len = 1;
      }

      // const combine_length=Antibodies_len*counterstain_len*previous_len
      const combine_length=Antibodies_len*previous_len*counterstain_len*phase_len
      // console.log("combine_length:"+Antibodies_len)

      return [combine_length,parsedAntibody,parse_antibody2,parsedCounterstain,parsedPhase,parse_previous];

    },
    duplicateArrayElementsR(array, length) {
  const duplicatedArray = [];
  const originalLength = array.length;

  if (originalLength === 0) {
    return duplicatedArray;
  }

  const numberOfDuplications = Math.ceil(length / originalLength);

  for (let i = 0; i < originalLength; i++) {
    for (let j = 0; j < numberOfDuplications; j++) {
      const duplicatedElement = { ...array[i], uuid: Math.floor(Math.random() * 100000) };
      duplicatedArray.push(duplicatedElement);
    }
  }

  return duplicatedArray.slice(0, length);
},

    duplicateArrayElements(array, length) {
      const duplicatedArray = [];
      const originalLength = array.length;

      if (originalLength === 0) {
        return duplicatedArray;
      }

      const numberOfDuplications = Math.ceil(length / originalLength);

      for (let i = 0; i < numberOfDuplications; i++) {
        duplicatedArray.push(...array);
      }

      return duplicatedArray.slice(0, length);
    },

    // 4th  change array lengthdublicate as per previous array
    splitObjectsIntoArrays(objects) {
      let resultArrays = [];
      objects.forEach(obj => {
        let keys = Object.keys(obj);
        let values = Object.values(obj);
        let newArray = [];

        for (let i = 0; i < keys.length; i++) {
          let key = keys[i];
          let value = values[i];
          newArray.push({ [key]: value });
        }

        resultArrays.push(newArray);
      });
      return resultArrays;
    },


    async change_length_arraysList(){
    const [
          combine_length,
          parsedAntibody,
          parse_antibody2,
          parsedCounterstain,
          parsedPhase,
          parse_previous,
        ] = await this.arraysLength();
        // console.log(parsedAntibody+"lllll")
      const combinedObjectsArray = this.printProperties();
      var increase_length_antibody=this.duplicateArrayElementsR(combinedObjectsArray,combine_length)

      // console.log(increase_length_antibody+"mmmIncreaseLength")
      // this.duplicateArrayElements(parse_antibody2,combine_length)
      var increase_length_counterstain=this.duplicateArrayElements(parsedCounterstain,combine_length)
      // this.duplicateArrayElements(parsedCounterstain,combine_length)

      var  increase_length_phase=this.duplicateArrayElements(parsedPhase,combine_length)

      var increase_length_previous=this.duplicateArrayElements(parse_previous,combine_length)
      // this.duplicateArrayElements(parse_previous,combine_length)
      // console.log(increase_length_antibody+"jjjjj")
      return [increase_length_antibody,increase_length_counterstain,increase_length_phase,increase_length_previous]
    },



printProperties() {
  const combinedObjectsArray = []; // Initialize an empty array to store the combined objects

  if (Array.isArray(this.receivedantibody)) { // Ensure receivedantibody is an array
    this.receivedantibody.forEach(innerArray => {
      if (Array.isArray(innerArray)) { // Ensure innerArray is an array
        const combinedObject = innerArray.reduce((acc, obj) => {
          acc.costain.push(obj?.costain || ''); // Handle null/undefined cases
          acc.primary.push(obj?.primary || '');
          acc.secondary.push(obj?.secondry || ''); // Retained typo "secondry"
          acc.uuid.push(obj?.uuid || '');
          return acc;
        }, { costain: [], phase: [], magnification: [], primary: [], secondary: [], uuid: [] });

        // Combine values as a comma-separated string
        const finalCombinedObject = {
          costain: combinedObject.costain.join(", ") || 'N/A',
          phase: combinedObject.phase.join(", ") || 'N/A',
          magnification: combinedObject.magnification.join(", ") || 'N/A',
          primary: combinedObject.primary.join(", ") || 'N/A',
          secondary: combinedObject.secondary.join(", ") || 'N/A', // 'secondry' retained in obj
          uuid: combinedObject.uuid.join(", ") || 'N/A',
        };

        combinedObjectsArray.push(finalCombinedObject); // Push the combined object into the array
      } else {
        console.warn('Inner array is not an array');
      }
    });

    console.log("Combined Objects Array:", combinedObjectsArray); // Log the combined objects array
    return combinedObjectsArray;
  } else {
    console.error('receivedantibody is not an array');
    return [];
  }
},


    async finalReadyArray(){
      const [
      increase_length_antibody,
      increase_length_counterstain,
      increase_length_phase,
      increase_length_previous,
        ] = await this.change_length_arraysList();

        const arraysToMerge = [
        increase_length_previous,
        increase_length_antibody,
        increase_length_counterstain,
        increase_length_phase,

      ];
      // console.log(increase_length_antibody+"check")
      const maxLength = Math.max(...arraysToMerge.map(arr => arr.length));
      const mergedArrays = [];

      for (let i = 0; i < maxLength; i++) {
        const mergedItem = {};
        arraysToMerge.forEach((arr, index) => {
          if (i < arr.length) {
            Object.assign(mergedItem, arr[i]);
          }
        });
        mergedArrays.push(mergedItem);
      }
            // Iterate through the receivedArray and update the uuid field
        for (var i = 0; i < mergedArrays.length; i++) {
          mergedArrays[i].uuid = this.generateRandomUUID();
        }
        this.finalMergesArray=mergedArrays;
        // console.log("Merged Arrays Index-wise:", this.finalMergesArray);

    },
    generateRandomUUID() {
      return Math.floor(Math.random() * 1000).toString();
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
            return this.rows.filter(row => {
              for (const key in row) {
                if (row[key] === null) {
                  return false; // Exclude the row if any field is null
                }
              }
              return true; // Include the row if all fields are not null
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
      key !== 'treatment_group' &&// Exclude 'treatment_group' from the loop
      key !== 'time'  &&
      key !== 'unit_harvest'
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
  if (this.rows.length > 0 && this.rows[0].hasOwnProperty('time')) {
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
  // Add a new column for "Treatment Group" outside of the loop
  columns.push({
    name: 'treatment_group',
    align: 'center',
    label: 'Treatment Group',
    field: 'treatment_group',
    sortable: true,
  });

  return columns;
}

},
}
</script>
