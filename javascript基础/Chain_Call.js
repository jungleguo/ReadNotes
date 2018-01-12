//使用Objectt.Create方法创建一个拥有arguments List的array-like的对象
Function.prototype.construct = function (args) {
    var oNew = Object.create(this.prototype);
    this.apply(oNew, args);
    return oNew;
}

//使用Object._proto_
Function.prototype.construct = function (args) {
    var oNew = {};
    oNew._proto_ = this.prototype;
    this.apply(oNew, args);
    return oNew;
}

//使用闭包
Function.prototype.construct = function (args) {
    var fConstructor = this, fNew
}