var target = {};
var handler = {
    get: function (receiver, name) {
        return `Hello, ${name}`;
    }
}

var p = new Proxy(target, handler);
console.log(`P.World is ${p.World}`);

var target_1 = function () { return "I'm the target"; };

var handler_1 = {
    apply: function (receiver, ...args) {
        return "I'm the proxy";
    }
};

var o = new Proxy(target_1, handler_1);
console.log(`o() is ${o()}`);