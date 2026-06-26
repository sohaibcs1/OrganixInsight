<template>
  <div>
    <!-- Form section -->
  
    <div class="q-pa-sm q-gutter-sm text-black">

      <div class="text-h6 text-center">Antibodies</div>
      <div class="fit">


        <div class="row justify-center fit ">
          


          <div class="text-center q-mr-lg">
          <q-btn
            color="green"
            label="ADD New Antibody/Insert Gene"
            @click="clearSelection(); addNewTable();"
          ></q-btn>
        </div>
          <q-input v-model="activeTable.editedItem.uuid" label="Id:" hidden />
          <q-select
            outlined
            v-model="activeTable.editedItem.primary"
            :options="optionsPrimary"
            label="Primary Antibody"
            stack-label
            dense
            style="min-width: 220px; font-size: 12px;"
            class="q-mr-lg"

          />
                        
          <q-select
            outlined
            v-model="activeTable.editedItem.secondry"
            :options="optionsSecondary"
            label="Secondary Antibody"
            stack-label
            dense
            style="min-width: 220px; font-size: 12px;"
            class="q-mr-lg"

          />
          <q-select
            outlined
            v-model="activeTable.editedItem.costain"
            :options="optionsConcentration"
            label="Costain"
            stack-label
            dense
            style="min-width: 220px; font-size: 12px;"
          />

          <q-checkbox v-model="autofluorescence" label="Autofluorescence" color="green" size="40px"/>

        <div class="row">
          <q-input
            type="number"
            outlined
            v-model="activeTable.editedItem.concentration_primary"
            stack-label
            label="Primary Concentration"
            dense
            style="max-width: 220px; font-size: 12px;"
            class="q-ml-xl"
          />

          <q-select
            outlined
            v-model="activeTable.editedItem.unit_primary"
            input-debounce="0"
            use-input
            :options="optionsPrimaryUnits"
            counter
            max-values="1"
            label="Unit"
            stack-label
            dense
            style="max-width: 220px; font-size: 12px;"
            class="q-mr-lg"
          />

          <q-input
            type="number"
            outlined
            v-model="activeTable.editedItem.concentration_secondary"
            stack-label
            label="Secondary Concentration"
            dense
            style="max-width: 220px; font-size: 12px;"
          />

          <q-select
            outlined
            v-model="activeTable.editedItem.unit_secondary"
            input-debounce="0"
            use-input
            :options="optionsSecondaryUnits"
            counter
            max-values="1"
            label="Unit"
            stack-label
            dense
            style="max-width: 220px; font-size: 12px;"
          />


        </div>
          <div class="text-center q-ml-sm">
            <q-btn
              style="width: 100PX"
              color="black"
              label="ADD"
              @click="addRow();handleselection();handleselection2();"
              :disable="disableButton"
            ></q-btn>
          </div>

        </div>
        
      </div>
    </div>

    <!-- Table section -->
    <div v-for="(table, index) in tables" :key="index">
      <q-table
        v-if="table.show"
        :rows="table.data"
        :columns="columns"
        :dense="$q.screen.lt.md"
        :row-key="table.rowKey"
        :max-width="table.maxWidth"
        :binary-state-sort="table.binaryStateSort"
        :table-header-style="table.tableHeaderStyle"
        :class="table.className"
        :pagination="table.pagination"

      >
  

        <template v-slot:body-cell-actions="props">
          <q-td key="actions" :props="props">
                <q-btn color="red" label="Delete " icon="delete" @click="deleteItem"  size="11px" class="q-mr-sm"></q-btn>
          </q-td>
        </template>

      </q-table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, onActivated, onDeactivated, emit  } from 'vue';
import API from "src/api";
import { exportFile, useQuasar } from "quasar";


