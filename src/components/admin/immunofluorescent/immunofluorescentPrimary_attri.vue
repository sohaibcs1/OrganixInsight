<template>

    <!--
    Forked from:
    https://quasar.dev/vue-components/table#Example--Popup-editing
  -->
    <div>
      <div class="q-pa-sm q-gutter-sm">
        <div class="text-h6 text-center bg-grey-6">{{ id_row }} Antibody Primary Attributes</div>
        <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
          binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
          class="q-table--dense" :pagination="pagination">
          <template v-slot:top>

            <div class="q-pa-sm q-gutter-sm">


              <q-dialog v-model="show_dialog">
                <q-card style="width:800px;max-width:800px;background-color: #F5F5F5" text-center>
                  <q-card-section>

                    <div class="text-h6 text-center bg-grey-5">Nuclear Counterstain Primary- {{ id_row }} Attributes</div>
                  </q-card-section>

                  <!-- add Camra Details Start -->
                  <q-card-section>



                    <div class="row ">
                      <q-input v-model="editedItem.uuid" label="Id:" hidden />

                          <!-- <q-select outlined v-model="editedItem.immortal" input-debounce="0"  @filter="filterImmortal" use-input multiple :options="optionsImmortal"   counter max-values="1"
                        hint="Max 1 selection" label="Fibroblast:" stack-label dense  /> -->
                          <q-space />


<!--
                        <q-select outlined v-model="editedItem.organism" input-debounce="0"  @filter="filterOrganism" use-input multiple :options="optionsOrganism"   counter max-values="1"
                        hint="Max 1 selection" label="Organism:" stack-label dense  /><q-space /> -->

                        <!-- <q-select outlined v-model="editedItem.subtype" input-debounce="0"  @filter="filterSubtype" use-input multiple :options="optionsSubtype"   counter max-values="1"
                        hint="Max 1 selection" label="Subtype:" stack-label dense  /><q-space />

                        <q-input outlined  v-model="editedItem.description"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Description"/><q-space /> -->


                        <q-input outlined type="textarea" class="fit"  v-model="editedItem.emission_frequency"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Please Type"/><q-space />
                        <!-- <q-select outlined v-model="editedItem.concentration_unit" input-debounce="0"  @filter="filterSource" use-input multiple :options="optionsSource"   counter max-values="1"
                        hint="Max 1 selection" label="Select Unit:" stack-label dense  /><q-space /> -->
                        <!-- <q-input outlined  v-model="editedItem.emission"  stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Enter Emission"/><q-space /> -->
                        <!-- <q-input outlined  v-model="editedItem.tumor_id" placeholder="Enter Tumor Id" stack-label
                        :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Tumor Id"/><q-space /> -->




                    </div>
                  </q-card-section>
                  <!-- add Camra Details END -->

                  <q-card-actions align="center">
                    <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
                    <div class="text-center q-mr-lg"><q-btn  dense color="black" v-close-popup
                        label="Cancel"></q-btn></div>
                    <div class="text-center"><q-btn  dense color="black" v-close-popup label="OK"
                        @click="addRow"></q-btn></div>
                  </q-card-actions>
                </q-card>
              </q-dialog>
            </div>

          </template>



          <template v-slot:body="props">
            <q-tr :props="props">

              <q-td key="desc" :props="props">
                <!-- {{ props.row.emission_frequency }} -->
                <q-checkbox color="teal" size="xs" v-model="OptionSelections" val="nuclear" label="Nuclear"></q-checkbox>
              <q-checkbox color="orange" size="xs" v-model="OptionSelections" val="cytoplasm" label="Cytoplasm"></q-checkbox>
              <q-checkbox color="red" size="xs" v-model="OptionSelections" val="membrane" label="Membrane"></q-checkbox>
              <q-checkbox color="cyan"  size="xs" v-model="OptionSelections" val="ecm" label="ECM"></q-checkbox>

                <q-input
                v-model="comment"
                label="Comment"
                outlined
                dense
                type="textarea"
                rows="2"
                class="q-mt-sm"
              />
            </q-td>

              <!-- <q-td key="one" :props="props">
                {{ props.row.emission }}
              </q-td> -->

              <!-- <q-td key="one" :props="props">
                {{ props.row.time}}
              </q-td> -->
              <!-- <q-td key="two" :props="props">
                {{ props.row.subtype  }}

              </q-td>

              <q-td key="three" :props="props">
                {{ props.row.description }}
              </q-td>
              <q-td key="four" :props="props">
                {{ props.row.mouse_id }}
              </q-td>
              <q-td key="five" :props="props">
                {{ props.row.tumor_id }}
              </q-td> -->

              <!-- <q-td key="nine" :props="props">
                {{ props.row.hyperlink }}
              </q-td> -->


              <!-- <q-td key="actions" :props="props">
                <q-btn color="green" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn>
                <q-btn color="red" label="Delete"  @click="deleteItem(props.row)" size="11px"></q-btn>
              </q-td> -->


            </q-tr>
          </template>
        </q-table>
      </div>

      <div class="text-center q-mt-sm">
        <!-- <q-btn   color="black" label="Add New" @click="show_dialog = true" dense class="q-mr-lg"></q-btn> -->
            <q-btn dense color="black" v-close-popup label="Cancel" class="q-mr-lg"></q-btn>
            <q-btn dense color="black" v-close-popup label="Ok"></q-btn>
      </div>

    </div>

  </template>

  <script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'



  const columns = [
    {
      name: 'desc',
      required: true,
      label: 'Selection ',
      align: 'center',
      field: row => row.emission_frequency,
      format: val => `${val}`,
      sortable: true
    },
    // { name: 'password', align: 'center', label: 'Password', field: 'password', sortable: true },
    // { name: 'first', align: 'center', label: 'Name', field: 'type_id', sortable: true },
    // { name: 'second', align: 'center', label: 'immortal', field: 'immortal', sortable: true },
    // { name: 'second', align: 'center', label: 'source', field: 'source', sortable: true },
    // { name: 'one', align: 'center', label: 'time', field: 'time', sortable: true },
    // { name: 'two', align: 'center', label: 'dosage', field: 'subtype', sortable: true },
    // { name: 'one', align: 'center', label: 'Selection', field: 'emission', sortable: true },
    // { name: 'four', align: 'center', label: 'mouse_id', field: 'mouse_id', sortable: true },
    // { name: 'five', align: 'center', label: 'tumor_id', field: 'tumor_id', sortable: true },
    // { name: "actions", align: 'center', label: "Actions", field: "actions" }

  ]

  var listLocation=[]
  var listRoute=[]

  const stringOptionsOrganism= ['mouse','human']
  const stringOptionsSubtype= ['Empty']
  const stringOptionsSource= ['Pascal']
  const stringOptionsImmortal=  ['Yes', 'No' ]
  const stringOptionsPassage=[]

