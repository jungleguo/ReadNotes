function makePerson(first, last) {
    return {
        first: first,
        last: last,
        fullName: function () {
            return this.first + '' + this.last;
        },
        fullNameReversed: function () {
            return this.last + ',' + this.first;
        }
    };
}

s = makePerson('Simon', 'Willsion');
s.fullName();
s.fullNameReversed();

var fullName = s.fullName;
console.log(fullName());