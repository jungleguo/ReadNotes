## 配置依赖
1. 打开需要导出项目的csproj
2. 添加如下配置，请注意是DotNetCliToolReference，切勿与PackageReference相混淆。
```
<ItemGroup>
    <DotNetCliToolReference Include="Microsoft.VisualStudio.Web.CodeGeneration.Tools" Version="2.0.0" />
    <DotNetCliToolReference Include="dotnet-aries" Version="*" /><!--添加该依赖-->
</ItemGroup>
```

## 如何使用?
这里假设你已经安装好了所需依赖，剩下的就非常简单。<br>
- 打开命令行工具，这里以Window为例，找到需要导出API文档的项目的基地址，也就是项目启动文件所在地址。<br>
需要该项目的Relase版本的dll文件，否则可能会遍历不到其依赖项。
```
dotnet publish -c Release
```
- 运行命令导出文档
```
dotnet aries doc -t D:\AriesDoc\ -f D:\Example\bin\Release\netcoreapp2.0\publish -b http://localhost:63298
```
- 如果命令执行成功则会输出：
```
Aries doc generate Done
```
至此，导出动作结束了。<br>
那么，导出的文件放在哪里了呢？还记得我们在运行命令进行导出时所设置的参数了么。导出文件存放地址就在这些参数当中，接下来就会介绍命令里的参数<br>

#### -t 所期望的文档导出地址 
这个参数是必须的。因为在导出API文档时需要指定将它导出到何处。
#### -f 目标项目的publish文件夹所处位置
这个参数也是必须的。在执行*dotnet aries doc xxxxxx*之前我们先执行了*dotnet publish -c Release*,这个命令会在bin目录下生成一个Release文件夹，而publish文件夹就在Release文件夹下。<br>
将这个绝对地址作为参数*-f*的值。AriesDoc的DocGenerator会去遍历这些dll。然后根据遍历的结果生成文档。
#### -b API部署的基地址
严格上来说这个字段是选填的，但是我们推荐填上。当我们有这样一个API文档，是期望能够对其进行调用的。如果缺少基地址，调用则不会成功。<br>
<b>注意：</b>最好不要在此处填写生产环境的基地址，以免造成不必要的错误。

#### -s 启动项目的类名
这个字段不是必须的，因为我们会默认一个启动项目的类名为<b>StartUp</b>,<b>注意：</b>如果你的项目的启动类名不为StartUp请使用 <b>-s</b>参数指定。

#### -v raml的版本
这个字段不是必须的。目前我们支持导出的文档为raml格式，如果没有提供该参数，我们会默认为<b>1.0</b>版本。