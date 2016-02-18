#d_builder

======

```
快速构建dockerfile的工具
```

###GETTING START
===
```
cd your_code_dir

git clone git@github.com:LuoDi-Nate/d_builder.git
```
* 将代码clone到本机

```
cd d_builder
```
* 进入项目根路径

```
python builder.py -t war -u /data3/deploy_history/project_0217  -n mercurius-webapi-user -v 0.1 -p 8080:8080
```
* 执行命令 生成dockerfile


###CUSTOMIZE ARGS
===

```
-t type, u must choose one in ("war", "jar", "html")
```
需要被部署到docker容器中的项目类型:

* war	web项目, 利用tomcat做容器, 部署war包到tomcat中, 必须对外暴露至少一个端口
* jar	java项目, soa的服务节点, 不必要对外暴露端口
* html	js项目, 利用nginx部署, 必须对外暴露至少一个端口

```
-u url, path of project which need to deploy
```
绝对路径或者相对路径都可以;

```
-n server name, the unique identification for your project
```
需要部署的项目的唯一标识, 相同项目的server_name 务必相同;

```
-v version, version of this build
```
本次部署的版本信息;

```
-p port binding, the port u need expose, ${host_port}:${virtual_port}

split with "#" if u need bind multiple relation
eg: 80:8080#443:8443
```
端口绑定关系, 前者是物理机的端口, 后者是docker容器中的端口;








