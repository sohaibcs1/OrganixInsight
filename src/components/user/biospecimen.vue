<template>



   <div class="text-black q-ml-lg fit" v-if="bio">

    <div class="text-center q-mb-lg" >
      <q-btn rounded color="red" label="Cancel" icon-right="cancel" @click="refreshPage" ></q-btn>
    </div>
    <div class="text-subtitle1 fit text-white bg-dark "><div class="q-ml-lg">Biosource</div></div>
    <!-- {{ exp_pass }} -->
      <q-list bordered >
        <q-item
          v-for="(item, index) in Biosource"
          :key="index"
          clickable
          v-ripple
          style="width: auto;"
          @click="biosource_model = item"

        >
          <q-radio  v-model="biosource_model" :val=item color="grey" />
          <q-item-section>{{ item }}</q-item-section>

        </q-item>

        <!-- <div class="q-ml-lg">{{ biosource_model }}</div> -->
      </q-list>




    </div>

  <div class="text-black q-ml-lg fit" v-if="bio">

<div class="text-subtitle1 fit text-white bg-dark "><div class="q-ml-lg">Other Treatment</div></div>
  <q-list bordered >
    <q-item
      v-for="(item, index) in other"
      :key="index"
      clickable
      v-ripple
      style="width: auto;"
      @click="toggleOtherSelection(item)"

    >
      <q-checkbox v-model="other_model" :val=item color="grey" />
      <q-item-section>{{ item }}</q-item-section>

    </q-item>

    <!-- <div class="q-ml-lg">{{ other_model }}</div> -->
  </q-list>


    <div class="text-center">
      <q-btn color="dark" label="Generate Exeperiment factors" icon-right="skip_next" class="q-mt-sm q-mr-lg"  @click=" bio=false; variable_selection=true;" ></q-btn>
    </div>

    </div>

  <div v-if="variable_selection">
    <variableSelection class="fit" :biosource_selection="biosource_model" :other_selection="other_model" :exp_pass_prop="exp_pass_biosp"></variableSelection>
  </div>
  <div v-if="home">
    <studies class="fit" ></studies>
  </div>


  </template>



  <script>

  import variableSelection from 'src/components/user/variableSelection';


  export default {
    props: {exp_pass: Array},
    components:{variableSelection},
    mounted(){
      const exp_passGlobal=[...this.exp_pass];
      this.exp_pass_biosp=exp_passGlobal
    //  console.log(this.exp_pass1,"kb1")
    },
    data() {
      return {
        variable_selection:false,
        exp_pass_biosp:[],
        home:false,
        bio:true,
        Biosource:[
          "Epithelial (select first co-culture)",
          "Stromal cells",
          "Organoid",
          "PDX",
          "Tumor"
        ],
        other:[
          "Drug",
          "Virus",
          "Plasmid",
          "EM Exposure",
          "Stiffness",
          "Harvest Time"
        ],
        biosource_model:[],
        other_model:[],

        receivedValue: "",

      };
    },
    methods: {

      refreshPage() {
      window.location.reload();
    }
,
    toggleOtherSelection(item) {
      const index = this.other_model.indexOf(item);
      if (index === -1) {
        this.other_model.push(item);
      } else {
        this.other_model.splice(index, 1);
      }
    },

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
