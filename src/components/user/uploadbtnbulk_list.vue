<template>
  <div class="q-mb-lg ">
    <q-card-section class="row">
      <q-space />
      <q-btn icon="close" round dense v-close-popup />
    </q-card-section>
  </div>



  <q-uploader
    class="full-width"
    ref="uploader"
    color="cyan"
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
            <q-item-label class="full-width ellipsis">{{ file.name }}</q-item-label>
            <q-item-label caption>{{ file.__sizeLabel }}</q-item-label>
          </q-item-section>
          <q-item-section v-if="file.__img" thumbnail class="gt-xs">
            <img :src="file.__img.src" />
          </q-item-section>
          <q-item-section top side>
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

  <div class="row text-center">
    <q-btn
      class="q-mt-lg"
      :color="uploadBtnColor"
      label="Upload Plate"
      @click="uploadFiles"
      :disable="uploadDisabled || uploading"
    />
    <q-spinner v-if="uploading" color="primary" size="50px" />
  </div>

  <div class="row justify-center" v-if="uploadMessage">{{ uploadMessage }}</div>
  <q-space />
   <!-- <div class="q-gutter-sm q-mt-xl">
      <q-radio v-model="shape" checked-icon="task_alt" unchecked-icon="panorama_fish_eye" val="Global" label="Global" />
      <q-radio v-model="shape" checked-icon="task_alt" unchecked-icon="panorama_fish_eye" val="Local" label="Local (as per Control)" />

  </div> -->
</template>

<script>
import API from 'src/api';
import { useQuasar,QSpinnerGears } from 'quasar'
import { ref, computed, onMounted, onUnmounted, onActivated, onDeactivated, emit  } from 'vue';

export default {


  props: {
    passUuid: String,
  },
  data() {
    return {
      selectedFiles: [],
      uploading: false,
      uploadDisabled: true,
      uploadMessage: '',
      fileUrls: [],
      shape: ref('Global'),

    };

  },
//  mounted() {
//   this.$nextTick(() => {
//     const inputEl = this.$refs.uploader?.$el?.querySelector('input[type="file"]');
//     if (inputEl) {
//       inputEl.setAttribute('webkitdirectory', true);
//       inputEl.setAttribute('directory', true);
//     }
//   });
// },

  computed: {
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
    syncFiles() {
  this.selectedFiles = this.$refs.uploader.files;
  this.uploadDisabled = this.selectedFiles.length === 0;
}
,
    // onFilesAdded(files) {
    //   this.selectedFiles = [...this.selectedFiles, ...files];
    //   this.uploadDisabled = files.length === 0;
    // },

    onFilesAdded(files) {
  const allowedExtensions = ['.czi'];

  const validFiles = files.filter(file =>
    allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  );

  const rejectedFiles = files.length - validFiles.length;

  this.selectedFiles = [...this.selectedFiles, ...validFiles];
  this.uploadDisabled = this.selectedFiles.length === 0;

  if (rejectedFiles > 0) {

    this.$q.notify({
          message: `${rejectedFiles} unsupported file(s) rejected. Only czi are allowed.`,
          color: 'danger',
          multiLine: true,
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          actions: [
            { label: 'Cancel', color: 'yellow', handler: () => { /* ... */ } }
          ],
          timeout: Math.random() * 25000 + 3000
        })
  }
}
,

    async uploadFiles() {
      if (!this.selectedFiles.length) return;
      this.uploading = true;
      const BATCH_SIZE = 10;
      const totalFiles = this.selectedFiles.length;
      const totalBatches = Math.ceil(totalFiles / BATCH_SIZE);
      for (let i = 0; i < totalFiles; i += BATCH_SIZE) {
        const batch = this.selectedFiles.slice(i, i + BATCH_SIZE);
        const formData = new FormData();
        batch.forEach(file => formData.append('files', file));

        const UPLOAD_URL = window.location.hostname === 'localhost'
          ? 'http://localhost:7070/upload'
          : `http://${window.location.hostname}:7070/upload`;

        try {
          const response = await fetch(UPLOAD_URL, {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) throw new Error('Upload failed');

          const data = await response.json();
          this.fileUrls.push(...data.files);

          // Save each uploaded file into DB
          for (const file of data.files) {
            const file_meta = JSON.stringify(file.headers);
            await API("auth.createFilebulk", {
              experiment_id: this.passUuid,
              file_addr: file.url,
              file_type: file.mimetype,
              file_size: file.size.toString(),
              file_meta,
            });
          }

          this.uploadMessage = `✅ Uploaded batch ${Math.floor(i / BATCH_SIZE) + 1} of ${totalBatches}`;


        } catch (err) {
          console.error('❌ Batch upload error:', err);
          this.uploadMessage = "❌ Upload failed. Please try again.";
          this.uploading = false;
          return;
        }
      }

      this.uploading = false;
      this.uploadMessage = "✅ All files uploaded.";

      // Notify backend to begin processing
      API('home.processFilesbulk', { randomid: this.passUuid }).then(res => {
        console.log("Server processing started:", res);

        this.$q.notify({
          message: res,
          spinner: QSpinnerGears,
          color: 'danger',
          multiLine: true,
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          actions: [
            { label: 'Cancel', color: 'yellow', handler: () => { /* ... */ } }
          ],
          timeout: Math.random() * 45000 + 3000
        })

      });

      setTimeout(() => {
        this.$emit('close-dialog');
      }, 1000);
    },
  },
};
</script>

<style>
.q-uploader__subtitle {
  display: none !important;
}

</style>
