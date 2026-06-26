<template>


   <div class="text-black q-ml-lg fit">

    <div class="text-subtitle1 fit text-white bg-dark "><div class="q-ml-lg">Immunization Selection</div></div>
      <q-list bordered >
        <q-item
          v-for="(item, index) in Immunization_items"
          :key="index"
          clickable
          @click="showPopup(index)"
          v-ripple
          style="width: auto;"
        >
          <q-checkbox v-model="biosource" :val=item color="cyan" />
          <q-item-section>{{ item }}</q-item-section>
          <q-item-label caption>Selected Value: {{ receivedValue }}</q-item-label>
        </q-item>
        
        <div >{{ biosource }}</div>
      </q-list>
      

      <q-dialog v-model="showingPopup" class="custom-dialog">
        <q-card style="width: 1000px;">
          <q-card-section>
            <span v-if="Immunization_items[currentIndex] == 'Counter Strain'">
              <div class="text-h6 text-center">Select {{ Immunization_items[currentIndex] }}</div>
              <epithelial @value-emitted="handleValueEmitted"></epithelial>
            </span>

            <span v-if="Immunization_items[currentIndex] == 'Primary Antibody'">
              <div class="text-h6 text-center">Select {{ Immunization_items[currentIndex] }}</div>
              <epithelial></epithelial>
            </span>

            <span v-if="Immunization_items[currentIndex] == 'Secondary Antibody'">
              <div class="text-h6 text-center">Select {{ Immunization_items[currentIndex] }}</div>
              <epithelial></epithelial>
            </span>
          
          </q-card-section>

         

        </q-card>
      </q-dialog>

  </div>

  
  </template>
  
  
  
  <script>
  import epithelial from 'src/components/user/selection/epithelial';

  export default {
    components:{epithelial},
    data() {
      return {
    
        Immunization_items:[
          "Counter Strain",
          "Primary Antibody",
          "Secondary Antibody",
        ],
        biosource:['Counter Strain'],

        showingPopup: false,
        currentIndex: null,
        receivedValue: "",
   
      };
    },
    methods: {
      handleValueEmitted(value) {
      this.receivedValue = value;
    },
      showPopup(index) {
        this.showingPopup = true;
        this.currentIndex = index;
      }
      
    }
  };
  </script>
  
  <!-- <style scoped>
  .custom-q-item {
    width: 200px; /* Set your desired width */
    height: 50px; /* Set your desired height */
  }
  .custom-dialog {
    width: 300px; /* Set your desired dialog box width */
  }
  </style> -->