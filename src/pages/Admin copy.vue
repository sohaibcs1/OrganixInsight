<template>
  <q-page class="q-pa-md">
    <!-- outer div responsive -->
    <div
      class="fit row wrap justify-start items-start content-start q-col-gutter-none"
    >
      <!-- 1 col -->
      <div class="col-1 col-xs-2 q-col-gutter-none" style="overflow: hidden">
        <div class="text-blck q-gutter-xs" style="font-size: 2em">
          <!-- q-gutter-xs for margin between icons -->

          <div class="q-pa-xs q-gutter-sm">
            <div
              style="font-size: 50%; font-weight: bold"
              class="q-pa-xs no-margin"
            >
              <q-list>
                <q-expansion-item
                  group="somegroup"
                  label="Users"
                  header-class="text-black"
                >
                  <q-card class="bg-blue-5">
                    <q-card-section>
                      <div class="hoo" @click="toggleUser">
                        <q-icon name="receipt" /> Add/Remove User
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-expansion-item
                  group="somegroup"
                  label="Biospecimen"
                  header-class="text-black"
                >
                  <q-card class="bg-blue-5">


                    <q-expansion-item
                      :header-inset-level="1"
                      label="Cells"
                      default>
                              <q-card class="bg-blue-5">
                                <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> MCF10A</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> MDA-MB-231 (TNB)
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> Hs578t</div>
                            </q-card-section>
                          </q-card>
                    </q-expansion-item>


                    <q-expansion-item
                      :header-inset-level="1"
                      label="Fibroblast"
                      default>
                      <q-card-section>
                 
                              <div class="hoo">
                                <q-icon name="receipt" /> P-MF-F(Fibroblast)
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> P-MF-F(CD36+)
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> P-MF-F(CD36-)
                              </div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> I_MF-F</div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> I_MF-F(CD36+)
                              </div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> I_MF-F(CD36-)
                              </div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> P_HC0671</div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> I_HC06771</div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> I_HC0671-CD36+
                              </div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> I_HC0671-CD36-
                              </div>
                            </q-card-section>
                            
                    </q-expansion-item>

                    
                    <q-expansion-item
                      :header-inset-level="1"
                      label="CAF"
                      default>

                      <q-card-section>
                      <div class="hoo">
                        <q-icon name="cameraswitch" /> CAF-PID 175611
                      </div>
                    </q-card-section>

                    <!-- <q-separator  inset /> -->
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="location_on" /> CAF-PID 176996
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="branding_watermark" /> CAF-PID 176996
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 179192
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 218683
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 272386
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 558632
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 868763
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 128162
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 338244
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> CAF-PID 415267
                      </div>
                    </q-card-section>

                    </q-expansion-item>

                    <q-expansion-item
                      :header-inset-level="1"
                      label="Organoid"
                      default>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="location_on" /> Patient ID 171881
                        </div>
                      </q-card-section>
                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="branding_watermark" /> Patient ID 337426
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 338244
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 415267
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 428986
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 562452
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 755229
                        </div>
                      </q-card-section>

                      <q-card-section>
                        <div class="hoo">
                          <q-icon name="travel_explore" /> Patient ID 868763
                        </div>
                      </q-card-section>

                    </q-expansion-item>

                    <q-expansion-item
                      :header-inset-level="1"
                      label="PDX"
                      default>
                      <q-card-section>
                      <div class="hoo">
                        <q-icon name="cameraswitch" /> Patient ID 171881
                      </div>
                    </q-card-section>

                    <!-- <q-separator  inset /> -->
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="location_on" /> Patient ID 193832
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="branding_watermark" /> Patient ID 337426
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 397859
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 412248
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 447297
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 562452
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 755229
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 868763
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 885512
                      </div>
                    </q-card-section>
                    </q-expansion-item>

                    <q-expansion-item
                      :header-inset-level="1"
                      label="Tumor"
                      default>
                      <q-card-section>
                      <div class="hoo">
                        <q-icon name="cameraswitch" /> MMTC-PyMT
                      </div>
                    </q-card-section>

                    <!-- <q-separator  inset /> -->
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="location_on" /> CD34+ NSC
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="branding_watermark" /> NOD-SCID
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> BALB/c
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> C57/BL6
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 447297
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 562452
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 755229
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 868763
                      </div>
                    </q-card-section>

                    <q-card-section>
                      <div class="hoo">
                        <q-icon name="travel_explore" /> Patient ID 885512
                      </div>
                    </q-card-section>
                    </q-expansion-item>

                  </q-card>
                </q-expansion-item>

                <q-separator />


                <q-expansion-item
                  group="somegroup"
                  label="Perturbagens"
                  default
                  header-class="text-black"
                >
                  <q-card class="bg-blue-5">
                   
                    <q-expansion-item
                      :header-inset-level="1"
                      label="Drug"
                      default>
                              <q-card class="bg-blue-5">
                                <q-card-section> Proteins</q-card-section>
                                <q-separator/>
                                <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> PENK RP</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> SLIT3 RP
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> FBLN1 RP</div>
                            </q-card-section>
                          </q-card>
                    </q-expansion-item>
                    
                    <q-separator/>
                    <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> Stiffness
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> Radiation
                              </div>
                            </q-card-section>
                   
                  </q-card>
                </q-expansion-item>
                <!-- Search Route -->

                <q-expansion-item
                  group="somegroup"
                  label="Immunofluorescent"
                  default
                  header-class="text-black"
                >
                  <q-card class="bg-blue-5">
                   
                    <q-expansion-item
                      :header-inset-level="1"
                      label="Nuclear Counterstain"
                      default>
                              <q-card class="bg-blue-5">
                                <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> DAPI</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" /> Hoechst
                              </div>
                            </q-card-section>
                          </q-card>
                    </q-expansion-item>
                  
                    <q-expansion-item
                      :header-inset-level="1"
                      label="Antibody"
                      default>
                              <q-card class="bg-blue-5">
                                <q-card-section> Primary</q-card-section>
                                <q-separator/>
                                <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> Alpha-SMA/ACTA2</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" />  integrin/ITGAG6
                              </div>
                            </q-card-section>

                            <q-card-section> Secondary</q-card-section>
                                <q-separator/>
                                <q-card-section>
                              <div class="hoo"><q-icon name="receipt" /> AF488</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo">
                                <q-icon name="receipt" />  AF64
                              </div>
                            </q-card-section>
                          </q-card>
                    </q-expansion-item>
              
                   
                  </q-card>
                </q-expansion-item>

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
      <div class="col-10 col-xs-10 q-col-gutter-none" style="overflow: hidden">
        <!--  importent START-->
        <div class="q-col-gutter-none no-margin no-margin">
          <div class="text-secondary row q‑pt‑xs">
            <addUserDetails v-if="show_addUserDetails" class="fit" />
          </div>
        </div>
      </div>
      <!-- 10 col END -->
    </div>
  </q-page>
</template>
<script>
import API, { REAL_TIME } from "src/api";
import { ref } from "vue";
import addUserDetails from "src/components/admin/addUserDetails";

export default {
  components: { addUserDetails },
  data() {
    // const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');
    return {
      show_addUserDetails: false,
    };
  },
  mounted() {},
  methods: {
    toggleUser() {
      this.show_addUserDetails = !this.show_addUserDetails;
    },
  },
};
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
