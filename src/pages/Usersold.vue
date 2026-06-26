<template>
  <q-page class="q-pa-md " >

    <!-- outer div responsive -->
    <div class="fit row wrap justify-start items-start content-start q-col-gutter-none">

      <!-- 1 col -->
      <div class="col-1 col-xs-2 q-col-gutter-none " style="overflow: hidden;">


        <div class="text-blck q-gutter-xs " style="font-size: 2em">
          <!-- q-gutter-xs for margin between icons -->


          <div class="q-pa-xs q-gutter-sm">

            <div style="font-size: 50%; font-weight: bold;" class="q-pa-xs no-margin">
              <q-list>

                <q-expansion-item  group="somegroup" label="Morphogenesis"  header-class="text-black">
                  <q-card  class="bg-blue-5" >

                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="receipt" /> Design
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="receipt" /> Visulization
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="receipt" /> HeatMap
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="receipt" /> Image Transfer
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="receipt" /> Data Analysis
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="receipt" /> Algorithm
                      </div>
                    </q-card-section>

                  </q-card>
                </q-expansion-item>

                <q-separator />

                <q-expansion-item group="somegroup" label="Morphogenesis Pilot" default-opened header-class="text-black">
                  <q-card class="bg-blue-5">
                    <!-- <q-card-section>
                        <div class="hoo"  @click="track =true"><q-icon name="send"/> Add</div> 
                      </q-card-section> -->

                      <q-card-section>
                      <div class="hoo" >
                        <q-icon name="cameraswitch" /> Gallahad Pilot Studies
                      </div>
                    </q-card-section>

                    <q-separator  inset />
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="location_on" /> Tissue Stanning
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="branding_watermark" /> PilotExp_DAPI
                      </div>
                    </q-card-section>
             
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="travel_explore" /> BR-Tissue Stanning
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="fiber_dvr" /> Puramatrix Pilot
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="share_location" /> Stiffness Ellen
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="share_location" /> Stiffness Ellen
                      </div>
                    </q-card-section> 

                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="share_location" /> Moduling ethanol
                      </div>
                    </q-card-section> 
                    <q-card-section>
                      <div class="hoo" >
                        <q-icon name="share_location" /> Ethanol Exposure
                      </div>
                    </q-card-section> 
                  
                  </q-card>

                </q-expansion-item>

                <!-- <q-expansion-item group="somegroup" label="Search Route" header-class="text-secondary">
                  <q-card>
                    <q-card-section>
                      <div class="hoo" @click="searachroute = true">
                        <q-icon name="send" /> Search
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item> -->
                <!-- Search Route -->
                <q-separator />
               
            

                <!-- <q-card-section>
                      <searchR></searchR>
                    </q-card-section> -->
                <!-- <hr style="border: 1px solid gray; "> -->




              </q-list>
            </div>

          </div>

        </div>
      </div>
      <!-- 2 col END-->


      <!-- 10 col START-->
      <div class="col-10 col-xs-10 q-col-gutter-none" style="overflow: hidden;">

        <!--  importent START-->
        <div class="q-col-gutter-none no-margin">
          <div class="text-secondary row q‑pt‑xs no-margin">

                         
      
          <div class="q-pa-md " >
            <q-uploader
              auto-upload
              label="Max File upload size (4k)"
              multiple
              max-total-size="4096"
              url="http://localhost:8080/upload"
              
            />
          </div>
          <!-- <q-circular-progress
            indeterminate
            size="90px"
            :thickness="0.2"
            color="green"
            center-color="info"
            track-color="transparent"
            class="q-ma-md"
          /> -->
         
       

            
          </div>
        </div>
        <!--  importent END-->

        <!-- <hr> -->
        <!-- unimportent START-->
        <div class="q-col-gutter-none">
          <div class="row justify-start q-col-gutter-none">

            

          </div>
        </div>
        <!-- unimportent END -->
      </div>
      <!-- 10 col END -->


    </div>


  </q-page>
</template>
<script>
import API, { REAL_TIME } from 'src/api'
import { ref } from 'vue'

export default {

  components: {},
  data() {
    // const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');
    return {
  
    }
  },
  mounted() {},
  methods: {}
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
  color: white
  cursor: pointer
  
.hoo2:hover 
  color: red
  cursor: pointer
  
      

</style>

