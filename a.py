import traceback
import copy
while True:
    try:
        n = int(input().strip())
        cp_n = copy.deepcopy(n)

        def get_all_zhishu(n, zhishu_lis=[]):
            """ 获取所有质数

            :param int n: 获取质数的范围
            :param list zhishu_lis: 质数列表
            """
            # TODO 性能
            for i in range(2, n+1):
                is_flag = True
                for y in zhishu_lis:
                    # 整除
                    if divmod(i, y)[1] == 0:
                        is_flag = False
                if is_flag:
                    zhishu_lis.append(i)
            #print(zhishu_lis)
            return zhishu_lis

        if n > 2:
            all_zhishu = get_all_zhishu(n, zhishu_lis=[2])
        elif n == 1:
            print(1)
        elif n < 0:
            pass

        res_lis = []
        while n not in all_zhishu:
            for i in all_zhishu:
                if divmod(n, i)[1] == 0:
                    n = divmod(n, i)[0]
                    res_lis.append(i)

        if n in all_zhishu:
            res_lis.append(n)

        
        res_lis.sort()
        res_lis = [str(i) for i in res_lis]

        
        print("%s=%s"%('*'.join(res_lis), str(cp_n)))

    except:
        print(traceback.format_exc())
        pass
 