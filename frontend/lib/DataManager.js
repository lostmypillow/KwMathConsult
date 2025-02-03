export default class DataManager {
    constructor(initialLength = 6) {
      this.data = Array.from({ length: initialLength }, (_, i) => ({
       device: i + 1,
        teacher: "",
        school: "",
        image: "",
      }));
    }
  
    getData() {
    
      return this.data;
    }
  
    updateObj(id, newAttr) {
      this.data = this.data.map((item) =>
        item.device === id ? { ...newAttr } : item
      );
      console.log(this.data)
    }
  }
  