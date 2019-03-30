## FROM 
指定基础镜像， 

```
FROM nginx
....
```
特殊的镜像-scratch-, 如果以该镜像为基础镜像，就意味着不以任何镜像为基础,Dockerfile中所写的指令都将作为镜像第一层
```
FROM scratch
...
```

## RUN
用于执行命令。<br>
两种格式
- shell格式
```
RUN echo ....
```

- exec 格式
```
RUN ["function", "param1", "param2"]
```
每个RUN指令都创建一层镜像，（Union FS最大层数是不超过 127 层）所以最好不要单独写RUN
```
RUN buildDeps = 'gcc libc6-dev make wget'\
    && apt-get update\
    && apt-get install -y $buildDeps\
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz"
    ...
    && apt-get purge -y --auto-remove &buildDeps
```

## 镜像构建上下文
Docker 在运行时分为Docker引擎和客户端工具，Docker 的引擎提供了一组 REST API , Docker 客户端则是通过这组API和Docker引擎交互。
镜像进行构建的时候，并非所有的定制都会通过RUN指令完成， 经常会将一些本地文件复制进镜像。如-COPY-，-ADD-指令，而Docker Build命令构建镜像，其实并非在本地构建，而是在服务端的Docker引擎中构建。（C/S架构）<br>
如何让服务端获取到本地文件？<br>
上下文的概念，当构建时，用户会指定构建镜像上下文路径， docker build 命令得知这个路径之后会将路径下的所有内容打包，然后传给Docker 引擎。引擎得到这个上下文包之后，展开会获得构建镜像所需的一切文件。<br>
例如：<br>
```
COPY ./package.json/app/
```
这并不是要复制执行 docker build 命令所在目录下的 package.json,也不是复制Dockerfile所在目录下的 package.json, 而是复制上下文目录下的 package.json , COPY 这类指令的源文件路径都是<b>相对路径</b>。
一般来说，应该会将Dockerfile置于一个空目录下，或者项目的根目录下。如果该目录下没有所需文件，那么应该把所需文件复制一份过来。如果目录下确实有不希望构建时传给 Docker 引擎，那么可以用 ```.dockerignore```过滤。
```
$ docker build -t nginx:v3 .
Sending build context to Docker daemon 2.048 kB
...
```
注意这个``` . ```，实际上是在指定上下文目录，不是 ```Dockerfile ```所在的目录，当然，默认情况下，如果不额外指定 ``` Dockerfile```的话，会将上下文目录下名为 ``` Dockerfile ```的文件作为 ``` Dockerfile ```.
这些事默认的行为， ``` Dockerfile```的文件名并不要求必须为 ```Dockerfile ```, 而且不要求必须位于上下文目录中，例如：
```
-f ../Dockerfile.php
```
指定某个文件作为 ```Dockerfile ```