for (let i = 1; i <= 100; i++) {
  stringOptionsPassage.push(i.toString());
}

  var key

  export default {

    props: ['id_row','type_biosp'],

    setup() {
      const $q = useQuasar()
      const optionsOrganism= ref(stringOptionsOrganism)
      const optionsSource=ref(stringOptionsSource)
      const optionsImmortal=ref(stringOptionsImmortal)
      const optionsPassage= ref(stringOptionsPassage)
      const optionsSubtype= ref(stringOptionsOrganism)

      return {
        pagination: {
        rowsPerPage: null // current rows per page being displayed
      },

        OptionSelections:ref([]),
        comment:ref(null),
        listLocation,
        listRoute,
        columns,
        show_dialog: ref(false),
        editedIndex: -1,
        userD: ref(false),
        editedItem: ref({
          uuid: ref(null),
          type: ref(null),
          emission_frequency: ref(null),

        }),

        defaultItem: ref({
          uuid: ref(null),
          type: ref(null),
          emission_frequency: ref(null),
        }),

        optionsOrganism,
        optionsSource,
        optionsImmortal,
        optionsPassage,
        optionsSubtype,

        filterSubtype (val, update, abort) {
          update(() => {
            const needle = val.toLowerCase()
            optionsSubtype.value = stringOptionsSubtype.filter(v => v.toLowerCase().indexOf(needle) > -1)
          })
        },

        filterPassage (val, update, abort) {
          update(() => {
            const needle = val.toLowerCase()
            optionsPassage.value = stringOptionsPassage.filter(v => v.toLowerCase().indexOf(needle) > -1)
          })
        },
         filterOrganism (val, update, abort) {
          update(() => {
            const needle = val.toLowerCase()
            optionsOrganism.value = stringOptionsOrganism.filter(v => v.toLowerCase().indexOf(needle) > -1)
          })
        },
        filterImmortal(val, update, abort) {
          update(() => {
            const needle = val.toLowerCase()
            optionsImmortal.value = stringOptionsImmortal.filter(v => v.toLowerCase().indexOf(needle) > -1)
          })
        },
        filterSource(val, update, abort) {
          update(() => {
            const needle = val.toLowerCase()
            optionsSource.value = stringOptionsSource.filter(v => v.toLowerCase().indexOf(needle) > -1)
          })
        }

      }
    },
    watch: {
    OptionSelections(newValue) {
      this.saveOptions(newValue);

    },
      comment(newValue) {
    this.saveComment(newValue)
  },

  },
    components: {},
    methods: {

      saveOptions(selections) {
        const selections1=selections.toString()
        // const type_id1=this.id_row
        const type_id1=this.id_row
        // console.log(type_id1)
        API("auth.updateImmunofluorescent_antibody_one", { emission_frequency: selections1,type_id:type_id1});
      },

       saveComment(value) {
      const type_id1=this.id_row
      // console.log("Saving comment:", value, type_id1)
      API("auth.updateImmunofluorescent_antibody_comment_one", {
        comment: value,type_id:type_id1
      })
    },

      async addRow() {

        const id11= this.editedItem.uuid

        const type1 = this.type_biosp
        // const type_id1 = this.editedItem.type_id
        const type_id1=this.id_row

        // const immortal1 = this.editedItem.immortal
        // const immortal1 = this.editedItem.immortal.toString()
        // const location1 = this.editedItem.location
        const emission_frequency1 = this.editedItem.emission_frequency

        // const passage1 = this.editedItem.passage.toString()
        // const transfected1 = this.editedItem.transfected
        // const unit1 = this.unit.toString()

        // const subtype1 = this.editedItem.subtype.toString()
        // // const lot_no1 = this.editedItem.lot_no
        // const description1 = this.editedItem.description
        // const mouse_id1 = this.editedItem.mouse_id
        // const tumor_id1 = this.editedItem.tumor_id
        // const hyperlink1 = this.editedItem.hyperlink
        // const assignedCamra1 = this.editedItem.assignedCamra.toString()
        // const assignedRoute1 = this.editedItem.assignedRoute.toString()

        // console.log( role1.constructor.name+"mmmmmmm")


        const editedIndex1 = this.editedIndex
        const oldRow = this.data[editedIndex1]
        const updatedRow = this.editedItem

        if (this.editedIndex > -1) {
          Object.assign(oldRow, updatedRow) && API("auth.updateImmunofluorescent_antibody", { id1: id11,type: type1,type_id:type_id1,emission_frequency:emission_frequency1});
        } else {
          if ( emission_frequency1 ) {

            this.data.push(this.editedItem) && API("auth.create_obj_antibdy", { type: type1,type_id:type_id1,emission_frequency:emission_frequency1});
          }
          else {
            this.$q.notify({
              message: 'please Enter all Details.',
              color: 'red',
              icon: 'announcement',
            })
          }
        }
        this.close()




      },

      async deleteItem(item) {
        const id = item.uuid
        console.log(id + "oooo")
        const index = this.data.indexOf(item);
        confirm("Are you sure you want to Delete this user?") &&
        this.data.splice(index, 1) && await API('auth.deleteImmunofluorescent_antibody', { id });
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
    formattedTransfected() {
      // Format the 'props.row.transfected' as needed
      // For example, to display a comma-separated string: "1, 8, 7, 3"
      return this.props.row.transfected.join(', ');
    },
  },

    mounted() {
    // API("auth.createArirports", { name:"DeliAir", latLong:"-873.45",noOfRunWay:"3",typesOfAircraft:"full",runWayConstType:"simple",AtcFacility:"fine",refuling:"ok" });
      // console.log(key)
      key=this.id_row
      // console.log(key)
      API('auth.Immunofluorescent_antibody_detials_id',{key}).then(res => {
        this.data = res
        const estring=res[0].emission_frequency
        const c=res[0].comment
        this.comment =c;
        // console.log(res,"dsfsdf" )
        const emissionArray = estring.split(',');
        // console.log(emissionArray);
        this.OptionSelections=emissionArray

      })

      // API('auth.findonlyRoute').then(res => {
      //   this.res=res
      //   // console.log(this.res)
      // })

      // API('auth.findLocID').then(res => {
      //   const objectArray = Object.entries(res);
      //   objectArray.forEach(([key, value]) => {
      //     this.listLocation.push(value)
      //   });
      // })

      // API('auth.findrouteNameID').then(res => {
      //   const objectArray = Object.entries(res);
      //   objectArray.forEach(([key, value]) => {
      //     this.listRoute.push(value.name)

      //   });
      // })



    },



  }
  </script>

  <style lang="sass" >
  .q-table--dense
    .q-table
      th
        font-size: 15px
      td
        font-size: 15px
  .q-input
    .label
        font-size: 15px



  </style>

