export default {
  events: {},
  on(name, cb) {
    if (!this.events[name]) {
      this.events[name] = cb;
    }
  },
  emit(name, value) {
    if(this.events[name]) {
      this.events[name](value);
    }
  }
}