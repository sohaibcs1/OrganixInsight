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
                <!-- <q-card-section>
                      <div class="hoo" @click="navigateToHome" >
                        <q-icon name="home" size="15px" /> Home
                      </div>
                </q-card-section>
                <hr> -->

                <q-card-section>
                      <div class="hoo" @click="navigateToOtherPage" >
                        <q-icon name="snippet_folder" size="15px" /> Experiment Design
                      </div>
                </q-card-section>
                <hr>
                <!-- <q-expansion-item
                  group="somegroup"
                  label="Users"
                  header-class="text-black"
                >

                  <q-card class="bg-grey-2">
                    <q-card-section>
                      <div class="hoo" @click="toggleUser">
                        <q-icon name="receipt" /> Add/Remove User
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item> -->


                <q-expansion-item
                  group="somegroup"
                  label="Biospecimen"
                  header-class="text-black"
                  default-opened
                >
                  <q-card >

                              <q-card class="bg-grey-2">
                                <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Epithelial'); toggle_biospecimenCell()" :class="{ active: activeMenu === 'Epithelial' }"><q-icon name="receipt" /> Epithelial</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Fibroblast'); toggle_biospecimenFib()" :class="{ active: activeMenu === 'Fibroblast' }">
                                <q-icon name="receipt"  /> Stroma
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('CAF'); toggle_biospecimenCAF()" :class="{ active: activeMenu === 'CAF' }"><q-icon name="receipt" /> CAF</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Organid'); toggle_biospecimenOrganid()" :class="{ active: activeMenu === 'Organid' }"><q-icon name="receipt" /> Organid</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('PdX'); toggle_biospecimenPdx()" :class="{ active: activeMenu === 'PdX' }"><q-icon name="receipt" /> PdX</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Tumor'); toggle_biospecimenTumor()" :class="{ active: activeMenu === 'Tumor' }"><q-icon name="receipt" /> Tumor</div>
                            </q-card-section>
                          </q-card>


                  </q-card>
                </q-expansion-item>

                <q-separator />


                 <q-expansion-item
                  group="somegroup"
                  label="Perturbagens"
                  default
                  header-class="text-black"
                >
                  <q-card >


                              <q-card class="bg-grey-2">

                                <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Drugs'); toggle_perturbagensDrug()" :class="{ active: activeMenu === 'Drugs' }"><q-icon name="receipt" /> Drugs</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Plasmid'); toggle_perturbagensPlasmid()" :class="{ active: activeMenu === 'Plasmid' }"> <q-icon name="receipt" /> Plasmid</div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Virus'); toggle_perturbagensVirus()" :class="{ active: activeMenu === 'Virus' }"> <q-icon name="receipt" /> Virus</div>
                            </q-card-section>


                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Stiffness'); toggle_perturbagensStiffness()"  :class="{ active: activeMenu === 'Stiffness' }">
                                <q-icon name="receipt" /> Stiffness
                              </div>
                            </q-card-section>

                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Radiation');  toggle_perturbagensRadiation()" :class="{ active: activeMenu === 'Radiation' }"><q-icon name="receipt" /> EM Exposure</div>
                            </q-card-section>
                          </q-card>




                  </q-card>
                </q-expansion-item>
                <!-- Search Route -->
                <q-separator/>


                <q-expansion-item
                  group="somegroup"
                  label="Immunofluorescent"
                  default
                  header-class="text-black"
                >
                  <q-card class="bg-grey-2">

                    <q-card-section>
                              <div class="hoo q-ml-lg" @click=" setActiveMenu('Nuclear Counterstain');  toggle_immunofluorescentNc()" :class="{ active: activeMenu === 'Nuclear Counterstain' }">
                                <q-icon name="receipt" />  Nuclear Counterstain
                              </div>
                      </q-card-section>
                      <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Primary Antibody');  toggle_immunofluorescentPrimary()" :class="{ active: activeMenu === 'Primary Antibody' }"><q-icon name="receipt" /> Primary Antibody</div>
                            </q-card-section>
                            <q-card-section>
                              <div class="hoo q-ml-lg" @click="setActiveMenu('Secondary Antibody'); toggle_immunofluorescentSecondary()" :class="{ active: activeMenu === 'Secondary Antibody' }"><q-icon name="receipt" /> Secondary Antibody</div>
                            </q-card-section>

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
            <biospecimen_cell v-if="show_biospecimenCell" class="fit" />
            <biospecimenFib v-if="show_biospecimenFib" class="fit"></biospecimenFib>
            <biospecimenCAF v-if="show_biospecimenCAF" class="fit"></biospecimenCAF>
            <biospecimenOrganid v-if="show_biospecimenOrganid" class="fit"></biospecimenOrganid>
            <biospecimenPdx v-if="show_biospecimenPdx" class="fit"></biospecimenPdx>
            <biospecimenTumor v-if="show_biospecimenTumor" class="fit"></biospecimenTumor>

            <perturbagens_drug v-if="show_perturbagensDrug" class="fit"></perturbagens_drug>
            <perturbagens_plasmid v-if="show_perturbagensPlasmid" class="fit"></perturbagens_plasmid>
            <perturbagens_virus v-if="show_perturbagensVirus" class="fit"></perturbagens_virus>
            <perturbagens_stiffness v-if="show_perturbagensStiffness" class="fit"></perturbagens_stiffness>
            <perturbagens_radiation v-if="show_perturbagensRadiation" class="fit"></perturbagens_radiation>

            <immunofluorescentNc v-if="show_immunofluorescentNc" class="fit"></immunofluorescentNc>
            <immunofluorescent_primary v-if="show_immunofluorescentPrimary" class="fit"></immunofluorescent_primary>
            <immunofluorescent_secondary v-if="show_immunofluorescentSecondary" class="fit"></immunofluorescent_secondary>
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
import biospecimen_cell from "src/components/admin/biospecimenCell";
import biospecimenFib from "src/components/admin/biospecimenFib";
import biospecimenCAF from "src/components/admin/biospecimenCAF";
import biospecimenOrganid from "src/components/admin/biospecimenOrganid";
import biospecimenPdx from "src/components/admin/biospecimenPdx";
import biospecimenTumor from "src/components/admin/biospecimenTumor";

