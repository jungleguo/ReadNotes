class SkinnedMesh extends THREE.Mesh {
    constructor(geometry, materials) {
      super(geometry, materials);
  
      this.idMatrix = SkinnedMesh.defaultMatrix();
      this.bones = [];
      this.boneMatrices = [];
      //...
    }
    update(camera) {
      //...
      super.update();
    }
    static defaultMatrix() {
      return new THREE.Matrix4();
    }
  }