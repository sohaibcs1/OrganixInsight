<template>
  <q-page class="q-pa-md " >
    <!-- outer div responsive -->
 
    <div class="fit row wrap justify-start items-start content-start q-col-gutter-none">

      <!-- 1 col -->
      <div class="col-1 col-xs-2 q-col-gutter-none " style="overflow: hidden;">


        <div class="text-black q-gutter-xs " style="font-size: 2em">
          <!-- q-gutter-xs for margin between icons -->

          <div class="q-pa-xs q-gutter-sm" >

            <div style="font-size: 50%; font-weight: bold;" class="q-pa-xs no-margin" >
              <q-list >


                  <q-card  class="bg-grey-2" style="height: 100vh;">

                    <!-- <q-card-section>
                      <div class="hoo" @click="navigateToHome">
                        <q-icon name="home" /> Home
                      </div>
                    </q-card-section>
                    <hr> -->
                    <!-- https://fonts.google.com/icons   for icons visit -->
                    <q-card-section>
                      <div class="hoo" @click="navigateToOtherPage">
                        <q-icon name="snippet_folder" /> Resource Manager
                      </div>
                    </q-card-section>
                    <hr>
                    
                <!-- <q-expansion-item group="somegroup"  label="Experimental Design" default header-class="text-black" @click="toggle_studies(); refreshPage()">

                </q-expansion-item> -->

                     <q-card-section>
                      <div class="hoo"  @click="toggle_studies(); refreshPage()">
                        <q-icon name="science" /> Experimental Design
                      </div>
                    </q-card-section>
              

                    <!-- <q-card-section>
                      <div class="hoo">
                        <q-icon name="image" @click="toggle_variableSelection"/> 3d Visulizer
                      </div>
                    </q-card-section> -->

                    <!-- <q-card-section>
                      <div class="hoo" @click="toggle_cellPickup">
                        <q-icon name="post_add" /> BioSpecimen
                      </div>
                    </q-card-section> -->
                    
                    <!-- <q-card-section>
                      <div class="hoo" @click="toggle_variableSelection">
                        <q-icon name="loupe" /> Variable Selection
                      </div>
                    </q-card-section> -->
                    <!-- <q-card-section>
                      <div class="hoo" @click="toggle_immunizationSelection">
                        <q-icon name="medical_information" /> combinations
                      </div>
                    </q-card-section> -->


                    <q-card-section>
                      <div class="hoo"  @click="toggle_fileUpload">
                        <q-icon name="analytics" /> Analysis & Visulization
                      </div>
                    </q-card-section> 

                <!-- <q-expansion-item group="somegroup"  label="Analysis & Visulization" default header-class="text-black" @click="toggle_fileUpload">
             
                </q-expansion-item> -->
                    <!-- <q-expansion-item group="somegroup"  label="Analytics" default header-class="text-black" @click="toggle_datanalysis">
                  <q-card class="bg-grey-2">
                  </q-card>
                </q-expansion-item> -->

                <!-- <q-expansion-item group="somegroup"  label="Analysis" default header-class="text-black">
                  <q-card class="bg-grey-2">
                    
                    <q-card-section>
                      <div class="hoo q-ml-sm" @click="toggle_datanalysis">
                        <q-icon name="query_stats" /> Analysis Details
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo q-ml-sm" @click="toggle_heatmap">
                        <q-icon name="bar_chart" /> Heatmap 
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo q-ml-sm" >
                        <q-icon name="category" /> Subtyping (working..)
                      </div>
                    </q-card-section>
                   
                  </q-card>
                </q-expansion-item>

                <q-expansion-item group="somegroup"  label="Visualization" default header-class="text-black">
                  <q-card class="bg-grey-2">
                    
                    <q-card-section>
                      <div class="hoo q-ml-sm" @click="toggle_visulizeData">
                        <q-icon name="visibility" /> Image Viewer
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo q-ml-sm" @click="toggle_viewer3d">
                        <q-icon name="view_in_ar" /> 3D Viewer
                      </div>
                    </q-card-section>
                   
                  </q-card>
                </q-expansion-item> -->

                  </q-card>

              </q-list>
            </div>

          </div>

        </div>
      </div>
      <!-- 2 col END-->


      <!-- 10 col START-->
      <div class="col-10 col-xs-10 q-col-gutter-none" style="overflow: hidden;">
        <!-- <q-breadcrumbs>
          <q-breadcrumbs-el label="Studies" icon="home" />
          <q-breadcrumbs-el label="Add Experiment" icon="widgets" />
          <q-breadcrumbs-el label="Cell Pickup" icon="widgets"/>
          <q-breadcrumbs-el label="Variable Pickup" icon="widgets"/>
          <q-breadcrumbs-el label="Select Combinations" icon="widgets"/>
          <q-breadcrumbs-el label="Save Exeperiment" icon="widgets"/>
          <q-breadcrumbs-el label="upload images" icon="widgets"/>
          <q-breadcrumbs-el label="Visulize Data" icon="widgets"/>
          <q-breadcrumbs-el label="Visulize Data" icon="widgets" />
        </q-breadcrumbs> -->

        <!--  importent START-->
        <div class="q-col-gutter-none no-margin ">
          <div class="text-secondary row q‑pt‑xs no-margin ">
            <!-- <fileUpload  ></fileUpload>  -->
            <studies class="fit" v-if="show_studies"></studies>
            <biospecimen class="fit" v-if="show_cellPickup"></biospecimen>
            <combinations class="fit" v-if="show_immunizationSelection"></combinations>
            <variableSelection class="fit" v-if="show_variableSelection"></variableSelection>
            <fileUpload class="fit" v-if="show_fileUpload"></fileUpload>
            <visulizeData class="fit" v-if="show_visulizeData"></visulizeData>
            <analyseData class="fit" v-if="show_datanalysis"></analyseData>
            <viewer3d class="fit" v-if="viewer3d"></viewer3d>
            <heatmap class="fit" v-if="show_heatmap"></heatmap>
       
          </div>
        </div>
        <!-- <div class="text-center q-mt-lg">
        <q-btn color="dark" label="Back" icon-right="skip_previous" class="q-mt-sm q-mr-lg" style="width: 150px;" @click="toggleComponentsPrevious"></q-btn>
        <q-btn color="dark" label="Next" icon-right="skip_next" class="q-mt-sm " style="width: 150px;" @click="toggleComponentsNext"></q-btn>
    </div> -->
        <!--  importent END-->

        <!-- <hr> -->
        <!-- unimportent START-->
        <!-- <div class="q-col-gutter-none">
          <div class="row justify-start q-col-gutter-none">


          </div>
        </div> -->
        <!-- unimportent END -->
      </div>
      <!-- 10 col END -->


    </div>


  </q-page>
