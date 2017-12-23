## 如何使用反射获取类型
如何获取类型信息
1. 得到实例对象
此时得到是这个实例对象，得到的方式也许是一个Object的引用，也许是一个接口的引用，但是并不知道它的确切类型。<br>
可以通过调用System.Object上声明的方法GetType来获取实例对象的类型对象。
```
//判断传递进来的参数是否实现了某个接口
public void Process(object processObj)
{
    Type t = processObj.GetType();
    if(t.GetInterface("ITest")!=null)
    {
        //do somthing
    }
}
```
2. 通过*Type.GetType*以及Assembly.GetType方法
```
    Type tt = Type.GetType("System.String");
```
要查找一个类，必须指定它所在的SDK,或者在已经获得的Assembly实例上面调用GetType.System.String是被包含在mscorlib.dll中，而.Net SDK编译时默认都引用了mscorlib,因此，在此处
直接写 Type.GetType("System.String")是正确的。<br>
一般的情况下需要指定SDK的名称版本等信息。
```
    Type t = Type.GetType("System.Data.DataTable,System.Data,Version=1.0.3300.0,  Culture=neutral,  PublicKeyToken=b77a5c561934e089");
```

## 如何根据类型来动态创建对象
*System.Activator*提供了方法来根据类型动态创建对象
```
    Type t = Type.GetType("System.Data.DataTable,System.Data,Version=1.0.3300.0,  Culture=neutral,  PublicKeyToken=b77a5c561934e089");
    DataTavle ttable = (DataTable)Activator.CreateInstance(t);
```
根据有参数的构造器创建对象
```
// TestClass
namespace TestSpace
{
    public class TestClass
    {
        private string _value;

        public TestClass(string value)
        {
            _value = value;
        }
    }
}
//How to Create
Type t = Type.GetType("TestSpace.TestClass");
Object[] constructParams = new object[]{"hello"};//构造函数参数，按照构造函数参数顺序将参数放入一个Object数组。
TestClass obj = (TestClass)Activator.CreateInstance(t, constructParams);

```

## 如何获取方法以及动态调用方法
```
    namespace TtestSpace
    {
        public class TestClass
        {
            private string _value;
            public TestClass()
            {

            }

            public TestClass(string value)
            {
                _value = value;
            }

            public string GetValue(string prefs)
            {
                if(_value == null)
                {
                    return "null";
                }
                else 
                {
                    return prefix + ":" + _value;
                }
            }

            public string Value
            (
                set{
                    _value = value;
                }
                get
                {
                    if(_value == null)
                    {
                        return "NULL";
                    }
                    else
                    {
                        return _value;
                    }
                }
            )
        }
    }
```
上面是一个简单的Class，包含有参构造函数，我们可以通过方法名称来得到方法并且调用。
```
    Type t = Type.GetType('TestSpace.TestClass');//获取类型
    object[] constructParam = new object[]{"timmy"};//构造函数参数
    object obj = Activator.CreateInstance(t,constructParam);//根据类型t创建对象
    MethodInfo method = t.GetMethod("GetValue");//获取方法信息
    BindingFlags flag = BindingFlags.public | BindingFlags.Instance;// 调用方法的标志位，此处含义为Public且是实例方法，
    //GetValue方法参数
    object[] perameters = new object[]{"Hello"}
    //调用方法，用一个Object接收返回值
    object returnValue = method.Invoke(obj, flag, Type.DefaultBinder, parameters, null);
```
## 动态创建委托
委托是实现事件的基础，有时候不可避免的要动态创建委托，System.Delegate提供了一些静态方法来动态创建一个委托。
```
namespace TestSpacee
{
    deletgate string TestDelegate(string value);
    public class TestClass
    {
        public TestClass()
        {

        }
        public string GetValue(string value)
        {
            return value;
        }
    }
}
```
如何使用
```
TestClass obj = new TestClass();
Type t = Type.GetTypee("TestSpace.TestClass");//获取类型，也可以用typeof来获取类型
//为何创建不成功?
TestDelegate method = (TestDelegate)Delegate.CreateDeletgate(t,obj,"GetValue");//创建委托，传入类型、创建委托的对象以及方法名称
string returnValue = method("hello");//
```