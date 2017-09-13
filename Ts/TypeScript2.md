# TypeScript学习

## 接口

例子
```
    function printLabel(labelledObj:{label:string}){
        console.log(labelledObj.label);
    }

    let myObj = {size:10,label:"Size 10 object"};
    printLabel(myObj);
```
类型查看器会查看printLabel的调用。printLabel有一个参数，并要求这个对象参数有一个名为label类型为string的属性。虽然我们传入的参数可能会包含很多属性，
但是编译器只会检查必须的属性是否存在，并且其类型是否匹配。

让我们使用接口来重构上面的例子
```
    interface Label{
        label:string;
    }
    function printLabel(labelledObj:Label){
        console.log(labelledObj.label);
    }
    let myObj = {size:10,label:"Size 10 object"};
    printLabel(myObj);
```
这里的接口不同于一般静态语言中的接口，这里的接口是用于规定参数的形态，并不是要求它要实现接口中的所有方法。
只要我们传入的参数满足接口中对参数的定义即可。传入的参数中只要包含接口中参数的属性并且类型相同，至于顺序我们也是不去关心的。

### 可选属性
接口里的属性不全都是必需的。可选属性应用在"option bags"模式中，即给函数传入的参数对象中只有部分属性赋值
```
    interface SquareConfig{
        color?:string;
        width?:number;
    }

    function createSquare(config: SquareConfig):{color:string;area:number}{
        let newSquare = {color:"white", area: 100};
        if(config.color){
            newSquare.color = config.color;
        }
        if(config.width){
            newSquare.area = config.width * config.width;
        }
        return newSquare;
    }
    let mySquare = createSquare({color:"black"});
```
可选属性的接口与普通接口定义差不多，只是在可选属性名字定义的后面加一个?。

### 只读属性
使用 __readonly__ 来指定只读属性。
```
    interface Point{
        readonly x:number;
        readonly y:number;
    }
```
也可以通过对象字面量来构造一个Point，赋值之后，x和y的值就不能被改变了。
```
    let p1: Point = {x:10,y:20};
    p1.x = 5; //error
```
__TypeScript__具有ReadonlyArray<T>类型，与Arry<T>相似。只是去掉了Arry<T>中可变方法。
```
    let a:number[] = [1,2,3,4];
    let ro:ReadonlyArry<number> = a;
    ro[0] = 12;//error
    ro.push(1); //error
    ro.length = 100; //error
    a = ro;//error
    //但是我们可以通过类型断言重写ReadonlyArry
    a = ro as number[];
```
### readonly 和 Const
官方文档里面是这样说的，判断应该用Readonly还是const，是要看它作为变量使用还是作为属性。作为**变量**使用则用**const**,作为**属性**使用则用**Readonly**.
### 额外的属性检查
```
    interface SquareConfig{
        color?:string;
        width?:number;
    }
    function createSquare(config:SquareConfig):{color:string;area:number}{
        //
    }
    let mySquare = createSquare({colour:"red",width:100});
```

额外属性检查不同于上面的可选属性，如果传入的参数中既包含接口中的属性，又包含接口中没有定义的属性，在Javascript里这样会默默的报错。
而在TypeScript里则会认为这段代码可能存在bug。对象字面量会被特殊对待而且会经过额外属性检查，当将他们赋值给变量或作为参数传递的时候。
如果一个对象字面量存在任何"**目标类型**"不包含的属性时，将会得到一个报错。

如何绕开这些类型检查
使用类型断言
```
    let mySquare = createSquare({width:100,opacity:0.5} as SquareConfig);
```
添加字符串索引签名(前提是确定这个额外对象有用)，接口可以这样定义.
```
    interface SquareConfig{
        color?: string;
        width?: string;
        [propName:string]:any;
    }
```
还有一种方式是将这个对象赋值给另一个变量，另一个变量不会经过额外的属性检查。
```
    let SquareOptions = {colour:"red",width:100};
    let mySquare = createSquare(SquareOptions);
```
## 函数类型
这里我们其实已经见过函数类型的定义了。除了描述带有属性的普通对象外，接口也可以描述函数类型。

为了使用接口表示函数类型，需要给接口定义一个调用签名。其实就是对函数的参数列表和返回值的类型的定义。
对应的，参数列表里的每个参数都需要名字和类型。
```
    interface SearchFunc{
        (source:string,subString:string):boolean;
    }
    //使用
    let mySearch:SearchFunc;
    mySearch = function(source:string,subString:string){
        let result = source.search(subString);
        if(result == -1){
            return false;
        }
        else
        {
            return true;
        }
    }
```
对于函数类型检查而言，函数传入的参数名并不需要与接口中的名字相同。只要求对应位置上的参数类型相同即可。
即使没有在函数中指定参数类型，TypeScript类型系统会推断出参数的类型，因为接口已经定义了参数和返回值的类型了。

### 可索引的类型

可索引类型具有一个**索引签名**,描述了对象索引的类型，还有相应的索引返回值类型。
```
    interface StringArry{
        [index:number]:string;
    }

    let myArry:StringArry;

    myArry = ["Bob", "Fread"];
    let str:string = myArry[0];
```
这里详细请参考[可索引的类型](https://zhongsp.gitbooks.io/typescript-handbook/content/doc/handbook/Interfaces.html)
## 类类型
### 实现接口
与静态语言中的接口一样，在TypeScript中如果一个类继承了接口则这个类需要实现该接口中的方法，并且需要对相应属性进行定义。
```
    interface ClockInterface{
        currentTime:Date;
    }

    /**
    * Clock 
    */
    class Clock implements ClockInterface {
        constructor(h:number,m: number) {
            
        }
    }
```
编译代码会报错
>   error TS2420: Class 'Clock' incorrectly implements interface 'ClockInterface'.Property 'currentTime' is missing in type 'Clock'.

同样的我们可以在接口中声明一个方法，然后在我们的class中实现它。
```
    interface ClockInterface{
        currentTime:Date;
        setTime(d:Date);
    }

    /**
    * Clock 
    */
    class Clock implements ClockInterface {
        currentTime:Date;
        
        constructor(h:number,m: number) {
            
        }

        setTime(d:Date){
            this.currentTime = d;
        }
    }
```




