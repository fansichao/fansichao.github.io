# -*- coding=utf-8 -*-
u""" Spark_Api

- 数据读取
- 数据处理
- 数据保存

Spark API 使用说明

- 服务启停 详见部署文档
- 服务配置连接 详见 Spark_api 中 __init__ 参数
- 如何使用spark_api 
    - 常用服务接口: 接口函数
        - cre_df                创建DataFrame
        - cre_table             创建table
        - read_file             读取文件 读取本地文件/HDFS文件
        - save_file             上传文件 上传到HDFS/下载到本地
        - del_file              删除文件 删除本地/HDFS文件
        - isempty               判断 数据对象 是否为空  df/rdd
        - check_param_type      参数类型检查
        - check_param_exist     检查参数是否存在
        - check_type            数据类型检查
        - df_drop_duplicates    数据去重
        - merge_df_from_data    数据合并
        - df_rename_col         列重命名
        - cre_table             创建表
        - drop_table            删除table表
        - cache_table           将指定的表缓存在内存中
        - save_df               保存df
    - 基础服务接口
        - stop_spark        关闭spark服务
        - show_df           展示df数据
        - run_cmd           运行CMD命令
        - query_table       查询所有table_name 
    - 调用接口说明: 部分接口函数/参数/公式说明
        - selectExpr_args:  selectExpr 公式说明
        - column_args:      字段参数/公式说明 select+filter/where
    - 内部调用函数: 仅此文件内部使用,外部无法调用
        - _save_df_to_csv        保存DataFrame 生成csv
        - _save_df_to_table
        - _cre_table_from_df     从DF创建table

    - 参考链接:
        - http://spark.apache.org/docs/latest/api/python/pyspark.sql.html

    - 临时记录:
        - 读取数据流
        - text_sdf = sqlContext.readStream.text(tempfile.mkdtemp())

exp:

.. code-block:: python

    # 对spark数据帧的同一列进行多次聚合操作
    from pyspark.sql.functions import mean, sum, max, col
    df = sc.parallelize([(1, 3.0), (1, 3.0), (2, -5.0)]).toDF(["k", "v"])
    groupBy = ["k"]
    aggregate = ["v"] 
    funs = [mean, sum, max]
    exprs = [f(col(c)) for f in funs for c in aggregate]
    
    # or equivalent df.groupby(groupBy).agg(*exprs)
    df.groupby(*groupBy).agg(*exprs)
    
    
    # where sum(xxx) 不能和group by 在同一层级 否则报错
    sql = "select distinct CUST_CERTNO,sum(TRAN_AMT) as TRAN_AMT from tran group by CUST_CERTNO "
    # where sum(TRAN_AMT)>=100



"""
import os
import sys
import copy
import datetime
import logging
import traceback
import uuid

reload(sys)
sys.setdefaultencoding("utf8")

import pandas as pd
from pyspark import SparkContext, SparkConf, SparkFiles
from pyspark.sql import Row, SparkSession, SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import expr, col, column

SPART_CONFIG = {
    'APPNAME': 'cdh',
    'HDFS_URL': 'hdfs://192.168.100.210:8020',
    'SPARK_URL': 'yarn',
    # old_SPARK_URL spark://192.168.172.70:7077

}

def input_param_check(param, defalut_param, s=''):
    u""" 检查参数

    :param param: 检查的参数 
    :param defalut_param: 默认参数
    :param s: 参数名称
    """
    if not bool(param):
        param = copy.deepcopy(defalut_param)
        logging.info(u"参数[%s]未输入,使用默认值[%s]" % (s, defalut_param))
    else:
        logging.info(u"参数[%s]已输入,使用值[%s]" % (s, param))
    return param




