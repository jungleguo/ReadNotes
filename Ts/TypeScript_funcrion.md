## this和箭头函数
在JavaScript里面，this的值在函数被调用的时候才会指定它。

看一个例子

```
    let deck = {
        suits: ["hearts", "spades", "clubs", "diamonds"],
        cards: Array(52),
        createCardPicker: function() {
            return function() {
                let pickedCard = Math.floor(Math.random() * 52);
                let pickedSuit = Math.floor(pickedCard / 13);

                return {suit: this.suits[pickedSuit], card: pickedCard % 13};
            }
        }
    }

    let cardPicker = deck.createCardPicker();
    let pickedCard = cardPicker();

    alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

不难看出CreateCardpicker是个函数，并且其返回值也是一个函数。当我们运行程序，并没有弹窗而是报错。
在CreateCardPicker返回的函数里的this被设置成了window而不是Deck对象。
我们只是独立的调用了cardPicker().顶层的非方法式调用会将this视作window,在严格模式下,this为undefined.

__解决问题__
我们可以在函数被返回时就绑好正确的this。这里我们可以使用ES6箭头语法。箭头函数能够保存函数创建时的this值，而不是调用时的值。
看看下面的代码。

```
    let deck = {
        suits: ["hearts", "spades", "clubs", "diamonds"],
        cards: Array(52),
        createCardPicker: function() {
            // NOTE: the line below is now an arrow function, allowing us to capture 'this' right here
            return () => {
                let pickedCard = Math.floor(Math.random() * 52);
                let pickedSuit = Math.floor(pickedCard / 13);

                return {suit: this.suits[pickedSuit], card: pickedCard % 13};
            }
        }
    }
    let cardPicker = deck.createCardPicker();
    let pickedCard = cardPicker();

    alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

## this 参数
在上面的例子中，this.suits[pickedSuit]的类型依旧为any.因为this来自对象字面量里的函数表达式。修改的方方法是，提供一个显示的this参数。
this参数是个假参数。
```
    let deck = {
        suits: ["hearts", "spades", "clubs", "diamonds"],
        cards: Array(52),
        createCardPicker: function(this:void) {
            // NOTE: the line below is now an arrow function, allowing us to capture 'this' right here
            return () => {
                let pickedCard = Math.floor(Math.random() * 52);
                let pickedSuit = Math.floor(pickedCard / 13);

                return {suit: this.suits[pickedSuit], card: pickedCard % 13};
            }
        }
    }
```
添加一些接口

```
    interface Card {
        suit: string;
        card: number;
    }
    interface Deck {
        suits: string[];
        cards: number[];
        createCardPicker(this: Deck): () => Card;
    }
    let deck: Deck = {
        suits: ["hearts", "spades", "clubs", "diamonds"],
        cards: Array(52),
        // NOTE: The function now explicitly specifies that its callee must be of type Deck
        createCardPicker: function(this: Deck) {
            return () => {
                let pickedCard = Math.floor(Math.random() * 52);
                let pickedSuit = Math.floor(pickedCard / 13);

                return {suit: this.suits[pickedSuit], card: pickedCard % 13};
            }
        }
    }

    let cardPicker = deck.createCardPicker();
    let pickedCard = cardPicker();

    alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```
现在this是Deck类型的，而不再是any了。

## this参数在回调函数里
当一个回调函数被调用的时候，它们会被当作一个普通函数调用，this将会为undefined,为了避免这个错误，我们首先要指定this的类型。
```
    interface UIElement{
        addClickListstener(onclick:({this:void,e:Event}) =>void):void;
    }
```