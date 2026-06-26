<template>
<q-page>
  <!-- <div>
    <button @click="filterarray">{{receivecombination}}
</button>
  </div> -->
  <div class="content-justify q-mt-0" v-if="bio">
    <div class="text-center q-mb-sm" >
      <q-btn rounded color="red" label="Cancel" icon-right="cancel" @click="refreshPage" ></q-btn>
    </div>
<!--
      <div class="content-justify q-mt-0"   v-if="biosource_selection">
        <cellCulture rounded-borders  @childMessage="handleChildMessage" ></cellCulture>
      </div> -->

        <cellCulture rounded-borders v-if="biosource_selection === 'Epithelial'" @childMessage="handleChildMessage_cell"></cellCulture>
        <fibroblast rounded-borders v-if="biosource_selection === 'Fibroblast'" @childMessage="handleChildMessage_fibroblast"></fibroblast>
        <organoid rounded-borders v-if="biosource_selection === 'Organoid'" @childMessage="handleChildMessage_organoid"></organoid>
        <pdx rounded-borders v-if="biosource_selection === 'PDX'" @childMessage="handleChildMessage_pdx"></pdx>
        <tumor rounded-borders v-if="biosource_selection === 'Tumor'" @childMessage="handleChildMessage_tumor"></tumor>


<!-- {{other_selection}}/ -->
      <div class="content-justify q-mt-0"   v-for="(item, index) in other_selection" :key="index">
        <harvestTime rounded-borders v-if="item === 'Harvest Time'" @childMessage="handleChildMessage_harvesttime"></harvestTime>
        <Stiffness rounded-borders v-if="item === 'Stiffness'" @childMessage="handleChildMessage_stiffness"></Stiffness>
        <radiation rounded-borders v-if="item === 'Radiation'" @childMessage="handleChildMessage_radiation"></radiation>
        <drug rounded-borders v-if="item === 'Drug'" @childMessage="handleChildMessage_drug" ></drug>
        <virus rounded-borders v-if="item === 'Virus'" @childMessage="handleChildMessage_virus"></virus>

      </div>


  <div class="text-center">
      <!-- <q-btn color="dark" label="Show Combination" icon-right="skip_next" class="q-mt-sm q-mr-lg"  @click="small=true ;finalReadyArray()"></q-btn> -->
      <q-btn color="dark" label="Show Combination" icon-right="skip_next" class="q-mt-sm q-mr-lg"  @click="startTimer() ;finalReadyArray()"></q-btn>
  </div>
  <!-- {{ exp_pass_prop }} -->

  </div>

  <!-- <button >Click me</button> -->
  <!-- finalReadyArray -->
  <div v-if="show_combinations" class="fit">
    <Showcombinations class="fit" :receivedArray="finalMergesArray" :exp_pass_combination_prop="exp_pass_combination" ></Showcombinations>
    <!-- <button @click="parseArrays(receivedcellculture); parseArrays(receivedharvest);parseArrays(receiveddrug); parseArrays(receivedradiation);parseArrays(receivedStiffness)">Click me</button> -->
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
</q-page>
</template>

<script>
import API from 'src/api'
import { ref } from 'vue'
import { exportFile, useQuasar } from 'quasar'
import cellCulture from "src/components/user/selection/cellCulture";
import fibroblast from "src/components/user/selection/fibroblast";

import organoid from "src/components/user/selection/organoid";
import pdx from "src/components/user/selection/pdx";
import tumor from "src/components/user/selection/tumor";
import harvestTime from "src/components/user/selection/harvestTime";
import Stiffness from "src/components/user/selection/stiffness";
import Showcombinations from "src/components/user/combinations";
import radiation from "src/components/user/selection/radiation";
import drug from "src/components/user/selection/drug";
import virus from "src/components/user/selection/virus";




