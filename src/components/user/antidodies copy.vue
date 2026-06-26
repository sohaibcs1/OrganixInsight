<template>
  <div>
    <!-- Form section -->
  
    <div class="q-pa-sm q-gutter-sm text-black">

      <div class="text-h6 text-center">Antibodies</div>
      <div class="fit">


        <div class="row justify-center fit">
          
          <div class="text-center q-mr-lg">
          <q-btn
            color="green"
            label="ADD New Antibody"
            @click="clearSelection(); addNewTable();"
          ></q-btn>
        </div>
        
          <q-input v-model="activeTable.editedItem.uuid" label="Id:" hidden />
          <q-select
            outlined
            v-model="activeTable.editedItem.primary"
            :options="optionsPrimary"
            hint="Max 1 selection"
            label="Primary Antibody"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />

      
                        
          <q-select
            outlined
            v-model="activeTable.editedItem.secondry"
            :options="optionsSecondary"
            hint="Max 1 selection"
            label="Secondary Antibody"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />
          <q-select
            outlined
            v-model="activeTable.editedItem.costain"
            :options="optionsConcentration"
            hint="Max 1 selection"
            label="Costain"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />

          <div class="text-center q-ml-xl">
            <q-btn
              style="width: 100PX"
              color="black"
              label="ADD"
              @click="addRow(); perform();handleselection();handleselection2();"
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
    const addRow = () => {
      const primary1 = activeTable.value.editedItem.primary;
      const secondry1 = activeTable.value.editedItem.secondry;
      const concentration1 = activeTable.value.editedItem.costain;

      if (primary1.length > 0 && secondry1.length > 0 && concentration1.length > 0) {
        const newItem = {
          uuid: activeTable.value.editedItem.uuid,
          primary: primary1,
          secondry: secondry1,
          costain: concentration1,
        };
        activeTable.value.data.push(newItem);
        all.push(newItem)
        // console.log(activeTable.value)
  
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
        },
      };
      tables.value.push(newTable);
      activeTableIndex.value = tables.value.length - 1;
    };

 

    return {
      optionsPrimary:ref([]),
      optionsSecondary:ref([]),
      optionsConcentration,
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
        this.optionsPrimary = res.map(item=>item.type_id);
      });

      API("auth.Immunofluorescent_details_Antibody_secondry").then((res) => {
        this.optionsSecondary = res.map(item=>item.type_id);
      });
    },

};



</script>

<style scoped>
</style>
