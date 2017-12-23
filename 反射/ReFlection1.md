# 反射
定义：审查元数据并收集它的类型信息的能力。元数据(编译后的最基本数据单元)就是一大堆表，当编译程序集或者模块时，编译器会创建一个类定义表，一个字段定义表，和一个方法定义表。<br>
```
//System.reflection命名空间包含的几个类，允许反射这些元素据表的代码。
System.Reflection.Assembly
System.Reflection.MemberInfo
System.Reflection.EventInfo
System.Reflection.FieldInfo
System.Reflection.MethodBase
System.Reflection.ConstructorInfo
System.Reflection.MethodInfo
System.Reflection.PropertyInfo
System.Type
```
以下为如上的几个类的使用方法
1. 使用Assembly定义和加载程序集，加载在程序集清单中列出模块，以及从此程序集中查找类型并创建该类型的实例
2. 使用Module了解包含程序集以及模块中的类等，还可以获取在模块上定义的所有全局方法或其它特定的飞全局方法。
3. 使用ConstructirInfo了解构造函数的名称、参数、访问修饰符、如public private和实现详细信息,如abstract或virtual等。使用Type的*GetConstructors*或*GetConstructor*方法来调用特定的构造函数。
4. 使用MethodInfo了解方法的名称、返回类型、参数、访问修饰符(如public private)和实现详细信息(如abstract virtual)等。使用Type的GetMethods或GetMethod方法来调用特定的方法。
5. 使用FieldInfo了解字段的名称、返回类型、参数、访问修饰符(如public private)和实现详细信息(如Static)等,并获取或设置字段值。
6. 使用EventInfo了解事件的名称、事件处理程序数据类型、自定义属性、声明类型和反射类型等，添加或移除事件处理程序。
7. 使用ParameterInfo了解参数名称、数据类型、是输入参数还是输出参数，以及参数在方法签名中的位置等。

#### 反射的作用
1. 可以使用反射动态地创建类型的实例，将类型绑定到现有对象，或从现有对象中获取类型
2. 应用程序需要在运行时从某个特定的程序集中载入一个特定的类型，以便实现某个任务时可以用到反射。
3. 反射主要应用与类库，这些类库需要知道一个类型的定义，以便提供更多的功能。

## 使用反射获取程序集
当需要反射AppDomain中所包含的所有程序集时
```
static void Main()
{
    //调用AppDomain对象的GetAssemblies方法，将返回一个由System.Reflection.Assembly元素组成的数组。
    foreach(Assembly assem in AppDomain.CurrentDomain.GetAssemblies())
    {
        //反射当前程序集的信息
        Reflector.ReflectOnAssembly(assem);
    }
}
```
<b>说明</b><br>
上面讲的方法是反射AppDomain的所有程序集，如果希望显示的调用其中的某一个程序集，System.Reflection.Assembly提供了如下方法：
1. Load方法：Load方法带有一个程序集标志并载入它，Load将引起CLR把策略应用到程序集上，先后在全局程序集缓冲区、应用程序根目录和私有路径下面查找该程序集，如果找不到该程序集则抛出异常。
2. LoadFrom方法：传递一个程序集文件的路径名称（包括扩展名），CLR会载入所指定的这个程序集，传递的这个参数不能包含任何关于版本号信息、区域性、和公钥信息，如果在指定的路径下找不到程序集则抛出异常。
3. LoadWithPartialName:最好不要使用这个方法，因为应用程序不能确定载入的程序集版本。该方法唯一用途就是帮助那些在.net框架的测试环节使用.net框架提供某种行为的客户。
*注意*System.AppDomain也提供了一种Load方法，和Assembly的静态Load方法不一样，AppDomain的Load方法是一种实例方法，返回的是一个对程序集的引用，Assembly的静态Load方法是将该程序集按值封装返回给发出调用的AppDomain,<b>在实际使用时应尽量避免使用AppDomain的Load方法</b>。

### 利用反射获取类型信息
```
using System;
using System.Reflection;

namespace Reflection2
{
    class Program
    {
        static void Main(string[] args)
        {
            Program reflecting = new Program();
            Assembly assem = Assembly.LoadFrom("./bin/Debug/netcoreapp2.0/Reflection2.dll");//调用程序集
            reflecting.GetReflectionInfo(assem);
        }

        private void GetReflectionInfo(Assembly assem)
        {
            Type[] types = assem.GetTypes();
            foreach(Type t in types)
            {
                ConstructorInfo[] constructors = t.GetConstructors();
                FieldInfo[] fields = t.GetFields();
                MethodInfo[] methods = t.GetMethods();
                PropertyInfo[] properties = t.GetProperties();
                EventInfo[] events = t.GetEvents();
            }
        }
    }
}

```
其它几种获取type对象的方法：
1. System.type   参数为字符串类型，该字符串必须指定类型的完整名称（包括其命名空间）
2. System.type 提供了两个实例方法：GetNestedType,GetNestedTypes
3. Syetem.Reflection.Assembly 类型提供的实例方法是：GetType,GetTypes,GetExporedTypes
4. System.Reflection.Moudle 提供了这些实例方法：GetType,GetTypes,FindTypes

### 反射类型的接口
如果你想要获得一个类型继承的所有接口集合，可以调用Type的FindInterfaces GetInterface或者GetInterfaces。所有这些方法只能返回该类型直接继承的接口，他们不会返回从一个接口继承下来的接口。要想返回接口的基础接口必须再次调用上述方法。

### 反射的性能
使用反射来调用类型或者触发方法，或者访问一个字段或者属性时clr 需要做更多的工作：校验参数，检查权限等等，所以速度是非常慢的。所以尽量不要使用反射进行编程，对于打算编写一个动态构造类型（晚绑定）的应用程序，可以采取以下的几种方式进行代替：
1. 通过类的继承关系。让该类型从一个编译时可知的基础类型派生出来，在运行时生成该类型的一个实例，将对其的引用放到其基础类型的一个变量中，然后调用该基础类型的虚方法。
2. 通过接口实现。在运行时，构建该类型的一个实例，将对其的引用放到其接口类型的一个变量中，然后调用该接口定义的虚方法。
3. 通过委托实现。让该类型实现一个方法，其名称和原型都与一个在编译时就已知的委托相符。在运行时先构造该类型的实例，然后在用该方法的对象及名称构造出该委托的实例，接着通过委托调用你想要的方法。这个方法相对与前面两个方法所作的工作要多一些，效率更低一些。