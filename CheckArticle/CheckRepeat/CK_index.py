#coding=utf-8
import jieba.posseg as pseg
import os
import time
import re
import jieba
import difflib


'''
创建文件
path：原语料路径
sumpath：提取简介保存路径
subpath：提取题目保存路径
'''
# def mkdirfile(*path):
#     for i in range(0,len(path)):
#         if not path[i]:
#             os.makedirs(path[i])
#             print(path[i]+' 创建成功')
#         else: pass


'''
切词处理
sumpath：规范化后简介的路径
subpath：规范化后题目标题的路径
'''
def cutword(flagpath,cutpath):
    print('-->请稍后，文本正在预处理中...')
    with open(flagpath,"r",encoding='utf-8') as f:
        txtlist=f.read() # 读取待处理的文本
        words =jieba.cut(txtlist.strip()) # 带词性标注的分词结果
        cutresult=""# 获取去除停用词后的分词结果
        for word in words:
            if word not in stopwords:
                if word == '\n':
                    cutresult += word
                else:
                    cutresult += word+" " #去停用词
        with open(cutpath,"w",encoding='utf-8') as f:
            for line in cutresult.split("\n"):
                f.write(re.sub(r'\s+',' ',line).replace("\ufeff","")+"\n")
            # f.write(cutresult) # 读取待处理的文本


'''
进行标记
path：原语料路径
sumpath：提取简介保存路径
subpath：提取题目保存路径
'''
def dealfile():
    # 1 针对语料路径进行配置
    path="../CheckRepeat/database/OrigCorpus/datas.txt" # 训练语料库
    flagpath="../CheckRepeat/database/OrigCorpus/flagdatas.txt" # 语料标记

    # 2 对原始语料进行标记和简单清洗
    listset="" # 标记后的语料集合
    i,j=1,1
    with open(path,'r',encoding='utf-8') as f:
        for rline in f.readlines():
            line = rline.strip().replace("&nbsp;","")
            if "summary" in line :
                listset +="\n"+str(i)+"_"+line
                i+=1 # 简介打标签
            elif "subject" not in line:
                listset +=line
            elif "subject" in line:
                listset +="\n"+str(j)+"_"+line
                j+=1 # 项目题目打标签

    # 3 保存标记后语料并统计标记结果
    with open(flagpath,'w',encoding='utf-8') as f1:
        f1.write(listset.strip())
    print("="*70)
    print("项目共计标题:"+str(len(listset.split("subject"))-1))
    print("项目共计简介:"+str(len(listset.split("summary"))-1))
    print("-"*70)

    # 4 对标记数据进行分词处理
    cutpath="../CheckRepeat/database/OrigCorpus/cutdatas.txt" # 保存分词后的结果
    cutword(flagpath,cutpath)


'''查重'''
def checkfun(namestr):
    dict={} # 记录查重结果，键值对，原句+重复率
    # 1 找到对比库的历史数据
    checkpath ="../CheckRepeat/database/OrigCorpus/cutdatas.txt" # 数据库中对比项目语料库
    with open(checkpath,"r",encoding="utf-8") as f:
        checklist=[line[:] for line in f.readlines()]
    subjectname=[sub for sub in checklist if "subject" in sub] # 项目名称
    summaryname=[summ for summ in checklist if "summary" in summ] # 项目简介
    print(namestr)
    # 2 进行验证操作
    totalnum=len(namestr.split(' ')) # 待验证数据长度
    ''' 验证题目的相似度
    思想：字符串str与对比库串line对比,w代表共存字词
          man{|sum(w)/len(str)-sum(w)/len(line)|}
    '''
    if "subject" in namestr:
        for line in subjectname:
            repeatnum=0
            for word in namestr.split(' '):
                if word in line:
                    repeatnum += 1
                else: pass
            ckp = float('%.4f'%(repeatnum/totalnum)) # 获取每条信息相似度概率值，保留四位有效数字
            ckl=float('%.4f'%(repeatnum/len(line))) # 获取对比库信息相似度概率值，保留四位有效数字
            if abs(ckp-ckl)<0.1:
                dict[str(line)]=abs(ckp-ckl)
            print(str(line),ckp,ckl)
    # if "summary" in namestr:
    #     for line in summaryname:
    #         repeatnum=0
    #         for word in namestr.split(' '):
    #             if word in line:
    #                 repeatnum += 1
    #         ckp = float('%.4f'%(repeatnum/totalnum)) # 获取每条信息相似度概率值，保留四位有效数字
    #         if ckp > 0.6:
    #             dict[str(line)]=ckp

    # 打印检测结果
    print("["+namestr.replace(' ','') + "]的查重结果如下：\n\n"+"-"*70 )

    for keys in dict:
        print("结果显示和 [ %s] 极为相似，距离相似率为：%f \n" %(keys.replace(" ",""),dict[keys]))
    # print("对比数据数目是：\t"+str(len(relist)))

def checkcut(checkstr):
        # 待处理语料规约化
    # stopwords ={}.fromkeys([line.strip() for line in open('../CheckRepeat/database/OrigCorpus/CK_stopWords.txt','r',encoding='utf-8')]) # 停用词表
    words =jieba.cut(checkstr.strip()) # 分词结果
    checkstr=""
    for word in words:
        if word not in stopwords:
            checkstr += word+" "
    return checkstr.rstrip()


def checkfun1(namestr):
    listtest=[]
    dict={} # 记录查重结果，键值对，原句+重复率
    # 1 找到对比库的历史数据
    checkpath ="../CheckRepeat/database/OrigCorpus/cutdatas.txt" # 数据库中对比项目语料库
    with open(checkpath,"r",encoding="utf-8") as f:
        checklist=[line[:] for line in f.readlines()]
    subjectname=[sub for sub in checklist if "subject" in sub] # 项目名称
    summaryname=[summ for summ in checklist if "summary" in summ] # 项目简介
    # 2 进行验证操作
    print(namestr)

    for line in subjectname:
        countp = difflib.SequenceMatcher(None,namestr,line).ratio()
        listtest.append(float('%.4f'%(countp)))
    print([p for p in listtest if p>0.8])


global stopwords
stopwords={}.fromkeys([line.strip() for line in open('../CheckRepeat/database/OrigCorpus/CK_stopWords.txt','r',encoding='utf-8')]) # 停用词表
if __name__ == '__main__' :
    t1=time.time()

    '''构建科技项目查重的训练模型'''
    # dealfile() # 原始语料抽取并进行标记
    print("="*70+"\n")

    '''构建科技项目查重的测试模型'''
    # str="subject汽车交通事故分析与鉴定研究"
    str1="扶贫专项产业类"
    checkstr =checkcut(str1)
    checkfun1("2370 subject 南充 职业 技术 学院 大学生 创新 创业园 建设") #检查重复情况
    # print("="*70+"\n")

    t2=time.time()
    print("Total spent "+str(t2-t1)+" s"+"\n")









