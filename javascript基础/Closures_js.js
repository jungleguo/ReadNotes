// 闭包
function makeAdder(a) {
    return function (b) {
        return a + b;
    };
}

var x = makeAdder(5);
var y = makeAdder(20);

console.log('x is',x(5));

console.log('y is', y(4));
