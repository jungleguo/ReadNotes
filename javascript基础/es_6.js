function Person(name) {
    this.name = name;
}

Person.prototype.getName = function () {
    return this.name;
}

function Builder(name, title) {
    Person.call(this, name);
    this.title = title;
}

Builder.prototype = Object.create(Person.prototype);
Builder.prototype.constructor = Builder;

var bob = new Builder('Bob', 'M');
var Ana = new Person('Ana');
console.log('bob hasOwnProperty', bob.hasOwnProperty('getName'));
console.log('Ana hasOwnProperty', Ana.hasOwnProperty('getName'));
console.log('Ana.__proto__ hasOwnPropeerty', Ana.__proto__.hasOwnProperty('getName'));// Ttrue
console.log('bob.__proto__ hasOwnProperty', bob.__proto__.hasOwnProperty('getName'));//false


function People(name) {
    this.name = name;

    this.getName = () => {
        return name;
    }
}

function Teacher(name) {
    People.call(this, name);
}

Teacher.prototype = Object.create(People.prototype)
Teacher.prototype.constructor = Teacher;

var lv = new Teacher('mada');

console.log('lv hasOwnProperty', lv.hasOwnProperty('getName'));