class Spark_Api(object):
    u"""
        Spark 调用接口
    """

    def __init__(self, appname=None, hdfs_url=None, spark_url=None, *lis, **kv):
        u""" 初始化
        :param appname: APP名称, 详细见Spark页面值
        :param spark_url: SparkURL, 详细见Spark页面值
        :param hdfs_url: 连接HDFS
        """

        # 参数配置 
        self.hdfs_url = input_param_check(hdfs_url, SPART_CONFIG.get('HDFS_URL'), 'HDFS_URL')
        self.spark_url = input_param_check(spark_url, SPART_CONFIG.get('SPARK_URL'), 'SPARK_URL')
        self.appname = input_param_check(appname, SPART_CONFIG.get('APPNAME'), 'APPNAME')

        # 创建连接 spark_session 必须在sc之后
        self.conf = kv.get('spark_conf') or SparkConf().setAppName(self.appname).setMaster(self.spark_url)
        self.sc = kv.get('spark_context') or SparkContext(conf=self.conf)

        self.spark_session = kv.get('spark_session') or SparkSession.builder.master(self.spark_url).appName(
            self.appname).config(
            "spark.some.config.option", "some-value").getOrCreate()

    def _connect(self):
        u""" 连接测试 """
        # TODO 
        pass

    #######################
    # 接口函数
    #######################
    u"""
    功能需求
        - 创建各种数据类型 df/list/rdd
        - 数据读取 & 数据存入
        - 其他功能
            - 创建临时表
            - 停止spark

    函数接口
        - cre_df: 从data/sql/table/DataFrame 创建DataFrame
        - cre_table: 从DataFrame创建table
        - read_file: 读取local/hdfs文件，返回 rdd/list/df
        - save_file: 保存list/df到local/hdfs
        - stop_sparl: 停止spark
    """
    # 创建
    def cre_df(self, data, data_type='data', **kv):
        u""" 创建DataFrame
        """
        data_type_lis = ['data', 'sql', 'table', 'DataFrame', 'rdd']
        if data_type in ['data', 'DataFrame', 'rdd']:
            # keys = ['schema', 'samplingRatio', 'verifySchema']
            # kv = self.check_params(keys, kv)
            return self._cre_df_from_data(data, **kv)
        elif data_type == 'sql':
            return self._cre_df_from_sql(data)
        elif data_type == 'table':
            return self._cre_df_from_table(data)
        else:
            logging.error('cre_df中data_type应该为%s' % str(data_type_lis))

    def cre_table(self, df, table_name='table_default'):
        u""" 从DF创建table
        """
        self._cre_table_from_df(df, table_name)

    def cre_df_from_file(self, file_path, **kv):
        u""" 读取csv创建DataFrame
        """
        default_dic = {
            'charToEscapeQuoteEscaping': 'None',
            'columnNameOfCorruptRecord': 'None',
            'comment': 'None',
            'dateFormat': 'None',
            'emptyValue': 'None',
            'encoding': 'None',
            'enforceSchema': 'None',
            'escape': 'None',
            'header': 'None',
            'ignoreLeadingWhiteSpace': 'None',
            'ignoreTrailingWhiteSpace': 'None',
            'inferSchema': 'None',
            'maxCharsPerColumn': 'None',
            'maxColumns': 'None',
            'maxMalformedLogPerPartition': 'None',
            'mode': 'None',
            'multiLine': 'None',
            'nanValue': 'None',
            'negativeInf': 'None',
            'nullValue': 'None',
            'positiveInf': 'None',
            'quote': 'None',
            'samplingRatio': 'None',
            'sep': 'None',
            'timestampFormat': 'None',
            'schema': 'None'
        }
        kv = self.check_params(default_dic.keys(), kv)
        print kv
        # spark_session.read.csv 支持多个文件读取 例如 tran*.csv 多个文件会存入到一个DF中
        # df = self.spark_session.read.csv(file_path, **kv, header=True) 即可指定所有表头
        df = self.spark_session.read.csv(file_path, **kv)
        return df

    def save_file_from_df(self, df, file_path, **kv):
        u""" 保存文件
        """
        default_dic = {
            'charToEscapeQuoteEscaping': 'None',
            'compression': 'None',
            'dateFormat': 'None',
            'emptyValue': 'None',
            'encoding': 'None',
            'escape': 'None',
            'escapeQuotes': 'None',
            'header': 'None',
            'ignoreLeadingWhiteSpace': 'None',
            'ignoreTrailingWhiteSpace': 'None',
            'nullValue': 'None',
            'quote': 'None',
            'quoteAll': 'None',
            'sep': 'None',
            'timestampFormat': 'None',
            'mode': 'None'}
        kv = self.check_params(default_dic.keys(), kv)
        df.write.csv(file_path, **kv)

    # 类型转换
    def convert_datatype(self, data, from_type, to_type='df'):
        u""" 数据 类型转换
        :param data: 需要转换的数据
        :param from_type: 需要转换的数据类型
        @parm to_type: 转换后的数据类型
        """
        data_types = ['rdd', 'df', 'list']
        # TODO from_type类型检查        
        if from_type not in data_types or to_type not in data_types:
            logging.error('>>>> 类型错误from_type[%s]或to_type[%s]不在%s中' % str(data_types))

        cmd = "new_data = self._tran_%s2%s(data)" % (from_type, to_type)
        print cmd
        exec (cmd)
        return new_data

    def convert_coltype(self, df, colname, dtype, new_colname=None):
        u""" 列 类型转换
        
        :param df: DataFrames数据
        :param colname: 列名称
        :param dtype: 转换后字段类型 dtype
        :param new_colname: 新的列名

        exps:

        .. code-block:: python

            dtypes = ['date', 'string', 'int', 'double', 'float', 'Timestamp']
            >>> df.select(df.age.cast("string").alias('ages')).collect()
            [Row(ages=u'2'), Row(ages=u'5')]
            >>> df.select(df.age.cast(StringType()).alias('ages')).collect()
            [Row(ages=u'2'), Row(ages=u'5')]
        """

        # DataTypeSingleton FractionalType, IntegralType, NumericType,, UserDefinedType
        dtypes = [StringType, ArrayType,  BinaryType, BooleanType, ByteType, DataType, 
            DateType, DecimalType, DoubleType, FloatType,  IntegerType, 
             LongType, MapType, NullType,  ShortType, 
            StructType, TimestampType]

        if not bool(dtype) or dtype not in dtypes:
            logging.info('>> 数据类型[%s]不在[%s]中,使用默认类型[%s]' % (dtype,str(dtypes), dtypes[0]))
            dtype = dtype or dtypes[0]

        new_colname = new_colname or colname
        df = df.select(col(colname()).cast(dtype).alias(new_colname))
        return df

    # 读取
    def read_file(self, file_path, file_type='local', read_type=None, return_type='df',
                  schema=None, header=True, sep='|'):
        u""" 读取文件 读取本地文件/HDFS文件
        :param file_path: 文件路径  注：本地文件需要服务器集群都能访问,否则偶发报错,文件不存在。
        :param file_type: 文件类型          local/hdfs
        @parma return_type: 返回文件类型    list/rdd/dataframes
        @parma schema: 表头结构 Scheam比header优先级更高
        @parma header: 是否有表头

        """
        return_type_lis = ['list', 'rdd', 'df']
        if return_type not in return_type_lis:
            logging.error(">>>> return_type[%s]参数错误,应为%s" % (return_type, str(return_type_lis)))
        file_path = self._get_file_path(file_path, file_type)

        rdd = None;
        ListData = None
        if not self.check_exist(file_path, file_type):
            print '>> 文件[%s]不存在' % file_path
            return False

        # Spark 自带方式读取  TODO map运算+自定义解析行函数
        rdd = self.sc.textFile(file_path).map(lambda line: line.split(sep))


        # 如果表头存在 提出表头
        header_cols = rdd.first() if header else []
        rdd_noheader = rdd.filter(lambda x: x != header_cols) if header else rdd

        # rdd = self.sc.textFile(file_path).map(lambda line: line.split(","))
        if return_type == 'rdd':
            return rdd
        elif return_type == 'list':
            return self.convert_datatype(rdd, 'rdd', to_type='list')
        elif return_type == 'df':
            if bool(schema) and bool(header):
                df = self._tran_rdd2df(rdd_noheader, schema)
            elif bool(schema) and not bool(header):
                df = self._tran_rdd2df(rdd, schema)
            else:
                df = self._tran_rdd2df(rdd_noheader, header_cols)
            return df
        else:
            logging.error(">>>> return_type[%s]参数错误,应为%s中一种" % (return_type, str(return_type_lis)))

    # 保存
    def save_file(self, rdd, file_path, file_type='local', save_type='text_file'):
        u""" 上传文件 上传到HDFS/下载到本地
        :param rdd: rdd
        :param file_path: 文件路径
        :param save_type: 保存文件方式

        """
        file_path = self._get_file_path(file_path, file_type)

        if self.check_exist(file_path, file_type):
            print '>> 文件[%s]已经存在' % file_path
            return False

        # TODO 详细参数
        save_type_dic = {
            'text_file': ['saveAsTextFile', file_path],
            'pickle_file': ['saveAsPickleFile', file_path],
            'Hadoop_File': ['saveAsHadoopFile', file_path],
            'hadoop_dataset': ['saveAsHadoopDataset', file_path],
            'new_hadoop_file': ['saveAsNewAPIHadoopFile', file_path],
            'new_hadoop_dataset': ['saveAsNewAPIHadoopDataset', file_path],
        }
        # TODO 存储成了字符串 ？ 
        # [u"[u'phone_num'", u" u'phone_flag'", u" u'peer_phone_num'", u" u'phone_sta_time'", u" u'phone_end_time']"]

        # rdd.saveAsTextFile(file_path)
        getattr(rdd, save_type_dic[save_type][0])(*save_type_dic[save_type][1:])
        print '>> 文件[%s]存储成功' % file_path
        logging.info('>> 文件[%s]存储成功' % file_path)

    # 文件删除
    def del_file(self, file_path, file_type='local'):
        u""" 删除文件 删除本地/HDFS文件

        """
        file_path = self._get_file_path(file_path, file_type)
        cmd = None;
        cmd2 = None
        if file_type == 'local':
            cmd = 'rm -r %s' % file_path[7:]
        elif file_type == 'hdfs':
            cmd = 'hadoop fs -rm %s' % file_path
            cmd2 = 'hadoop fs -rm -R %s' % file_path
        else:
            print(">> file_type[%s]错误,应该为local/hdfs" % file_type)
        print cmd, cmd2

        try:
            os.system(cmd)
            os.system(cmd2)
        except:
            pass

    def check_type(self, data):
        u""" 类型检查 检查data的数据类型

        """
        # rdd/df/list

        pass

    def show_df(self, df, n=None, truncate=None, vertical=False):
        df.show(n=None, truncate=None, vertical=False)
        # df.stats
        # df.describe().show()

    def df_drop_duplicates(self, df, cols=[]):
        u""" 列数据去重
        """
        return df.drop_duplicates(cols)

    # def merge_df_from_data(self, dfA, dfB, merge_cols, select_cols=[], merge_type='inner'):
    def merge_df_from_data(self, dfA, dfB, merge_cols, merge_type='inner'):
        u""" 数据合并
        :param dfA: DataFrames1
        :param dfB: DataFrames2
        :param merge_type: 合并类型

        """
        merge_types = ['inner', 'cross', 'outer', 'full', 'full_outer', 'left', 'left_outer',
                       'right', 'ight_outer', 'left_semi', 'left_anti']
        merge_type = merge_type if merge_type in merge_types else merge_types[0]
        # select_cols = select_cols or dfA.columns + dfB.columns

        # df_new = self._cre_df_from_data(data=[],header=select_cols)
        # df_new = dfA.join(dfB, merge_cols, merge_type).show()
        df_new = dfA.join(dfB, merge_cols, merge_type)
        # df_new = dfA.join(dfB, merge_cols, merge_type).select(*select_cols)
        return df_new

    # df.sort() df.where df.select df.selectExpr df.summary df.describe()
    def df_rename_col(self, df, name_dic):
        u""" 重命名字段
        """
        for key, val in name_dic.items():
            if not key in df.columns:
                continue
            df = df.withColumnRenamed(key, val)
        return df

    def check_param_exist(self, param='test'):
        u""" 检查参数是否存在
        """
        pass

    def check_param_type(self, val='test', expect_type='str'):
        u""" 参数类型检查

        # isinstance('ss',str)
        """
        expect_type_dic = {
            '字符串': ['str'],
            '整型': ['int'],
            '浮点': ['float'],
            '日期': ['datetime.date', 'datetime.datetime'],
        }
        expect_type_lis = []
        for key, val in expect_type_dic.items():
            expect_type_lis.extend(val)
        if expect_type not in expect_type_lis:
            print('>>>> expect_type[%s]数值异常,应该为%s' % (expect_type, str(expect_type_lis)))

        return isinstance(val, eval(expect_type))

    def check_exist(self, file_path, file_type='local'):
        u""" 检查文件是否存在

        :param file_path: 文件路径
        :param file_type: 文件路径类型 hdfs/local
        """
        if file_type == 'local':
            file_path_exists = file_path[7:]
            if not os.path.exists(file_path_exists):
                return False
        elif file_type == 'hdfs':
            try:
                textFile = self.sc.textFile(file_path).collect()
            except:
                return False
        else:
            logging.error('>> 文件类型[%s]异常' % file_type)

        return True

    def check_params(self, keys, kv):
        u""" 参数检查-获取kv中key在keys中的数据

        :param keys:有效参数列表
        :param kv: 参数k-v
        """
        kv_tmp = copy.deepcopy(kv)
        not_keys_dic = dict()
        for k in kv_tmp.keys():
            if k not in keys:
                not_keys_dic[k] = kv_tmp[k]
                del kv_tmp[k]
        if bool(not_keys_dic):
            print ">> 传入多余参数%s" % str(not_keys_dic)
        return kv_tmp

    def query_table(self):
        u" 查询所有 table_name "
        # df = SQLContext.tables()
        return SQLContext.tableNames(dbname='default')

    def drop_table(self, table_name):
        u" 删除 table表"
        SQLContext.dropTempTable(table_name)

    def cache_table(self, table_name):
        u""" 将指定的表缓存在内存中
        """
        SQLContext.cacheTable(table_name)
        # SQLContext.clearCache()

    def isempty(self, data, data_type='df'):
        u""" 判断 df 是否为空 df/rdd
        """
        if data_type == 'df':
            res = bool(data.first())
        elif data_type == 'rdd':
            res = data.isEmpty()
        else:
            res = bool(data)
        return not res

    def save_df(self, df, name, return_type='csv', *args, **kwargs):
        u""" 保存DF

        :param df: DF对象
        :param return_type: 返回类型 csv/table
        """
        if return_type == 'csv':
            self._save_df_to_csv(df, name, *args, **kwargs)
        elif return_type == 'table':
            self._save_df_to_table(df, name)
        else:
            pass

    ##############################
    ### 基础服务接口 存放一些基础服务
    ##############################

    def _get_file_path(self, file_path, file_type=None):
        u""" 生成文件路径

        :param file_path: 本地文件路径/HDFS文件路径
        :param file_type: 文件类型 hdfs/local

        样例: 
            file:///home/fdm/a.csv
            hdfs://192.168.172.70:9000/tmp
        """
        _default_file_type = 'local'
        file_type = input_param_check(file_type, _default_file_type, 'file_type').lower()

        if file_type == 'local':
            if bool(file_path) and file_path.startswith('file://'):
                return file_path

            if not bool(file_path) or not bool(os.path.exists(file_path)):
                logging.info(">> 输入的路径[%s]不存在" % file_path)
                return file_path

            abspath = os.path.abspath(file_path)
            return "file://" + abspath
        elif file_type == 'hdfs':
            # hdfs 文件存在检查
            if not file_path.startswith('hdfs://'):
                return self.hdfs_url + file_path

        return file_path

    def run_cmd(self, cmd, run_flag=False):
        u""" 运行CMD命令
        """
        print cmd
        if run_flag:
            os.system(cmd)

    def stop_spark(self):
        u" 关闭spark连接 "
        self.sc.stop()
        self.spark_session.stop()

    ##############################
    ### 调用接口说明
    ##############################
    def selectExpr_args(self, df, expr="", col="test"):
        u""" Spark SelectExpr 支持说明
        """
        # left right
        expr = "left(%s,2) as new_col " % col
        expr = "right(%s,2) as new_col " % col

        # 用 * 代替原有df所有字段
        exprs = ["CUST_CERTNO", "INWARD_REMITTANCE_AMT", "True as F00016"]
        exprs = ["*", "True as F00016"];
        df.selectExpr(*exprs)

        print df.selectExpr(expr).show()

    def column_args(self, df):
        u""" Select 支持说明
            # 支持函数
            http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Column
            expr='right(phone_num,2)'; df.selectExpr(expr).show()
            expr='left(phone_num,2)'; df.selectExpr(expr).show()
            expr='length(phone_num)'; df.selectExpr(expr).show()
            expr='trim(phone_num)'; df.selectExpr(expr).show()
            expr='max(phone_num)'; df.selectExpr(expr).show()
            expr='min(phone_num)'; df.selectExpr(expr).show()
            expr='max(peer_phone_num)'; df.selectExpr(expr).show()
            expr='min(peer_phone_num)'; df.selectExpr(expr).show()
            expr='abs(peer_phone_num)'; df.selectExpr(expr).show()
            expr='round(peer_phone_num,2)'; df.selectExpr(expr).show()
            expr='year(phone_sta_time)'; df.selectExpr(expr).show()
            expr='month(phone_sta_time)'; df.selectExpr(expr).show()
            expr='day(phone_sta_time)'; df.selectExpr(expr).show()
            expr='max(phone_sta_time)'; df.selectExpr(expr).show()
            expr='min(phone_sta_time)'; df.selectExpr(expr).show()
            expr='datediff(phone_end_time,phone_sta_time)'; df.selectExpr(expr).show()
            expr="phone_flag='来电'"; df.selectExpr(expr).show()
            expr="phone_flag is null"; df.selectExpr(expr).show()
            expr="sum(peer_phone_num)"; df.selectExpr(expr).show()
            expr="count(peer_phone_num)"; df.selectExpr(expr).show()
            expr="avg(peer_phone_num)"; df.selectExpr(expr).show()

            df.filter("phone_num>'14759332647'").show()
            df.filter("phone_num>='14759332647'").show()
            df.filter("phone_num<'14759332647'").show()
            df.filter("phone_num<='14759332647'").show()
            df.filter("phone_num='14759332647'").show()
            df.filter("phone_num!='14759332647'").show()
            string='14';df.filter("left(phone_num,%s)='%s'"%(len(string),string)).show()
            string='14';df.filter("right(phone_num,%s)='%s'"%(len(string),string)).show()
            "In [212]: import pyspark.sql.functions as psf
            In [213]: df.filter(psf.col('phone_num').rlike('75')).show() 或
            df.filter(""phone_num rlike '75'"").show()"
            df.filter("phone_num not rlike '75'").show()
            df2.filter(""year(phone_sta_time)>2017"").show()"
            df.filter("col > 1").filter("col < 2")
            df.filter("col > 1 and col < 2")
            df.filter("col > 1 or col < 2")


        """
        # df.select(df.age.alias('age2')).collect()
        func_info = {
            'alias': [u"列别名", u"df.select(df.age.alias('age2')).collect()"],
            'asc': ["升序','df.select(df.name).orderBy(df.name.asc()).collect()"],
            'asc_nulls_first': ["返回基于列的升序的排序表达式,并且空值在非空值之前返回",
                                "df.select(df.name).orderBy(df.name.asc_nulls_first()).collect()"],
            'asc_nulls_last': ["返回基于列的升序的排序表达式,并且在非空值之后显示空值。",
                               "df.select(df.name).orderBy(df.name.asc_nulls_last()).collect()"],
            'astype': ["类型转换astype()是别名cast(),详见cast"],
            'between': ["如果此表达式的值在给定列之间,则计算结果为true", "df.select(df.name,df.age.between(2,4)).show()"],
            'bitwiseAND': ["使用另一个表达式计算此表达式的按位AND", "df.select(df.a.bitwiseAND(df.b)).collect()"],
            'bitwiseOR': ["计算此表达式与另一个表达式的按位OR", "df.select(df.a.bitwiseOR(df.b)).collect()"],
            'bitwiseXOR': ["使用另一个表达式计算此表达式的按位XOR", "df.select(df.a.bitwiseXOR(df.b)).collect()"],
            'cast': ["将列转换为类型dataType。",
                     "df.select(df.age.cast('string').alias('ages')).collect(),df.select(df.age.cast(StringType()).alias('ages')).collect()"],
            'contains': ["包含其他元素。返回Column基于字符串匹配的布尔值。", "df.filter(df.name.contains('o')).collect()"],
            'desc': ["返回基于列的降序的排序表达式。", "df.select(df.name).orderBy(df.name.desc()).collect()"],
            'desc_nulls_firs': ["返回基于列的降序的排序表达式,并且空值出现在非空值之前。",
                                "df.select(df.name).orderBy(df.name.desc_nulls_first()).collect()"],
            'desc_nulls_last': ["返回基于列的降序的排序表达式,并且在非空值之后显示空值。",
                                "df.select(df.name).orderBy(df.name.desc_nulls_last()).collect()"],
            'endswith': ["字符串以xxx结尾", "df.filter(df.name.endswith('ice$')).collect()"],
            'eqNullSafe': ["对空值安全的等式测试,PySpark不认为NaN值为NULL",
                           "df1.join(df2,df1['value'].eqNullSafe(df2['value'])).count()"],
            'getField': ["在StructField中按名称获取字段的表达式",
                         "df=spark.createDataFrame([Row(r=Row(a=1,b='b'))]);df.select(df.r.getField('b')).show()"],
            'getItem': ["将项目放在ordinal列表中的位置,或者从字典中取项目",
                        "df=spark.createDataFrame([([1,2],{'key':'value'})],['l','d']);df.select(df.l.getItem(0),df.d.getItem('key')).show()"],
            'isNotNull': ["如果当前表达式为非null,则为True。", "df.filter(df.height.isNotNull()).collect()"],
            'isNull': ["如果当前表达式为null,则为True", "df.filter(df.height.isNull()).collect()"],
            'isin': ["如果参数的计算值包含此表达式的值", "df[df.name.isin('Bob','Mike')].collect(),df[df.age.isin([1,2,3])].collect()"],
            'like': ["模糊匹配", "df.filter(df.name.like('Al%')).collect()"],
            'namename': ["是别名alias()",
                         "df.select(df.age.cast('string').alias('ages')).collect(),df.select(df.age.cast(StringType()).alias('ages')).collect()"],
            'otherwise': ["计算条件列表并返回多个可能的结果表达式之一", "df.select(df.name,F.when(df.age>3,1).otherwise(0)).show()"],
            'over': ["定义窗口列", "df.select(rank().over(window),min('age').over(window))"],
            'rlike': ["模糊匹配,与正则表达式相似", "df.filter(df.name.rlike('ice$')).collect()"],
            'startswith': ["字符串以xxx开头", "df.filter(df.name.startswith('Al')).collect()"],
            'substr': ["返回指定起始结束位置的列", "df.select(df.name.substr(1,3).alias('col')).collect()"],
            'when': ["计算条件列表并返回多个可能的结果表达式之一",
                     "df.select(df.name,F.when(df.age>4,1).when(df.age<3,-1).otherwise(0)).show()"],
        }

        for i in func_info:
            print i, func_info[i][0], func_info[i][1:]

    ##############################
    ### 内部函数
    ##############################

    # >>>>>>>>>>>>>>>>>>> save_df
    def _save_df_to_csv(self, df, file_path, *args, **csv_param):
        u""" 保存DataFrame 生成csv
            pyspark.sql.DataFrameWriter DataFrame文件写入
        """
        file_path = self._get_file_path(file_path, 'local')
        csv_param = {
            'mode': 'append',  # append,overwrite,ignore,error
            'sep': ',',
            'quote': '"',
            'escape ': '\\',
            'header': 'false',
            'encoding': 'utf-8',
        }
        df.write.csv(file_path, **csv_param)

    def _save_df_to_table(self, df, table_name):
        u" 通过DataFrame 生成table表"
        SQLContext.registerDataFrameAsTable(df, table_name)

    # >>>>>>>>>>>>>>>>>>> cre_df
    def _cre_df_from_data(self, data=[[]], header=[]):
        u""" 从Data 创建DataFrame

        :param data: 行数据
        :param header: 表头数据
        """
        rows = copy.deepcopy(data)
        if not bool(header):
            header = rows[0]
            del rows[0]
            df = self.spark_session.createDataFrame(rows, header)
        else:
            # df = self.spark_session.createDataFrame(rows)
            df = self.spark_session.createDataFrame(rows, header)
        # sqlContext.createDataFrame(l, ['name', 'age']).collect()
        return df

    def _cre_df_from_rdd(self, rdd, columns_type='', header=[]):
        u""" 从RDD 创建DataFrame

        :param data: 行数据
        :param header: 表头数据

        schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", IntegerType(), True)])
        df3 = spark.createDataFrame(rdd, schema)
        """
        # columns_type "a: string, b: int"
        df = self.spark_session.createDataFrame(rdd, header, columns_type)
        return df

    def _cre_df_from_sql(self, sql):
        u""" 从SQL 创建DataFrame
        """
        df = SQLContext.sql(sql)
        return df

    def _cre_df_from_table(self, table_name):
        u""" 从Table 创建DataFrame
        """
        df = spark.table(table_name)
        return df

    def _cre_table_from_df(self, df, table_name):
        u""" 从DF 创建table
        """
        df.createOrReplaceTempView(table_name)

    # >>>>>>>>>>>>>>>>>>> tran_convert
    def _tran_list2df(self, ListData):
        u" 类型转换 list2df "
        return self.spark_session.createDataFrame(ListData)

    def _tran_list2rdd(self, ListData):
        u" 类型转换 list2rdd "
        return self.sc.parallelize(ListData)

    def _tran_rdd2list(self, rdd):
        u" 类型转换 rdd2list "
        return rdd.collect()

    def _tran_rdd2df(self, rdd, schema=None):
        u" 类型转换 rdd2df "
        return self.spark_session.createDataFrame(rdd, schema)

    def _tran_df2rdd(self, df):
        u" 类型转换 df2rdd "
        return df.rdd

    def _tran_df2list(self, df):
        u" 类型转换 df2list "
        return [list(row) for row in df.collect()]

    ##############################
    ### 测试函数/临时函数
    ##############################

    def SparkConf(self):
        u""" Spark应用程序的配置
        """
        # conf = SparkConf().setAppName(self.appname).setMaster(self.spark_url)

        # 设置应用名称
        SparkConf().setAppName(self.appname)
        # 设置主URL
        SparkConf().setMaster(self.spark_url)
        # 设置安装Spark路径
        # SparkConf().setSparkHome('/usr/local/spark')

        # 打印配置信息
        self.conf.toDebugString()
        # 获取所有配置 键值对
        self.conf.getAll()
        # 获取指定key的val
        self.conf.get('spark.master')
        # 配置指定key的val
        self.conf.set('spark.master', self.master)

    def StorageLevel(self, rdd, storagelevel='MEMORY_ONLY'):
        u""" 设置数据存储级别

        :param rdd: 数据
        :param storagelevel: 存储级别

        说明:
            是否使用内存 是否内存不足时使用磁盘
            是否以java序列化存储到内存中 是否多个节点复制
        """
        # 全局设置 TODO
        storagelevel_lis = [
            'DISK_ONLY',
            'DISK_ONLY_2',  # 数据存2份
            'MEMORY_AND_DISK',
            'MEMORY_AND_DISK_2',
            'MEMORY_AND_DISK_SER',
            'MEMORY_AND_DISK_SER_2',
            'MEMORY_ONLY',
            'MEMORY_ONLY_2',
            'MEMORY_ONLY_SER',  # 序列化
            'MEMORY_ONLY_SER_2',
            'OFF_HEAP',  # 减少垃圾回收开销
        ]
        # 查询数据存储级别
        print rdd.getStorageLevel()
        if storagelevel in storagelevel_lis:
            # 设置数据存储级别
            rdd.persist(getattr(StorageLevel, storagelevel))

    def SparkFiles(self, file_path):
        u""" 访问Spark作业文件
        """
        # 获取添加文件
        SparkFiles.get(file_path)
        # 获取包含添加文件的根目录
        SparkFiles.getRootDirectory()

        with open(SparkFiles.get(file_path)) as f:
            rows = f.readlines()
            for row in rows:
                print row

        return rows

    def TaskContext(self):
        pass

    def df_deal_filter(self, col_name, func_type, func_val):
        u""" 数据过滤

        :param col_name: 过滤的字段
        :param func_type: 过滤采用的函数
        :param func_val: 过滤采用的值
        """
        # TODO func_val 类型检查
        # 更多的函数处理
        func_type_dic = {
            '>': '>',
            '>=': '>=',
            '=': '=',
            '<': '<',
            '<=': '<',
            '!=': '!=',
            '开头为': 'left',
            '结尾为': 'right',
            '包含': 'rlike',
            '不包含': 'not rlike'
        }
        new_func_type = func_type_dic.get(func_type)
        if not bool(new_func_type):
            print(u"func_type[%s]类型错误" % func_type)
            return
        update_dic = {
            'func_type': new_func_type,
            'col_name': col_name,
            'func_val': func_val,
            'len_func_val': len(str(func_val)),
        }

        # df.filter("phone_num>'14759332647'")
        if new_func_type in ['>', '>=', '=', '<=', '<', '!=']:
            # TODO 类型 整型等
            expr = "{col_name} {func_type} {func_val}".format(**update_dic)
        elif new_func_type in ['left', 'right']:
            # string='14';df.filter("left(phone_num,%s)='%s'"%(len(string),string))
            expr = "{func_type}({col_name},{len_func_val}) = '{func_val}'".format(**update_dic)
        elif new_func_type in ['rlike', 'not rlike']:
            # import pyspark.sql.functions as psf
            # df.filter(psf.col('phone_num').rlike('75')).show()
            # expr = "phone_num rlike 'qwe'"
            expr = "{col_name} {func_type} '{func_val}'".format(**update_dic)
        else:
            # 默认处理
            expr = "%s %s '%s'" % (col_name, new_func_type, func_val)
        print expr
        df = df.filter(expr)
        return df

    def df_deal_select(self, col_name, func_type, func_val=None, new_col_name=None, col_name2=None):
        u""" 数据选取

        :param col_name: 过滤的字段
        :param func_type: 过滤采用的函数
        :param func_val: 过滤采用的值
        """
        # TODO func_val 类型检查
        # 更多的函数处理
        # 大小写不敏感
        deal_select_dic = {
            'right': 'right',
            'left': 'left',
            'len': 'length',
            'trim': 'trim',
            'max': 'max',
            'min': 'min',
            'abs': 'abs',
            'round': 'round',
            'year': 'year',
            'month': 'month',
            'day': 'day',
            'datediff': 'datediff',
            'if': '=',
            'isnull': 'is null',
            'sum': 'sum',
            'avg': 'avg',
            'count': 'count',
            # 日期处理 TODO
            'DATEADD': 'DATEADD',
            'SECONDDIFF': 'SECONDDIFF',
            'MINUTEDIFF': 'MINUTEDIFF',
            '在()和()之间': '在()和()之间',
            '在()和()之外': '在()和()之外',
            '在[]和[]之间': '在[]和[]之间',
            '在[]和[]之外': '在[]和[]之外',
        }
        new_col_name = new_col_name if bool(new_col_name) else  col_name + '_new'
        new_func_type = func_type_dic.get(func_type)
        update_dic = {
            'func_type': new_func_type,
            'col_name': col_name,
            'new_col_name': new_col_name,
            'func_val': func_val,
            'col_name2': col_name2,
        }

        if new_func_type in ['ABS', 'AVG', 'COUNT', 'DAY', 'MAX', 'MIN', 'SUM', 'TRIM', 'YEAR', 'MONTH']:
            #  expr = 'AVG(phone_num) as new_col';
            expr = "{func_type}({col_name}) as {new_col_name}".format(**update_dic)
        elif new_func_type in ['DATEDIFF']:
            if not bool(col_name2):
                print "col_name2,必须要两个时间字段"
            # expr='datediff(phone_end_time,phone_sta_time)';
            expr = "{func_type}({col_name},{col_name2}) as {new_col_name}".format(**update_dic)
        elif new_func_type in ['=', 'is null']:
            # expr="phone_flag is null as new_col"; df.selectExpr(expr).show()
            expr = "{col_name} {func_type} as {new_col_name}".format(**update_dic)
        elif new_func_type in ['ROUND', 'right', 'left', ]:
            # expr = 'right(phone_num,2) as new_col';
            expr = "{func_type}({col_name},{func_val}) as {new_col_name}".format(**update_dic)
        else:
            # 默认 TODO
            expr = "{col_name} {func_type} as {new_col_name}".format(**update_dic)

        df = df.selectExpr(expr)
        return df


if __name__ == '__main__':
    spark_api = Spark_Api()
    # 数据读取
#    rdd = spark_api.read_file('/data/faker_data/record.csv', sep=',',return_type='rdd')
#    print rdd.take(2)
    df = spark_api.read_file('/data/faker_data/record.csv', sep=',', return_type='df', file_type='local')
    print df.show()
    # 数据保存
#    spark_api.save_file(rdd, '/data/record2.csv', file_type='hdfs', save_type='text_file')
#    spark_api.save_file_from_df(df, "/data/record2.csv")

    # convert_coltype 类型转换

#    # 数据读取
#    rdd = spark_api.read_file('/data/record2.csv', file_type='hdfs', sep=',', return_type='rdd')
#    print rdd.take(2)




    
