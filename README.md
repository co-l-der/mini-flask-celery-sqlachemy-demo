#### 简要描述：

此项目在mini-flask-restful-demo基础上修改,添加了celery和sqlachemy模板,包括

1. mini-falsk-restful-demo

2. celery使用示例

3. sqlachemy使用示例

4. 两个关于使用celery的restful接口


#### 项目启动方式(注意启动celery):

1. python run.py
2. celery -A app.tasks.celery_task


#### 接口示例:

1. 调用celery task接口
- ` http://localhost:5000/cat/detail`

  
**请求方式：**

- POST 

​
**请求示例**

``` 

 {

    "id": 1,

    "name": "tom",

    "gender": "male"

}

```

 **返回示例**

``` 

{

    "code": 0,

    "data": {

        "gender": "male",

        "id": 1,

        "name": "tom"

    }

}

```

2. 调用celery task执行状态接口
- ` http://localhost:5000/cat/status`

  
**请求方式：**

- POST 

​
**请求示例**

``` 

 {

    "task_id": "",

}

```

 **返回示例**

``` 

{

    "code": 0,

    "data": {

        "status": "SUCCESS",

    }

}

```