export default {
  components:{cellCulture,fibroblast,harvestTime,Stiffness,Showcombinations,radiation,drug,organoid,pdx,tumor,virus},
  // props: {exp_pass_prop: Array},
  // props: ['biosource_selection','other_selection'],
  props: {
  exp_pass_prop: Array,
  biosource_selection: String,
  other_selection: String,
},

  setup() {



    return {

      show_combinations:ref(false),
      bio:ref(true),
      small:ref(null),
      receivedcellculture: "",
      isDrugCombine:"",
      receivedharvest: "",
      receiveddrug:"",
      receivedvirus:"",
      receivedradiation:"",
      receivedStiffness:"",
      isLoading: true,
      exp_pass_combination:[],

      // parse_cellClture:[],
      // parse_harvest:[],
      // parse_drug:[],
      // parse_radiation:[],
      // parase_stiffness:[],
      finalMergesArray:["hello"]

    }
  },
  mounted() {
    const exp_pass__propGlobal=[...this.exp_pass_prop];
    this.exp_pass_combination=exp_pass__propGlobal
},
created() {

  },
  computed: {

    // cellCultureValue() {
    //   return this.parseArrays(this.receivedcellculture);
    // }
},
  methods: {

    startTimer() {
      this.$q.notify({
      message: 'Processed',
      color: 'green', // You can change the color to indicate success
      icon: 'announcement',
    });

      setTimeout(() => {
        this.bio = false;
        this.show_combinations = true;
        // this.small = false; // Close the dialog
      }, 1000);
    },
   async formated_arryes(){
      const parse_cellClture=this.parseArrays(this.receivedcellculture);
      const parse_harvest=this.parseArrays(this.receivedharvest) ;
      const parse_drug=this.parseArrays(this.receiveddrug);
      const parse_virus=this.parseArrays(this.receivedvirus);
      const parse_radiation=this.parseArrays(this.receivedradiation);
      const parase_stiffness=this.parseArrays(this.receivedStiffness);
            return [
          parse_cellClture,
          parse_harvest,
          parse_drug,
          parse_virus,
          parse_radiation,
          parase_stiffness
        ];
    },
    // async arraysLength(){
    //         const [
    //       parsedCellCulture,
    //       parsedHarvest,
    //       parsedDrug,
    //       parsedVirus,
    //       parsedRadiation,
    //       parsedStiffness
    //     ] = await this.formated_arryes();
    //   var cellCulture_len=parsedCellCulture.length;
    //   var harvesttime_len=parsedHarvest.length ;
    //   var drug_len=parsedDrug.length;
    //   var virus_len=parsedVirus.length;
    //   var radiation_len=parsedRadiation.length;
    //   var Stiffness_len=parsedStiffness.length;
    //   // console.log("cellCulture_len"+cellCulture_len+"harvesttime_len"+harvesttime_len+"drug_len"+drug_len+"radiation_len"+radiation_len+"Stiffness_len"+Stiffness_len);
    //   if (cellCulture_len === 0) {
    //     cellCulture_len = 1;
    //   }
    //   if (harvesttime_len === 0) {
    //     harvesttime_len = 1;
    //   }
    //   if (drug_len === 0) {
    //     drug_len = 1;
    //   }
    //    if (drug_len >1 ) {
    //     drug_len = drug_len*2;
    //     console.log(parsedDrug,"drug")
    //   }
    //   if (virus_len === 0) {
    //     virus_len = 1;
    //   }
    //   if (radiation_len === 0) {
    //     radiation_len = 1;
    //   }
    //   if (Stiffness_len === 0) {
    //     Stiffness_len = 1;
    //   }

    //   const combine_length=cellCulture_len*harvesttime_len*drug_len*virus_len*radiation_len*Stiffness_len
    //   console.log("combine_length:"+combine_length)

    //   return [combine_length,parsedCellCulture,parsedHarvest,parsedDrug,parsedVirus,parsedRadiation,parsedStiffness];

    // },
    generateDrugCombinations(parsedDrug) {
  const allCombinations = [];

  // Step 1: Add individual drug entries
  allCombinations.push(...parsedDrug);

  // Step 2: Group by drug name
  const drugMap = {};
  parsedDrug.forEach(d => {
    if (!drugMap[d.drug]) drugMap[d.drug] = [];
    drugMap[d.drug].push(d);
  });

  const drugNames = Object.keys(drugMap);

  // Step 3: Create pairwise combinations (Penk_DMX with 0_4)
  for (let i = 0; i < drugNames.length; i++) {
    for (let j = i + 1; j < drugNames.length; j++) {
      const drugA = drugNames[i];
      const drugB = drugNames[j];
      const comboName = `${drugA}_${drugB}`;

      const listA = drugMap[drugA];
      const listB = drugMap[drugB];

      for (const a of listA) {
        for (const b of listB) {
          allCombinations.push({
            drug: comboName,
            concentration: `${a.concentration}_${b.concentration}`,
            unit_drug: a.unit_drug || b.unit_drug || '',
            comment_drug: a.comment_drug || b.comment_drug || ''
          });
        }
      }
    }
  }

  return allCombinations;
}

// ....
,
    async arraysLength() {
  const [
    parsedCellCulture,
    parsedHarvest,
    parsedDrug,
    parsedVirus,
    parsedRadiation,
    parsedStiffness
  ] = await this.formated_arryes();

  const cellCulture_len = parsedCellCulture.length || 1;
  const harvesttime_len = parsedHarvest.length || 1;
  const virus_len = parsedVirus.length || 1;
  const radiation_len = parsedRadiation.length || 1;
  const Stiffness_len = parsedStiffness.length || 1;

  var drug_len;
  var drugsarray=[];

  if(this.isDrugCombine==="nc"){
  drug_len = parsedDrug.length || 1;;
  drugsarray.push(...parsedDrug);  // ✅ append without overriding
  }
 else{
    // ✅ Get all single + combination drugs
  const allDrugCombos = this.generateDrugCombinations(parsedDrug);
  const allcombinationdrug_len = allDrugCombos.length || 1;;
  drug_len=allcombinationdrug_len
  drugsarray.push(...allDrugCombos);  // ✅ append without overriding
  }

  console.log("✅ Drug entries including pairwise combos:", drug_len);
  // console.table(allDrugCombos);

  const combine_length =
    cellCulture_len *
    harvesttime_len *
    drug_len *
    virus_len *
    radiation_len *
    Stiffness_len;

  console.log("🧪 Final Combination Length:", combine_length);

  return [
    combine_length,
    parsedCellCulture,
    parsedHarvest,
    drugsarray,
    parsedVirus,
    parsedRadiation,
    parsedStiffness
  ];
}

,

   async change_length_arraysList(){
    const [
          combine_length,
          parsedCellCulture,
          parsedHarvest,
          parsedDrug,
          parsedVirus,
          parsedRadiation,
          parsedStiffness
        ] = await this.arraysLength();

      var increase_length_cellculture=this.duplicateArrayElements(parsedCellCulture,combine_length)
      if(this.isDrugCombine==="c"){
      console.log(this.isDrugCombine,"testttttttttttttttttttttttttttt")

      var increase_length_harvest=this.duplicateArrayElementsR(parsedHarvest,combine_length)
      var increase_length_drug=this.duplicateArrayElementsR(parsedDrug,combine_length)
      var increase_length_virus=this.duplicateArrayElementsR(parsedVirus,combine_length)
      var increase_length_radiation=this.duplicateArrayElementsR(parsedRadiation,combine_length)
      var increase_length_stiffness=this.duplicateArrayElementsR(parsedStiffness,combine_length)
      }
      else{
      console.log(this.isDrugCombine,"testttttttttttttttttttttttttttt")
      var increase_length_harvest=this.duplicateArrayElementsRnoCombination(parsedHarvest,combine_length)
      var increase_length_drug=this.duplicateArrayElementsRnoCombination(parsedDrug,combine_length)
      var increase_length_virus=this.duplicateArrayElementsRnoCombination(parsedVirus,combine_length)
      var increase_length_radiation=this.duplicateArrayElementsRnoCombination(parsedRadiation,combine_length)
      var increase_length_stiffness=this.duplicateArrayElementsRnoCombination(parsedStiffness,combine_length)
      }

      // console.log(increase_length_harvest,increase_length_cellculture,increase_length_drug,increase_length_radiation,increase_length_stiffness)
      return [increase_length_harvest,increase_length_cellculture,increase_length_drug,increase_length_virus,increase_length_radiation,increase_length_stiffness]
    },


    async finalReadyArray(){
      const lastDrug = this.receiveddrug[this.receiveddrug.length - 1];
      const value = lastDrug.isCombinationDrug;
      this.isDrugCombine=value;
      // console.log(value,"cobinationllllllll")
      const [
      increase_length_harvest,
      increase_length_cellculture,
      increase_length_drug,
      increase_length_virus,
      increase_length_radiation,
      increase_length_stiffness,
        ] = await this.change_length_arraysList();

        const arraysToMerge = [
        increase_length_harvest,
        increase_length_cellculture,
        increase_length_drug,
        increase_length_virus,
        increase_length_radiation,
        increase_length_stiffness,
      ];

      console.log("increase_length_cellculture",increase_length_cellculture)
      console.log("increase_length_drug",increase_length_drug)
      console.log("increase_length_virus",increase_length_virus)


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
//     duplicateArrayElementsR(array, length) {
//   const duplicatedArray = [];
//   const originalLength = array.length;

//   if (originalLength === 0) {
//     return duplicatedArray;
//   }

//   const numberOfDuplications = Math.ceil(length / originalLength);

//   for (let i = 0; i < originalLength; i++) {
//     for (let j = 0; j < numberOfDuplications; j++) {
//       const duplicatedElement = { ...array[i], uuid: Math.floor(Math.random() * 100000) };
//       duplicatedArray.push(duplicatedElement);
//     }
//   }

//   return duplicatedArray.slice(0, length);
// }

//Change fromGPT12
//  duplicateArrayElementsR(array, length) {
//   const duplicatedArray = [];
//   const originalLength = array.length;

//   if (originalLength === 0) {
//     return duplicatedArray;
//   }

//   const numberOfDuplications = Math.ceil(length / originalLength);

//   // Create the duplicated elements
//   for (let i = 0; i < originalLength; i++) {
//     for (let j = 0; j < numberOfDuplications; j++) {
//       const duplicatedElement = { ...array[i], uuid: Math.floor(Math.random() * 100000) }; // Assign new uuid
//       duplicatedArray.push(duplicatedElement);
//     }
//   }

//   // Limit the array to the desired length
//   const finalArray = duplicatedArray.slice(0, length);

//   // Ensure no two subsequent elements have the same 'time'
//   for (let i = 1; i < finalArray.length; i++) {
//     if (finalArray[i].time === finalArray[i - 1].time) {
//       // If the current element has the same 'time' as the previous one, find a non-consecutive element to swap
//       for (let j = i + 1; j < finalArray.length; j++) {
//         if (finalArray[j].time !== finalArray[i].time && finalArray[j].time !== finalArray[i - 1].time) {
//           // Swap the elements to avoid having the same 'time' consecutively
//           [finalArray[i], finalArray[j]] = [finalArray[j], finalArray[i]];
//           break;
//         }
//       }
//     }
//   }

//   return finalArray;
// }

// combination
duplicateArrayElementsR(array, length) {

  const duplicatedArray = [];
  const originalLength = array.length;

  if (originalLength === 0) {
    return duplicatedArray;
  }

  let currentIndex = 0;
  while (duplicatedArray.length < length) {
    const duplicatedElement = { ...array[currentIndex % originalLength], uuid: Math.floor(Math.random() * 100000) };
    duplicatedArray.push(duplicatedElement);
    currentIndex++;
  }

  return duplicatedArray;
},
//No combination
 duplicateArrayElementsRnoCombination(array, length) {
  const duplicatedArray = [];
  const originalLength = array.length;

  if (originalLength === 0) {
    return duplicatedArray;
  }

  const numberOfDuplications = Math.ceil(length / originalLength);

  // Create the duplicated elements
  for (let i = 0; i < originalLength; i++) {
    for (let j = 0; j < numberOfDuplications; j++) {
      const duplicatedElement = { ...array[i], uuid: Math.floor(Math.random() * 100000) }; // Assign new uuid
      duplicatedArray.push(duplicatedElement);
    }
  }

  // Limit the array to the desired length
  const finalArray = duplicatedArray.slice(0, length);

  // Ensure no two subsequent elements have the same 'time'
  for (let i = 1; i < finalArray.length; i++) {
    if (finalArray[i].time === finalArray[i - 1].time) {
      // If the current element has the same 'time' as the previous one, find a non-consecutive element to swap
      for (let j = i + 1; j < finalArray.length; j++) {
        if (finalArray[j].time !== finalArray[i].time && finalArray[j].time !== finalArray[i - 1].time) {
          // Swap the elements to avoid having the same 'time' consecutively
          [finalArray[i], finalArray[j]] = [finalArray[j], finalArray[i]];
          break;
        }
      }
    }
  }

  return finalArray;
}


,



    parseArrays(array){
       // Convert and log the values as a JSON array
        const jsonArray = JSON.stringify(Object.values(array));
        const parsedArray = JSON.parse(jsonArray);
        console.log('kkkk:', array);

        //Making parsing array
        const parsedDataArray = parsedArray.map(item => {
        const parsedItem = { ...item };
        for (const key in parsedItem) {
          if (Array.isArray(parsedItem[key]) && parsedItem[key].length > 0) {
            parsedItem[key] = parsedItem[key][0];
          }
        }

        return parsedItem;
      });
      // console.log(parsedDataArray);

      return parsedDataArray;
    },

    // filterarray(){
    //   const cellCulture=this.receivedcellculture
    //   // return
    //   console.log( )
    // },


    handleChildMessage_cell(message) {
      this.receivedcellculture = message;
    },
    handleChildMessage_fibroblast(message) {
      this.receivedcellculture = message;
    },
    handleChildMessage_organoid(message) {
      this.receivedcellculture = message;
    },
    handleChildMessage_pdx(message) {
      this.receivedcellculture = message;
    },
    handleChildMessage_tumor(message) {
      this.receivedcellculture = message;
    },

    handleChildMessage_harvesttime(message) {
      this.receivedharvest = message;
    },
    handleChildMessage_drug(message) {
      this.receiveddrug = message;
    },

    handleChildMessage_virus(message) {
      this.receivedvirus = message;
    },
    handleChildMessage_radiation(message) {
      this.receivedradiation = message;
    },
    handleChildMessage_stiffness(message) {
      this.receivedStiffness = message;
    },

    refreshPage() {
      window.location.reload();
    }




  },

  data: () => ({



  }),






}
</script>


