<template>
<!-- {{passEx_type}}
{{pro_phase_info}} -->


<!-- {{pro_random_id}} -->
      <div class="q-mb-lg ">
      <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section>
      </div>

      <!-- 2d model visulize -->
      <div style="width: 100%;" class="q-mt-lg" v-if="passEx_type === '2D Experiment' && (pro_magnification==='10x' || pro_magnification==='4x') && (pro_counterstain === 'DAPI' || pro_counterstain === 'Hoechst')">
        <!-- <div style="width: 100%;" class="q-mt-lg" v-if="passEx_type === '2D Experiment'"> -->

        <!-- <twoDmodel_list :experiment_id="passUuid" :passEx_type="passEx_type" ></twoDmodel_list> -->
      </div>
      <!-- 2d model visulize END -->

    <q-uploader
    class="full-width"
      ref="uploader"
      color="amber"
      text-color="black"
      :label="uploaderLabel"
      @added="onFilesAdded"
      @removed="syncFiles"
      no-thumbnails
      multiple
      hide-upload-btn

    >

    <template v-slot:list="scope">

        <q-list separator>

          <q-item v-for="file in scope.files" :key="file.__key">
            <q-item-section>
              <q-item-label class="full-width ellipsis">
                {{ file.name }}
              </q-item-label>
<!--
              <q-item-label caption>
                Status: {{ file.__status }}
              </q-item-label> -->

              <q-item-label caption>
                <!-- {{ file.__sizeLabel }} / {{ file.__progressLabel }} -->
                {{ file.__sizeLabel }}
              </q-item-label>
            </q-item-section>

            <q-item-section
              v-if="file.__img"
              thumbnail
              class="gt-xs"
            >
              <img :src="file.__img.src">
            </q-item-section>

            <q-item-section top side >
              <q-btn
                class="gt-xs"
                size="12px"
                flat
                dense
                round
                icon="delete"
                @click="scope.removeFile(file)"
              />
            </q-item-section>
          </q-item>

        </q-list>



      </template>


  </q-uploader>
    <div class="row text-center" >
      <q-btn class="q-mt-lg "   :color="uploadBtnColor"  label="Upload Well" @click="uploadFiles" :disable="uploadDisabled || uploading" />
      <q-spinner v-if="uploading" color="primary" size="50px" />

    </div>
    <div class="row justify-center" v-if="uploadMessage">{{ uploadMessage }}</div>



<q-space />




</template>




<script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'
  import uploadbtn from 'src/components/user/uploadbtn';
  // import twoDmodel_list from 'src/components/user/2dmodel_list';


export default {
  components: {},

  // comming form uploadImgActivity.vue
  props: {
    passUuid:String,
    passStudy_id:String,
    passEx_type:String,
    pro_phase_info:String,
    pro_counterstain:String,
    pro_magnification:String,
    pro_random_id:String
    },
  data() {

    return {

      selectedFiles: [],
      uploading: false,
      uploadDisabled: true,
      uploadMessage: "", // Added a new data property to hold the upload message
      fileUrls: [],
      processingdone:false,
    };
  },
  mounted(){

  },
  computed:{
    uploadBtnColor() {
      return this.selectedFiles.length > 0 ? 'green' : 'red';
    },
     uploaderLabel() {
  if (!this.selectedFiles.length) return 'Select files to upload';

  const totalSize = this.selectedFiles.reduce((sum, f) => sum + f.size, 0);

  let sizeLabel;
  if (totalSize < 1024) {
    sizeLabel = `${totalSize} B`;
  } else if (totalSize < 1024 * 1024) {
    sizeLabel = `${(totalSize / 1024).toFixed(2)} KB`;
  } else if (totalSize < 1024 * 1024 * 1024) {
    sizeLabel = `${(totalSize / (1024 * 1024)).toFixed(2)} MB`;
  } else {
    sizeLabel = `${(totalSize / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  return `${this.selectedFiles.length} file(s), ${sizeLabel} total`;
}

  },
  methods: {

     call_serverfunction_processf(){


          API('home.processFiles').then(res => {
          console.log(res,"server funcation call");


        })
    },

    addFiles() {
  try {
    const a = this.fileUrls;

    a.forEach((experiment) => {
      const {
        url,
        mimetype,
        size,
        headers,

      } = experiment;

      const file_meta = JSON.stringify(headers);

      // Make the API call with the extracted values
      API("auth.createFile", {
        study_id:this.passStudy_id,
        experiment_id:this.passUuid,
        ex_type:this.passEx_type,
        phase_info: this.pro_phase_info,
        counterstain: this.pro_counterstain,
        file_addr:url,
        file_type:mimetype,
        file_size:size.toString(),
        file_meta,
        random_id:this.pro_random_id
      });
    });
    // console.log(this.pro_random_id,"chcek")
    // If the loop completes without errors, show the notification
    this.$q.notify({
      message: 'Files Uploaded',
      color: 'green', // You can change the color to indicate success
      icon: 'announcement',
    });
    // Call server function to process
    this.call_serverfunction_processf();

  } catch (error) {
    // If an error occurs, you can handle it here
    console.error('Error in addcheck:', error);

    this.$q.notify({
      message: 'Error occurred while saving Files',
      color: 'red',
      icon: 'announcement',
    });
  }
},
syncFiles() {
  this.selectedFiles = this.$refs.uploader.files;
  this.uploadDisabled = this.selectedFiles.length === 0;
}
,
    onFilesAdded(files) {
      this.selectedFiles = [...this.selectedFiles, ...files];
      this.uploadDisabled = files.length === 0;
    },
    uploadFiles() {
  if (!this.selectedFiles.length) return;

  this.uploading = true;
  const formData = new FormData();

  for (let i = 0; i < this.selectedFiles.length; i++) {
    formData.append('files', this.selectedFiles[i]);
  }
 // Dynamically detect the upload URL
 const UPLOAD_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:7070/upload'  // Localhost for development
    : `http://${window.location.hostname}:7070/upload`;  // Dynamic IP in production

  fetch(UPLOAD_URL, {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to upload files.');
      }
      return response.json();
    })
    .then((data) => {
      // console.log(data.message);

      // Store the file URLs in the data property
      // this.fileUrls = data.files.map((file) => file.url);
      this.fileUrls = data.files;
      this.uploadMessage = "Upload Next: All will be process on server!";
      this.uploading = false;
      this.addFiles();

      setTimeout(() => {
        this.$emit('close-dialog');
      }, 1000);


    })
    .catch((error) => {
      console.error('Error uploading files:', error);
      this.uploadMessage = "Error uploading files. Please try again.";
      this.uploading = false;
    });
},

  },
};
</script>

<style>
.q-uploader__subtitle {
  display: none !important;
}
</style>