export default {
  setup() {

    const optionsConcentration = ref(['True', 'False']);
    const optionsPrimaryUnits = ref(['ug/mL','mg/mL','ng/mL','ug/uL','M','mM','nM','pM','% v/v']);
    const optionsSecondaryUnits = ref(['ug/mL','mg/mL','ng/mL','ug/uL','M','mM','nM','pM','% v/v']);
    const columns = [
      {
        name: 'desc',
        required: true,
        label: 'Primary',
        align: 'center',
        field: row => row.primary,
        format: val => `${val}`,
        sortable: true,
      },
      { name: 'three', align: 'center', label: 'Secondary', field: 'secondry', sortable: true },
      { name: 'four', align: 'center', label: 'costain', field: 'costain', sortable: true },

      { name: "five", align: "center", label: "Concentration Primary", field: "concentration_primary", sortable: true },
      { name: "six", align: "center", label: "Primary Unit", field: "unit_primary", sortable: true },
      { name: "seven", align: "center", label: "Concentration Secondary", field: "concentration_secondary", sortable: true },
      { name: "eight", align: "center", label: "Secondary Unit", field: "unit_secondary", sortable: true },

      { name: 'actions', align: 'center', label: 'Actions', field: 'actions' },
    ];

    const tables = ref([
      {
        data: [], // Initial data for the first table
        columns: columns,
        rowKey: 'name', // Customize as needed
        maxWidth: '100%', // Customize as needed
        binaryStateSort: true, // Customize as needed
        tableHeaderStyle: 'background-color: #C0C0C0', // Customize as needed
        className: 'q-table--dense', // Customize as needed
        pagination: {
          rowsPerPage: 10, // Customize as needed
        },
        show: true, // Initially show the first table
        editedItem: ref({
          uuid: Math.floor(Math.random() * 1000).toString(),
          primary: [],
          secondry: [],
          costain: [],
          concentration_primary: [],
          unit_primary: [],
          concentration_secondary: [],
          unit_secondary: [],
        }),
      },
    ]);

    const deleteItem=(item)=> {

        const index = activeTable.value.data.indexOf(item);
        confirm("Are you sure you want to Delete this user?") &&
        activeTable.value.data.splice(index, 1) ;
      }

    const disableButton = ref(false);
    const activeTableIndex = ref(0); // Initialize with the index of the first table

    const activeTable = computed(() => tables.value[activeTableIndex.value]);

    var all=[];
    // const addRow = () => {
    //   const primary1 = activeTable.value.editedItem.primary;
    //   const secondry1 = activeTable.value.editedItem.secondry;
    //   const concentration1 = activeTable.value.editedItem.costain;
    //   const concentration_primary1=activeTable.value.editedItem.concentration_primary;
    //   const unit_primary1=activeTable.value.editedItem.unit_primary;
    //   const concentration_secondary1=activeTable.value.editedItem.unit_secondary;
    //   const unit_secondary1=activeTable.value.editedItem.unit_secondary;
      

    //   if (primary1.length > 0 && secondry1.length > 0 && concentration1.length > 0 && concentration_primary1.length > 0 && unit_primary1.length > 0 && concentration_secondary1.length > 0 && unit_secondary1.length > 0) {
    //     const newItem = {
    //       uuid: activeTable.value.editedItem.uuid,
    //       primary: primary1,
    //       secondry: secondry1,
    //       costain: concentration1,
    //       concentration_primary:concentration_primary1,
    //       unit_primary:unit_primary1,
    //       concentration_secondary:concentration_secondary1,
    //       unit_secondary:unit_secondary1,

    //     };
    //     activeTable.value.data.push(newItem);
    //     all.push(newItem)
    //     // console.log(activeTable.value)
  
    //   }
    // };
const addRow = () => {
  const item = activeTable.value.editedItem;

  const allFieldsFilled =
    item.primary.length &&
    item.secondry.length &&
    item.costain.length &&
    item.concentration_primary &&
    item.unit_primary.length &&
    item.concentration_secondary &&
    item.unit_secondary.length;

  if (allFieldsFilled) {
    const newItem = { ...item };  // shallow copy of item
    activeTable.value.data.push(newItem);
    all.push(newItem);

    perform();  // Call your existing perform() to control button state
  }
};




    const perform = () => {
      disableButton.value = activeTable.value.editedItem.costain.includes('False');
    };



    const clearSelection = () => {
      activeTable.value.editedItem.costain = [];
      disableButton.value = false;
    };


    const tablesData = computed(() => {
      const a= tables.value.map(table => table.data); 
    return a;
});




    const addNewTable = () => {
      const newTable = {
        data: [], // Initial data for the new table
        columns: columns, // Initial columns for the new table
        rowKey: 'name', // Customize as needed
        maxWidth: '100%', // Customize as needed
        binaryStateSort: true, // Customize as needed

        tableHeaderStyle: 'background-color: #C0C0C0', // Customize as needed
        className: 'q-table--dense', // Customize as needed
        pagination: {
          rowsPerPage: 10, // Customize as needed
        },
        show: true, // Initially show the new table
        editedItem: {
          uuid: Math.floor(Math.random() * 1000).toString(),
          primary: [],
          secondry: [],
          costain: [],
          concentration_primary:[],
          unit_primary:[],
          concentration_secondary:[],
          unit_secondary:[]
        },
      };
      tables.value.push(newTable);
      activeTableIndex.value = tables.value.length - 1;
    };

 

    return {
      optionsPrimary:ref([]),
      optionsSecondary:ref([]),
      autofluorescence: ref(false),
      optionsConcentration,
      optionsPrimaryUnits,
      optionsSecondaryUnits,
      columns,
      tables,
      disableButton,
      activeTable,
      addRow,
      perform,
      clearSelection,
      addNewTable,
      deleteItem,
      all,
      tablesData,
      // MoreArrsparsedData,
      
    };
    
  },


  methods:{

    async check(){

      this.combi(this.all).then(result => {
          console.log(result); // This will log the array with the combined object
        })
        .catch(error => {
          console.error(error);
        });
      
    },  

    async combi(json_array) {
    let combined_object = {};
    for (const obj of json_array) {
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (!(key in combined_object)) {
                  combined_object[key] = obj[key];
              } else {
                combined_object[key] += ', ' + obj[key];
              }
            }
        }
    }
    return [combined_object]; // Wrap the combined object in an array and return
}

