## 提升web应用性能 使用 Web Worker

worker是使用运行命名的JavaScript文件的构造函数创建的对象，此文件包含将在worker线程中的代码。
worker在当前window的另一个完全无关的上下文中运行。
因此，使用window的快速方式从worker中获取当前全局作用域（除了它自己）的东西将会报错。

在worker(由单个脚本使用的*标准worker*;多个worker使用多个线程全局范围)的情况下。worker 上下文由worker线程全局范围对象表示。
worker线程只能从首先生成它的脚本中访问，而*共享线程*可以从多个脚本中访问。

### 数据交换
数据通过消息系统在工作线程和主线程之间传递。两者都使用postMessage()方法发送消息，并通过onmessage事件处理程序（消息包含在Message事件的data属性中）来响应消息。
数据是Copy而不是共享。

反之，worker线程可以产生新的线程，只要这些worker与父页面在同一源下托管。此外，worker可以对网络I/O使用XMLHttpRequest,但XMLHttpRequest上的responseXML和通道属性总是返回null

### 专用worker(标准worker)
正如以上所提到的，一个专用的worker只能够被调用它的脚本访问。在此部分，我们讨论的是专用worker.

```
    //main.js
    //主线程
    var first = document.querySelector('#number1');
    var second = document.querySelector('#number2');
    var result = document.querySelector('.result');

    if(window.Worker){
        let myworker = new worker("worker.js");
        first.onchange = ()=>{
            myworker.postMessage([first.value,second.value]);
        };

        second.onchange = ()=>{
            myworker.postMessage([first.value,second.value]);
        }

        myworker.onmessage = (e)=>{
            result.textContent = e.data; 
        }        
    }
```
*注意* onmessage,postMessage方法在主线程中被调用时会hung off worker对象，而不是在worker对象中调用才会挂起。这是因为在worker内部，worker的作用域是全局范围。
```
    //worker.js
    //worker线程
    onmessage = (e)=>{
        let workerResult = e.data[0] * e.data[1];
        postMessage(workerResult);
    }
```

### 终止一个worker线程

``` 
    myworker.terminate()//主线程中调用
```
这个worker线程会被立即kill掉。不会完成它的操作或者是之后的清理。
```
    close()//worker线程中关闭自己则使用close()方法
```

### 异常处理
当worker线程运行时发生异常时，会调用 *onerror* 事件对异常进行处理。接收实现了ErrorEvent接口的error事件。

## 生成子线程
Workers may spawn more workers if they wish. So-called sub-workers must be hosted within the same origin as the parent page. 
Also, the URIs for subworkers are resolved relative to the parent worker's location rather than that of the owning page. 
This makes it easier for workers to keep track of where their dependencies are.

### Importing scripts and libraries
Worker threads have access to a global function, importScripts(), which lets them import scripts in the same domain into their scope. 
It accepts zero or more URIs as parameters to resources to import; all of the following examples are valid:

```
    importScripts();                        /* imports nothing */
    importScripts('foo.js');                /* imports just "foo.js" */
    importScripts('foo.js', 'bar.js');      /* imports two scripts */
```
## 共享worker线程
创建
```
    let myworker = new ShareWorker("worker.js")
```
*区别* 第一个很大的区别就是一个共享的worker

