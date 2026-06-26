<!-- <template>
  <q-img
    :src="thumbnail || src"
    spinner-color="white"
    style="height: 140px; width: 140px; border: 1px solid #ccc;"
    :alt="alt"
  />
</template>

<script>
export default {
  name: 'ThumbnailImage',
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      thumbnail: null
    };
  },
  mounted() {
    this.generateThumbnail(this.src);
  },
  methods: {
    generateThumbnail(url) {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.src = url;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 80;
        canvas.height = 80;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        this.thumbnail = canvas.toDataURL('image/jpeg', 0.02);
      };
    }
  }
};
</script>

<style scoped>
</style> -->
    <!-- :src="thumbnail || src" -->

<template>
  <q-img
    :src="src"
    :alt="alt"
    spinner-color="white"
    class="thumb"
    :style="boxStyle"
    fit="cover"
    @error="onImgError"
  />
</template>

<script>
export default {
  name: 'ThumbnailImage',
  props: {
    src: { type: String, required: true },
    alt: { type: String, default: '' },
    /* size=0 -> responsive; else fixed px box */
    size: { type: Number, default: 140 },
    quality: { type: Number, default: 0.8 }
  },
  data: () => ({ thumbnail: null }),
  computed: {
    boxStyle () {
      if (this.size > 0) {
        // fixed box (legacy behavior)
        return `width:${this.size}px; height:${this.size}px; border:1px solid #ccc;`
      }
      // responsive square that grows with column width
      return `width:100%; aspect-ratio:1/1; border:1px solid #ccc;`
    }
  },
  mounted () { this.buildThumb(this.src) },
  watch: { src (v) { this.thumbnail = null; this.buildThumb(v) } },
  methods: {
    onImgError () { /* optional: set placeholder */ },
    async buildThumb (url) {
      try {
        const img = new Image()
        img.crossOrigin = 'anonymous'
        img.decoding = 'async'
        img.src = url
        await img.decode().catch(() => new Promise(r => (img.onload = r)))

        // compute render size in CSS pixels
        const box = document.createElement('div')
        box.style.cssText = 'position:absolute; visibility:hidden; width:200px; aspect-ratio:1/1;'
        document.body.appendChild(box)
        const cssW = this.size > 0 ? this.size : box.clientWidth
        document.body.removeChild(box)

        const dpr = Math.min(window.devicePixelRatio || 1, 2)
        const w = Math.max(1, Math.round(cssW * dpr))
        const h = w

        const canvas = document.createElement('canvas')
        canvas.width = w
        canvas.height = h
        const ctx = canvas.getContext('2d')
        ctx.imageSmoothingEnabled = true
        ctx.imageSmoothingQuality = 'high'
        ctx.drawImage(img, 0, 0, w, h)
        this.thumbnail = canvas.toDataURL('image/jpeg', this.quality)
      } catch (e) {
        // fall back to original src
        this.thumbnail = null
        console.warn('Thumb build failed:', e)
      }
    }
  }
}
</script>

<style scoped>
.thumb { display:block; }
</style>
