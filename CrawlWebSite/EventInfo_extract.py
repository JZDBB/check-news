# -*- coding: utf-8 -*-
from CrawlWebSite import fact_triple_extraction1chen, configpar


def EventInfo_extraction(inputtxt):
    '''
函数名称：EventInfo_extraction
函数原型：def EventInfo_extraction(inputtxt)
参数名称：inputtxt:待提取信息的文字（utf-8编码）
返回值：成功，返回列表{“date”：时间发生日期，“address”:“时间发生地点”,"type":"事件类型"，
“gname”：“组织名称”，“total”:“伤亡总人数”，“nwound”:"伤亡人数"，“nkill”:"死亡总人数"}
'''
    EventInfo={}
    
    try:
        packagePath=configpar.parse_args("config.conf")
        print(packagePath)
        EventExtractMd=fact_triple_extraction1chen.EventInfoExtract(packagePath,"out.txt")
        EventExtractMd.InitModule()
        TimeAndAddress=EventExtractMd.addresssTime_extract(inputtxt.encode("utf-8"))
        fact_attribute = EventExtractMd.fact_attribute_from_text(inputtxt.encode("utf-8"))
        orgnization = EventExtractMd.organization_from_text(inputtxt.encode("utf-8"))
        death_num,hurt_num,total_num = EventExtractMd.death_num_from_text(inputtxt.encode("utf-8"))
        if TimeAndAddress[0]["date"]=="" and TimeAndAddress[0]["address"]=="":
            EventInfo=None
            EventExtractMd.release_module()
        else:
            EventInfo['Event_time']=TimeAndAddress[0]['date']
            EventInfo['Event_address']=TimeAndAddress[0]['address']
            EventInfo['Event_type']=fact_attribute
            if(total_num!=None):
                EventInfo['Event_total']="伤亡:" + total_num
            else:
                if death_num==None:
                    death_num="0"
                if hurt_num==None:
                    hurt_num="0"
            EventInfo['Event_total']="死亡：" + death_num + "，受伤：" + hurt_num
            EventInfo["Event_gname"]=orgnization
            EventInfo['Event_nwound']=hurt_num
            EventInfo['Event_nkill']=death_num
            print(EventInfo)
            EventExtractMd.release_module()
    except:
        EventInfo=None
        # EventExtractMd.release_module()
    return EventInfo
        

