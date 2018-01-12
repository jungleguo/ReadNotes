function Person(first, last) {
    this.first = first;
    this.last = last;
}
Person.prototype.fullName = function () {
    return this.first + ' ' + this.last;
};
Person.prototype.fullNameReversed = function () {
    return this.last + ', ' + this.first;
};


function trivialNew(constructor, ...args) {
    var o = {};
    constructor.apply(o, args);
    return o;
}