</template>
<script>
import API, { REAL_TIME } from 'src/api'
import { ref } from 'vue'
import fileUpload from 'src/components/user/va';
import biospecimen from 'src/components/user/biospecimen';
import combinations from 'src/components/user/combinations';
import variableSelection from 'src/components/user/variableSelection';
import visulizeData from 'src/components/user/visulizeData';
import studies from 'src/components/user/studies';
import thumbnail from 'src/components/user/uploadbtn';
import analyseData from 'src/components/user/analyse';
import viewer3d from 'src/components/user/3dviewer';
import heatmap from 'src/components/user/heatmap';
// import heatmap from 'src/components/admin/addUserDetails';

export default {

  components: {biospecimen,combinations, variableSelection, fileUpload, visulizeData,studies,analyseData,viewer3d,heatmap},
  data() {
    // const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');
    return {
      show_cellPickup: false,
      show_immunizationSelection:false,
      show_variableSelection:false,
      show_fileUpload:false,
      show_visulizeData:false,
      show_datanalysis:false,
      show_studies:true,
      viewer3d:false,
      show_heatmap:false,
      
      
    }
  },
  mounted() {
    
  },
  methods: {
    refreshPage() {
      window.location.reload();
    },
    navigateToOtherPage() {
      this.$router.push('/resources'); // Navigate to '/rotherpage' route
    },
    navigateToHome() {
      this.$router.push('/design'); // Navigate to '/rotherpage' route
    },
    toggle_cellPickup() {
      this.show_cellPickup = true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_cellPickup) {
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_fileUpload=false;
          this.show_visulizeData=false;
          this.show_studies= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }

    },
    toggle_immunizationSelection() {
      // this.show_immunizationSelection= !this.show_immunizationSelection;
      this.show_immunizationSelection= true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_immunizationSelection) {
          this.show_cellPickup=false;
          this.show_variableSelection=false;
          this.show_fileUpload=false;
          this.show_visulizeData=false;
          this.show_studies= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }
    },

    toggle_variableSelection() {
      this.show_variableSelection= true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_variableSelection) {
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_fileUpload=false;
          this.show_visulizeData=false;
          this.show_studies= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }
    },

    
    toggle_fileUpload() {
      this.show_fileUpload= true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_fileUpload) {
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_visulizeData=false;
          this.show_studies= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }
    },
    toggle_visulizeData() {
      this.show_visulizeData= true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_visulizeData) {
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_fileUpload=false;
          this.show_studies= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;
      }
    },
    toggle_datanalysis() {
      this.show_datanalysis=true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_datanalysis) {
          this.show_visulizeData= false;
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_studies= false;
          this.show_fileUpload= false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }
    },

    toggle_heatmap() {
      
      this.show_heatmap=true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_heatmap) {
          this.show_visulizeData= false;
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_studies= false;
          this.show_fileUpload= false;
          this.viewer3d=false;
          this.show_datanalysis=false;

      }
    },
    toggle_viewer3d() {
      
      this.viewer3d=true;
 
        // If biospecimenCell is shown, hide addUserDetails
        if (this.viewer3d) {
          this.show_visulizeData= false;
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_studies= false;
          this.show_fileUpload= false;
          this.show_datanalysis=false;
          this.show_heatmap=false;
      }
    },
    
    toggle_studies() {
      this.show_studies= true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_studies) {
          this.show_cellPickup=false;
          this.show_immunizationSelection=false;
          this.show_variableSelection=false;
          this.show_fileUpload=false;
          this.show_visulizeData= false;
          this.show_datanalysis=false;
          this.viewer3d=false;
          this.show_heatmap=false;

      }
    },

    toggleComponentsNext() {
      if (this.show_cellPickup) {
        this.show_cellPickup = false;
        this.show_variableSelection = true;
      } else if (this.show_variableSelection) {
        this.show_variableSelection = false;
        this.show_immunizationSelection = true;
      } else if (this.show_immunizationSelection) {
        this.show_immunizationSelection = false;
        this.show_fileUpload = true;
      } else if (this.show_fileUpload) {
        this.show_fileUpload = false;
        this.show_visulizeData = true;
      } else if (this.show_visulizeData) {
  
      }
    },

    toggleComponentsPrevious(){

      if (this.show_variableSelection) {
        this.show_variableSelection = false;
        this.show_cellPickup = true;
      } else if (this.show_immunizationSelection) {
        this.show_immunizationSelection = false;
        this.show_variableSelection = true;
      } else if (this.show_fileUpload) {
        this.show_fileUpload = false;
        this.show_immunizationSelection = true;
      } else if (this.show_visulizeData) {
        this.show_visulizeData = false;
        this.show_fileUpload = true;
      } else if (this.show_cellPickup) {
  
        
      }

    }

  }
}
</script>

<style lang="sass" scoped>
.example-item
  height: 49%
  width: 49%
.example-itemImp
  height: 49%
  width: 49%
.hoo:hover
  color: red
  cursor: pointer

.hoo2:hover
  color: red
  cursor: pointer
  
      
.center-container 
  justify-content: left
  align-items: center
  

</style>

