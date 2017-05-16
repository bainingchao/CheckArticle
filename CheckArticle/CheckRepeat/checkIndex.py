#coding=utf-8
import jieba.posseg as pseg
import os
import time
import re
import jieba
import difflib
import sys



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
    subject={} # 记录查重结果，键值对，原句+重复率
    summary={}
    # 1 找到对比库的历史数据
    checkpath ="../CheckRepeat/database/OrigCorpus/cutdatas.txt" # 数据库中对比项目语料库
    with open(checkpath,"r",encoding="utf-8") as f:
        checklist=[line[:] for line in f.readlines()]
    subjectname=[sub for sub in checklist if "subject" in sub] # 项目名称
    summaryname=[summ for summ in checklist if "summary" in summ] # 项目简介

    if "subject" in namestr:
        # 2 进行项目名称验证操作
        for rline in subjectname:
            line = ''.join(str(rline).split(' ')[2:])
            subp = difflib.SequenceMatcher(None,namestr.split('\n')[0].replace('subject',''),line).ratio()
            subject[line]=float('%.4f'%(subp))
    if "summary" in namestr:
        # 3 进行项目简介验证操作
        for rline in summaryname:
            line = ''.join(str(rline).split(' ')[2:])
            sump = difflib.SequenceMatcher(None,namestr.split('\n')[1].replace('summary',''),line).ratio()
            summary[line]=float('%.4f'%(sump))

    # 4 打印检测结果
    outreslut=""
    sort1=sorted(subject.items(),key=lambda e:e[1],reverse=True)   #排序
    outreslut +="项目名称："+"*"*5+"["+namestr.split('\n')[0].replace('subject','') + "]"+"*"*5+"的查重结果如下:\n\n"
    for item in sort1[:1]:
        if item[1] >= 0.5:
            outreslut += "与项目库中\t[<span style=\"color:red\">"+item[0].replace("\n",'')+"</span>]\t的相似率最高：<span style=\"color:red\">"+str(item[1]) +"</span>\n"
        else:
            outreslut += "<span style=\"color:green\">没有查出重复的项目简介</span>\n"

    sort2=sorted(summary.items(),key=lambda e:e[1],reverse=True)   #排序
    outreslut += "\n\n项目简介："+"*"*5+"["+namestr.split('\n')[1].replace('summary','') + "]"+"*"*5+"的查重结果如下：\n\n"
    for item in sort2[:1]:
        if item[1] >= 0.5:
            outreslut += "与项目库中\t[<span style=\"color:red\">"+item[0].replace("\n",'')+"</span>]\t的相似率最高：<span style=\"color:red\">"+str(item[1]) +"</span>\n"
        else:
            outreslut += "<span style=\"color:green\">没有查出重复的项目简介</span>\n"

    # 5 写到文件里面
    with open("../CheckRepeat/database/DealCorpus/checkout.txt",'w',encoding='utf-8') as f:
        f.write(outreslut)
    print(outreslut)

'''
接收文本参数并进行分词操作
subject：文本框中的题目
summary：文本框中的简介
'''
def checkcut(subject,summary):
    # 1 将文本框中的数据读入文件中
    if summary=="":
        checkstr ='subject:'+subject
    else:
        checkstr ='subject:'+subject+'\nsummary:'+summary
    dealpath="../CheckRepeat/database/DealCorpus/check.txt"
    with open(dealpath,'w',encoding='utf-8') as f:
        f.write(checkstr)

    # 2 数据切词与预处理
    # words=jieba.cut(open(dealpath,'r',encoding='utf-8').read())
    words =jieba.cut(checkstr.strip()) # 分词结果
    checkresult=""
    for word in words:
        if word not in stopwords:
            checkresult += word+" "
    return checkresult.replace(' ','')




global stopwords
stopwords={}.fromkeys([line.strip() for line in open('../CheckRepeat/database/OrigCorpus/CK_stopWords.txt','r',encoding='utf-8')]) # 停用词表

if __name__ == '__main__' :
    t1=time.time()

    '''1 构建科技项目查重的训练模型'''
    # dealfile() # 原始语料抽取并进行标记

    '''2 构建科技项目查重的测试模型'''
    subject = sys.argv[1]
    summary = sys.argv[2]
    # subject = r"全科护士临床“二级”规范化培训模式初探"
    # summary = r"本研究借鉴国外培养社区护士的先进经验，以我国全科医师培养模式为参考，在高等院校护理教育的基础上，采用轮岗培训与社区实践相结合的方式，初探全科护士“二级”规范化培训模式的可行性，旨在培养一批既能承担临床医疗工作又能在社区作卫生保健、用药指导、健康教育、饮食指导、临终关怀以及独立家庭访视工作的全科护士，为今后各大医院进行全科护士规范化培训、国家实施全科护士规范化培训改革、出台相关政策法规提供参考依据。"
    checkfun(checkcut(subject,summary)) #检查重复情况

    t2=time.time()
    print("Total spent "+str(t2-t1)+"s"+"\n")