,

        async handleselection2() {
          // const a= this.combi(this.all);
          this.combi(this.all).then(result => {
            // this.$emit("childMessage2", result); // This will log the array with the combined object
            this.$emit("childMessage2", this.all); 
        })
        .catch(error => {
          console.error(error);
        });
        
       },

     handleselection() {
      const parsedData = this.parseData(this.tablesData);
      const rawData = parsedData.map(sublist => sublist.map(item => JSON.parse(JSON.stringify(item))));
 
        this.$emit("childMessage", rawData);
       },

 
      parase(){
      const parsedData = this.parseData(this.tablesData);
      const rawData = parsedData.map(sublist => sublist.map(item => JSON.parse(JSON.stringify(item))));
      console.log(rawData);
        
      },
      parseData(input_data) {
      let parsed_data = {};

      for (let sublist of input_data) {
        for (let item of sublist) {
          let uuid = item.uuid;
          if (!parsed_data[uuid]) {
            parsed_data[uuid] = [];
          }
          parsed_data[uuid].push(item);
        }
      }

      return Object.values(parsed_data);
    }
  },


  mounted() {
      API("auth.Immunofluorescent_details_Antibody_primary").then((res) => {
        // this.optionsPrimary = res.map(item=>item.type_id);
            this.optionsPrimary = res.map(item => item.type_id).sort((a, b) => a.localeCompare(b));

      });

      API("auth.Immunofluorescent_details_Antibody_secondry").then((res) => {
        // this.optionsSecondary = res.map(item=>item.type_id);
            this.optionsSecondary = res.map(item => item.type_id).sort((a, b) => a.localeCompare(b));

      });
    },

};



</script>

<style scoped>
</style>
