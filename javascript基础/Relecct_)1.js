var o = { a: 1 };
Object.defineProperty(o, 'b', { value: 2 });
o[Symbol('c')] = 3;

console.log('o has keys:', Reflect.ownKeys(o));

function C(a, b){
    this.c = a + b;
}

var instacnce = Reflect.construct(C, [20, 22]);
console.log('The value of c is:', instacnce.c);