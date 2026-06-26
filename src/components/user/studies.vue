  <template>
      <!--
        Forked from:
        https://quasar.dev/vue-components/table#Example--Popup-editing
      -->
      <div>
        <div class="q-pa-sm q-gutter-sm" v-if="tableShow">
          <div class="text-center text-black text-h6">List of Studies</div>
          <div class="text-center">
          <q-btn
            color="black"
            label="Add New Study"
            icon-right="note_add"
            @click="show_dialog = true"
            dense
          ></q-btn>
        </div>

          <q-table
            title="Treats"
            :rows="data"
            :columns="columns"
            :dense="$q.screen.lt.md"
            row-key="uuid"
            max-width="100%"
            binary-state-sort
            table-header-style="background-color: #C0C0C0"
            bg-blue-5
            style="background-color: #F5F5F5"
            class="q-table--dense compact-table"
            :pagination="pagination"
          >
            <template v-slot:top>
              <div class="q-pa-sm q-gutter-sm"></div>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <!-- <q-td key="desc" :props="props"  @click="  show_dialog_attributes = true; getid(props.row);" > -->
                  <q-td  style="cursor: pointer;" key="desc" :props="props"  @click="show_dialog_attributes = true;  getid(props.row);" >
                    <!-- {{ props.row.name }} -->

                  <q-badge  class=" text-white text-caption ">
                    {{ props.row.name }}
                  </q-badge>
                </q-td>
                <!-- <q-td key="first" :props="props">
                  <q-badge color="grey-6" class="text-white text-caption" >

                    {{ props.row.name }}
                  </q-badge>
                </q-td> -->


                <!-- <q-td key="second" :props="props">
                  <q-badge color="grey-6" class="text-white text-caption" >

                    {{ props.row.type_id }}
                  </q-badge>
                </q-td> -->
    <!--
                <q-td key="third" :props="props">
                  <q-badge color="grey-6" class="text-white text-caption" >

                    {{ props.row.subtype }}
                  </q-badge>
                </q-td> -->

                <q-td key="actions" :props="props">
                  <q-btn
                    color="black"
                    label="Experiments"
                    icon-right="add"
                    @click="
                      tableShow=false;
                      show_dialog_attributes_newExp = true;
                      getid(props.row);
                    "
                    v-model="props.row.uuid"
                    size="11px"
                    class="q-mr-sm"
                    dense
                  ></q-btn>


                  <q-btn
                    color="red"
                    label="Delete"
                    icon-right="delete"
                    @click="deleteItem(props.row)"
                    size="11px"
                    class="q-mr-sm"
                    dense
                  ></q-btn>
                  <q-btn dense color="green" label="Edit" @click="editItem(props.row)" size="11px" class="q-mr-sm"></q-btn>

                </q-td>
              </q-tr>
            </template>
          </q-table>

        </div>


        <q-dialog v-model="show_dialog">
          <q-card style="width: 500px; max-width: 500px; background-color: #F5F5F5">
            <q-card-section>
              <div class="text-h6 text-center bg-grey-5">Add Study</div>
            </q-card-section>

            <!-- add Camra Details Start -->
            <q-card-section align="center">
              <div class="row text-center">
                <q-input v-model="editedItem.uuid" label="Id:" hidden />
                <!-- <q-input outlined  v-model="editedItem.type"  stack-label placeholder="Type"
                            :rules="[val => val && val.length > 0 || 'Please type something']" autofocus/><q-space /> -->
                <q-input
                class="fit"
                  outlined
                  v-model="editedItem.name"
                  label="Please Enter Study Name"
                  stack-label
                  :rules="[
                    (val) => (val && val.length > 0) || 'Please type something',
                  ]"
                  dense
                />
                <q-input
                class="fit"
                type="textarea"
                  outlined
                  v-model="editedItem.description"
                  label="Please Enter Description"
                  stack-label
                  :rules="[
                    (val) => (val && val.length > 0) || 'Please type something',
                  ]"
                  dense
                />

                <!-- <q-input
                class="fit"
                type="textarea"
                  outlined
                  v-model="editedItem.notes"
                  label="Please Enter Note"

                  stack-label
                  :rules="[
                    (val) => (val && val.length > 0) || 'Please type Notes',
                  ]"
                  dense
                /> -->

                <q-space />
              </div>
            </q-card-section>
            <!-- add Camra Details END -->

            <q-card-actions align="center">
              <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
              <div class="text-center q-mr-lg">
                <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>
              </div>
              <div class="text-center">
                <q-btn
                  dense
                  color="black"
                  v-close-popup
                  label="OK"
                  @click="addRow()"

                ></q-btn>
              </div>
            </q-card-actions>
          </q-card>
        </q-dialog>

        <q-dialog v-model="show_dialog_attributes" >

          <q-card style="width: 2000px; max-width: 2000px">

            <!-- close button -->
            <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section>
        <!-- close button end -->
            <q-card-section>
            <!-- <div class="text-center text-h5">Visulize Factors and Delete</div> -->
              <div >
                <studies_expList
                  :id_row="idParamenterRow" :study_name="typeBio"
                  class="fit"
                ></studies_expList>
              </div>
            </q-card-section>
          </q-card>

        </q-dialog>
        <div v-if="show_dialog_attributes_newExp" >
          <q-card class="fit">

            <!-- add Camra Details Start -->
            <q-card-section align="center" >
              <div class="row text-center">
                <!-- Define attributes table -->
                <studies_newExp
                  :id_row="idParamenterRow" :study_name="typeBio"
                  class="fit"
                ></studies_newExp>
                <!-- attributes table END -->
              </div>
            </q-card-section>
            <!-- add Camra Details END -->


          </q-card>
        </div>
        <div>
          <q-dialog v-model="warning">
            <q-card>
              <q-card-section class="row items-center q-pb-none">
                <div class="text-h6">Warning</div>
                <q-space />
                <q-btn icon="close" flat round dense v-close-popup />
              </q-card-section>

              <q-card-section>
                Study Already Exist
              </q-card-section>
            </q-card>
          </q-dialog>
        </div>

      </div>
    </template>

    <script>
    import API from "src/api";
    import { ref } from "vue";
    import { exportFile, useQuasar } from "quasar";

    import studies_expList from "src/components/user/studies_expList";
    // import studies_expList_2 from "src/components/user/studies_expList_2";
    import studies_newExp from "src/components/user/studies_newExp";

    const columns = [
      {
        name: "desc",
        required: true,
        label: "Study Name",
        align: "center",
        field: (row) => row.name,
        format: (val) => `${val}`,
        sortable: true,
      },

      // { name: 'first', align: 'center', label: 'name', field: 'name', sortable: true },

      { name: "actions", align: "center", label: "Actions", field: "actions" },
    ];

    var listLocation = [];
    var listRoute = [];

    const stringOptionsCam = listLocation;
    const stringOptionsRoute = listRoute;
    const stringOptionsRole = ["admin", "officer"];

    export default {
      setup() {
        const $q = useQuasar();
        const optionsCam = ref(stringOptionsCam);
        const optionsRoute = ref(stringOptionsRoute);
        const optionsRole = ref(stringOptionsRole);

        return {
          pagination: {
            rowsPerPage: 20 // current rows per page being displayed
          },
          listLocation,
          listRoute,
          warning:false,
          warning_check:false,
          idParamenterRow: null,
          typeBio:null,
          tableShow:ref(true),
          columns,
          show_dialog: ref(false),
          show_dialog_attributes: ref(false),
          show_dialog_attributes_newExp:ref(false),
          editedIndex: -1,
          userD: ref(false),
          editedItem: ref({
            uuid: ref(null),
            name: ref(null),
            description:ref(null),
            notes:ref(null),
          }),
          defaultItem: ref({
            uuid: ref(null),
            name: ref(null),
            description:ref(null),
            notes:ref(null),
          }),

          optionsCam,
          optionsRoute,
          optionsRole,

          filterRole(val, update, abort) {
            update(() => {
              const needle = val.toLowerCase();
              optionsRole.value = stringOptionsRole.filter(
                (v) => v.toLowerCase().indexOf(needle) > -1
              );
            });
          },
        };
      },
      components: { studies_expList,studies_newExp },
      methods: {
        refreshPage() {

    window.location.reload()

    },
        async addRow() {
          const id1 = this.editedItem.uuid;
          const name1 = this.editedItem.name;
          const description1 = this.editedItem.description;
          const notes1 = this.editedItem.notes;

          const editedIndex1 = this.editedIndex;
          const oldRow = this.data[editedIndex1];
          const updatedRow = this.editedItem;

          if (this.editedIndex > -1) {
            Object.assign(oldRow, updatedRow) ;
            // this.data[editedIndex1] = updatedRow;
              API("auth.update_study", { id1: id1, name: name1,description:description1});
          } else {
            if (name1 ) {
              // console.log("Added row:", this.editedItem); // Debugging line: Check the added row data
              var response=await API("auth.create_obj_study", { name: name1, description:description1, notes: localStorage.getItem("username") });
              if(response!="exist"){this.data.push(this.editedItem);this.refreshPage();}
              else{
                this.warning_check=true;
                    this.$q.notify({
                    message: 'Already Exist.',
                    color: 'red',
                    icon: 'announcement',
                  })
              }
            } else {
              this.$q.notify({
                message: "please Enter all Details.",
                color: "red",
                icon: "announcement",
              });
            }
          }
          this.close();
        },

        getid(item) {
          const id = item.uuid;
          const t = item.name;
          this.idParamenterRow = id;
          this.typeBio=t;
          // console.log(this.typeBio + "oooo")
        },
        // async deleteItem(item) {
        //   const id = item.uuid;
        //   // console.log(id + "oooo")
        //   const index = this.data.indexOf(item);
        //   confirm("Are you sure you want to Delete this user?") &&
        //     this.data.splice(index, 1) &&
        //     (await API("auth.deleteStudy", { id }));
        // },
        async deleteItem(item) {
          const id = item.uuid;
          const index = this.data.indexOf(item);

          const userInput = prompt("Type 'DELETE' to confirm deletion:");

          if (userInput === "DELETE") {
            this.data.splice(index, 1);
            await API("auth.deleteStudy", { id });
          } else {
            alert("Deletion canceled. Please type 'DELETE' to confirm.");
          }
        }
        ,
        async editItem(item) {
          this.editedIndex = this.data.indexOf(item);
          this.editedItem = Object.assign({}, item);
          this.show_dialog = true;
        },
        async close() {
          this.show_dialog = false;
          setTimeout(() => {
            this.editedItem = Object.assign({}, this.defaultItem);
            this.editedIndex = -1;
          }, 300);
        },
      },

      data: () => ({
        data: [],
      }),

      mounted() {

        // API("auth.study_details" ).then((res) => {
        API("auth.study_details").then((res) => {
          this.data = res;
          // console.log(this.data.type+"dsfsdf" )
        });
      },
    };
    </script>

    <style>
    .compact-table td {
      padding: 0px 0px !important; /* Reduces cell padding */
    }

    </style>
