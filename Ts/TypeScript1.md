# TypeScript学习 #
## 变量声明 ##


### 解构数组 ###

1.解构赋值
```    let input = [1,2];
    let [first,second] = input;
    console.log(first);
    console.log(second);
```
2.作用于函数参数
```
    function f([first,second]:[number,number]){
    console.log(first);
    console.log(second);    
    }
    f(input);
```
3.使用...name的语法创建一个剩余变量列表
``` 
    let [first,...rest] = [1,2,3,4];
    console.log(first);// 1
    console.log(rest); //2,3,4
```
### 对象解构 ###
1.通常情况
```
    let o = {
        a:"foo",
        b:12,
        c:"bar"
    }
    let {a,b} = 0;
```
对于我们不需要的值我们可以忽略他，只取我们需要的值就可以了。
2.默认值的情况，当属性为undefined时使用缺省值。
```
    function keepWholeObject(wholeObject:{a:string,b?:number}){
        let {a,b=1001} = wholeObject;
    }
```
即使b为undefined，keepWholeObject函数变量wholeObject 的属性a 和 b 都会有值。
## 函数声明 ##

1.解构也能用于函数声明。
```
    type C={a:string,b?:number};
    function f({a,b}:C):void{
        //
    }
```
但是通常情况下是用于指定默认值，但是这里有些麻烦的是，需要知道在设置默认值之前设置其类型。
```
    function f({a,b} = {a:" ",b:0 }):void{
        //
    }
    f(); 
```
当存在深层次嵌套解构的时候就需要我们注意，就算这个时候没有堆叠在一起的重命名、默认值和类型注解，也是比较复杂的情况。结构表达式应当尽量小而简单。