import perturbagens_drug from "src/components/admin/perturbagens/perturbagens_drug";
import perturbagens_plasmid from "src/components/admin/perturbagens/perturbagens_plasmid";
import perturbagens_virus from "src/components/admin/perturbagens/perturbagens_virus";


import perturbagens_stiffness from "src/components/admin/perturbagens/perturbagens_stiffness";
import perturbagens_radiation from "src/components/admin/perturbagens/perturbagens_radiation";

import immunofluorescentNc from "src/components/admin/immunofluorescent/immunofluorescentNc";
import immunofluorescent_primary from "src/components/admin/immunofluorescent/immunofluorescent_primary";
import immunofluorescent_secondary from "src/components/admin/immunofluorescent/immunofluorescent_secondary";

export default {
  components: { addUserDetails,biospecimen_cell,biospecimenFib,biospecimenCAF,biospecimenOrganid,biospecimenPdx,biospecimenTumor,
    perturbagens_drug,perturbagens_plasmid, perturbagens_stiffness,perturbagens_radiation,
    immunofluorescentNc,immunofluorescent_primary,immunofluorescent_secondary,perturbagens_virus},
  data() {
    // const TodatDate = date.format((new Date()), 'DD-MMMM-YYYY');
    return {
      show_addUserDetails: false,
      show_biospecimenCell:true,
      show_biospecimenFib:false,
      show_biospecimenCAF:false,
      show_biospecimenOrganid:false,
      show_biospecimenPdx:false,
      show_biospecimenTumor:false,
      show_perturbagensDrug:false,
      show_perturbagensPlasmid:false,
      show_perturbagensVirus:false,
      show_perturbagensStiffness:false,
      show_perturbagensRadiation:false,
      show_immunofluorescentNc:false,
      show_immunofluorescentPrimary:false,
      show_immunofluorescentSecondary:false,
      activeMenu: 'Epithelial',

    };
  },
  mounted() {},
  methods: {
    setActiveMenu(menu) {
      this.activeMenu = menu;
    },
    navigateToOtherPage() {
      this.$router.push('/design'); // Navigate to '/rotherpage' route
    },
    navigateToHome() {
      this.$router.push('/resources'); // Navigate to '/rotherpage' route
    },
    toggleUser() {

      this.show_addUserDetails = true;
         // If addUserDetails is shown, hide biospecimenCell
         if (this.show_addUserDetails) {
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;

        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },
    toggle_biospecimenCell() {
      // this.show_biospecimenCell = !this.show_biospecimenCell;
      this.show_biospecimenCell = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenCell) {
        this.show_addUserDetails = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;

        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_biospecimenFib() {
      this.show_biospecimenFib = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenFib) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;

        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_biospecimenCAF() {
      this.show_biospecimenCAF = true;
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenCAF) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },
    toggle_biospecimenOrganid() {
      this.show_biospecimenOrganid = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenOrganid) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_biospecimenPdx() {
      this.show_biospecimenPdx = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenPdx) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenTumor=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_biospecimenTumor() {
      this.show_biospecimenTumor = true;
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_biospecimenTumor) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;

        this.show_perturbagensDrug=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },


    toggle_perturbagensDrug() {
      this.show_perturbagensDrug = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_perturbagensDrug) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_perturbagensPlasmid() {
      this.show_perturbagensPlasmid = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_perturbagensPlasmid) {
        this.show_addUserDetails = false;
        this.show_perturbagensVirus=false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_perturbagensDrug=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_perturbagensVirus() {
      this.show_perturbagensVirus = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_perturbagensVirus) {
        this.show_addUserDetails = false;
        this.show_perturbagensPlasmid = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_perturbagensDrug=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_perturbagensStiffness() {
      this.show_perturbagensStiffness = true;
        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_perturbagensStiffness) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;

        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_perturbagensRadiation() {
      this.show_perturbagensRadiation = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_perturbagensRadiation) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;
        this.show_perturbagensStiffness=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },


    toggle_immunofluorescentNc() {
      this.show_immunofluorescentNc = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_immunofluorescentNc) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentPrimary=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_immunofluorescentPrimary() {
      this.show_immunofluorescentPrimary = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_immunofluorescentPrimary) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensVirus=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentSecondary=false;
      }

    },

    toggle_immunofluorescentSecondary() {
      this.show_immunofluorescentSecondary = true;

        // If biospecimenCell is shown, hide addUserDetails
        if (this.show_immunofluorescentSecondary) {
        this.show_addUserDetails = false;
        this.show_biospecimenCell = false;
        this.show_biospecimenFib=false;
        this.show_biospecimenCAF=false;
        this.show_biospecimenOrganid=false;
        this.show_biospecimenPdx=false;
        this.show_biospecimenTumor=false;
        this.show_perturbagensDrug=false;
        this.show_perturbagensPlasmid=false;
        this.show_perturbagensStiffness=false;
        this.show_perturbagensRadiation=false;
        this.show_immunofluorescentNc=false;
        this.show_immunofluorescentPrimary=false;
      }

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
  color: red
  cursor: pointer

.hoo2:hover
  color: red
  cursor: pointer

.hoo.active
  color: red
  font-weight: bold

</style>
