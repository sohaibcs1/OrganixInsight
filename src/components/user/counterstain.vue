<template>

    <div 	>
      <div class="q-pa-sm q-gutter-sm text-black" >
        <div class="text-h6 text-center ">Counterstain</div>
        
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" 
          class="q-table--dense" :pagination="pagination">
          <template v-slot:top> 
  
            <div class="fit">
                    <div class="row justify-center fit">
                     

                      <q-input v-model="editedItem.uuid" label="Id:" hidden />

                          <q-select outlined v-model="editedItem.counterstain"  :options="optionsCounterstain"   
                          hint="Max 1 selection" label="Counter Stain" stack-label dense  style="min-width: 300px; font-size: 12px;"   multiple
                          use-chips/>
                          <!-- <q-input outlined  v-model="editedItem.comment_drug"  stack-label 
                          dense label="comment_drug" style="max-width: 180px; font-size: 12px;"/> -->
                          <div class="text-center q-ml-xl"><q-btn style="width: 100PX;"  color="black"  label="ADD" @click="addRow();handleselection();"></q-btn></div>
                        
                    </div>
  
                  
            </div>
       
           
  
          </template>
  
   
  
          <template v-slot:body="props">
            <q-tr :props="props" >
              
              <q-td key="desc" :props="props">
                {{ props.row.counterstain }}
              </q-td>
  
       
   
              
              
  
              <q-td key="actions" :props="props">
                <q-btn color="red" label="Delete"  @click="deleteItem(props.row)" size="11px" class="q-mr-sm"></q-btn>
                
              </q-td>
            </q-tr>
          </template>
        </q-table>
      
      </div>
  
      <!-- <div class="text-center">
                      <q-btn color="dark" label="Submit" icon-right="skip_next" class="q-mt-sm q-mr-lg" ></q-btn>
                  </div> -->
      
    </div>
  </template>
  
  <script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'
  import axios from "axios";

  // import biospecimen from "src/components/user/biospecimen";
  
  
  // const date = require('date-and-time')
  // const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');
  
  const selectedExp=""
  
  const columns = [
    {
      name: 'desc',
      required: true,
      label: 'Counterstain',
      align: 'center',
      field: row => row.counterstain,
      format: val => `${val}`,
      sortable: true
    },
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    // { name: 'one', align: 'center', label: 'Time drug', field: 'drug', sortable: true },
  
  
    { name: "actions", align: 'center', label: "Actions", field: "actions" }
  
  ]
  
  var listLocation=[]
  var listRoute=[]
   
  const stringOptionsPrimary= ['Alpha6 integrin, ITGA6','Alpha_SMA, ACTA2','Beta Catenin, CTNNB','Caspase-3, CASP3','NucView Caspase3, L_CASP3','CD36',
'CD3','CD3D','CD8, CD8A','Ecadherin,CDH1','FABPP4','Keratin 5, KRT5','Keratin 7, KRT7', 'Keratin 8, KRT8','Keratin 14, KRT4',
'Keratin 18, KRT18','VIM']
  const stringOptionsSecondary=['AF488','AF647']
  // const stringOptionsCounterStain=['DAPI','Hoechst']
  
  
  
  var key
  
  export default {
    
    components:{},
  
    // props: ['id_row','study_name'],
  
    setup() {
      const $q = useQuasar()
      const optionsPrimary= ref(stringOptionsPrimary)
      const optionsSecondary= ref(stringOptionsSecondary)
      // const optionsCounterstain= ref(stringOptionsCounterStain)
  
      return {
        pagination: {
        rowsPerPage: null // current rows per page being displayed
      },
      // expShow:true,
        // show_biospeciman:ref(false),
        listLocation,
        listRoute,
        columns,
        show_dialog: ref(false),
        editedIndex: -1,
        userD: ref(false),
        callselectedExperemtnValu:"",
        editedItem: ref({
          uuid: Math.floor(Math.random() * 1000).toString(),
        
          counterstain:[],
        }),
        defaultItem: ref({
          uuid: Math.floor(Math.random() * 1000).toString(),
    
          counterstain:[],
        }),
  
        optionsPrimary,
        optionsSecondary,
        optionsCounterstain:ref([]),
  
      }
    },
    // watch: {
    // // Watch for changes in the editedItem.primary property and perform the search
    // "editedItem.primary": function (newValue) {
    //   this.fetchData(newValue);
    // }},
    
    methods: {

   
  
      // async fetchData(query) {
      // try {
      //   const response = await axios.get(
      //     `https://www.genenames.org/tools/search/#!/?query=${query}`
      //   );

      //   // Assuming the API returns data in a certain format, you can extract and format it here.
      //   // For example, if the API returns an array of options:
      //   const options = response.data.results.map((result) => ({
      //     label: result.label, // Label to display in the <q-select> dropdown
      //     value: result.value, // Value to store in editedItem.primary
      //   }));

      //   this.optionsPrimary = options;
      //   console.log(options+"kkkk")
      // } catch (error) {
      //   console.error("Error fetching data:", error);
      // }},
      handleselection() {
          var SelectionModel = this.data;
          this.$emit("childMessage", SelectionModel);
         },
  
         async addRow() {
  if (!this.data) return;

  const counterstainArr = this.editedItem.counterstain;

  // ✅ validate (must select at least 1)
  if (!Array.isArray(counterstainArr) || counterstainArr.length === 0) {
    this.$q.notify({
      message: "Please select at least one Counterstain.",
      color: "red",
      icon: "announcement",
    });
    return;
  }

  // ✅ convert array -> " | " string
  const counterstainStr = counterstainArr.join(" | ");

  const editedIndex1 = this.editedIndex;

  // Build row to save (store STRING not array)
  const rowToSave = {
    uuid: this.editedItem.uuid,
    counterstain: counterstainStr,
  };

  if (editedIndex1 > -1) {
    // ✅ update existing row
    Object.assign(this.data[editedIndex1], rowToSave);
  } else {
    // ✅ add new row
    this.data.push(rowToSave);
  }

  this.callselectedExperemtnValu = this.data;
  this.close();
}
,
      // async addRow() {
  
      //   if(this.data){
      //   const counterstain1=this.editedItem.counterstain

        
      //   const editedIndex1 = this.editedIndex
      //   const oldRow = this.data[editedIndex1]
      //   const updatedRow = this.editedItem
  
      //   if (this.editedIndex > -1) {
      //     Object.assign(oldRow, updatedRow);
      //   } else {
  
      //     if ( counterstain1 ) {
            
           
      //      this.data.push(this.editedItem)
      //      this.callselectedExperemtnValu=this.data
      //     }
      //     else {
      //       this.$q.notify({
      //         message: 'please Enter all Details.',
      //         color: 'red',
      //         icon: 'announcement',
              
      //       })
      //     }
      //   }
      //   this.close()
      // }

  
  
  
      // },
  
      async deleteItem(item) {
        const id = item.uuid
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
    // formattedTransfected() {
    //   // Format the 'props.row.transfected' as needed
    //   // For example, to display a comma-separated string: "1, 8, 7, 3"
    //   return this.props.row.transfected.join(', ');
    // },
  },
  
    mounted() {
    
      

      API("auth.Immunofluorescent_details_nc_DAPI_Hoechst").then((res) => {
        this.optionsCounterstain = res.map(item=>item.type_id);
        // console.log(this.data.type+"dsfsdf" )
      });


    },
    
  
  
  
  }
  </script>
  
  
  